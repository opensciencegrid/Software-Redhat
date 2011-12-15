
Name: yum-remove-osg
Version: 1.0
Release: 0.2%{?dist}
Summary: Yum plugin to assist in removing OSG packages

Group: System Environment/Base

License: BSD
URL: https://vdt.cs.wisc.edu/svn/native/redhat/trunk/yum-remove-osg
Source0: remove-osg.py
Source1: remove-osg.conf

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: yum >= 3.2.19

%description
%{summary}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/yum-plugins
install -m 0755 %SOURCE0 $RPM_BUILD_ROOT%{_prefix}/lib/yum-plugins/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/yum/pluginconf.d/
install -m 0644 %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/yum/pluginconf.d/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_prefix}/lib/yum-plugins/remove-osg.py*
%{_sysconfdir}/yum/pluginconf.d/remove-osg.conf

%changelog
* Mon Nov 28 2011 Neha Sharma <neha@fnal.gov> - 1.0-0.2
- Commented code that removed packages from non-OSG repos

* Tue Sep 20 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.0-0.1
- Initial attempt at an OSG removal plugin.

