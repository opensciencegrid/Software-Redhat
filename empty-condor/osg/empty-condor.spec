Name:           empty-condor
Version:        1.0
Release:        3%{?dist}
Summary:        An empty Condor package

Group:          Applications/System
License:        Unknown
URL:            http://vdt.cs.wisc.edu

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Provides:       condor

%description

This pacakge is empty (it provides no files), but it claims to provide all of
Condor. This allows users to install Condor with a different mechanism 
(such as from a binary tarball or built from source), and fake out RPM so that it 
believes that Condor has been installed via RPM. 

%prep

%build

%install

%clean

%files

%doc

%changelog
* Mon Jan 30 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-3
- Removing conflict with condor

* Mon Jan 30 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-2
- Adding conflict with RPM based Condor

* Thu Nov 17 2011 Alain Roy <roy@cs.wisc.edu> - 1.0-1
- Initial version
