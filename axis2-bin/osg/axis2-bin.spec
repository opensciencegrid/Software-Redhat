Summary: A Web Services / SOAP / WSDL engine provided by Apache
%define realname axis2
Name: %{realname}-bin
Version: 1.6.2
Release: 2%{?dist}
License: ASL 2.0
Group: Development/Libraries/Java
Url: http://axis.apache.org
# To create source:
# Download axis2-%{version}-bin.zip from an apache mirror
# unzip axis2-%{version}-bin.zip
# mv axis2-%{version} axis2-bin-%{version}
# tar czf axis2-bin-%{version}.tar.gz axis2-bin-%{version}
Source0: %{name}-%{version}.tar.gz
Patch0: scripts.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Provides: %{realname} = %{version}
Requires: java
AutoReq: yes
AutoProv: yes
BuildArch: noarch

# disable jar repacking
%global __os_install_post /bin/true


%description
%{summary}



%prep
# %%setup quick reference:
#   -a N        Unpack source N after cd
#   -b N        Unpack source N before cd
#   -c          Create and cd to dir before unpacking
#   -D          Do not delete dir before unpacking
#   -n DIR      Name of extract dir (instead of NAME-VERSION)
#   -T          Do not autounpack Source0

%setup
%patch0 -p1











%install
[[ %{buildroot} != / ]] && rm -rf %{buildroot}
mkdir -p %{buildroot}
# scripts
mkdir -p %{buildroot}%{_bindir}
install -m 0755 bin/axis2.sh %{buildroot}%{_bindir}/%{realname}
install -m 0755 bin/axis2server.sh %{buildroot}%{_bindir}/%{realname}-server
install -m 0755 bin/java2wsdl.sh %{buildroot}%{_bindir}/%{realname}-java2wsdl
install -m 0755 bin/wsdl2java.sh %{buildroot}%{_bindir}/%{realname}-wsdl2java
mkdir -p %{buildroot}%{_datadir}/%{realname}
install -m 0755 bin/setenv.sh %{buildroot}%{_datadir}/%{realname}/setenv.sh

# libs
mkdir -p %{buildroot}%{_javadir}/%{realname}
mv lib/*.jar lib/endorsed/ %{buildroot}%{_javadir}/%{realname}/

# docs
mkdir -p %{buildroot}%{_datadir}/doc/%{realname}-%{version}/
mv lib/*.txt *.txt release-notes.html %{buildroot}%{_datadir}/doc/%{realname}-%{version}/

# webapp and related
mv webapp/ %{buildroot}%{_datadir}/%{realname}/
mv repository/{modules,services} %{buildroot}%{_datadir}/%{realname}/webapp/WEB-INF/
mv conf/ %{buildroot}%{_datadir}/%{realname}/webapp/WEB-INF/
# lib symlinks
mkdir -p %{buildroot}%{_datadir}/%{realname}/webapp/WEB-INF/lib
for jar in %{buildroot}%{_javadir}/%{realname}/*.jar; do
    jar_no_buildroot=${jar##%{buildroot}}
    ln -sf $jar_no_buildroot %{buildroot}%{_datadir}/%{realname}/webapp/WEB-INF/lib/$(basename $jar)
done

# skip samples
rm -rf samples/


%clean
[[ %{buildroot} != / ]] && rm -rf %{buildroot}




%files
%{_bindir}/axis2*
%dir %{_datadir}/%{realname}
%{_datadir}/%{realname}/setenv.sh
%dir %{_javadir}/%{realname}
%{_javadir}/%{realname}/*.jar
%{_javadir}/%{realname}/endorsed/*.jar
%docdir %{_datadir}/doc/%{realname}-%{version}
%{_datadir}/doc/%{realname}-%{version}/*
%dir %{_datadir}/%{realname}/webapp
%{_datadir}/%{realname}/webapp/build.xml
%{_datadir}/%{realname}/webapp/WEB-INF/web.xml
%{_datadir}/%{realname}/webapp/WEB-INF/conf/*
%{_datadir}/%{realname}/webapp/WEB-INF/classes/*.properties
%{_datadir}/%{realname}/webapp/WEB-INF/classes/META-INF/*
%{_datadir}/%{realname}/webapp/WEB-INF/classes/org/apache/axis2/transport/http/AxisAdminServlet.class
%{_datadir}/%{realname}/webapp/WEB-INF/classes/org/apache/axis2/webapp/*
%{_datadir}/%{realname}/webapp/WEB-INF/modules/*
%{_datadir}/%{realname}/webapp/WEB-INF/lib/*
%{_datadir}/%{realname}/webapp/WEB-INF/services/*
%{_datadir}/%{realname}/webapp/axis2-web/*.jsp
%{_datadir}/%{realname}/webapp/axis2-web/Error/*
%{_datadir}/%{realname}/webapp/axis2-web/css/*
%{_datadir}/%{realname}/webapp/axis2-web/images/*
%{_datadir}/%{realname}/webapp/axis2-web/include/*







%changelog
* Mon Jul 16 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6.2-2
- Disable jar repacking

* Thu Jul 12 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6.2-1
- Created


# vim:ft=spec
