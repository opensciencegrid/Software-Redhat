%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:                   graphtool
Version:                0.6.6
Release:                23%{?dist}
Summary:                CMS Common Graphing Package.

Group:                  Development/Libraries
License:                Apache 2.2.15
URL:                    http://t2.unl.edu/documentation/graphtool
Source0:                %{name}-%{version}.tar.gz
BuildRoot:              %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:              noarch


BuildRequires:          python-setuptools
Requires:               python >= 2.3 
Requires:               python-matplotlib >= 0.97.1 
Requires:               numpy >= 1.2.1 
Requires:               python-imaging >= 1.1.5
Requires:               python-setuptools

%description
GraphTool is a python graphing tool using the matplotlib library that
runs under CherryPy.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install --skip-build --root %{buildroot}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
/usr/bin/graphtool


%changelog

* Tue Feb 10 2015 Juan F. Mosquera <jmorales@fnal.gov>
- modifications to solve bug GRATIAWEB-69

* Tue Jan 06 2015 Carl Edquist <edquist@cs.wisc.edu> - 0.6.6-22
- revert mysql_util / regex reducing changes for now (goc/23461)

* Fri Nov 14 2014 Juan F. Mosquera <jmorales@fnal.gov>
- modifications and program additions to resolve OSG
- SOFTWARE-1671 and GRATIAWEB-60.

* Tue Sep 30 2014 Juan F. Mosquera <jmorales@fnal.gov>
- modifications and program additions to resolve OSG
- GRATIAWEB-58.

* Tue Mar 18 2014 William B Hurst <wbhurst@cse.unl.edu>
- package fixes and bump of version release

* Fri Mar 14 2014 William B Hurst <wbhurst@cse.unl.edu>
- Enhanced mysql database connector error handling as
- requested by GratiaWeb-48

* Fri Mar 14 2014 William B Hurst <wbhurst@cse.unl.edu>
- updated and restructured rpm package management

* Wed Feb 20 2013 Ashu Guru <aguru2@unl.edu>
- Added space gaps for the query placeholders in connection_manager to avoid index clashes in find

* Fri Jan 11 2013 Ashu Guru <aguru2@unl.edu>
- Moving spec file to upstream

* Wed Jan 09 2013 Ashu Guru <aguru2@unl.edu>
- Fixing the problem of static sites

* Tue Oct 02 2012 Ashu Guru <aguru2@unl.edu>
- Fixing xsl for safari and Chrome

* Mon May 31 2012 Ashu Guru <aguru2@unl.edu>
- Updated for fixing the number of bins and days of bar chart report issue
- (https://jira.opensciencegrid.org/browse/GRATIAWEB-17)

* Mon Apr 9 2012 Ashu Guru <aguru2@unl.edu>
- Updated the javascript code for resolving the IE dropdown incompatability
- (http://jira.opensciencegrid.org/browse/GRATIAWEB-14)

