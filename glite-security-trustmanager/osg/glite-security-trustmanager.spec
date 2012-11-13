%global with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}

Name:           glite-security-trustmanager
Version:        2.5.5
Release:        4.1%{?dist}
Summary:        Java trustmanager interface supporting a GSI grid name space

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            https://twiki.cern.ch/twiki/bin/view/EGEE/TrustManager
# The source for this package was pulled from upstream's cvs. Use the
# following commands to generate the tarball:
# cvs -q -d:pserver:anonymous:@glite.cvs.cern.ch:/cvs/glite checkout \
#      -r  glite-security-trustmanager_R_2_5_5  org.glite.security.trustmanager
# find org.glite.security.trustmanager -type f -print0 | xargs -0 chmod a-x 
# find org.glite.security.trustmanager -name CVS -print0 | xargs -0  rm -rf 
# tar cvfz glite-security-trustmanager-2.5.5.tar.gz org.glite.security.trustmanager
Source0:        %{name}-%{version}.tar.gz
Source1:        README.Fedora
Source2:        %{name}-log4j.properties

# trustmanager-use-vomsjapi.patch
# Since VOMSValidator class has been patched out of glite-security-util-java
# in favour of using the vomsjapi  package we have to patch this to
# use org.glite.voms.VOMSValidator rather than org.glite.security.voms.VOMSValidator
# https://savannah.cern.ch/bugs/?68035
Patch0:         trustmanager-use-vomsjapi.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{with_gcj}
BuildRequires:    java-gcj-compat-devel >= 1.0.31
Requires(post):   java-gcj-compat >= 1.0.31
Requires(postun): java-gcj-compat >= 1.0.31
%else
BuildArch:      noarch
%endif

BuildRequires:  jpackage-utils
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  ant
BuildRequires:  axis
BuildRequires:  bouncycastle
BuildRequires:  log4j
BuildRequires:  voms-api-java >= 2.0.8
BuildRequires:  servletapi5
BuildRequires:  glite-security-util-java >= 2.5.5
BuildRequires:  tomcat5-server-lib

Requires:       java >= 1:1.6.0
Requires:       voms-api-java >= 2.0.8
Requires:       jpackage-utils
Requires:       axis
Requires:       bouncycastle
Requires:       log4j
Requires:       glite-security-util-java >= 2.5.5
Requires:       servletapi5

%if 0%{?el5}
ExcludeArch: ppc
%endif 


%description
glite-security-trustmanager together with glite-security-util-java is 
an implementation of the java TrustManager interface with implementation 
of cert path checking, grid name space restrictions and dynamic loading
of CA certs, credentials, CRLs and name space restrictions.  
Also provided is integration into tomcat, axis and axis2. There 
are many utility classes and methods for certificate and proxy handling 
in glite-security-util-java. It can be used both in the server side for 
the server SSL handler and on the client side for the opening of SSL 
connections. 

%package tomcat5
Summary: Java trustmanager interface supporting a GSI grid name space
Group:   System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: tomcat5
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:      noarch
%endif

%description tomcat5
glite-security-trustmanager together with glite-security-util-java is 
an implementation of the java TrustManager interface with implementation 
of cert path checking, grid name space restrictions and dynamic loading
of CA certs, credentials, CRLs and name space restrictions.  
Also provided is integration into tomcat, axis and axis2. There 
are many utility classes and methods for certificate and proxy handling 
in util-java. It can be used both in the server side for the server SSL 
handler and on the client side for the opening of SSL connections. 

glite-security-trustmanager-tomcat5 provides the necessary files
for a tomcat connector to be set up.


%package javadoc
Summary:        Documentation as javadocs for %{name}
Group:          Documentation
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:      noarch
%endif
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n org.glite.security.trustmanager
%patch0 -p1
find -name '*.jar' -o -name '*.class' -exec rm -f '{}' \;
cp %{SOURCE1} .
cp %{SOURCE2} .

%build
export CLASSPATH=$(build-classpath vomsjapi tomcat5 glite-security-util-java servletapi5 commons-logging bcprov log4j axis)
%ant -q -Dprefix=build compile-extcp
%ant -Dprefix=build doc-extcp

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p  build/share/java/%{name}.jar  \
$RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp build/share/%{name}/doc/html/*  \
$RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %{with_gcj}
%{_bindir}/aot-compile-rpm
%endif

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_var}/log/%{name}

cp -p %{name}-log4j.properties $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/trustmanager-log4j.properties

%post 
%if %{with_gcj}
  if [ -x %{_bindir}/rebuild-gcj-db ] 
  then
    %{_bindir}/rebuild-gcj-db
  fi
%endif

%post tomcat5
# This is bad packaging: The symbolic links created below are needed
# but they are not cleaned up when the package is removed and it is not
# obvious that removing them will do more harm than good.
# tomcat5 seems to be perfectly happy to run with dangling symlinks 
# and they are cleaned up when the tomcat5 package itself is removed.

build-jar-repository /var/lib/tomcat5/server/lib log4j bcprov vomsjapi  \
      glite-security-util-java %{name}

%postun
%if %{with_gcj}
  if [ -x %{_bindir}/rebuild-gcj-db ] 
  then
    %{_bindir}/rebuild-gcj-db
  fi
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_javadir}/*
%if %{with_gcj}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%endif

%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/trustmanager-log4j.properties
%doc LICENSE doc/USAGE

%files tomcat5
%defattr(-,root,root,-)
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/%{name}
%dir %attr(-,tomcat,tomcat) %{_var}/log/%{name}
%doc README.Fedora

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

%changelog
* Mon Nov 12 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.5.5-4.1
- Require 'voms-api-java >= 2.0.8' instead of 'vomsjapi'

* Thu May 27 2010 Steve Traylen <steve.traylen@cern.ch> - 2.5.5-4
- Don't build for ppc on .el5.

* Thu May 27 2010 Steve Traylen <steve.traylen@cern.ch> - 2.5.5-3
- Add upstream bug reference for  trustmanager-use-vomsjapi.patch

* Sat May 22 2010 Steve Traylen <steve.traylen@cern.ch> - 2.5.5-2
- Various fixes following fedora review process.

* Fri Apr 29 2010 Steve Traylen <steve.traylen@cern.ch> - 2.5.5-1
- Upstream to 2.5.5
- Drop external classpath patch since now upstream.
- New BR and R vomsjapi
- glite-security-util-java minimum version 2.5.5.
- Add trustmanager-use-vomsjapi.patch

* Mon Mar 29 2010 Steve Traylen <steve.traylen@cern.ch> - 2.0.6-3
- Add README.Fedora describing how to configure the server.xml file.
- Create a -tomcat5 subpackage.

* Thu Dec 10 2009 Steve Traylen <steve.traylen@cern.ch> - 2.0.6-2
- Add in default configuration files.

* Sun Sep 12 2009 Steve Traylen <steve.traylen@cern.ch> - 2.0.6-1
- Initial build.

