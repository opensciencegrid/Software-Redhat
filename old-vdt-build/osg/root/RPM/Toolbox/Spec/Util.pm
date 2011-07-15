# vim:ts=2:sts=2:sw=2:et
package RPM::Toolbox::Spec::Util;

use warnings;
use strict;
use Carp;

our $DEBUG;
our $X_MARKER = '-=#RPMTOOLBOX#=-';

# Remove leading and trailing whitespace from each string in the list.
sub trim {
  my @list = wantarray ? @_ : shift;
  local $_;
  for (@list) {
    defined or next;
    s/^\s+//go;
    s/\s+$//go
  };
  return @list if wantarray;
  return shift @list
}

# Usage: read_file $FILENAME
#        read_file $FILENAME, $FILE_HANDLE
sub read_file($) {
  my ($filename, $fh) = @_;
  my $close;
  unless ($fh) {
    $fh = IO::File->new ($filename, 'r') or die "$filename: $!\n";
    $close = 1
  };
  my $buf = '';
  while (1) {
    my $n = $fh->read ($buf, 4096, length ($buf));
    $n == 0 and last;
    $n < 0 and die "$filename: $!\n";
    last if $n == 0;
  };
  if ($close) {
    $fh->close or die "$filename: $!\n"
  };
  return $buf
}

# Usage: write_file ($DATA, $FILENAME)
sub write_file($$) {
  my ($data, $filename) = @_;
  my $fh = IO::File->new ($filename, 'w') or die "$filename: $!\n";
  $fh->print ($data);
  $fh->close or die "$filename: $!\n";
}

# Construct a string from a list, with each item shell-quoted.
# Example: shellquote ('a', 'b c', 'd') returns 'a "b c" d'
sub shellquote {
  my @list = @_;
  local $_;
  for (@list) {
    defined or confess "undef value in shellquote";
    length == 0 and do {
      $_ = '""';
      next
    };
    /([]~`!#\$\%\&\*\(\)\{\};"'<>\?\\[]|\s)/ and do {
      s/(["\\\$])/\\$1/go;
      $_ = '"' . $_ . '"';
      next
    }
  };
  return join (' ', @list)
}

# Quote an RPM macro
sub rpmquote {
  my $s = shift;
  $s =~ s/\%/\%\%/go;
  return $s
}

# Log a debug message
sub debug {
  return unless $DEBUG;
  print STDERR @_, "\n";
}

# Log a shell command
sub debug_shellcmd {
  return unless $DEBUG;
  print STDERR '% ', @_, "\n";
}

BEGIN {
  use Exporter ();
  our @ISA = qw(Exporter);
  our @EXPORT = qw();
  our @EXPORT_OK =
  qw($X_MARKER $DEBUG
     trim read_file write_file shellquote rpmquote
     debug debug_shellcmd);
  our %EXPORT_TAGS = ( all => [ @EXPORT_OK ] );
}

1;

