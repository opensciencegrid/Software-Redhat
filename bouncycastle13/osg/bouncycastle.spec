%define archivever  133

Summary:          Bouncy Castle Crypto Package for Java
Name:             bouncycastle13
Version:          1.33
Release:          4
Group:            System Environment/Libraries
License:          BSD
URL:              http://www.%{name}.org/
# bcprov-jdk14-133.tar.gz with patented algorithms removed.
Source0:          bcprov-jdk14-133-FEDORA.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:         jpackage-utils
Requires:         java
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils
BuildRequires:    java-devel
BuildRequires:    jpackage-utils

BuildArch: noarch

%description
The Bouncy Castle JCE provider.

%prep
%setup -q -n bcprov-jdk14-133

# Remove provided binaries
find . -type f -name "*.class" -exec rm -f {} \;
find . -type f -name "*.jar" -exec rm -f {} \;
find . -type f -name "*.zip" -exec rm -f {} \;

%build
pushd src
  find . -type d -name examples | xargs rm -rf
  find . -type d -name test | xargs rm -rf
  javac `find . -type f -name "*.java"`
  jarfile="../bcprov-%{version}.jar"
  files="`find . -type f -name "*.class"`"
  test ! -d classes && mf="" || mf="`find classes/ -type f -name "*.mf" 2>/dev/null`"
  test -n "$mf" && jar cvfm $jarfile $mf $files || jar cvf $jarfile $files
popd

%install
rm -rf $RPM_BUILD_ROOT

#install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/java/security/security.d
#touch $RPM_BUILD_ROOT%{_sysconfdir}/java/security/security.d/2000-org.bouncycastle.jce.provider.BouncyCastleProvider

# install bouncy castle provider
#install -dm 755 $RPM_BUILD_ROOT%{_javadir}/gcj-endorsed
#install -pm 644 bcprov-%{version}.jar \
#  $RPM_BUILD_ROOT%{_javadir}/gcj-endorsed/bcprov-%{version}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p bcprov-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/bcprov-%{version}.jar

#%{_bindir}/aot-compile-rpm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc *.html
%{_javadir}/bcprov-%{version}.jar

%changelog
* Thu Mar 01 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.33-4
- Update for RHEL5.

* Tue Jul 25 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.33-3
- Bump release number.

* Mon Jul 10 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.33-2
- Fix problems pointed out by reviewer.

* Fri Jul  7 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 1.33-1
- First release.
