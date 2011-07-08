# vim:ts=2:sts=2:sw=2:et

package RPM::Toolbox::Spec::Workspace;

use warnings;
use strict;
use Carp;
use File::Temp qw(tempdir);
use File::Spec::Functions;
use File::Path qw(mkpath rmtree);
use RPM::Toolbox::Spec::Util qw(:all);

# Usage: new (workdir => "/path/to/workdir")
sub new {
  my ($class, %args) = @_;
  my $self = {};
  bless $self, $class;
  my $wd = $args{workdir};
  if ($wd) {
    $self->{cleanup} = undef;
    unless (-d $wd) {
      debug qq(creating directory "$wd");
      mkpath ($wd);
    }
  } else {
    $wd = tempdir ("rpmtoolbox_XXXXXX", DIR => File::Spec->tmpdir,
      CLEANUP => 1);
    debug qq(created directory $wd);
    $self->{cleanup} = 1;
  };
  $self->{workdir} = $wd;
  return $self;
}

sub dir {
  my ($self, $subdir) = @_;
  $subdir or return $self->{workdir};
  my $path = catfile ($self->{workdir}, $subdir);
  unless (-d $path) {
    debug qq(creating directory "$path");
    mkpath ($path);
  }
  return $path;
}

sub DESTROY {
  my $self = shift;
  if ($self->{cleanup}) {
    debug "removing directory \"", $self->{workdir}, "\"";
    rmtree $self->{workdir};
  };
}


1;

