# vim:ts=2:sts=2:sw=2:et

# Constructor options:
#   rpm_command => $string
#   rpmbuild_command => $string
#   defines => [ "MACRO VALUE", ... ]
#   rcfile => "FILE[:FILE...]"
#   target => "ARCH-VENDOR-OS"
#   expand => { KEY => "EXPR", ... }
#   workdir => "PATH"
#   debug => 1

# Member vars:
#  package_tags => { PACKAGE => { TAG => VALUE, ... }, ... }
#  global_tags => { TAG => VALUE, ... }
#  expansions => { KEY => VALUE, ... }
#  rpm => RPM::Toolbox::Spec::RPM->new

package RPM::Toolbox::Spec;

use 5.008;
use warnings;
use strict;

use Carp;
use IO::File;
use Cwd qw(abs_path);
use File::Basename;
use File::Spec::Functions;
use File::Path qw(mkpath);
use RPM::Toolbox::Spec::Util qw(:all);
use RPM::Toolbox::Spec::RPM;
use RPM::Toolbox::Spec::Workspace;
use RPM::Toolbox::Spec::Cache;
use RPM::Toolbox::Spec::Expander;

our $VERSION = "0.05";

our $_WORKSPACE;
our $_SPECFILE;
our $_SPECTEXT;
our %_ARGS;
our ($_FIRST_DUMMY_ICON_FILE, $_FIRST_DUMMY_SOURCE_FILE);
our (%_SOURCE_HASH, %_PATCH_HASH);
our $_BUILD_NAME_FMT;

my @_CACHE_KEYS = qw(global_tags package_tags expansions);

sub _STRING { 1 }
sub _LIST   { 2 }
sub _BUILD  { 4 }
sub _GLOBAL { 8 }

my %_TAG_SPECS = (
# tag function name      type/scope                query format for "rpm -q"
# --------------------------------------------------------------------------
  name              => [ _STRING,                  '%{NAME}'          ],
  epoch             => [ _STRING,                  '%{EPOCH}'         ],
  version           => [ _STRING,                  '%{VERSION}'       ],
  release           => [ _STRING,                  '%{RELEASE}'       ],
  summary           => [ _STRING,                  '%{SUMMARY}'       ],
  group             => [ _STRING,                  '%{GROUP}'         ],
  description       => [ _STRING,                  '%{DESCRIPTION}'   ],
  license           => [ _STRING,                  '%{LICENSE}'       ],
  vendor            => [ _STRING,                  '%{VENDOR}'        ],
  packager          => [ _STRING,                  '%{PACKAGER}'      ],
  url               => [ _STRING,                  '%{URL}'           ],
  distribution      => [ _STRING,                  '%{DISTRIBUTION}'  ],
  arch              => [ _STRING,                  '%{ARCH}'          ],
  requires          => [ _LIST,                    '%{REQUIRENAME}%{REQUIREFLAGS:depflags}%{REQUIREVERSION}'    ],
  conflicts         => [ _LIST,                    '%{CONFLICTNAME}%{CONFLICTFLAGS:depflags}%{CONFLICTVERSION}' ],
  provides          => [ _LIST,                    '%{PROVIDENAME}%{PROVIDEFLAGS:depflags}%{PROVIDEVERSION}'    ],
  obsoletes         => [ _LIST,                    '%{OBSOLETENAME}%{OBSOLETEFLAGS:depflags}%{OBSOLETEVERSION}' ],
  buildrequires     => [ _BUILD | _GLOBAL | _LIST, '%{REQUIRENAME}%{REQUIREFLAGS:depflags}%{REQUIREVERSION}'    ],
  buildconflicts    => [ _BUILD | _GLOBAL | _LIST, '%{CONFLICTNAME}%{CONFLICTFLAGS:depflags}%{CONFLICTVERSION}' ],
  buildarchs        => [ _BUILD | _GLOBAL | _LIST, '%{BUILDARCHS}'    ],
  excludearch       => [ _BUILD | _GLOBAL | _LIST, '%{EXCLUDEARCH}'   ],
  excludeos         => [ _BUILD | _GLOBAL | _LIST, '%{EXCLUDEOS}'     ],
  exclusivearch     => [ _BUILD | _GLOBAL | _LIST, '%{EXCLUSIVEARCH}' ],
  exclusiveos       => [ _BUILD | _GLOBAL | _LIST, '%{EXCLUSIVEOS}'   ],

  # these are handled specially, not via "rpm -qf"
  sourceurls        => [ _GLOBAL | _LIST,          undef              ],
  patcheurls        => [ _GLOBAL | _LIST,          undef              ],
  iconurls          => [ _GLOBAL | _LIST,          undef              ],
  packages          => [ _GLOBAL | _LIST,          undef              ],
  buildroot         => [ _GLOBAL | _STRING,        undef              ],
  sourcerpm         => [ _GLOBAL | _STRING,        undef              ],
  _binary_rpm_filename => [ _STRING,               undef              ],
);

# Create a copy of the original spec file with some text appended to it.
# Usage: $self->_create_specfile ($dir, $text);
sub _create_specfile {
  my ($self, $dir, $text_suffix) = @_;
  my $filename = catfile ($dir, basename ($_SPECFILE));
  debug qq(creating specfile "$filename");
  my $fh = IO::File->new ($filename, 'w') or die "$filename: $!\n";
  $fh->print ($_SPECTEXT, "\n");
  $text_suffix and $fh->print ($text_suffix);
  $fh->close or die "$filename: $!\n";
  return $filename;
}

# Create a dummy icon to keep rpm/rpmbuild happy. Rpm validates the
# existance of files behind "Icon:" directives while parsing. If these
# files don't exist, RPM's spec parser craps out. This function creates
# a dummy XPM file for each such icon.
#
# Usage: $self->_create_dummy_icon ($abs_dir, $filename, $first_filename_ref)
# - $abs_dir: the absolute path of the temporary SOURCES directory
#   (inside WORKSPACE dir)
# - $filename: the name of the file relative to $abs_dir that rpm expects
#   to exist
sub _create_dummy_icon {
  my ($self, $abs_dir, $filename) = @_;
  my $basename = basename ($filename);
  my $icon_path = catfile ($abs_dir, $basename);
  my $icon_src;

  # We had already generated an icon, just create a symlink to that first
  # file
  if ($_FIRST_DUMMY_ICON_FILE) {
    my $src = $_FIRST_DUMMY_ICON_FILE;
    unlink $icon_path;
    debug qq(creating dummy icon symlink "$icon_path" => "$src");
    symlink $src, $icon_path or die "$icon_path: $!\n";

  # This is the first icon file, really create it
  } else {
    debug qq(creating dummy icon "$icon_path");
    my $fh = IO::File->new ($icon_path, 'w') or die "$icon_path: $!\n";
    $fh->print (<<_END
/* XPM */
_END
    );
    $fh->close or die "$icon_path: $!\n";
    $_FIRST_DUMMY_ICON_FILE = $icon_path;
  };

  # The spec parser in some RPM versions doesn't strip the dirname from
  # "Icon" URLs, so they expects file names like
  # "%_sourcedir/http:/foo/bar.gif". This doesn't seem to happen in the build
  # stage, only in the parser. So we need the icon in both locations => create
  # a symlink.
  if ($basename ne $filename) {
    my $symlink_src = $_FIRST_DUMMY_ICON_FILE;
    my $symlink_path = catfile ($abs_dir, $filename);
    my $symlink_dir = dirname ($symlink_path);
    unless (-d $symlink_dir) {
      debug qq(creating directory "$symlink_dir");
      mkpath $symlink_dir or die "$symlink_dir: $!\n";
    };
    unlink $symlink_path;
    debug qq(creating dummy icon symlink "$symlink_path" => "$symlink_src");
    symlink $symlink_src, $symlink_path or die "$symlink_path: $!\n";
  }
}

# Create an empty (not!) source file so that rpmbuild can succeed.
# Usage: $self->_create_dummy_source ($abs_dir, $filename)
# - $abs_dir: absolute path to the "SOURCES" directory within WORKSPACE
# - $filename: the source file relative to $abs_dir
#
sub _create_dummy_source {
  my ($self, $abs_dir, $filename) = @_;
  my $path = catfile ($abs_dir, $filename);
  if ($_FIRST_DUMMY_SOURCE_FILE) {
    debug qq(creating dummy source symlink "$path" => "$_FIRST_DUMMY_SOURCE_FILE");
    unlink $path;
    symlink $_FIRST_DUMMY_SOURCE_FILE, $path or die "$path: $!\n";
  } else {
    debug qq(creating dummy source file "$path");
    my $fh = IO::File->new ($path, 'w') or die "$path: $!\n";
    # Defeat RPM's sanity check on file size by creating a non-empty file
    $fh->print ("dummy source file\n");
    $fh->close or die "$path: $!\n";
    $_FIRST_DUMMY_SOURCE_FILE = $path;
  };
}


# Abbreviate a tag value (for debugging).
# Usage: $abbrev_string = _abbrev ($string)
sub _abbrev($) {
  my $s = shift;
  my $want_suffix;
  $s =~ s/\n.*//s and $want_suffix = 1;
  if (length ($s) > 30) {
    $s = substr ($s, 0, 30);
    $want_suffix = 1;
  };
  $s =~ s/\s+$//g;
  $want_suffix and $s .= "...";
  return $s;
}

# Given a tag id and a string, convert that string to the right value:
# - if tag expects list values, split the string on commas and return a
#   list ref
# - otherwise return the string as is
# - the string '(none)' is treated as an undef scalar or empty list,
#   depending on tag type.
#
# Usage: $self->_make_tag_value ($tag, $value_string)
sub _make_tag_value($$) {
  my ($tag, $value_str) = @_;
  $value_str = undef if $value_str eq '(none)';
  if (($_TAG_SPECS{$tag}->[0] & _LIST) != 0) {
    defined ($value_str) and return [ split (/\s*,\s*/o, $value_str) ];
    return undef;
  };
  return $value_str;
}

# Save a package-specific tag (e.g., one obtained by doing "rpm -q" on the
# spec file). The tag is saved in $self->{package_tags}->{$package}->{$tag}.
# The value wil be saved a string or a list ref, depending on tag type.
#
# Usage: $self->_save_package_tag ($package, $tag, $value_str)
sub _save_package_tag {
  my ($self, $package, $tag, $value_str) = @_;
  my $abbrev = _abbrev ($value_str);
  my $value = _make_tag_value ($tag, $value_str);
  return unless defined ($value);
  debug qq(  $tag: \"$abbrev\");
  if (defined ($value)) {
    $self->{package_tags}->{$package}->{$tag} = $value;
    return;
  };
  delete $self->{package_tags}->{$package}->{$tag};
}

# Save a global tag in $self->{global_tags}->{$tag} (e.g., BuildDepends).
# The value wil be saved a string or a list ref, depending on tag type.
#
# Usage: $self->_save_package_tag ($package, $tag, $value_str)
sub _save_global_tag {
  my ($self, $tag, $value_str) = @_;
  my $abbrev = _abbrev ($value_str);
  my $value = _make_tag_value ($tag, $value_str);
  return unless defined ($value);
  debug qq($tag: "$abbrev");
  if (defined ($value)) {
    $self->{global_tags}->{$tag} = $value;
    return;
  };
  delete $self->{global_tags}->{$tag};
}

# phase1:
# - create a copy of the spec file with a call to the LUA script appended
#   at the end. The lua script evaluates macro expressions and a few
#   important macros and dumps the results in a file. See Expander.pm.
# - also append %dump at the end to pick up Source, Patch and Icon URLs
# - run that modified spec file via "rpm -q --qf ..."
# - analyze the output for "-q --qf" and "%dump" results
# - pick up the LUA output file and extrace macro expressions from it
#
# Usage: $self->_phase1
sub _phase1 {
  my $self = shift;
  local $_;

  my @package_list;
  my %icon_hash;
  my $sourcedir = $_WORKSPACE->dir ("SOURCES");
  my $abs_sourcedir = abs_path ($sourcedir) or die "$sourcedir: $!\n";
  my $specdir = $_WORKSPACE->dir ("PHASE_1");
  my $logfile = catfile ($specdir, "rpm.log");
  my $expander = RPM::Toolbox::Spec::Expander->new ($specdir, %_ARGS);

  # Format the text to be appended to the spec file:

  # The suffix is wrapped in a conditional similar to this:
  #   %ifarch noarch i386
  # We need it because if "BuildArch" is present RPM evaluates the spec
  # file multiple times (once for each compatible arch).
  my $suffix = '%ifarch noarch ' . $self->{rpm}->macro_value ('_target_cpu') . "\n";

  # Restore %_sourcedir to original value before expanding macros
  my $real_sourcedir = rpmquote ($self->{rpm}->macro_value ('_sourcedir'));
  $suffix .= "\%global _sourcedir " . $real_sourcedir . "\n";

  # Add user's macro expressions to LUA script
  $expander->add_user_expand_hash ($_ARGS{expand});

  # Add a few additional macros
  $expander->add_expr ("buildroot", '%{?buildroot}');
  $expander->add_expr ("build_name_fmt", '%{?_build_name_fmt}');

  # Create the LUA file and append a macro that executes it to the spec file
  $suffix .= $expander->finalize . "\n";

  # Also dump all macros, so we can collect Source, Patch and Icon URLs
  $suffix .= "\%{echo:$X_MARKER:DUMP-->}\%dump\%{echo:<--$X_MARKER:DUMP}\n";
  $suffix .= "\%endif\n";

  # Create the spec file
  my $specfile = $self->_create_specfile ($specdir, $suffix);

  # Create a query format for "rpm -q --qf..."
  my @tags = ('name', grep { $_ ne 'name' } keys (%_TAG_SPECS));
  @tags = grep { ($_TAG_SPECS{$_}->[0] & _GLOBAL) == 0 and $_TAG_SPECS{$_}->[1] } @tags;
  my @qf_list;
  for (@tags) {
    if (($_TAG_SPECS{$_}->[0] & _LIST) != 0) {
      push @qf_list, '[' . $_TAG_SPECS{$_}->[1] . ',]';
      next;
    };
    push @qf_list, $_TAG_SPECS{$_}->[1];
  };

  my $qf = "$X_MARKER:QF-->" . join ($X_MARKER, @qf_list) . "<--$X_MARKER:QF";
  my $cmd = $self->{rpm}->rpm ('-q', '--qf', $qf,
    '--define', "_sourcedir " . $abs_sourcedir, '--specfile', $specfile) . " 2>&1";

  # Call rpm; it may fail due to missing icons; create them and call rpm
  # again, repeatedly
  my $rpm_exit_status;
  my $rpm_output;
  my %icon_filename_hash;
  while (1) {
    debug_shellcmd $cmd;
    $rpm_output = `$cmd`;
    $rpm_exit_status = $?;
    $? == 0 and last;
    $rpm_output =~ /error: Unable to open icon \Q$abs_sourcedir\E\/(.*): /o or last;
    my $icon_filename = $1;
    $icon_filename_hash{$icon_filename} and last;
    $self->_create_dummy_icon ($abs_sourcedir, $icon_filename);
    $icon_filename_hash{$icon_filename} = 1;
  };
  debug "rpm returned $rpm_exit_status";

  # Save rpm output to log file
  my $log = IO::File->new ($logfile, 'w') or die "$logfile: $!\n";
  $log->print ($rpm_output);
  $log->close or die "$logfile: $!\n";

  # Parse out the stuff that we had added (delimited by $X_MARKER, etc.)
  while ($rpm_output =~ s/\Q$X_MARKER\E:([^:]+)-->(.*?)<--\Q$X_MARKER\E:\1//s) {
    my ($what, $data) = ($1, $2);

    # rpm -q results
    if ($what eq 'QF') {
      my @parts = split (/\Q$X_MARKER\E/o, $data, -1);
      $#parts == $#tags or confess qq(internal error: unexpected "rpm -q" output);
      my $package = $parts[0];
      push @package_list, $package;
      debug qq(found package "$package");
      for (my $i = 0; $i <= $#tags; ++$i) {
        my $tag = $tags[$i];
        my $value = $parts[$i];
        if ($tag eq 'obsoletes') { # rpm5 puts spaces around obsoleteflags
          $value =~ s/\s+//g;
        };
        $self->_save_package_tag ($package, $tag, $value);
      };
      next;
    };

    # %dump output
    if ($what eq 'DUMP') {
      while ($data =~ /^\s*-[0-9]+:\s*(SOURCEURL|PATCHURL)([0-9]+)\s+(.*)$/gmo) {
        my ($key, $seq, $url) = ($1, $2, trim ($3));
        my $basename = basename ($url);
        if ($key eq 'SOURCEURL') {
          $_SOURCE_HASH{$basename} = [ $seq, $url ];
        } else {
          $_PATCH_HASH{$basename} = [ $seq, $url ];
        };
        $self->_create_dummy_source ($abs_sourcedir, $basename);
      };
      next;
    };

    confess "internal error: unexpected output from rpm";
  };

  # Print remaining output
  print STDERR $rpm_output;
  $rpm_exit_status == 0 or die "rpm failed\n";

  # Parse macro expressions
  $self->{expansions} = $expander->parse_query_output;
  
  # Save package list
  $self->{global_tags}->{packages} = [ @package_list ];

  # Save buildroot
  $self->{global_tags}->{buildroot} = $self->{expansions}->{":buildroot"};
  delete $self->{expansions}->{":buildroot"};

  # Get build_name_fmt
  $_BUILD_NAME_FMT = $self->{expansions}->{":build_name_fmt"} || \
    '%%{ARCH}/%%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm';
  delete $self->{expansions}->{":build_name_fmt"};
  
  # Delete non-user expansions
  if (keys (%{$self->{expansions}}) == 0) {
    delete $self->{expansions};
  }

}

# phase2: build a dummy source package, then call "rpm -q" on it to determine
# build dependencies, etc.
#
# Usage: $self->_phase2
sub _phase2 {
  my $self = shift;
  my (%source_hash, %patch_hash, %icon_hash);
  my $real_sourcedir = $self->{rpm}->macro_value ('_sourcedir');
  my $sourcedir = $_WORKSPACE->dir ("SOURCES");
  my $abs_sourcedir = abs_path ($sourcedir) or die "$sourcedir: $!\n";
  my $specdir = $_WORKSPACE->dir ("PHASE_2");
  my $specfile = $self->_create_specfile ($specdir);
  my $rpmbuild_logfile = catfile ($specdir, "rpmbuild.log");
  my $rpm_logfile = catfile ($specdir, "rpm.log");
  my $cmd = $self->{rpm}->rpmbuild (
    '-bs',
    '--define', "_sourcedir " . $abs_sourcedir,
    '--define', "_srcrpmdir " . $specdir,
    '--nodeps',
    $specfile) . " 2>&1";

  # Remove all *.rpm files
  unlink glob ("$specdir/*.rpm");

  # Call rpmbuild and watch for "no such file" errors; create the missing
  # files; do that until rpm succeeds or fails for some other reason.
  my $rpmbuild_output;
  my $rpmbuild_exit_status;
  my %source_filename_hash;
  while (1) {
    debug_shellcmd $cmd;
    $rpmbuild_output = `$cmd`;
    $rpmbuild_exit_status = $?;
    $? == 0 and last;
    $rpmbuild_output =~ /error: .*? \Q$abs_sourcedir\E\/(.*): No such file/io or last;
    my $source_filename = $1;
    $source_filename_hash{$source_filename} and last;
    $self->_create_dummy_source ($abs_sourcedir, $source_filename);
    $source_filename_hash{$source_filename} = 1;
  };
  my $log = IO::File->new ($rpmbuild_logfile, 'w') or die "$rpmbuild_logfile: $!\n";
  $log->print ($rpmbuild_output);
  $log->close or die "$rpmbuild_logfile: $!\n";
  unless ($rpmbuild_exit_status == 0) {
    print STDERR $rpmbuild_output;
    die "rpmbuild failed\n";
  };
  my $source_rpm_filename = (glob ("$specdir/*.rpm"))[0];
  $source_rpm_filename or confess "internal error: rpmbuild failed";

  # Now query the source rpm for sources, patches and build dependencies.
  my @tags = grep { ($_TAG_SPECS{$_}->[0] & _BUILD) != 0 and $_TAG_SPECS{$_}->[1] } keys (%_TAG_SPECS);
  my @qf_list;
  for (@tags) {
    if (($_TAG_SPECS{$_}->[0] & _LIST) != 0) {
      push @qf_list, '[' . $_TAG_SPECS{$_}->[1] . ',]';
      next;
    };
    push @qf_list, $_TAG_SPECS{$_}->[1];
  };
  push @qf_list, '[%{SOURCE},]';
  push @qf_list, '[%{PATCH},]';
  my $qf = "$X_MARKER:QF-->" . join ($X_MARKER, @qf_list) . "<--$X_MARKER:QF";
  $cmd = $self->{rpm}->rpm (
    '-q', '--qf', $qf,
    '-p', $source_rpm_filename)
    . " 2>&1";
  debug_shellcmd $cmd;
  my $rpm_output = `$cmd`;
  my $rpm_exit_status = $?;
  $log = IO::File->new ($rpm_logfile, 'w') or die "$rpm_logfile: $!\n";
  $log->print ($rpm_output);
  $log->close or die "$rpm_logfile: $!\n";
  unless ($rpm_exit_status == 0) {
    print STDERR $rpm_output;
    die "rpm failed\n";
  };
  while ($rpm_output =~ s/\Q$X_MARKER\E:QF-->(.*?)<--\Q$X_MARKER\E:QF//go) {
    my @parts = split (/\Q$X_MARKER\E/o, $1, -1);
    $#parts == $#qf_list or 
      confess "internal error: unexpected output from rpm --qf:\n" .
              "  invalid number of query results:\n" .
              "  expected=" . scalar (@qf_list) . ", got=", scalar (@parts) . "\n ";
    for (my $i = 0; $i <= $#tags; ++$i) {
      my ($tag, $value) = ($tags[$i], $parts[$i]);
      $self->_save_global_tag ($tag, $value);
    };
    my $patch_str = pop (@parts);
    for (split (/\s*,\s*/o, $patch_str)) {
      next if $_ eq '(none)';
      debug qq(found patch file "$_");
      $patch_hash{$_} = undef;
    }
    my $source_str = pop (@parts);
    for (split (/\s*,\s*/o, $source_str)) {
      next if $_ eq '(none)';
      debug qq(found source file "$_");
      $source_hash{$_} = undef;
    }
  };

  # Get the list of all source files
  $cmd = $self->{rpm}->rpm ('-qlp', $source_rpm_filename);
  debug_shellcmd $cmd;
  my @all_source_files = map { basename $_ } split (/\n+/o, `$cmd`);
  $? == 0 or die "rpm failed\n";

  # Filter out sources, patches and the spec file; what remains are
  # the icons.
  my $spec_basename = basename ($_SPECFILE);
  for (@all_source_files) {
    next if exists $source_hash{$_};
    next if exists $patch_hash{$_};
    next if $_ eq $spec_basename;
    debug qq(found icon file "$_");
    $icon_hash{$_} = undef;
  };

  # Adjust source and patch order using the information we saved in phase1 in
  # %_SOURCE_HASH and %_PATCH_HASH
  my $seq_sort = sub {
    my $hash = shift;
    my $rec_a = $hash->{$a};
    my $rec_b = $hash->{$b};
    if (!defined ($rec_a) and !defined ($rec_b)) {
      return $a cmp $b;
    };
    if (!defined ($rec_a)) {
      return -1;
    };
    if (!defined ($rec_b)) {
      return 1;
    };
    return $rec_a->[0] <=> $rec_b->[0];
  };
  my @source_list = sort { &{$seq_sort} (\%_SOURCE_HASH) } keys (%source_hash);
  my @patch_list = sort { &{$seq_sort} (\%_PATCH_HASH) } keys (%patch_hash);
  my @icon_list = sort (keys (%icon_hash));

  # Save source, patch and icon URLs
  if (@source_list) {
    $self->{global_tags}->{sourceurls} = [ map {
      my $rec = $_SOURCE_HASH{$_};
      $rec ? $rec->[1] : $_
    } @source_list ];
  }

  if (@patch_list) {
    $self->{global_tags}->{patchurls} = [ map {
      my $rec = $_PATCH_HASH{$_};
      $rec ? $rec->[1] : $_
    } @patch_list ];
  }

  if (@icon_list) {
    $self->{global_tags}->{iconurls} = [ @icon_list ];
  };
  
  # Save srcrpmfile
  $self->{global_tags}->{sourcerpm} = basename ($source_rpm_filename);

}

# phase3:
#   - get binary RPM file names
sub _phase3 {
  my $self = shift;
  my $sourcedir = $_WORKSPACE->dir ("SOURCES");
  my $abs_sourcedir = abs_path ($sourcedir) or die "$sourcedir: $!\n";
  my $specdir = $_WORKSPACE->dir ("PHASE_2"); # reuse phase2 spec
  my $specfile = catfile ($specdir, basename ($_SPECFILE));
  my $cmd = $self->{rpm}->rpm (
    '-q',
    '--qf', $_BUILD_NAME_FMT . '\\n',
    '--define', "_sourcedir " . $abs_sourcedir,
    '--specfile',
    $specfile);
  debug_shellcmd $cmd;
  my $output = `$cmd`;
  $? == 0 or die "rpm failed\n";
  my @rpm_file_names = trim (split (/\n+/o, $output));
  scalar (@rpm_file_names) == scalar (@{$self->{global_tags}->{packages}})
    or confess "internal error: unexpected rpm output";
  for (my $i = 0; $i <= $#rpm_file_names; ++$i) {
    my $package = $self->{global_tags}->{packages}->[$i];
    my $filename = $rpm_file_names[$i];
    debug qq(found binary rpm file name "$filename");
    $self->{package_tags}->{$package}->{_binary_rpm_filename} = $filename;
  }
}

# Parse a spec file
# Usage: $self->_parse ($specfile, $spectext, %args);
# - $specfile: name of spec file
# - $spectext: contents of spec file
# - %args: constructor options
sub _parse {
  my ($self, $specfile, $spectext, %args) = @_;
  local $_WORKSPACE = RPM::Toolbox::Spec::Workspace->new (%args);
  local $_SPECFILE = $specfile;
  local $_SPECTEXT = $spectext;
  local %_ARGS = %args;
  local ($_FIRST_DUMMY_ICON_FILE, $_FIRST_DUMMY_SOURCE_FILE);
  local (%_SOURCE_HASH, %_PATCH_HASH);
  local $_BUILD_NAME_FMT;
  $self->_phase1;
  $self->_phase2;
  $self->_phase3;
}

# Construct a new object.
# Usage: __PACKAGE__->_newobj ($specfile, $spectext, $args):
# - $specfile: name of spec file
# - $spectext: contents of spec file
# - %args: constructor options
sub _newobj ($$$%) {
  my ($class, $specfile, $spectext, %args) = @_;
  local $_;
  local $RPM::Toolbox::Spec::Util::DEBUG = $args{debug};
  my $self = {};
  bless $self, $class;
  $self->{rpm} = RPM::Toolbox::Spec::RPM->new (%args);
  my $cache = RPM::Toolbox::Spec::Cache->new ($specfile, $spectext, %args);
  my $data = $cache->load;
  if ($data) {
    for (@_CACHE_KEYS) {
      $self->{$_} = $data->{$_};
    };
  } else {
    $self->_parse ($specfile, $spectext, %args);
    my %save_hash = map { $_ => $self->{$_} } @_CACHE_KEYS;
    $save_hash{expansions} or delete $save_hash{expansions};
    $cache->save ( \%save_hash );
  }
  return $self;
}

# Construct a new object by parsing a file.
# Usage: __PACKAGE__->parse_file ($filename, %args);
sub parse_file {
  my ($class, $filename, %args) = @_;
  my $spectext = read_file ($filename);
  _newobj ($class, $filename, $spectext, %args);
}

# Construct a new object by parsing a string.
# Usage: __PACKAGE__->parse_string ($text, %args);
sub parse_string {
  my ($class, $spectext, %args) = @_;
  my $filename = "spec";
  _newobj ($class, $filename, $spectext, %args);
}

# Autoload tag methods
sub AUTOLOAD {
  my $self = shift;
  my $type = ref ($self) or croak "$self is not an object";
  our $AUTOLOAD;
  my $tag = $AUTOLOAD;
  $tag =~ s/.*://;

  exists ($_TAG_SPECS{$tag})
    or croak qq(Can't locate object method "$tag" via package "$type");
  my $tag_spec = $_TAG_SPECS{$tag};

  my $value;
  if (($tag_spec->[0] & _GLOBAL) == 0) {
    my $package = shift || $self->{global_tags}->{packages}->[0];
    $self->{package_tags}->{$package} and
      $value = $self->{package_tags}->{$package}->{$tag};
  } else {
    $value = $self->{global_tags}->{$tag};
  };
  
  if (($tag_spec->[0] & _LIST) == 0) {
    return $value;
  };
  if (defined ($value) and ref ($value) ne 'ARRAY') {
    confess "internal error: tag data corrupted ($tag: $value)";
  };
  return defined ($value) ? @{$value} : ();
}

# Avoid autoload errors
sub DESTROY {}

# Return the name of the first package
sub mainpackage { (shift->packages)[0] }

# Concatenate version-related parts into one string
sub fullversion {
  my ($self, $package) = @_;
  if (defined ($package)) {
    $self->{package_tags}->{$package} or return undef;
  } else {
    $package = $self->mainpackage;
  };
  my $epoch = $self->epoch ($package);
  my $version = $self->version ($package);
  my $release = $self->release ($package);
  my $fullversion = defined ($epoch) ? $epoch . ':' : '';
  $fullversion .= $version . '-' . $release;
  return $fullversion;
}

# Full path of the package's binary rpm file name
sub binaryrpmfile {
  my ($self, $package) = @_;
  if (defined ($package)) {
    $self->{package_tags}->{$package} or return undef;
  } else {
    $package = $self->mainpackage;
  };
  my $rel_filename =
    $self->{package_tags}->{$package}->{_binary_rpm_filename};
  return catfile ($self->{rpm}->macro_value ('_rpmdir'), $rel_filename);
}

# Basename of the package's binary rpm file name
sub binaryrpm {
  my ($self, $package) = @_;
  return basename ($self->binaryrpmfile ($package));
}

# List of all binary rpm full paths
sub rpmfiles {
  my $self = shift;
  my @list;
  for my $p ($self->packages) {
    push @list, $self->binaryrpmfile ($p);
  }
  return @list;
}

# List of all binary rpm base names
sub rpms {
  my $self = shift;
  my @list;
  for my $p ($self->packages) {
    push @list, $self->binaryrpm ($p);
  }
  return @list;
}


# Return various source file tags with %_sourcedir prepended
sub _fqsrcfiles {
  my ($self, $tag) = @_;
  local $_;
  my $sourcedir = $self->{rpm}->macro_value ('_sourcedir');
  my @basenamelist = map { basename $_ } @{$self->{global_tags}->{$tag}};
  return map { catfile ($sourcedir, $_) } @basenamelist;
}
sub sourcefiles { shift->_fqsrcfiles ('sourceurls') }
sub patchfiles  { shift->_fqsrcfiles ('patchurls') }
sub iconfiles   { shift->_fqsrcfiles ('iconurls') }

# Return basenames of various source file tags
sub _srcfiles {
  my ($self, $tag) = @_;
  local $_;
  my @basenamelist = map { basename $_ } @{$self->{global_tags}->{$tag}};
  return @basenamelist;
};
sub sources { shift->_srcfiles ('sourceurls') }
sub patches { shift->_srcfiles ('patchurls') }
sub icons   { shift->_srcfiles ('iconurls') }

# Return source rpm file name with %_sourcedir prepended
sub sourcerpmfile {
  my $self = shift;
  return catfile (
    $self->{rpm}->macro_value ('_srcrpmdir'),
    $self->{global_tags}->{sourcerpm});
};

# Return the result of evaluating an expression passed to constructor in
# expand hash
sub expansion {
  my ($self, $key) = @_;
  exists $self->{expansions} or return undef;
  return $self->{expansions}->{"user:$key"};
}

1;

