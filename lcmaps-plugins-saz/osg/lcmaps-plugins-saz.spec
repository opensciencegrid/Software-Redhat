
%define modname lcmaps_saz_client.mod

Name:           lcmaps-plugins-saz
Version:        0.0.1
Release:        1
Summary:        SAZ support for lcmaps

Group:          System Environment/Tools
License:        Apache 2.0

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:       lcmaps-plugins-scas-client

%description
%{summary}

%prep

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/modules
cd $RPM_BUILD_ROOT%{_libdir}/modules
ln -s lcmaps_scas_client.mod %{modname}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/modules/%{modname}

%changelog
* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.1-1
- Initial packaging.

