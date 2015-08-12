Name:           osg-site-web-page
Version:        0.15
Release:        3%{?dist}
Summary:        OSG Site Web Page Generation Script
Group:          System Environment
License:        ASL 2.0
URL:            https://vdt.cs.wisc.edu/svn/software/osg-site-web-page/trunk/README

Source0:        %{name}-%{version}.tar.gz

#BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch:      noarch
# BuildRequires:  /bin/hostname
Requires:       httpd python 
Requires:       osg-configure

# definitions
%define clean_buildroot             [[ -n "%buildroot" && "%buildroot" != / ]] && rm -rf %buildroot
%define is_true()                   %{expand:%%{?%{1}}%%{?!%{1}:0}}
%define is_false()                  ! %{expand:%%{?%{1}}%%{?!%{1}:0}}


%description
This package creates a site home page for OSG sites. 
It relies on information discovered at the site, mainly in the config.ini file.
Page can be viewed at https://your_hostname/site (or https://localhost/site)

%prep
# %%setup quick reference:
#   -a N        Unpack source N after cd
#   -b N        Unpack source N before cd
#   -c          Create and cd to dir before unpacking
#   -D          Do not delete dir before unpacking
#   -n DIR      Name of extract dir (instead of NAME-VERSION)
#   -T          Do not autounpack Source0
#   -q          quiet
#%setup -q -n %{name}
#%setup -c 
%setup

%build
# sed -i "s/HOSTNAME/`/bin/hostname`/" bin/setup-osg-portal

%install
%clean_buildroot
# make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/osg
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
mkdir -p $RPM_BUILD_ROOT%{_datadir}/osg/www.d/
mkdir -p $RPM_BUILD_ROOT%{_sbindir}/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/www

install -m 0644 etc/%{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 0644 etc/%{name}.site $RPM_BUILD_ROOT%{_datadir}/osg/www.d/
for i in bin/*; do
	install -m 0755 $i $RPM_BUILD_ROOT%{_sbindir}
done
for i in web/*; do
	install -m 0644 $i $RPM_BUILD_ROOT%{_datadir}/%{name}/www
done

# Touch files so that are removed with uninstall
touch $RPM_BUILD_ROOT%{_sysconfdir}/osg/siteindexconfig.ini

%post
if [ -f /etc/osg/config.ini ]
then
 # conditional execution instead of creating a temporary config.ini 
 # cat /etc/osg/ce.ini /etc/osg/storage.ini /etc/osg/gums.ini /etc/osg/rsv.ini > /etc/osg/config.ini
 /usr/sbin/osg-make-portal-config -q
 /usr/sbin/osg-make-portal -q
fi
# restart apache if running to get the new configuration
/sbin/service httpd condrestart 2>&1 > /dev/null || :

%postun
# $1, only if actual deinstallation, not uninstall for upgrade
if [ $1 -eq 0 ] ; then
   /sbin/service httpd condrestart >/dev/null 2>&1 || :
fi

%clean
%if %is_false NOCLEAN
%clean_buildroot
%endif

%files
%{_sbindir}/*
%{_datadir}/%{name}/www/*
%{_datadir}/osg/www.d/%{name}.site
%{_sysconfdir}/osg/siteindexconfig.ini
%{_sysconfdir}/httpd/conf.d/%{name}.conf

%changelog
* Fri Sep 16 2011 Marco Mambelli <marco@hep.uchicago.edu> 0.15
improved post and postun (rel 3)
* Mon Aug 1 2011 Marco Mambelli <marco@hep.uchicago.edu> 0.15
running the scripts only is config.ini exists already 
* Mon Aug 1 2011 Marco Mambelli <marco@hep.uchicago.edu> 0.15
binaries renamed osg-make-... instead of make-osg-...
some URL fixed in the tamplate
warning added if configuration is incomplete
running the scripts in post install
* Thu Jul 28 2011 Marco Mambelli <marco@hep.uchicago.edu> 0.14
removed OSG_LOCATION options, improved Makefile
* Sat Jul 23 2011 Marco Mambelli <marco@hep.uchicago.edu> 0.14
pre and post-install added
* Fri Jul 22 2011 Marco Mambelli <marco@hep.uchicago.edu> 0.14
modification to eliminate setup-osg-portal
* Thu Jul 21 2011 Marco Mambelli <marco@hep.uchicago.edu> 0.14
Initial creation of spec file
