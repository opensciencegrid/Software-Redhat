Name:           osg-panda-repo
Version:        0.1
Release:        1%{?dist}
Summary:        OSG PanDA packages

Group:          System Environment/Base 
License:        GPL 
URL:            http://koji-hub.batlab.org/mnt/koji/repos/panda-el6/latest/

Source0:        osg-panda.repo

Source40:       RPM-GPG-KEY-OSG

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Requires:       redhat-release >= %{rhel}

%description
%{summary}

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT

#GPG Key
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg
install -pm 644 %{SOURCE40} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-OSG

# yum
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

install -m 644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-OSG

