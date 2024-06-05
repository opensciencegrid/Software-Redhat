Name:           empty-condor
Version:        1.1
Release:        13%{?dist}
Summary:        An empty HTCondor package

License:        Unknown
URL:            http://vdt.cs.wisc.edu


# This fulfills depenendencies for most OSG packages that depend on Condor
# Versioned provides are needed for versioned dependencies, e.g. in htcondor-ce.
Provides:       condor = 99
Provides:       condor-all = 99
Provides:       condor-aviary = 99
Provides:       condor-aviary-common = 99
Provides:       condor-aviary-hadoop = 99
Provides:       condor-aviary-hadoop-common = 99
Provides:       condor-bosco = 99
Provides:       condor-classads = 99
Provides:       condor-classads-devel = 99
Provides:       condor-cream-gahp = 99
Provides:       condor-deltacloud-gahp = 99
Provides:       condor-external-libs = 99
Provides:       condor-externals = 99
Provides:       condor-kbdd = 99
Provides:       condor-parallel-setup = 99
Provides:       condor-plumage = 99
Provides:       condor-procd = 99
Provides:       condor-python = 99
Provides:       condor-qmf = 99
Provides:       condor-static-shadow = 99
Provides:       condor-std-universe = 99
Provides:       condor-test = 99
Provides:       condor-vm-gahp = 99
Provides:       python2-condor = 99
Provides:       python3-condor = 99

Conflicts:      /usr/sbin/condor_master

# These fulfill dependencies for glexec, specifically lcmaps-plugins-glexec-tracking
# so that people can use their own Condor install and still install osg-wn-client-glexec
Provides:       /usr/sbin/condor_procd
Provides:       /usr/sbin/gidd_alloc
Provides:       /usr/sbin/procd_ctl

# EL9 osg-ce-* depend on condor-blahp rather than blahp
%if 0%{?rhel} > 8
Provides: condor-blahp = 99
Provides: blahp = 99
%endif

# For htcondor-ce-client (htcondor.so) and blahp (libclassad.so.8)
%ifarch x86_64
Provides: htcondor.so()(64bit)
Provides: libclassad.so.8()(64bit)
%else
Provides: htcondor.so()
Provides: libclassad.so.8()
%endif

%description

This pacakge is empty (it provides no files), but it claims to provide all of
Condor. This allows users to install Condor with a different mechanism 
(such as from a binary tarball or built from source), and fake out RPM so that it 
believes that Condor has been installed via RPM. 

%prep

%build

%install

%files

%doc

%changelog
* Wed Jun 27 2023 Matt Westphall <westphall@wisc.edu> - 1.1-12
- Provide condor-blahp (SOFTWARE-5599)

* Fri Jun 11 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1-11
- Provide python2-condor (SOFTWARE-4661)

* Fri Jan 29 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1-10
- Provide python3-condor (SOFTWARE-4451)

* Fri Jan 19 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1-9
- Bump provides versions to 99 to allow versioned requires to work without
  having to update the versions
- Provide libclassad.so.8() for blahp for htcondor-ce

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
