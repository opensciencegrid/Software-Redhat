
Name:           maven3
Version:        3.0.4
Release:        2%{?dist}
Summary:        Java project management and project comprehension tool

Group:          Development/Tools
License:        ASL 2.0 and MIT and BSD
URL:            http://maven.apache.org/
# Source URL is for testing only, final version will be in different place:
# http://www.apache.org/dyn/closer.cgi/maven/source/apache-%{name}-%{version}-src.tar.gz
Source0:        apache-maven-%{version}-src.tar.gz
Patch0:         build.patch

# custom resolver java files
# source: git clone git://fedorapeople.org/~sochotni/maven-javadir-resolver/
#Source100:      JavadirWorkspaceReader.java
#Source101:      MavenJPackageDepmap.java

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ant >= 1.5
BuildRequires:  java7-devel
BuildRequires:  jpackage-utils
Requires:       java7
Requires:       jpackage-utils

# I am not sure it needs all this crap
#Requires:       apache-commons-cli
#Requires:       plexus-classworlds >= 2.4
#Requires:       guava
#Requires:       hamcrest
#Requires:       nekohtml
#Requires:       plexus-cipher
#Requires:       plexus-containers-component-annotations
#Requires:       plexus-containers-container-default
#Requires:       plexus-interpolation
##Requires:       plexus-sec-dispatcher
#Requires:       plexus-utils
#Requires:       xbean
#Requires:       xerces-j2
#Requires:       maven-wagon
#Requires:       aether >= 1.11
#Requires:       async-http-client
##Requires:       sonatype-oss-parent
#Requires:       sisu >= 2.1.1-2
#Requires:       google-guice >= 3.0
#Requires:       atinject
#Requires:       animal-sniffer >= 1.6-5
#Requires:       mojo-parent
#Requires:       apache-commons-parent


Requires(post): jpackage-utils
Requires(postun): jpackage-utils


%description
Maven is a software project management and comprehension tool. Based on the
concept of a project object model (POM), Maven can manage a project's build,
reporting and documentation from a central piece of information.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description    javadoc
%{summary}.

%prep
%setup -q -n apache-maven-%{version}%{?ver_add}
%patch0

%build

#use bootstrap build
export M2_HOME=/usr/share/apache-maven-3.0
ant

%install

pushd apache-maven
pushd target

unzip apache-maven-3.0.4-bin.zip
mkdir -p $RPM_BUILD_ROOT/usr/share
mv apache-maven-3.0.4 $RPM_BUILD_ROOT/usr/share
chmod 755 $RPM_BUILD_ROOT/usr/share/apache-maven-3.0.4/bin/mvn

popd
popd


%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%doc LICENSE.txt NOTICE.txt README.txt
/usr/share/apache-maven-3.0.4
%attr(0755,root,root) /usr/share/apache-maven-3.0.4/bin/mvn


%changelog
* Wed Apr 03 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.0.4-2
- Build with OpenJDK7

* Fri Jul 6 2012 Doug Strain <dstrain@fnal.gov> - 3.0.4-1
- Created bootstrap rpm based off of some fedora srpms

