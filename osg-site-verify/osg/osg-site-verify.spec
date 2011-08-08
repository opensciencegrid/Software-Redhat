
Name:           osg-site-verify
Version:        3.0.0
Release:        1%{?dist}
Summary:        CE verification script for the OSG

Group:          System Environment/Tools
License:        Apache 2.0
URL:            https://twiki.grid.iu.edu/bin/view/ReleaseDocumentation/ValidatingComputeElement

# Generated on Sun, 7 Aug 2011 (r12597) doing the following:
# svn export https://vdt.cs.wisc.edu/svn/vdt/trunk/OSG-Site-Verify/verify osg-site-verify-3.0.0
# tar zcf osg-site-verify-3.0.0.tar.gz osg-site-verify-3.0.0
Source0:        %{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
%{summary}

%prep
%setup -q

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp site_verify.pl $RPM_BUILD_ROOT%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}

%changelog
* Sun Aug 07 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-1
- Initial packaging of osg-site-verify

