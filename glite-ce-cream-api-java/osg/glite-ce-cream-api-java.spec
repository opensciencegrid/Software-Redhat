Summary: Java libraries for the CREAM service
Name: glite-ce-cream-api-java
Version: 1.14.0
%global upstream_release 4
Release: %{upstream_release}.1%{?dist}
License: Apache Software License
Vendor: EMI
URL: http://glite.cern.ch/
Group: System Environment/Libraries
BuildArch: noarch
BuildRequires: ant
%if %undefined extbuilddir
BuildRequires: emi-delegation-java
BuildRequires: emi-trustmanager
BuildRequires: glite-ce-common-java >= 1.14.0
BuildRequires: glite-ce-wsdl >= 1.14.0
BuildRequires: glite-jdl-api-java >= 3.2.0
%endif
BuildRequires: axis2 >= 1.6.1
BuildRequires: bouncycastle
BuildRequires: jclassads
Requires: axis2
Requires: bouncycastle
Requires: emi-delegation-java
Requires: emi-trustmanager 
Requires: glite-ce-common-java >= 1.14.0
Requires: glite-jdl-api-java >= 3.2.0
Requires: jclassads
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}-%{version}-%{upstream_release}.sl5.tar.gz
Patch0: build.patch

%description
Java libraries for the CREAM service

%prep


%setup -c -q
%patch0 -p1

%build
%if %undefined extbuilddir
    printf "dist.location=%{buildroot}
stage.location=
module.version=%{version}">.configuration.properties
    echo Classpath is $CLASSPATH
    set +o errexit
    ( perl -e 'print join("\n", split(":", <>))' <<< $CLASSPATH ) | while read entry; do
        echo ---- $entry
        for x in `find $entry -name \*.jar -o -name \*.class`; do
            echo -------- $x
            if [[ "$x" != "${x%.jar}" ]]; then
                jar tf $x
            fi
        done
    done
    ant
    err=$?
    if [[ $err -ne 0 ]]; then
        find . -ls
        exit $err
    fi
%endif


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
%if %undefined extbuilddir
    ant install
%else
    mkdir -p %{buildroot}/usr/share/java
    cp %{extbuilddir}/usr/share/java/*.jar %{buildroot}/usr/share/java
    mkdir -p %{buildroot}/usr/share/doc/glite-ce-cream-api-java-%{version}
    cp %{extbuilddir}/usr/share/doc/glite-ce-cream-api-java-%{version}/LICENSE %{buildroot}/usr/share/doc/glite-ce-cream-api-java-%{version}
%endif



%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/share/java/glite-ce-*.jar
%dir /usr/share/doc/glite-ce-cream-api-java-%{version}/
%doc /usr/share/doc/glite-ce-cream-api-java-%{version}/LICENSE

%changelog
* Fri Jun 01 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.1.osg
- Add dist tag
- Add patch to change where ant looks for some jar files used in building
- Add versions to dependencies

* Wed May 16 2012 CREAM group <cream-support@lists.infn.it> - 1.14.0-4.sl5
- Major bugs fixed


