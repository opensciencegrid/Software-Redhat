Name:           empty-torque
Version:        2.0
Release:        2%{?dist}
Summary:        An empty Torque/PBS package

Group:          Applications/System
License:        Unknown
URL:            http://vdt.cs.wisc.edu

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Provides:       torque
Provides:       torque-server
Provides:       torque-client

%description

This pacakge is empty (it provides no files), but it claims to provide all of
Torque. This allows users to install Torque with a different mechanism 
(such as from a binary tarball or using PBS), and fake out RPM so that it 
believes that Torque has been installed via RPM. 

%prep

%build

%install

%clean

%files

%doc

%changelog
* Thu Mar 24 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 2.0-2
- bump to rebuild

* Wed May 23 2012 Alain Roy <roy@cs.wisc.edu> - 1.0-2
- Rebuild to update dist tag and build on SL6 

* Thu Nov 17 2011 Alain Roy <roy@cs.wisc.edu> - 1.0-1
- Initial version
