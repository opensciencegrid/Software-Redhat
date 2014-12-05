%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global pyver %(%{__python} -c "import sys; print sys.version[0]+sys.version[2]")
%global pydotver %(%{__python} -c "import sys; print sys.version[:3]")

Name: voms-admin-client
Version: 2.0.17
Release: 1.1%{?dist}
Summary: The VOMS administration service command line tool

Group: Applications/Internet
License: ASL 2.0
URL: https://twiki.cnaf.infn.it/twiki/bin/view/VOMS
Source: %{name}-%{version}.tar.gz

BuildRequires: python-ZSI
BuildRequires: python-devel
BuildRequires: python-simplejson
BuildRequires: asciidoc

Requires: python
Requires: python-ZSI
Requires: python-simplejson

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Packager: Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it>

%description

The Virtual Organization Membership Service (VOMS) is an attribute authority
which serves as central repository for VO user authorization information,
providing support for sorting users into group hierarchies, keeping track of
their roles and other attributes in order to issue trusted attribute
certificates and SAML assertions used in the Grid environment for 
authorization purposes.

The VOMS Admin service is a web application providing tools for administering
the VOMS VO structure. It provides an intuitive web user interface for daily
administration tasks

The voms-admin command line tool provides access to the most common VOMS Admin
service administrative operations.

%prep
%setup -q  

%build
# Nothing to build
  
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr
make install prefix=$RPM_BUILD_ROOT/usr

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%dir %{python_sitelib}/VOMSAdmin
%{python_sitelib}/VOMSAdmin/*

%{_bindir}/voms-admin

%doc %{_mandir}/man1/voms-admin.1.gz
%dir %{_docdir}/%{name}/
%doc %{_docdir}/%{name}/CHANGELOG
%doc %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README

# Egg packaging
%if (%{pyver} > 24)
%{python_sitelib}/voms_admin_client-%{version}-py%{pydotver}.egg-info
%endif

%changelog
* Fri Dec 05 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 2.0.17-1.1
- Remove PyXML dependency, build for EL7

* Thu Aug 25 2011 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 2.0.17-1
- Removed dependency on the VOMS_LOCATION environment variable
- Restructured packaging and build towards Fedora packaging guidelines full compliance
- Added man page for voms-admin script
