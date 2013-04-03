# Copyright (c) 2000-2007, JPackage Project

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
%global jettyname jetty
%global homedir     %{_datadir}/%{name}
%global jettylibdir %{_localstatedir}/lib/%{name}

%global addver v20120524

Name: %{jettyname}
Version: 8.1.4.%{addver}
Release: 2%{?dist}
Summary: Java Webserver and Servlet Container
Group: Applications/Internet
# Jetty is dual licensed under both ASL 2.0 and EPL 1.0, see NOTICE.txt
License: ASL 2.0 or EPL
URL: http://jetty.mortbay.org/jetty/
Source0: http://vdt.cs.wisc.edu/upstream/jetty/8.1.4.v20120524/jetty-hightide-8.1.4.v20120524.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{jettyname}-%{version}-%{release}-XXXXXX)
Provides: %{jettyname} = %{version}
Requires: java7
Requires: jpackage-utils
AutoProv: yes
AutoReq: yes
BuildArch: noarch

%description
Jetty is a 100% Java HTTP Server and Servlet Container.

%package ajp
Summary:        ajp module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-http    = %{version}-%{release}
Requires:       jetty-io      = %{version}-%{release}
Requires:       jetty-server  = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
#Requires:       tomcat-servlet-3.0-api
%description    ajp

%package annotations
Summary:        annotations module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project  = %{version}-%{release}
Requires:       jetty-plus     = %{version}-%{release}
Requires:       jetty-security = %{version}-%{release}
Requires:       jetty-server   = %{version}-%{release}
Requires:       jetty-servlet  = %{version}-%{release}
Requires:       jetty-util     = %{version}-%{release}
Requires:       jetty-webapp   = %{version}-%{release}
Requires:       objectweb-asm
Requires:       geronimo-annotation
Requires:       tomcat-lib
%description    annotations

%package        client
Summary:        client module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-http    = %{version}-%{release}
Requires:       jetty-io      = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
%description    client

%package        continuation
Summary:        continuation module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
#Requires:       tomcat-servlet-3.0-api
%description    continuation

%package        deploy
Summary:        deploy module for Jetty
Group: 		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-jmx     = %{version}-%{release}
Requires:       jetty-server  = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
Requires:       jetty-webapp  = %{version}-%{release}
Requires:       jetty-xml     = %{version}-%{release}
%description    deploy

%package        http
Summary:        http module for Jetty
Group: 		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-io      = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
#Requires:       tomcat-servlet-3.0-api
%description    http

%package        io
Summary:        io module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
%description    io

%package        jmx
Summary:        jmx module for Jetty
Group:          Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
%description	jmx

%package        jndi
Summary:        jndi module for Jetty
Group: 		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-server  = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
Requires:       jetty-webapp  = %{version}-%{release}
Requires:       %{_javadir}/javamail/mail.jar
%description    jndi

%package        overlay-deployer
Summary:        overlay-deployer module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-deploy  = %{version}-%{release}
Requires:       jetty-http    = %{version}-%{release}
Requires:       jetty-jndi    = %{version}-%{release}
Requires:       jetty-server  = %{version}-%{release}
Requires:       jetty-servlet = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
Requires:       jetty-webapp  = %{version}-%{release}
Requires:       jetty-xml     = %{version}-%{release}
Requires:       geronimo-jta
#Requires:       tomcat-servlet-3.0-api
%description    overlay-deployer

%package        plus
Summary:        plus module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project  = %{version}-%{release}
Requires:       jetty-jndi     = %{version}-%{release}
Requires:       jetty-security = %{version}-%{release}
Requires:       jetty-server   = %{version}-%{release}
Requires:       jetty-servlet  = %{version}-%{release}
Requires:       jetty-util     = %{version}-%{release}
Requires:       jetty-webapp   = %{version}-%{release}
Requires:       jetty-xml      = %{version}-%{release}
#Requires:       tomcat-servlet-3.0-api
%description    plus

%package        policy
Summary:        policy module for Jetty
Group: 		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
%description    policy

%package        rewrite
Summary:        rewrite module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-client  = %{version}-%{release}
Requires:       jetty-http    = %{version}-%{release}
Requires:       jetty-io      = %{version}-%{release}
Requires:       jetty-server  = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
#Requires:       tomcat-servlet-3.0-api
%description    rewrite

%package        security
Summary:        security module for Jetty
Group: 		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-http    = %{version}-%{release}
Requires:       jetty-server  = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
#Requires:       tomcat-servlet-3.0-api
%description    security

%package        server
Summary:        server module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project      = %{version}-%{release}
Requires:       jetty-continuation = %{version}-%{release}
Requires:       jetty-http         = %{version}-%{release}
Requires:       jetty-io           = %{version}-%{release}
Requires:       jetty-jmx          = %{version}-%{release}
Requires:       jetty-util         = %{version}-%{release}
#Requires:       tomcat-servlet-3.0-api
%description    server

%package        servlet
Summary:        servlet module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project      = %{version}-%{release}
Requires:       jetty-continuation = %{version}-%{release}
Requires:       jetty-http         = %{version}-%{release}
Requires:       jetty-io           = %{version}-%{release}
Requires:       jetty-jmx          = %{version}-%{release}
Requires:       jetty-security     = %{version}-%{release}
Requires:       jetty-server       = %{version}-%{release}
Requires:       jetty-util         = %{version}-%{release}
#Requires:       tomcat-servlet-3.0-api
%description    servlet

%package        servlets
Summary:        servlets module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project      = %{version}-%{release}
Requires:       jetty-client       = %{version}-%{release}
Requires:       jetty-continuation = %{version}-%{release}
Requires:       jetty-http         = %{version}-%{release}
Requires:       jetty-io           = %{version}-%{release}
Requires:       jetty-server       = %{version}-%{release}
Requires:       jetty-util         = %{version}-%{release}
Requires:       jetty-webapp       = %{version}-%{release}
#Requires:       tomcat-servlet-3.0-api
%description    servlets

%package        util
Summary:        util module for Jetty
# Utf8Appendable.java is additionally under MIT license
Group:		Applications/Internet
License:        (ASL 2.0 or EPL) and MIT
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
#Requires:       tomcat-servlet-3.0-api
Requires:       slf4j
%description    util

%package        webapp
Summary:        webapp module for Jetty
Group:		Applications/Internet
License:        ASL 2.0 or EPL
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project  = %{version}-%{release}
Requires:       jetty-http     = %{version}-%{release}
Requires:       jetty-io       = %{version}-%{release}
Requires:       jetty-security = %{version}-%{release}
Requires:       jetty-server   = %{version}-%{release}
Requires:       jetty-servlet  = %{version}-%{release}
Requires:       jetty-util     = %{version}-%{release}
Requires:       jetty-xml      = %{version}-%{release}
#Requires:       glassfish-jsp
#Requires:       glassfish-jsp-api
Requires:       jakarta-taglibs-standard
#Requires:       tomcat-servlet-3.0-api
%description    webapp

%package        websocket
Summary:        websocket module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-http    = %{version}-%{release}
Requires:       jetty-io      = %{version}-%{release}
Requires:       jetty-server  = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
#Requires:       tomcat-servlet-3.0-api
%description    websocket

%package        xml
Summary:        xml module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
%description    xml

%if 0%{?rhel} <= 0
%package        nosql
Summary:        nosql module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project = %{version}-%{release}
Requires:       jetty-server  = %{version}-%{release}
Requires:       jetty-util    = %{version}-%{release}
Requires:       mongo-java-driver >= 2.6.5-4
Requires:       tomcat-servlet-3.0-api
%description    nosql

%package        osgi
Summary:        OSGi module for Jetty
Group:		Applications/Internet
Requires:       java7
Requires:       jpackage-utils
#Requires:       jetty-project     = %{version}-%{release}
Requires:       jetty-annotations = %{version}-%{release}
Requires:       jetty-deploy      = %{version}-%{release}
Requires:       jetty-nested      = %{version}-%{release}
Requires:       jetty-server      = %{version}-%{release}
Requires:       jetty-servlet     = %{version}-%{release}
Requires:       jetty-util        = %{version}-%{release}
Requires:       jetty-webapp      = %{version}-%{release}
Requires:       jetty-xml         = %{version}-%{release}
Requires:       eclipse-platform
Requires:       eclipse-rcp
#Requires:       glassfish-jsp
#Requires:       glassfish-jsp-api
Requires:       tomcat-servlet-3.0-api
Requires:       tomcat-el-2.2-api
Requires:       tomcat-jsp-2.2-api
Requires:       tomcat-lib
%description    osgi
%endif

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
# some MIT-licensed code (from Utf8Appendable) is used to generate javadoc
License:        (ASL 2.0 or EPL) and MIT
Requires:       jpackage-utils
%description    javadoc

%prep
%setup -n jetty-hightide-%{version}
%install
[[ %{buildroot} != / ]] && rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/java/jetty
pwd
ls
for module in jetty-ajp jetty-annotations jetty-client jetty-continuation \
		jetty-deploy jetty-http jetty-io jetty-jmx jetty-jndi \
		jetty-overlay-deployer jetty-plus jetty-policy \
		jetty-rewrite jetty-security jetty-server jetty-servlet \
		jetty-servlets jetty-util jetty-webapp jetty-websocket \
		jetty-xml; do
	mv lib/$module-%{version}.jar \
		%{buildroot}%{_javadir}/jetty/$module-%{version}.jar
done

%files
%dir %{_javadir}/jetty

%files ajp
%{_javadir}/jetty/jetty-ajp-%{version}.jar

%files annotations
%{_javadir}/jetty/jetty-annotations-%{version}.jar

%files client
%{_javadir}/jetty/jetty-client-%{version}.jar

%files continuation
%{_javadir}/jetty/jetty-continuation-%{version}.jar

%files deploy
%{_javadir}/jetty/jetty-deploy-%{version}.jar

%files http
%{_javadir}/jetty/jetty-http-%{version}.jar

%files io
%{_javadir}/jetty/jetty-io-%{version}.jar

%files jmx
%{_javadir}/jetty/jetty-jmx-%{version}.jar

%files jndi
%{_javadir}/jetty/jetty-jndi-%{version}.jar

%files overlay-deployer
%{_javadir}/jetty/jetty-overlay-deployer-%{version}.jar

%files plus
%{_javadir}/jetty/jetty-plus-%{version}.jar

%files policy
%{_javadir}/jetty/jetty-policy-%{version}.jar

%files rewrite
%{_javadir}/jetty/jetty-rewrite-%{version}.jar

%files security
%{_javadir}/jetty/jetty-security-%{version}.jar

%files server
%{_javadir}/jetty/jetty-server-%{version}.jar

%files servlet
%{_javadir}/jetty/jetty-servlet-%{version}.jar

%files servlets
%{_javadir}/jetty/jetty-servlets-%{version}.jar

%files util
%{_javadir}/jetty/jetty-util-%{version}.jar

%files webapp
%{_javadir}/jetty/jetty-webapp-%{version}.jar

%files websocket
%{_javadir}/jetty/jetty-websocket-%{version}.jar

%files xml
%{_javadir}/jetty/jetty-xml-%{version}.jar

%changelog
* Wed Apr 03 2013 Carl Edquist <edquist@cs.wisc.edu> - 8.1.4-2
- Build with OpenJDK7

* Wed Jul 26 2012 Neha Sharma <neha@fnal.gov> - 8.1.4-1
- Passing through the tarballs needed by Bestman
