# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Summary:        Web Services Description Language Toolkit for Java
Name:           wsdl4j
Version:        1.6.3
Release:        3.1%{?dist}
Epoch:          0
License:        CPL
URL:            http://sourceforge.net/projects/wsdl4j
BuildArch:      noarch
Source0:        http://downloads.sourceforge.net/project/wsdl4j/WSDL4J/%{version}/wsdl4j-src-%{version}.zip
Source1:        %{name}-MANIFEST.MF
Source2:        http://repo1.maven.org/maven2/wsdl4j/wsdl4j/%{version}/wsdl4j-%{version}.pom
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:       java
Requires:       jpackage-utils
BuildRequires:  ant, ant-junit
BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  zip

Provides:       javax.wsdl

%description
The Web Services Description Language for Java Toolkit (WSDL4J) allows the
creation, representation, and manipulation of WSDL documents describing
services.  This code base will eventually serve as a reference implementation
of the standard created by JSR110.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-1_6_3

%build
ant compile javadocs

%install
# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -d build/lib/%{name}.jar META-INF/MANIFEST.MF
zip build/lib/%{name}.jar META-INF/MANIFEST.MF

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -m 644 build/lib/qname.jar $RPM_BUILD_ROOT%{_javadir}/qname.jar

# POMs
install -d -m 0755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -p -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}/

install -d -m 755 %{buildroot}%{_javadir}/javax.wsdl/
ln -sf ../%{name}.jar %{buildroot}%{_javadir}/javax.wsdl/
ln -sf ../qname.jar %{buildroot}%{_javadir}/javax.wsdl/


%files -f .mfiles
%doc license.html
%{_javadir}/javax.wsdl/
%{_javadir}/qname.jar

%files javadoc
%doc license.html
%{_javadocdir}/%{name}

%changelog
* Fri Jul 03 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 0:1.6.3-3.1.osg
- Force replacement of META-INF/MANIFEST.MF in jar file (delete and re-add instead of update) to prevent timestamp issues from causing build failures

* Mon Aug 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.6.3-3
- Add javax.wsdl provides and directory

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 03 2013 Mat Booth <fedora@matbooth.co.uk> - 0:1.6.3-1
- Update to latest upstream version rhbz #915252.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.6.2-6
- Do not include versioned javadoc.

* Fri Jun 15 2012 Gerard Ryan <galileo@fedoraproject.org> - 0:1.6.2-5
- Fix file encoding for wsdl4j-MANIFEST.MF
- Update Bundle-Version in OSGi manifest
- Fix installation of jars in specfile
- Clean up specfile - remove javadoc dir version; remove clean section

* Thu Feb 16 2012 Andy Grimm <agrimm@gmail.com> - 0:1.6.2-4
- add POM file

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 4 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.6.2-1
- Update to 1.6.2.
- Cleanups to comply with current guidelines more.

* Wed Oct 6 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.2-8
- Drop gcj support.
- Fix groups.

* Mon May 31 2010 Ville Skyttä <ville.skytta@iki.fi> - 0:1.5.2-7.7
- Fix specfile encoding.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.2-7.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Deepak Bhole <dbhole@redhat.com> - 0:1.5.2-6.6
- Update OSGi manifest

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.2-6.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.2-5.5
- Add osgi manifest for eclipse-dtp.

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.5.2-5.4
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.5.2-5jpp.3
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.5.2-5jpp.2
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> 1.5.2-4jpp.2
- Rebuild for ppc32 execmem issue and new build-id
- Add %%{?dist} as per new policy

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> 1.5.2-4jpp.1
- Added missing requirements.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.5.2-3jpp_2fc
- Rebuilt

* Wed Jul 19 2006 Deepak Bhole <dbhole@redhat.com> 0:1.5.2-3jpp_1fc
- Remove name/release/version defines as applicable.

* Tue Jul 18 2006 Deepak Bhole <dbhole@redhat.com> 0:1.5.2-2jpp
- Merge changes from fc.
- Add conditional native compilation.

* Mon Jan 30 2006 Ralph Apel <r.apel at r-apel.de> 0:1.5.2-1jpp
- update to 1.5.2
- move qname*.jar to %%{_javadir}/wsdl4j/qname*.jar
  to make place for qname provided by geronimo-specs

* Thu Jun 02 2005 Fernando Nasser <fnasser@redhat.com> 0:1.5.1-1jpp
- update to 1.5.1

* Fri Mar 11 2005 Ralph Apel <r.apel at r-apel.de> 0:1.5-1jpp
- update to 1.5

* Mon Aug 30 2004 Ralph Apel <r.apel at r-apel.de> 0:1.4-3jpp
- Build with ant-1.6.2

* Thu Jun 26 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:1.4-2jpp
- Do not drop qname.jar

* Tue May 06 2003 David Walluck <david@anti-microsoft.org> 0:1.4-1jpp
- 1.4
- update for JPackage 1.5

* Sat Sep  7 2002 Ville Skyttä <ville.skytta@iki.fi> 1.1-1jpp
- First JPackage release.
