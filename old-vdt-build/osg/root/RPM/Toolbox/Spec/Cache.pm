# vim:ts=2:sts=2:sw=2:et

package RPM::Toolbox::Spec::Cache;

use warnings;
use strict;
use RPM::Toolbox::Spec::Util qw(:all);
use Digest::MD5;
use MIME::Base64;
use Cwd qw(abs_path);

sub new {
  my ($class, $specfile, $spectext, %args) = @_;
  my $self = {
    specfile => $specfile,
    spectext => $spectext,
    args => { %args },
  };
  eval "use YAML qw(Dump DumpFile LoadFile)";
  if ($@) {
    debug "caching disabled: YAML module is not available"
  } else {
    $self->{cache_enabled} = 1
  }
  return bless ($self, $class)
}

sub save {
  my ($self, $data) = @_;
  return unless $self->{cache_enabled} && $self->{args}->{cache};
  eval {
    local $YAML::UseCode = undef;
    my $digest = $self->_digest;
    debug "saving cache to \"", $self->{args}->{cache}, "\"";
    DumpFile ($self->{args}->{cache},
      $RPM::Toolbox::Spec::VERSION, $digest, $data)
  };
  if ($@) {
    $@ =~ s/\n+$//o;
    debug $@;
    debug "failed to save cache"
  }
}

sub load {
  my ($self) = @_;
  my ($cache_version, $cache_digest, $cache_data);

  if ($self->{args}->{cache} and $self->{cache_enabled} and -f $self->{args}->{cache}) {
    eval {
      local $YAML::UseCode = undef;
      my $digest = $self->_digest;
      debug "loading cache from \"", $self->{args}->{cache}, "\"";
      ($cache_version, $cache_digest, $cache_data) =
        LoadFile ($self->{args}->{cache});
      $cache_version eq $RPM::Toolbox::Spec::VERSION
        or die "cache file version mismatch\n";
      $digest eq $cache_digest or
        die "cache digest mismatch\n";
    };
    if ($@) {
      $@ =~ s/\n+$//o;
      debug $@;
      debug "failed to load cache";
      return undef
    }
  };
  return $cache_data
}

sub _add_file_to_digest ($$) {
  my ($md5, $filename) = @_;
  -f $filename or next;
  debug qq(adding file "$filename" to cache digest);
  my @stat = stat ($filename) or return;
  my $path = abs_path ($filename) or next;
  $md5->add ($path);
  $md5->add ($stat[7]);   # size
  $md5->add ($stat[9]);   # mtime
}

sub _digest {
  my ($self) = @_;

  unless (defined ($self->{digest})) {
    local $_;

    my $md5 = Digest::MD5->new;

    # Add the text of the spec file
    debug "adding spec text to cache digest";
    $md5->add ($self->{spectext});

    # Add user's macros file
    my $homedir = (getpwuid ($>))[7];
    $homedir and _add_file_to_digest ($md5, "$homedir/.rpmmacros");

    # Add user arguments
    for (sort (keys (%{$self->{args}}))) {
      my $arg_value = $self->{args}->{$_};

      /^expand$/ and $arg_value and do {
        for my $key (sort (keys (%{$arg_value}))) {
          debug qq(adding expand key "$key" to cache digest);
          $md5->add ($key);
          my $value = $arg_value->{$key};
          if (defined ($value)) {
            $md5->add ($value);
            $value =~ /^\@/o and
              _add_file_to_digest ($md5, substr ($value, 1));
          };
        };
        next;
      };

      /^rpm_command|rpmbuild_command|rcfile|target$/ and do {
        defined $arg_value or next;
        debug qq(adding argument "$_" to cache digest");
        $md5->add ($_);
        $md5->add ($arg_value);
        next;
      };

      /^defines$/ and do {
        if (ref ($arg_value) and ref ($arg_value) eq 'LIST') {
          debug qq(adding rpm "defines" argument to cache digest");
          $md5->add (sort (@{$arg_value}));
        };
        next;
      };
    } # for

    my $digest = unpack ('H*', $md5->digest);
    debug qq(cache digest: $digest);
    $self->{digest} = "MD5:$digest";
  };
  return $self->{digest}
}

1;

