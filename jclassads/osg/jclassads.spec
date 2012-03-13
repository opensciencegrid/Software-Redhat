Name:           jclassads
Version:        2.4
Release:        2%{?dist}
Summary:        Java Classad Implementation 

Group:          System Environment/Daemons

License:        Unknown
URL:            http://www.cs.wisc.edu/condor/classad/


Source0:        classad_java_src.tar.gz
Patch0:         find-java-home.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  java-1.6.0-sun-compat
Requires: java-1.6.0-sun-compat


%description
Java classad implementation and API


%prep
%setup -q -n java_classad.%{version}
%patch0 -p1


%build
make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}/jclassads
install -m 644 condor/classad/classad.jar $RPM_BUILD_ROOT%{_javadir}/jclassads/
install -m 644 condor/cedar/cedar.jar $RPM_BUILD_ROOT%{_javadir}/jclassads/

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/share/java/jclassads/cedar.jar
/usr/share/java/jclassads/classad.jar

%changelog
* Tue Mar 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.4-2
- Patched build to find JAVA_HOME more effectively on EL6.

* Thu Sep 15 2011 Doug Strain <dstrain@fnal.gov> - 2.4-1
- Initial RPM

