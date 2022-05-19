Name:           pegasus
Version:        4.9.3
Release:        1.2%{?dist}
Summary:        Workflow management system for HTCondor, grids, and clouds
Group:          Applications/System
License:        ASL 2.0
URL:            http://pegasus.isi.edu/
Packager:       Pegasus Development Team <pegasus-support@isi.edu>

Source:         pegasus-%{version}.tar.gz

BuildRequires:  python-setuptools, openssl-devel, pyOpenSSL ant, ant-apache-regexp, gcc, groff, python-devel, gcc-c++, make, jpackage-utils, asciidoc, libxslt, fop, R-devel
%if 0%{?rhel} < 7
BuildRequires:  ant-nodeps, java-1.8.0-openjdk-devel, /usr/share/java-1.8.0
%endif
%if 0%{?rhel} >= 7
BuildRequires:  java-devel = 1:1.8.0, /usr/share/java-1.8.0
%endif
Requires:       java >= 1:1.8.0, python >= 2.6, condor >= 8.6, graphviz, pyOpenSSL, python-amqplib, python-six

%define sourcedir %{name}-%{version}

# rpmbuild might add python3 as a dependency due to some Singularity example
# workflows. This is a false dependency, so make sure it is excluded.
%global __requires_exclude ^/usr/bin/python3$

%description
The Pegasus project encompasses a set of technologies that
help workflow-based applications execute in a number of
different environments including desktops, campus clusters,
grids, and now clouds. Scientific workflows allow users to
easily express multi-step computations. Once an application
is formalized as a workflow the Pegasus Workflow Management
Service can map it onto available compute resources and
execute the steps in appropriate order.


%prep
%setup -q -n %{sourcedir}

%build
ant dist-release

# strip executables
strip dist/pegasus-%{version}/bin/pegasus-cluster
strip dist/pegasus-%{version}/bin/pegasus-kickstart
strip dist/pegasus-%{version}/bin/pegasus-keg

%install

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}

cp -aR dist/pegasus-%{version}/etc/* %{buildroot}/%{_sysconfdir}/%{name}/
cp -aR dist/pegasus-%{version}/bin/* %{buildroot}/%{_bindir}/
cp -aR dist/pegasus-%{version}/lib* %{buildroot}/usr/
cp -aR dist/pegasus-%{version}/share/* %{buildroot}/%{_datadir}/

# rm unwanted files
rm -f %{buildroot}/%{_bindir}/keg.condor
rm -f %{buildroot}/%{_datadir}/%{name}/java/COPYING.*
rm -f %{buildroot}/%{_datadir}/%{name}/java/EXCEPTIONS.*
rm -f %{buildroot}/%{_datadir}/%{name}/java/LICENSE.*
rm -f %{buildroot}/%{_datadir}/%{name}/java/NOTICE.*

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/
%{_bindir}/*
%{_libdir}/pegasus
%{_libdir}/python*
%{_datadir}/doc/%{name}
%{_datadir}/man/man1/*
%{_datadir}/%{name}


%changelog
* Tue Mar 10 2020 Mátyás Selmeci <matyas@cs.wisc.edu> 4.9.3-1.2
- Add python-six dependency (SOFTWARE-4014)

* Mon Feb 03 2020 Pegasus Development Team <pegasus-support@isi.edu> 4.9.3
- 4.9.3 automatic build

* Mon Dec 02 2013 Pegasus Development Team <pegasus-support@isi.edu> 4.3.2cvs
- Relaxed the "java" requirements in order for the package to work on plan
  CentOS machines

