Name:		voms-clients-java
Version:	3.0.6
Release:	3.1%{?dist}
Summary:	Virtual Organization Membership Service Java clients

License:	ASL 2.0
URL:		https://wiki.italiangrid.it/VOMS
Source0:	https://github.com/italiangrid/voms-clients/archive/v%{version}.tar.gz
#		Uncaught exception with canl-java version 2 or later
Patch0:		%{name}-except.patch
#		Fix javadoc warnings
Patch1:		%{name}-javadoc.patch
Patch100:       Make-RFC-3820-proxies-by-default-SOFTWARE-2381.patch
BuildArch:	noarch

BuildRequires:	maven-local
%if %{?fedora}%{!?fedora:0}
#		Missing in EPEL
BuildRequires:	mvn(com.mycila.maven-license-plugin:maven-license-plugin)
%endif
BuildRequires:	mvn(commons-cli:commons-cli)
BuildRequires:	mvn(commons-io:commons-io)
BuildRequires:	mvn(org.italiangrid:voms-api-java)

Requires(post):		%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

# Older versions of voms-clients did not have alternatives
Conflicts:	voms-clients < 2.0.12

Provides:	voms-clients = %{version}-%{release}

%description
The Virtual Organization Membership Service (VOMS) is an attribute authority
which serves as central repository for VO user authorization information,
providing support for sorting users into group hierarchies, keeping track of
their roles and other attributes in order to issue trusted attribute
certificates and SAML assertions used in the Grid environment for
authorization purposes.

This package provides the Java version of the command line clients for VOMS:
voms-proxy-init, voms-proxy-destroy and voms-proxy-info.

%prep
%setup -q -n voms-clients-%{version}
%patch0 -p1
%patch1 -p1
%patch100 -p1

%mvn_package org.italiangrid:voms-clients:tar.gz:* __noinstall

%if %{?fedora}%{!?fedora:0}
%pom_xpath_inject "pom:project/pom:build/pom:plugins/pom:plugin[pom:groupId='com.mycila.maven-license-plugin']/pom:configuration/pom:excludes" "<exclude>.xmvn/**</exclude>"
%pom_xpath_remove "pom:project/pom:build/pom:plugins/pom:plugin[pom:groupId='com.mycila.maven-license-plugin']/pom:configuration/pom:strictCheck"
%else
# Missing in EPEL
%pom_remove_plugin com.mycila.maven-license-plugin:maven-license-plugin
%endif

%build
%mvn_build -j

%install
%mvn_install

mkdir -p %{buildroot}%{_bindir}

cat > %{buildroot}%{_bindir}/voms-proxy-init3 << EOF
#!/bin/sh
VOMS_CLIENTS_JAVA_OPTIONS=\${VOMS_CLIENTS_JAVA_OPTIONS:-"-Xmx16m"}
java \$VOMS_CLIENTS_JAVA_OPTIONS -cp \$(build-classpath voms-clients-java voms-api-java canl-java bcpkix bcprov commons-cli commons-io) org.italiangrid.voms.clients.VomsProxyInit "\$@"
EOF
chmod 755 %{buildroot}%{_bindir}/voms-proxy-init3

cat > %{buildroot}%{_bindir}/voms-proxy-info3 << EOF
#!/bin/sh
VOMS_CLIENTS_JAVA_OPTIONS=\${VOMS_CLIENTS_JAVA_OPTIONS:-"-Xmx16m"}
java \$VOMS_CLIENTS_JAVA_OPTIONS -cp \$(build-classpath voms-clients-java voms-api-java canl-java bcpkix bcprov commons-cli commons-io) org.italiangrid.voms.clients.VomsProxyInfo "\$@"
EOF
chmod 755 %{buildroot}%{_bindir}/voms-proxy-info3

cat > %{buildroot}%{_bindir}/voms-proxy-destroy3 << EOF
#!/bin/sh
VOMS_CLIENTS_JAVA_OPTIONS=\${VOMS_CLIENTS_JAVA_OPTIONS:-"-Xmx16m"}
java \$VOMS_CLIENTS_JAVA_OPTIONS -cp \$(build-classpath voms-clients-java voms-api-java canl-java bcpkix bcprov commons-cli commons-io) org.italiangrid.voms.clients.VomsProxyDestroy "\$@"
EOF
chmod 755 %{buildroot}%{_bindir}/voms-proxy-destroy3

touch %{buildroot}%{_bindir}/voms-proxy-init
chmod 755 %{buildroot}%{_bindir}/voms-proxy-init
touch %{buildroot}%{_bindir}/voms-proxy-info
chmod 755 %{buildroot}%{_bindir}/voms-proxy-info
touch %{buildroot}%{_bindir}/voms-proxy-destroy
chmod 755 %{buildroot}%{_bindir}/voms-proxy-destroy

mkdir -p %{buildroot}%{_mandir}/man1
install -p -m 644 man/voms-proxy-init.1 \
    %{buildroot}%{_mandir}/man1/voms-proxy-init3.1
install -p -m 644 man/voms-proxy-info.1 \
    %{buildroot}%{_mandir}/man1/voms-proxy-info3.1
install -p -m 644 man/voms-proxy-destroy.1 \
    %{buildroot}%{_mandir}/man1/voms-proxy-destroy3.1

touch %{buildroot}%{_mandir}/man1/voms-proxy-init.1
touch %{buildroot}%{_mandir}/man1/voms-proxy-info.1
touch %{buildroot}%{_mandir}/man1/voms-proxy-destroy.1

mkdir -p %{buildroot}%{_mandir}/man5
install -p -m 644 man/vomsdir.5 %{buildroot}%{_mandir}/man5/vomsdir.5
install -p -m 644 man/vomses.5 %{buildroot}%{_mandir}/man5/vomses.5

%post
%{_sbindir}/update-alternatives --install %{_bindir}/voms-proxy-init \
    voms-proxy-init %{_bindir}/voms-proxy-init3 90 \
    --slave %{_mandir}/man1/voms-proxy-init.1.gz voms-proxy-init-man \
    %{_mandir}/man1/voms-proxy-init3.1.gz
%{_sbindir}/update-alternatives --install %{_bindir}/voms-proxy-info \
    voms-proxy-info %{_bindir}/voms-proxy-info3 90 \
    --slave %{_mandir}/man1/voms-proxy-info.1.gz voms-proxy-info-man \
    %{_mandir}/man1/voms-proxy-info3.1.gz
%{_sbindir}/update-alternatives --install %{_bindir}/voms-proxy-destroy \
    voms-proxy-destroy %{_bindir}/voms-proxy-destroy3 90 \
    --slave %{_mandir}/man1/voms-proxy-destroy.1.gz voms-proxy-destroy-man \
    %{_mandir}/man1/voms-proxy-destroy3.1.gz

%postun
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove voms-proxy-init \
    %{_bindir}/voms-proxy-init3
    %{_sbindir}/update-alternatives --remove voms-proxy-info \
    %{_bindir}/voms-proxy-info3
    %{_sbindir}/update-alternatives --remove voms-proxy-destroy \
    %{_bindir}/voms-proxy-destroy3
fi

%files -f .mfiles
%dir %{_javadir}/%{name}
%if %{?fedora}%{!?fedora:0} >= 21 || %{?rhel}%{!?rhel:0} >= 8
%dir %{_mavenpomdir}/%{name}
%endif
%{_bindir}/voms-proxy-destroy3
%{_bindir}/voms-proxy-info3
%{_bindir}/voms-proxy-init3
%ghost %{_bindir}/voms-proxy-destroy
%ghost %{_bindir}/voms-proxy-info
%ghost %{_bindir}/voms-proxy-init
%{_mandir}/man1/voms-proxy-destroy3.1*
%{_mandir}/man1/voms-proxy-info3.1*
%{_mandir}/man1/voms-proxy-init3.1*
%ghost %{_mandir}/man1/voms-proxy-destroy.1*
%ghost %{_mandir}/man1/voms-proxy-info.1*
%ghost %{_mandir}/man1/voms-proxy-init.1*
%{_mandir}/man5/vomsdir.5*
%{_mandir}/man5/vomses.5*
%doc AUTHORS README.md
%license LICENSE

%changelog
* Wed Jul 06 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.0.6-3.1
- Make RFC 3820 proxies by default (SOFTWARE-2381)

* Sat Jul 11 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.0.6-3
- Fix javadoc warnings

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 18 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.0.6-1
- Update to version 3.0.6
- Implement new license packaging guidelines
- Add virtual provides voms-clients (the old voms-clients package was
  renamed voms-clients-cpp)

* Mon Nov 17 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.0.5-1
- Initial build
