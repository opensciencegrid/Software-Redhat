Name:           empty-gridengine
Version:        1.0
Release:        3%{?dist}
Summary:        An empty gridengine package

License:        Unknown
URL:            http://vdt.cs.wisc.edu

BuildArch:      noarch

Provides:       gridengine

%description

This pacakge is empty (it provides no files), but it claims to provide
all of Gridengine. This allows users to install Gridengine with a
different mechanism (such as from a binary tarball), and fake out RPM
so that it believes that Gridengine has been installed via RPM.

%prep

%build

%install

%files

%doc

%changelog
* Thu Mar 31 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0-3
- rebuilt

* Wed May 23 2012 Alain Roy <roy@cs.wisc.edu> - 1.0-2
- Rebuild to update dist tag and build on SL6

* Thu Nov 17 2011 Alain Roy <roy@cs.wisc.edu> - 1.0-1
- Initial version
