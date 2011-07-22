Name:           osg-site-web-page
Version:        0.14
Release:        1
Summary:        OSG Site Web Page Generation Script
Group:          System Environment
License:        ASL 2.0
URL:            https://vdt.cs.wisc.edu/svn/software/osg-site-web-page/trunk/README

Source0:        %{name}-%{version}.tar.gz

#BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch:      noarch
# BuildRequires:  /bin/hostname
Requires:       apache perl python 
Requires:       osg-configure

# definitions
%define clean_buildroot             [[ -n "%buildroot" && "%buildroot" != / ]] && rm -rf %buildroot
%define is_true()                   %{expand:%%{?%{1}}%%{?!%{1}:0}}
%define is_false()                  ! %{expand:%%{?%{1}}%%{?!%{1}:0}}


%description
This package creates a site home page for OSG sites. 
It relies on information discovered at the site, mainly in the config.ini file.

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
%setup -c 

%build
# sed -i "s/HOSTNAME/`/bin/hostname`/" bin/setup-osg-portal

%install
%clean_buildroot
# make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sbindir}/
# from osg-config: mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/osg
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}/www

for i in bin/*; do
	install -m 0755 $i $RPM_BUILD_ROOT%{_sbindir}
done
for i in web/*; do
	install -m 0644 $i $RPM_BUILD_ROOT%{_libdir}/%{name}/www
done

%clean
%if %is_false NOCLEAN
%clean_buildroot
%endif

%files
%{_sbindir}/*
%{_libdir}/%{name}/www/*
#%{_sysconfdir}/siteindexconfig.ini


%changelog
* Thu Jul 21 2011 Marco Mambelli <marco@hep.uchicago.edu> 0.14
Initial creation of spec file
