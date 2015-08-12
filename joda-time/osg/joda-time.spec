%define tzversion tzdata2008d


Name:           joda-time
Version:        1.5.2
Release:        7.2.%{tzversion}%{?dist}
Summary:        Java date and time API

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://joda-time.sourceforge.net/index.html
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.gz
Source1:        ftp://elsie.nci.nih.gov/pub/%{tzversion}.tar.gz
Patch0:         joda-time-use-system-junit.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  java7-devel
BuildRequires:  ant
%if 0%{?rhel} < 7
BuildRequires:  ant-nodeps
%endif
BuildRequires:  jpackage-utils
BuildRequires:  junit
Requires:       java7
Requires:       jpackage-utils

%description
Joda-Time provides a quality replacement for the Java date
and time classes. The design allows for multiple calendar
systems, while still providing a simple API. The 'default'
calendar is the ISO8601 standard which is used by XML. The
Gregorian, Julian, Buddhist, Coptic and Ethiopic systems
are also included, and we welcome further additions.
Supporting classes include time zone, duration, format
and parsing.


%package        javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils


%description    javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}-src
%patch0 -p1

# all java binaries must be removed from the sources
find . -name '*.jar' -exec rm -f '{}' \;
find . -name '*.class' -exec rm -f '{}' \;

# prove that these binaries aren't used in building joda-time
rm -rf src/testdata/

# replace internal tzdata
rm -f src/java/org/joda/time/tz/src/*
tar -xzf %{SOURCE1} -C src/java/org/joda/time/tz/src/


%build
ant
ant javadoc


%install
rm -rf %{buildroot}

# jars
install -d -m 755 %{buildroot}%{_javadir}
# Don't install a versioned jar and symlink to it, instead install
# the unversioned jar as per Java Packaging Guidelines
install -m 644 build/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# javadocs
install -p -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -a build/docs/* %{buildroot}%{_javadocdir}/%{name}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE.txt RELEASE-NOTES.txt ToDo.txt
%{_javadir}/%{name}.jar


%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}


%changelog
* Thu Oct 02 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.2-7.2.tzdata2008d
- Remove ant-nodeps build dep on EL7

* Thu Apr 04 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.5.2-7.1.tzdata2008d
- Build with OpenJDK7

* Sat Jul 19 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-7.tzdata2008d
- New version with new tzdata (2008d).

* Mon Jun 9 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-6.tzdata2008c
- New version with new tzdata (2008c).

* Sun Apr 6 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-5.tzdata2008b
- Don't compile GCJ bits yet as we hit some GCJ bug.

* Sat Apr 5 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-4.tzdata2008b
- Update to tzdata2008b.
- Use unversioned jar.
- Some small things to comply with Java Packaging Guidelines.
- GCJ support.

* Mon Mar 17 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-3.tzdata2008a
- Many small changes from bz# 436239 comment 6.
- Change -javadocs to -javadoc in accordance with java packaging
  guidelines draft.

* Sun Mar 16 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-2
- Use system junit via Mamoru Tasaka's patch.

* Mon Mar 3 2008 Conrad Meyer <konrad@tylerc.org> - 1.5.2-1
- Initial package.
