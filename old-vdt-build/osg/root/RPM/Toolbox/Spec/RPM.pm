# vim:ts=2:sts=2:sw=2:et

package RPM::Toolbox::Spec::RPM;

use warnings;
use strict;
use RPM::Toolbox::Spec::Util qw(:all);
use Carp;
use IO::File;

# Usage:
#   new (
#     rpm_command => "rpm",
#     rpmbuild_command => "rpmbuild",
#     defines => [ "MACRO VALUE", ... ]
#     rcfile => "FILE:FILE:...",
#     target => "ARCH-VENDOR-OS",
#     buildroot => "/path/to/build/root",
#  )
sub new {
  my ($class, %args) = @_;
  my $self = { %args };
  bless $self, $class;
  $self->{rpm_command} = 'rpm' unless $self->{rpm_command};
  $self->{rpmbuild_command} = 'rpmbuild' unless $self->{rpmbuild_command};
  $self->{defines} = [] unless $self->{defines};
  $self->_init_macros;
  return $self;
}

sub _cmd {
  my ($self, $prog, @args) = @_;
  my @all_args;
  local $_;
  if ($self->{rcfile}) {
    push @all_args, "--rcfile", $self->{rcfile}
  }
  for (@{$self->{defines}}) {
    push @all_args, '--define', $_
  };
  if ($prog eq 'rpmbuild_command') {
    push @all_args, '--target', $self->{target}
      if $self->{target};
    push @all_args, '--buildroot', $self->{buildroot}
      if $self->{buildroot};
  };
  push @all_args, @args;
  my $env = 'LC_ALL=C LANG=';
  return $env . ' ' . $self->{$prog} . ' ' . shellquote (@all_args);
}

sub _init_macros {
  my $self = shift;
  my @macros = qw(_topdir _specdir _sourcedir _srcrpmdir _rpmdir _tmppath _target_cpu);
  my $eval_str = join ($X_MARKER, map { '%' . $_ } @macros);
  my $cmd = $self->rpm ("--eval", $eval_str);
  debug_shellcmd $cmd;
  my $fh = IO::File->new ("$cmd|") or die "rpm failed\n";
  local $_;
  my $buf = '';
  while (defined ($_ = $fh->getline)) {
    $buf .= $_
  }
  $fh->close or die "rpm failed\n";
  my @macro_values = split (/\Q$X_MARKER\E/o, $buf);
  $#macros == $#macro_values or confess "internal error";
  for (my $i = 0; $i <= $#macros; ++$i) {
    my ($macro, $value) = ($macros[$i], trim ($macro_values[$i]));
    $self->{macros}->{$macro} = $value;
  }; 
}

sub rpm { shift->_cmd ('rpm_command', @_) }

sub rpmbuild { shift->_cmd ('rpmbuild_command', @_) }

sub macro_value {
  my ($self, $macro) = @_;
  return $self->{macros}->{$macro}
}

1;

