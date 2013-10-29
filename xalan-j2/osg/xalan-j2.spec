# Copyright (c) 2000-2008, JPackage Project
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

%define _with_repolib 1

# If you want repolib package to be built,
# issue the following: 'rpmbuild --with repolib'
%define with_repolib %{?_with_repolib:1}%{!?_with_repolib:0}
%define without_repolib %{!?_with_repolib:1}%{?_with_repolib:0}

%define repodir %{_javadir}/repository.jboss.com/apache-xalan/2.7.0.patch01-brew
%define repodirlib %{repodir}/lib
%define repodirsrc %{repodir}/src

# % define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}
# We don't want to use gcj
%define gcj_support 0
%define bootstrap %{?_with_bootstrap:1}%{!?_with_bootstrap:%{?_without_bootstrap:0}%{!?_without_bootstrap:%{?_bootstrap:%{_bootstrap}}%{!?_bootstrap:0}}}

%define section free
%define cvs_version 2_7_0

Name:           xalan-j2
Version:        2.7.0
Release:        10.1%{?dist}
Epoch:          0
Summary:        Java XSLT processor
License:        ASL 2.0
Source0:        http://www.apache.org/dist/xml/xalan-j/xalan-j_%{cvs_version}-src.tar.gz
Source1:        xalan-j2-2.7.0-component-info.xml
Patch0:         %{name}-noxsltcdeps.patch
Patch1:         %{name}-manifest.patch
Patch2:         %{name}-crosslink.patch
# Fix the XALANJ-2376:
#TransformerFactory.newTransformer(source) returns null instead throwing
#an exception and according to the specs newTransformer() should not
#return null.
Patch4:         %{name}-XALANJ-2376.patch
URL:            http://xalan.apache.org/
Group:          Text Processing/Markup/XML
%if ! %{gcj_support}
BuildArch:      noarch
%endif
Provides:       jaxp_transform_impl
Requires:       jaxp_parser_impl
Requires(post):  /usr/sbin/update-alternatives
Requires(preun): /usr/sbin/update-alternatives
BuildRequires:  jpackage-utils
BuildRequires:  java7-devel
BuildRequires:  ant
%if ! %{bootstrap}
BuildRequires:  java_cup
BuildRequires:  bcel
BuildRequires:  jlex
BuildRequires:  regexp
BuildRequires:  sed
BuildRequires:  servletapi5
%endif
BuildRequires:  xerces-j2 >= 0:2.7.1
BuildRequires:  xml-commons-apis >= 0:1.3
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Xalan is an XSLT processor for transforming XML documents into HTML,
text, or other XML document types. It implements the W3C Recommendations
for XSL Transformations (XSLT) and the XML Path Language (XPath). It can
be used from the command line, in an applet or a servlet, or as a module
in other program.

%if %{with_repolib}
%package         repolib
Summary:         Artifacts to be uploaded to a repository library
Group:  Development/Libraries/Java

%description     repolib
Artifacts to be uploaded to a repository library.
This package is not meant to be installed but so its contents
can be extracted through rpm2cpio.
%endif

%if ! %{bootstrap}
%package        xsltc
Summary:        XSLT compiler
Group:          Text Processing/Markup/XML
Requires:       java_cup
Requires:       bcel
Requires:       jlex
Requires:       regexp
Requires:       jaxp_parser_impl
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%endif

%description    xsltc
The XSLT Compiler is a Java-based tool for compiling XSLT stylesheets into
lightweight and portable Java byte codes called translets.
%endif

%package        manual
Summary:        Manual for %{name}
Group:          Text Processing/Markup/XML

%description    manual
Documentation for %{name}.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation
BuildRequires:  java7-javadoc

%description    javadoc
Javadoc for %{name}.

%if ! %{bootstrap}
%package        demo
Summary:        Demo for %{name}
Group:          Text Processing/Markup/XML
Requires:       %{name} = %{epoch}:%{version}-%{release}, servlet
BuildRequires:  servlet

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%endif

%description    demo
Demonstrations and samples for %{name}.
%endif

%prep
%setup -q -n xalan-j_%{cvs_version}
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch4 -p0
# Remove all binary libs, except ones needed to build docs and N/A elsewhere.
for j in $(find . -name "*.jar"); do
        #mv $j $j.no
        rm $j
done

# FIXME: who knows where the sources are? xalan-j1 ?
#mv tools/xalan2jdoc.jar.no tools/xalan2jdoc.jar
#mv tools/xalan2jtaglet.jar.no tools/xalan2jtaglet.jar

%{__chmod} 0755 samples/extensions/sql/*.sh

%build
export JAVA_HOME=%{java_home}
pushd lib
ln -sf $(build-classpath java_cup-runtime) runtime.jar
ln -sf $(build-classpath bcel) BCEL.jar
ln -sf $(build-classpath regexp) regexp.jar
ln -sf $(build-classpath xerces-j2) xercesImpl.jar
ln -sf $(build-classpath xml-commons-apis) xml-apis.jar
popd
pushd tools
ln -sf $(build-classpath java_cup) java_cup.jar
ln -sf $(build-classpath ant) ant.jar
ln -sf $(build-classpath jlex) JLex.jar
ln -sf $(build-classpath xml-stylebook) stylebook-1.0-b3_xalan-2.jar
popd
export CLASSPATH=$(build-classpath servletapi5)
export OPT_JAR_LIST=:
%if %{bootstrap}
ant \
  -Djava.awt.headless=true \
  -Dapi.j2se=%{_javadocdir}/java \
  -Dbuild.xalan-interpretive.jar=build/xalan-interpretive.jar \
  xalan-interpretive.jar
%else
ant \
  -Djava.awt.headless=true \
  -Dapi.j2se=%{_javadocdir}/java \
  -Dbuild.xalan-interpretive.jar=build/xalan-interpretive.jar \
  xalan-interpretive.jar\
  xsltc.unbundledjar \
  docs \
  xsltc.docs \
  javadocs \
  samples \
  servlet
%endif

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 build/xalan-interpretive.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
%if ! %{bootstrap}
install -p -m 644 build/xsltc.jar \
  $RPM_BUILD_ROOT%{_javadir}/xsltc-%{version}.jar
%endif
install -p -m 644 build/serializer.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-serializer-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# add a symlink to serializer.jar to match upstream jar naming
ln -sf %{name}-serializer-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/serializer.jar
ln -sf %{name}.jar $RPM_BUILD_ROOT%{_javadir}/xalan.jar

%if ! %{bootstrap}

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
# FIXME: (dwalluck): breaks --short-circuit
rm -rf build/docs/apidocs

# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
install -p -m 644 build/xalansamples.jar \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-samples.jar
install -p -m 644 build/xalanservlet.war \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-servlet.war
cp -pr samples $RPM_BUILD_ROOT%{_datadir}/%{name}

# fix link between manual and javadoc
(cd build/docs; ln -sf %{_javadocdir}/%{name}-%{version} apidocs)
%endif

# jaxp_transform_impl ghost symlink
ln -s %{_sysconfdir}/alternatives \
  $RPM_BUILD_ROOT%{_javadir}/jaxp_transform_impl.jar

%if %{with_repolib}
        install -d -m 755 $RPM_BUILD_ROOT%{repodir}
        install -d -m 755 $RPM_BUILD_ROOT%{repodirlib}
        install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{repodir}/component-info.xml
        sed -i 's/@VERSION@/2.7.0.patch01-brew/g' $RPM_BUILD_ROOT%{repodir}/component-info.xml
        tag=`echo %{name}-%{version}-%{release} | sed 's|\.|_|g'`
        sed -i "s/@TAG@/$tag/g" $RPM_BUILD_ROOT%{repodir}/component-info.xml
        install -d -m 755 $RPM_BUILD_ROOT%{repodirsrc}
        install -p -m 644 %{PATCH0} $RPM_BUILD_ROOT%{repodirsrc}
        install -p -m 644 %{PATCH4} $RPM_BUILD_ROOT%{repodirsrc}
        install -p -m 644 %{SOURCE0} $RPM_BUILD_ROOT%{repodirsrc}
        cp -p $RPM_BUILD_ROOT%{_javadir}/serializer.jar $RPM_BUILD_ROOT%{repodirlib}
        cp -p $RPM_BUILD_ROOT%{_javadir}/xalan.jar $RPM_BUILD_ROOT%{repodirlib}
%endif

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-alternatives --install %{_javadir}/jaxp_transform_impl.jar \
  jaxp_transform_impl %{_javadir}/%{name}.jar 30

%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%preun
{
  [ $1 = 0 ] || exit 0
  update-alternatives --remove jaxp_transform_impl %{_javadir}/%{name}.jar
} >/dev/null 2>&1 || :

%if 0
%post xsltc
update-alternatives --install %{_javadir}/jaxp_transform_impl.jar \
  jaxp_transform_impl %{_javadir}/xsltc.jar 10

%preun xsltc
{
  [ $1 = 0 ] || exit 0
  update-alternatives --remove jaxp_transform_impl %{_javadir}/xsltc.jar
} >/dev/null 2>&1 || :
%endif

%if ! %{bootstrap}
%if %{gcj_support}
%post xsltc
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun xsltc
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%post demo
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun demo
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif
%endif

%files
%defattr(0644,root,root,0755)
%doc KEYS licenses/xalan.LICENSE.txt licenses/xalan.NOTICE.txt licenses/serializer.LICENSE.txt licenses/serializer.NOTICE.txt
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-serializer-%{version}.jar
%{_javadir}/%{name}-serializer.jar
%{_javadir}/serializer.jar
%{_javadir}/xalan.jar
%ghost %{_javadir}/jaxp_transform_impl.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-serializer-%{version}.jar.*
%endif

%if ! %{bootstrap}
%files xsltc
%defattr(0644,root,root,0755)
%{_javadir}/xsltc-%{version}.jar
%{_javadir}/xsltc.jar
#%ghost %{_javadir}/jaxp_transform_impl.jar

%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/xsltc-%{version}.jar.*
%endif

%files manual
%defattr(0644,root,root,0755)
%doc build/docs/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,0755)
%{_datadir}/%{name}
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-samples.jar.*
%endif
%endif

%if %{with_repolib}
%files repolib
%defattr(0644,root,root,0755)
%{_javadir}/repository.jboss.com
%endif

%changelog
* Thu Apr 04 2013 Carl Edquist <edquist@cs.wisc.edu> - 0:2.7.0-10.1
- Build with OpenJDK7, comment out gcj, use java7-javadoc

* Fri Sep 19 2008 David Walluck <dwalluck@redhat.com> 0:2.7.0-10
- fix file list
- fix repolib

* Fri Jun 13 2008 Fernando Nasser <fnasser@redhat.com> 0:2.7.0-9
- Rebuild without JPP 1.7

* Wed May 28 2008 David Walluck <dwalluck@redhat.com> 0:2.7.0-8.jpp5
- add repolib option
- add XALANJ-2376.patch
- remove javadoc scriptlets
- remove spurious requirement on gnu-crypto
- fix License
- fix duplicate %%changelog section
- fix macros in %%changelog
- properly comment out xsltc scripts

* Mon Feb 12 2007 Ralph Apel <r.apel at r-apel.de> 0:2.7.0-7jpp
- Add option to omit -xsltc subpackage while bootstrapping
- Restore unapplied patches
- Fix empty post/postun

* Fri Aug 18 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:2.7.0-6jpp
- Add a postun section to rebuild jar db provided GCJ support is enabled.

* Thu Aug 10 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:2.7.0-5jpp
- Add Requires post/preun for update-alternatives.
- Remove Requires for update-alternatives.
- Add Requires(x) for javadoc subpackage.
- Add postun section for javadoc subpackage.

* Fri Jul 21 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:2.7.0-4jpp
- Fix two typos in files section. 

* Wed Jul 19 2006 Vivek Lakshmanan <vivekl@redhat.com> - 0:2.7.0-3jpp
- Conditional native compilation with GCJ.
- Use NVR macros wherever possible.
- Exclude war which blocks aot compilation of main jar (RH BZ#171005)
  (Archit Shah - Nov 1 2005 - 0:2.6.0-3jpp_4fc)

* Wed Mar 22 2006 Ralph Apel <r.apel at r-apel.de> 0:2.7.0-2jpp
- First JPP-1.7 release
- Fix some (Build)Requires

* Fri Oct 07 2005 Ralph Apel <r.ape at r-apel.de> 0:2.7.0-1jpp
- Upgrade to 2.7.0
- Include serializer.jar as xalan-j2-serializer.jar

* Fri May 27 2005 Gary Benson <gbenson at redhat.com> 0:2.6.0-3jpp
- Add NOTICE file as per Apache License version 2.0.
- Build with servletapi5.

* Thu Aug 26 2004 Ralph Apel <r.ape at r-apel.de> 0:2.6.0-2jpp
- Build with ant-1.6.2
- Try with -Djava.awt.headless=true 

* Tue Mar 23 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:2.6.0-1jpp
- Updated to 2.6.0 
- Patches supplied by <aleksander.adamowski@altkom.pl>

* Sat Nov 15 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.5.2-1jpp
- Update to 2.5.2.
- Re-enable javadocs, new style versionless symlink handling, crosslink
  with local J2SE javadocs.
- Spec cleanups.

* Sat Jun  7 2003 Vil le Skyttä <ville.skytta at iki.fi> - 0:2.5.1-1jpp
- Update to 2.5.1.
- Fix jpackage-utils version in BuildRequires, add xerces-j2.
- Non-versioned javadoc symlinking.
- Add one missing epoch.
- Clean up manifests from Class-Path's and other stuff we don't include.
- xsltc no longer provides a jaxp_transform_impl because of huge classpath
  and general unsuitablity for production-use, system-installed transformer.
- Own (ghost) %%{_javadir}/jaxp_transform_impl.jar.
- Remove alternatives in preun instead of postun.
- Disable javadoc subpackage for now:
  <http://issues.apache.org/bugzilla/show_bug.cgi?id=20572>

* Thu Mar 27 2003 Nicolas Mailhot <Nicolas.Mailhot@One2team.com> 0:2.5.0.d1-1jpp
- For jpackage-utils 1.5

* Wed Jan 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 2.4.1-2jpp
- bsf -> oldbsf.
- Use non-versioned jar in alternative, don't remove it on upgrade.
- Remove hardcoded packager tag.

* Mon Nov 04 2002 Henri Gomez <hgomez@users.sourceforge.net> 2.4.1-1jpp
- 2.4.1

* Tue Sep 10 2002 Ville Skyttä <ville.skytta at iki.fi> 2.4.0-1jpp
- 2.4.0.

* Thu Aug 22 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.4-0.D1.3jpp
- corrected case for Group tag
- fixed servlet classpath

* Tue Aug 20 2002 Ville Skyttä <ville.skytta at iki.fi> 2.4-0.D1.2jpp
- Remove xerces-j1 runtime dependency.
- Add bcel, jlex, regexp to xsltc runtime requirements:
  <http://xml.apache.org/xalan-j/xsltc_usage.html>
- Build with -Dbuild.compiler=modern (IBM 1.3.1) to avoid stylebook errors.
- XSLTC now provides jaxp_transform_impl too.
- Earlier changes by Henri, from unreleased 2.4-D1.1jpp:
    Mon Jul 15 2002 Henri Gomez <hgomez@users.sourceforge.net> 2.4-D1.1jpp
  - 2.4D1
  - use the jlex 1.2.5-5jpp (patched by Xalan/XSLTC team) rpm
  - use the stylebook-1.0-b3_xalan-2.jar included in source file till it will
    be packaged in jpackage
  - use jaxp_parser_impl (possibly xerces-j2) instead of xerces-j1 for docs
    generation, since it's tuned for stylebook-1.0-b3_xalan-2.jar
  - build and provide xsltc in a separate rpm

* Mon Jul 01 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.3.1-2jpp 
- provides jaxp_transform_impl
- requires jaxp_parser_impl
- stylebook already requires xml-commons-apis
- jaxp_parser_impl already requires xml-commons-apis
- use sed instead of bash 2.x extension in link area to make spec compatible with distro using bash 1.1x

* Wed Jun 26 2002 Henri Gomez <hgomez@users.sourceforge.net> 2.3.1-2jpp
- fix built classpath (bsf, bcel are existing jpackage rpms),
- add buildrequires for javacup and JLex

* Wed May 08 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.3.1-1jpp 
- 2.3.1
- vendor, distribution, group tags

* Mon Mar 18 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.3.0-2jpp 
- generic servlet support

* Wed Feb 20 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.3.0-1jpp 
- 2.3.0
- no more compat jar

* Sun Jan 27 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2.0-2jpp 
- adaptation to new stylebook1.0b3 package
- used source tarball
- section macro

* Fri Jan 18 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2.0-1jpp
- 2.2.0 final
- versioned dir for javadoc
- no dependencies for manual and javadoc packages
- stricter dependency for compat and demo packages
- fixed package confusion
- adaptation for new servlet3 package
- requires xerces-j1 instead of jaxp_parser
- xml-apis jar now in required xml-commons-apis external package

* Wed Dec 5 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2.D14-1jpp
- 2.2.D14
- javadoc into javadoc package
- compat.jar into compat package
- compat javadoc into compat-javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 2.2.D13-2jpp
- changed extension to jpp
- prefixed xml-apis

* Tue Nov 20 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 2.2.D13-1jpp
- 2.2.D13
- removed packager tag

* Sat Oct 6 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2.D11-1jpp
- 2.2.D11

* Sun Sep 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2.D10-2jpp
- first unified release
- s/jPackage/JPackage

* Fri Sep 14 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2.D10-1mdk
- cvs references
- splitted demo package
- moved demo files to %%{_datadir}/%%{name}
- only manual package requires stylebook-1.0b3
- only demo package requires servletapi3

* Wed Aug 22 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2.D9-1mdk
- 2.2.9
- used new source packaging policy
- added samples data

* Wed Aug 08 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2.D6-1mdk
- first Mandrake release
