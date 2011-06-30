Name:           bestman2
Version:        2.1.0.pre2
Release:        49
Summary:        SRM server for Grid Storage Elements

Group:          System Environment/Daemons
License:        https://sdm.lbl.gov/bestman/
URL:            https://sdm.lbl.gov/bestman/

%define install_root /usr/lib/%{name}
%define bestman_url https://codeforge.lbl.gov/frs/download.php/316/bestman2-2.1.0-pre2.tar.gz

Source0:        bestman2.tar.gz
Source1:        bestman2.sysconfig
Source2:        bestman2.init
Source3:        bestman.logrotate
Source4:        bestman2.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-roo1t-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  jdk wget ant

Obsoletes: bestman

%description
Application server for exporting local file systems securely using the
SRM protocol.

%package server
Summary: BeStMan SRM server
Group: System Environment/Daemons

Obsoletes: bestman2

Requires: %{name}-libs = %{version}-%{release}
Requires(pre): shadow-utils
Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service

%description server
BeStMan SRM server

%package libs
Summary: BeStMan SRM Java libraries
Group: System Environment/Libraries
Requires:  jdk
%description libs
The BeStMan SRM Java libraries

%package client
Summary: SRM clients
Group: System Environment/Applications
Requires: %{name}-libs = %{version}-%{release}
%description client
The srm-* client tools

%prep
%setup -q -n %{name}

%build


./build.configure --with-bestman-url=%{bestman_url} --with-bestman2-version=%{version} --with-revision=%{release} --with-java-home=/usr/java/latest --enable-cached-src=yes --enable-cached-pkg=yes

make

pushd bestman2

SRM_HOME=%{install_root}
export SRM_HOME
GLOBUS_LOCATION=/usr
export GLOBUS_LOCATION

pushd setup
./configure --with-srm-home=$SRM_HOME \
    --enable-gateway-mode \
    --enable-gums \
    --enable-sudofsmng \
    --with-java-home=/usr/java/latest \
    --with-eventlog-path=/var/log/%{name} \
    --with-cachelog-path=/var/log/%{name} \
    --with-plugin-path=$SRM_HOME/lib \
    --with-gums-url=https://GUMS_HOST:8443/gums/services/GUMSAuthorizationServicePort \
    --enable-backup=no \
    --with-certfile-path=/etc/grid-security/http/httpcert.pem \
    --with-keyfile-path=/etc/grid-security/http/httpkey.pem \
    --with-gums-certfile-path=/etc/grid-security/http/httpcert.pem \
    --with-gums-keyfile-path=/etc/grid-security/http/httpkey.pem \
    --with-sysconf-path=/etc/sysconfig/bestman2 \
    --with-bestman2-conf-path=../conf/bestman2.rc
popd

SRM_HOME=/usr/lib/bestman2
export SRM_HOME

popd

%install
rm -rf $RPM_BUILD_ROOT

pushd bestman2

mkdir -p $RPM_BUILD_ROOT%{install_root}
mkdir -p $RPM_BUILD_ROOT%{install_root}/setup
mkdir -p $RPM_BUILD_ROOT%{install_root}/sbin
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mv conf/bestman2.rc $RPM_BUILD_ROOT%{_sysconfdir}/
cp -ar conf $RPM_BUILD_ROOT%{install_root}
cp -ar lib $RPM_BUILD_ROOT%{install_root}
cp -ar properties $RPM_BUILD_ROOT%{install_root}
cp -ar setup/bestman.in $RPM_BUILD_ROOT%{install_root}/setup


install -m 0755 version $RPM_BUILD_ROOT%{install_root}/
install -m 0755 setup/configure $RPM_BUILD_ROOT%{install_root}/setup/configure
install -m 0755 sbin/bestman.server $RPM_BUILD_ROOT%{install_root}/sbin/bestman.server


mkdir -p $RPM_BUILD_ROOT%{_bindir}
for i in `ls bin`; do
  install -m 0755 bin/$i $RPM_BUILD_ROOT%{_bindir}/
done

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/%{name}
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}
install -m 0755 %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/grid-security/vomsdir
touch $RPM_BUILD_ROOT%{_sysconfdir}/grid-security/vomsdir/vdt-empty.pem

mkdir -p $RPM_BUILD_ROOT%{_var}/log/%{name}

popd

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
getent group bestman >/dev/null || groupadd -r bestman
getent passwd bestman >/dev/null || \
       useradd -r -g bestman -d %{install_root} -c "Bestman SRM user" \
       -s /bin/bash bestman

%post server
/sbin/chkconfig --add %{name}

%preun server
if [ "$1" = "0" ]; then
    /sbin/chkconfig --del %{name}
fi

%postun server
if [ "$1" -ge "1" ] ; then
    /sbin/service bestman2 condrestart >/dev/null 2>&1 || :
fi

%files libs
%defattr(-,root,root,-)
%dir %{install_root}
%{install_root}/lib/axis
%{install_root}/lib/jglobus
%{install_root}/lib/bestman2.jar
%{install_root}/lib/bestman2-stub.jar
%{install_root}/lib/bestman2-printintf.jar
%{install_root}/lib/bestman2-transfer.jar
%{install_root}/version
%{install_root}/properties
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%files client
%defattr(-,root,root,-)
%{install_root}/lib/bestman2-aux.jar
%{install_root}/lib/bestman2-client.jar
%{install_root}/lib/bestman2-tester-driver.jar
%{install_root}/lib/bestman2-tester-main.jar
%config(noreplace) %{install_root}/conf/srmclient.conf
%{install_root}/conf/srmclient.conf.sample
%config(noreplace) %{install_root}/conf/srmtester.conf
%{install_root}/conf/srmtester.conf.sample
%{_bindir}/*

%files server
%defattr(-,root,root,-)
%{install_root}/lib/others
%{install_root}/lib/voms
%{install_root}/lib/gums
%{install_root}/lib/gums2
%{install_root}/lib/jetty
%{install_root}/lib/plugin
%{install_root}/sbin/bestman.server
%{install_root}/conf/WEB-INF
%{install_root}/conf/bestman2.gateway.sample.rc
%{install_root}/conf/grid-mapfile.empty
%{install_root}/conf/bestman-diag-msg.conf
%{install_root}/conf/bestman-diag.conf.sample
%config(noreplace) %{_sysconfdir}/%{name}.rc
%{_initrddir}/%{name}
%{_sbindir}/%{name}
%{install_root}/setup/configure
%{install_root}/setup/bestman.in/*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0644,root,root) %{_sysconfdir}/grid-security/vomsdir/vdt-empty.pem
%attr(-,bestman,bestman) %dir %{_var}/log/%{name}

%changelog
* Mon Jun 13 2011 Doug Strain <dstrain@fnal.gov> 2.0.13.t5-43
Creating Bestman2 spec file based on Hadoop repository

