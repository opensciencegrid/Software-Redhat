Name:           empty-condor
Version:        1.1
Release:        8%{?dist}
Summary:        An empty Condor package

Group:          Applications/System
License:        Unknown
URL:            http://vdt.cs.wisc.edu

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# This fulfills depenendencies for most OSG packages that depend on Condor
# Versioned provides is needed to deal with conflicts causes in htcondor-ce
# (SOFTWARE-2495).
Provides:       condor = 8.4.9
Provides:       condor-all = 8.4.9
Provides:       condor-aviary = 8.4.9
Provides:       condor-aviary-common = 8.4.9
Provides:       condor-aviary-hadoop = 8.4.9
Provides:       condor-aviary-hadoop-common = 8.4.9
Provides:       condor-bosco = 8.4.9
Provides:       condor-classads = 8.4.9
Provides:       condor-classads-devel = 8.4.9
Provides:       condor-cream-gahp = 8.4.9
Provides:       condor-deltacloud-gahp = 8.4.9
Provides:       condor-external-libs = 8.4.9
Provides:       condor-externals = 8.4.9
Provides:       condor-kbdd = 8.4.9
Provides:       condor-parallel-setup = 8.4.9
Provides:       condor-plumage = 8.4.9
Provides:       condor-procd = 8.4.9
Provides:       condor-python = 8.4.9
Provides:       condor-qmf = 8.4.9
Provides:       condor-static-shadow = 8.4.9
Provides:       condor-std-universe = 8.4.9
Provides:       condor-test = 8.4.9
Provides:       condor-vm-gahp = 8.4.9

Conflicts:      /usr/sbin/condor_master

# These fulfill dependencies for glexec, specifically lcmaps-plugins-glexec-tracking
# so that people can use their own Condor install and still install osg-wn-client-glexec
Provides:       /usr/sbin/condor_procd
Provides:       /usr/sbin/gidd_alloc
Provides:       /usr/sbin/procd_ctl

# This fulfills dependencies for htcondor-ce-client
%ifarch x86_64
Provides: htcondor.so()(64bit)
%else
Provides: htcondor.so()
%endif

%description

This pacakge is empty (it provides no files), but it claims to provide all of
Condor. This allows users to install Condor with a different mechanism 
(such as from a binary tarball or built from source), and fake out RPM so that it 
believes that Condor has been installed via RPM. 

%prep

%build

%install

%clean

%files

%doc

%changelog
* Tue Oct 25 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1-8
- Provide all other condor subpackages (SOFTWARE-2507)

* Mon Oct 24 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1-7
- Provide condor = 8.4.9 and condor-python-8.4.9 (SOFTWARE-2495)

* Thu Aug 04 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1-6
- Provide condor-python (SOFTWARE-2423)

* Thu Mar 31 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1-5
- rebuilt

* Tue Aug 20 2013 Brian Lin <blin@cs.wisc.edu> - 1.1-4
- Provide htcondor.so to work with htcondor-ce
- Make separate builds for different architectures

* Tue Aug 28 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.1-2
- Conflict with /usr/sbin/condor_master to avoid having this being installed
  alongside a real RPM Condor.

* Mon Aug 6 2012 Alain Roy <roy@cs.wisc.edu> - 1.1-1
- Added more provides clauses so this works with glexec-tracking plugin for lcmaps 

* Mon Jan 30 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-3
- Removing conflict with condor

* Mon Jan 30 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-2
- Adding conflict with RPM based Condor

* Thu Nov 17 2011 Alain Roy <roy@cs.wisc.edu> - 1.0-1
- Initial version
