# % global with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}
# We don't want to use gcj
%global with_gcj 0

Name:           glite-security-util-java
Version:        2.8.0
Release:        3.2%{?dist}
Summary:        Java Utilities for GSI Credentials

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            https://twiki.cern.ch/twiki/bin/view/EGEE/TrustManager
# The source for this package was pulled from upstream's cvs. Use the
# following commands to generate the tarball:
# cvs -q -d:pserver:anonymous:@glite.cvs.cern.ch:/cvs/glite checkout \
#      -r  glite-security-util-java_R_2_7_1  org.glite.security.util-java
# find org.glite.security.util-java -type f -print0 | xargs -0 chmod a-x 
# find org.glite.security.util-java -name CVS -print0 | xargs -0  rm -rf 
# rm -rf org.glite.security.util-java/src/org/glite/security/voms
# rm -rf org.glite.security.util-java/test
# tar cvfz glite-security-util-java-2.7.1.tar.gz org.glite.security.util-java
Source0:        %{name}-%{version}.tar.gz
# The following script can be use to generate the source tar ball.
# e.g  bash ./glite-security-util-java-generate-tarball.sh 2.7.1
Source1:        %{name}-generate-tarball.sh
Patch0:         build.xml.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{with_gcj}
BuildRequires:    java-gcj-compat-devel >= 1.0.31
Requires(post):   java-gcj-compat >= 1.0.31
Requires(postun): java-gcj-compat >= 1.0.31
%else
BuildArch:      noarch
%endif

#No suitable java stack in EPEL5/6 on ppc/ppc64
%if 0%{?el5}
ExcludeArch:    ppc
%endif

%if 0%{?el6}
ExcludeArch:    ppc64
%endif

BuildRequires:  jpackage-utils
BuildRequires:  java7-devel
BuildRequires:  ant
BuildRequires:  bouncycastle
BuildRequires:  log4j
%if 0%{?el5}
BuildRequires:  servletapi5
%endif
%if 0%{?el6}
BuildRequires:  servlet6
%endif
BuildRequires:  axis
BuildRequires:  voms-api-java >= 2.0.8

Requires:       jpackage-utils
Requires:       java7
Requires:       bouncycastle
Requires:       log4j
Requires:       voms-api-java >= 2.0.8
%if 0%{?el5}
Requires:       servletapi5
%endif
%if 0%{?el6}
Requires:       servlet6
%endif
Requires:       axis

%description
glite-security-util-java together with glite-security-trustmanger is 
an implementation of the java TrustManager interface with implementation 
of cert path checking, grid namespace restrictions and dynamic loading of 
CA certs, credentials, CRLs and namespace restrictions. Also provided is 
integration into tomcat, axis and axis2. There are many utility classes 
and methods for certificate and proxy handling in util-java. It can be 
used both in the server side for the server ssl handler and on the client 
side for the opneing of ssl connections. 

%package        javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:      noarch
%endif
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n org.glite.security.util-java

%patch0 -p0 

# remove private copy of vomsjapi and use the provided package.
rm -rf src/org/glite/security/voms
sed s/org.glite.security.voms.VOMSValidator/org.glite.voms.VOMSValidator/ \
    -i src/org/glite/security/SecurityContext.java
find -name '*.jar' -o -name '*.class' -exec rm -f '{}' \;

%build
export CLASSPATH=$(build-classpath bcprov log4j axis %{?el5:servletapi5} %{?el6:servlet} vomsjapi)
%ant -Dprefix=build compile-extcp
%ant -Dprefix=build doc-extcp

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p  build/share/java/%{name}.jar  \
   $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -rp build/share/%{name}/doc/html/*  \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
pushd $RPM_BUILD_ROOT%{_javadocdir}
ln -s %{name}-%{version} %{name}
popd

%if %{with_gcj}
%{_bindir}/aot-compile-rpm
%endif

%post 
%if %{with_gcj}
  if [ -x %{_bindir}/rebuild-gcj-db ] 
  then
    %{_bindir}/rebuild-gcj-db
  fi
%endif

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
%{_libdir}/gcj/%{name}
%endif

%doc LICENSE

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}


%changelog
* Tue Apr 02 2013 Carl Edquist <edquist@cs.wisc.edu> - 2.8.0-3.2
- Build for OpenJDK7, don't use gcj

* Wed Nov 14 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.8.0-3.1
- Conditionalize build to work on both el5 (with tomcat5) and el6 (with tomcat6)
- Change vomsjapi requirement to voms-api-java >= 2.0.8

* Wed Aug 4 2010 Steve Traylen <steve.traylen@cern.ch> - 2.8.0-3
- Don't build ppc64 on .el6. To much java missing.

* Fri Jul 30 2010 Steve Traylen <steve.traylen@cern.ch> - 2.8.0-2
- Adapt to use tomcat6 on newer releases.

* Tue May 25 2010 Steve Traylen <steve.traylen@cern.ch> - 2.8.0-1
- Upstream to 2.8.0

* Thu Apr 28 2010 Steve Traylen <steve.traylen@cern.ch> - 2.7.1-1
- Upstream to 2.7.1

* Wed Apr 28 2010 Steve Traylen <steve.traylen@cern.ch> - 2.5.5-1
- Upstream to 2.5.5
- Drop glite-security-util-java-external-classpath.patch since
  now present upstream.
- First build in EPEL5
- Requires servletapi5 rather than servlet
- Exclude arch ppc due to lack of suitable java on that platform.

* Thu Nov 12 2009 Steve Traylen <steve.traylen@cern.ch> - 2.0.3-7
- Correct typos in SPEC file.

* Sun Nov 9 2009 Steve Traylen <steve.traylen@cern.ch> - 2.0.3-6
- Don't use private vomsjapi and use vomsjapi package instead.
- Remove uneeded code and consequently "EU Datagrid license"

* Mon Oct 26 2009 Steve Traylen <steve.traylen@cern.ch> - 2.0.3-5
- Change summary field to something more sensible.

* Thu Oct 22 2009 Steve Traylen <steve.traylen@cern.ch> - 2.0.3-4
- Addition of axis and java-devel >= 1:1.6.0 as BR.

* Thu Sep 10 2009 Steve Traylen <steve.traylen@cern.ch> - 2.0.3-3
- Shorten line length of description.

* Thu Sep 10 2009 Steve Traylen <steve.traylen@cern.ch> - 2.0.3-2
- Add patch to support external CLASSPATH env variable:
  glite-security-external-classpath.patch

* Sun Sep 6 2009 Steve Traylen <steve.traylen@cern.ch> - 2.0.3-1
- Initial build.

