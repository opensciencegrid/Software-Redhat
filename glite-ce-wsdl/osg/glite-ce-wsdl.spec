Summary: WS definitions for the CREAM service
Name: glite-ce-wsdl
Version: 1.14.0
%global upstream_release 4
Release: %{upstream_release}.1%{?dist}
License: Apache Software License
URL: http://glite.cern.ch/
Group: Development/Libraries
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}-%{version}-%{upstream_release}.sl5.tar.gz


%description
WS definitions for the CREAM service

%prep
 
%setup -c -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
%{!?extbuilddir:%define extbuilddir "--"}
if test "x%{extbuilddir}" == "x--" ; then
  ./project/install.sh %{buildroot}/usr 
else
  cp -R %{extbuilddir}/* %{buildroot}
fi


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir /usr/share/wsdl/
%dir /usr/share/wsdl/cream-ce/
%dir /usr/share/wsdl/cream-ce/es
/usr/share/wsdl/cream-ce/*.wsdl
/usr/share/wsdl/cream-ce/*.xsd
/usr/share/wsdl/cream-ce/es/*.wsdl
/usr/share/wsdl/cream-ce/es/*.xsd


%changelog
* Thu Jun 07 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.1.osg
- Add dist tag

* Wed May 16 2012 CREAM group <cream-support@lists.infn.it> - 1.14.0-4.sl5
- Major bugs fixed


