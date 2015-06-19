Name:		empty-slurm
Version:	1.0
Release:	1%{?dist}
Summary:	An empty slurm package
Group:		Applications/Misc
License:	Apache 2.0
BuildArch:	noarch
Provides:	slurm

%description
An empty package that provides slurm (not really)

For installing OSG software that requires slurm, which is not available
from the standard repos (OS + EPEL + OSG), without actually having to
install slurm.  In particular, this is for gratia-probe-slurm.
  
%install
%clean
%files
%changelog
* Thu Jun 18 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.0-1
- Initial release
