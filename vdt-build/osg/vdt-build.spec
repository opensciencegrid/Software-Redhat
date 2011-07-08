
Name:           vdt-build
Version:        0.0.1
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

This package improperly contains RPM::Toolbox::Spec.  It will be fixed in the future.

#Requires: perl(RPM::Spec)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%prep
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 %{name} $RPM_BUILD_ROOT/%{_bindir}

mkdir -p $RPM_BUILD_ROOT/%{perl_vendorlib}
mv RPM $RPM_BUILD_ROOT/%{perl_vendorlib}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/RPM/Toolbox/Spec/Expander.pm
%{perl_vendorlib}/RPM/Toolbox/Spec/Util.pm
%{perl_vendorlib}/RPM/Toolbox/Spec/RPM.pm
%{perl_vendorlib}/RPM/Toolbox/Spec/Workspace.pm
%{perl_vendorlib}/RPM/Toolbox/Spec/Cache.pm
%{perl_vendorlib}/RPM/Toolbox/Spec.pm
%{perl_vendorlib}/RPM/Toolbox/Spec.pod
%{_bindir}/%{name}

%changelog
* Thu Jul  7 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.1-2
- Made vdt-build obey our own packaging guidelines.

* Fri Jul  1 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.1-1
- Created an initial vdt-build RPM for ease-of-use
- Contains RPM::Toolbox::Spec for now.

