
Name:           vdt-build
Version:        0.0.3
Release:        1
Summary:        Build tools for the VDT

Group:          System Environment/Tools
License:        Apache 2.0
URL:            https://twiki.grid.iu.edu/bin/view/SoftwareTeam/RPMDevelopmentGuide

Source0:        %{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-roo1t-%(%{__id_u} -n)
BuildArch:      noarch

%description
%{summary}


%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/%{name}/VDTBuildConstants.py*
%{_datadir}/%{name}/VDTBuildUtils.py*
%doc %{_datadir}/%{name}/sample-vdt-build.ini

%changelog
* Fri Jul 15 2011 Matyas Selmeci <matyas@cs.wisc.edu> 0.0.3-1
- Various bugfixes (SOFTWARE-{14,15,16})

* Thu Jul 14 2011 Matyas Selmeci <matyas@cs.wisc.edu> 0.0.2-1
- Python rewrite

* Thu Jul  7 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.1-2
- Made vdt-build obey our own packaging guidelines.

* Fri Jul  1 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.1-1
- Created an initial vdt-build RPM for ease-of-use
- Contains RPM::Toolbox::Spec for now.

