## Gotta define where python stuff is on EL5
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif
Name: cctools
Version: 4.0.2
Release: 4%{?dist}
Summary: A collection of tools for harnessing large scale distributed systems.
License: GPL 2.0 
URL: http://www3.nd.edu/~ccl/
Group: System Environment/Daemons

Source0: %{name}-%{version}-source.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: cvmfs-devel xrootd-devel fuse-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: python-devel >= 2.4
BuildRequires: swig
%if 0%{?rhel} > 5
BuildRequires: perl-ExtUtils-Embed
%endif
#Addded so documentation is built 
BuildRequires: m4 doxygen 
BuildRequires: /usr/bin/nroff


%description
The Cooperative Computing Tools are a collection of tools for harnessing large
scale distributed systems, such as clusters, clouds, and grids.


%package parrot
Group: System Environment/Daemons
Summary: User-level virtual filesystem that allows programs to attach to remote storage systems
%description parrot
Parrot is a tool for attaching existing programs to remote I/O systems through
the filesystem interface. Parrot "speaks" a variety of remote I/O services
include HTTP, FTP, GridFTP, iRODS, HDFS, XRootD, GROW, and Chirp on behalf of
ordinary programs. It works by trapping a program's system calls through the
ptrace debugging interface, and replacing them with remote I/O operations as
desired.


%package chirp
Group: System Environment/Daemons
Summary: Personal user-level distributed filesystem 
Requires: cctools-dttools
%description chirp
Chirp is a user-level file system for collaboration across distributed systems
such as clusters, clouds, and grids. Chirp allows ordinary users to discover,
share, and access storage, whether within a single machine room or over a wide
area network. 

%package makeflow
Group: Development/Tools
Summary: Workflow system for parallel and distributed computing
%description makeflow
Makeflow is a workflow engine for executing large complex workflows on clusters,
clouds, and grids. Makeflow is very similar to traditional Make, so if you can
write a Makefile, then you can write a Makeflow. You can be up and running
workflows in a matter of minutes. 

%package sand
Group: Development/Tools
Summary: Modules augmenting the Celera genome assembler
%description sand
SAND is a set of modules for genome assembly that are built atop the Work Queue
platform for large-scale distributed computation on clusters, clouds, or grids.
SAND was designed as a modular replacement for the conventional overlapper in
the Celera assembler, separated into two distinct steps: candidate filtering
and alignment. 

%package work_queue
Group: System Environment/Libraries
Summary: System and library for creation and management of master-worker style programs
Requires: python >= 2.4
Requires: perl
%description work_queue
Work Queue is a framework for building large master-worker applications that
span many computers including clusters, clouds, and grids. Work Queue
applications are written in C, Perl, or Python using a simple API that allows
users to define tasks, submit them to the queue, and wait for completion. Tasks
are executed by a standard worker process that can run on any available machine.
Each worker calls home to the master process, arranges for data transfer, and
executes the tasks. The system handles a wide variety of failures, allowing for
dynamically scalable and robust applications. 

%package dttools
Group: System Environment/Libraries
Summary: Common libraries for CCTools software
%description dttools
Common libraries for CCTools software 

%package wavefront
Group: System Environment/Libraries
Summary: Framework for dynamic programming problems on distributed systems
%description wavefront
The Wavefront abstraction computes a two dimensional recurrence relation. You
provide a function F that accepts the left (x), right (y), and diagonal (d)
values and initial values for the edges of the matrix. You may optionally
provide additional parameters for each cell, given by a matrix P. The
abstraction then runs each of the functions in the order of dependency, handling
load balancing, data movement, fault tolerance, and so on. 

%package resource_monitor
Group: System Environment/Libraries
Summary: Resource monitoring tools for distributed systems
%description resource_monitor
Resource Monitor generates up to three report files: a summary file with the
maximum values of resource used, a time-series that shows the resources used at
given time intervals, and a list of files that were opened during execution,
together with the count of read and write operations. Additionally, the monitor
can be used as a watchdog. Maximum resource limits can be specified, and if one
of the resources goes over the limit, then the monitor terminates the task,
including a report of the resource that was above the limit. 

%prep
%setup -c
%build
cd %{name}-%{version}-source
## Initial RPM will only workqueue
./configure --without-system-resource_monitor_visualizer --with-cvmfs-path /usr
make

## need to have -devel packages in buildrequires.
## for OSG Connect, we want to build globus, xrootd, and cvmfs support at least.
## But if this doesn't require the packages on the remote system, just build everything.
#*** skipping rfio support
#*** skipping dcap support
#*** skipping globus support
#*** skipping irods support
#*** skipping mysql support
#*** skipping mpi support
#*** skipping xrootd support
#*** skipping cvmfs support
#*** skipping krb5 support


%install
rm -rf %{buildroot}
cd %{name}-%{version}-source
mkdir -p %{buildroot}/usr/lib64
make CCTOOLS_INSTALL_DIR=%{buildroot}/usr install

###################################################################
## in version two lets just move lib to lib64 if 64-bit arch !! ###
###################################################################
%ifarch i386 i686
rm %{buildroot}/usr/lib/lib/libparrot_helper.so
%endif

%ifarch amd64 x86_64
rm %{buildroot}/usr/lib/lib64/libparrot_helper.so
mv %{buildroot}/usr/lib/libchirp.a %{buildroot}/%{_libdir}
mv %{buildroot}/usr/lib/libdttools.a %{buildroot}/%{_libdir}
mv %{buildroot}/usr/lib/libftp_lite.a %{buildroot}/%{_libdir}
mv %{buildroot}/usr/lib/librmonitor_helper.so %{buildroot}/%{_libdir}
mv %{buildroot}/usr/lib/libparrot_helper.so %{buildroot}/%{_libdir}
mv %{buildroot}/usr/lib/libparrot_client.a %{buildroot}/%{_libdir}
mv %{buildroot}/usr/lib/libwork_queue.a %{buildroot}/%{_libdir}
%endif

## apparently site_perl is no longer in vogue. need to create vendor_perl
mkdir -p %{buildroot}%{_libdir}/perl5/vendor_perl
# ## pm should be noarch and .so is 64-bit, and moved to vendor_perl
mv %{buildroot}/usr/lib/perl5/site_perl/*/* %{buildroot}/%{_libdir}/perl5/vendor_perl/

# Shared library conflicts with our condor package
mkdir %{buildroot}/%{_libdir}/cctools
mv %{buildroot}/usr/lib/libchirp_client.so %{buildroot}/%{_libdir}/cctools

## /usr/doc is not canonical. it's /usr/share/doc
mkdir -p %{buildroot}/usr/share/doc/
mv %{buildroot}/usr/doc %{buildroot}/usr/share/doc/cctools

# removing some files we probably dont need..
rm %{buildroot}/usr/etc/Makefile.config

%files
%{_docdir}/cctools/allpairs.html
%{_docdir}/cctools/awe.html
%{_docdir}/cctools/ftsh.html
%{_docdir}/cctools/index.html
%{_docdir}/cctools/install.html
#Added so the documentation and the man pages are included
%{_docdir}/%{name}/api/html/*
%{_docdir}/%{name}/man/*
%_mandir/man1/*


%files resource_monitor
%{_bindir}/resource_monitor
%{_bindir}/resource_monitorv
%{_libdir}/librmonitor_helper.so
%{_docdir}/cctools/resource_monitor.html

%files wavefront
%{_bindir}/wavefront
%{_bindir}/wavefront_master
%{_docdir}/cctools/wavefront.html
%{_docdir}/cctools/images/*

%files sand
%{_bindir}/allpairs_master
%{_bindir}/allpairs_multicore
%{_bindir}/sand_align_kernel
%{_bindir}/sand_align_master
%{_bindir}/sand_compress_reads
%{_bindir}/sand_filter_kernel
%{_bindir}/sand_runCA_5.4
%{_bindir}/sand_runCA_6.1
%{_bindir}/sand_runCA_7.0
%{_bindir}/sand_uncompress_reads
%{_bindir}/sand_filter_master
%{_docdir}/cctools/sand.html

%files makeflow
%{_bindir}/makeflow
%{_bindir}/makeflow_log_parser
%{_bindir}/makeflow_monitor
%{_bindir}/starch
%{_bindir}/condor_submit_makeflow
%{_docdir}/cctools/makeflow.html

%files parrot
## ftp lite 
%{_libdir}/libftp_lite.a
%{_includedir}/cctools/ftp_lite.h
%{_docdir}/cctools/ftp_lite.html
## s3tools
%{_bindir}/make_growfs
## parrot proper
%{_bindir}/parrot_cp
%{_bindir}/parrot_getacl
%{_bindir}/parrot_identity_box
%{_bindir}/parrot_locate
%{_bindir}/parrot_lsalloc
%{_bindir}/parrot_md5
%{_bindir}/parrot_mkalloc
%{_bindir}/parrot_run
%{_bindir}/parrot_run_hdfs
%{_bindir}/parrot_search
%{_bindir}/parrot_setacl
%{_bindir}/parrot_whoami
%{_bindir}/parrot_timeout
%{_includedir}/cctools/parrot_client.h
%{_libdir}/libparrot_client.a
%{_libdir}/libparrot_helper.so
%{_docdir}/cctools/parrot.html

%files chirp
%{_bindir}/chirp
%{_bindir}/chirp_audit_cluster
%{_bindir}/chirp_benchmark
%{_bindir}/chirp_distribute
%{_bindir}/chirp_fuse
%{_bindir}/chirp_get
%{_bindir}/chirp_put
%{_bindir}/chirp_server
%{_bindir}/chirp_server_hdfs
%{_bindir}/chirp_status
%{_bindir}/chirp_stream_files
%{_includedir}/cctools/chirp_client.h
%{_includedir}/cctools/chirp_global.h
%{_includedir}/cctools/chirp_matrix.h
%{_includedir}/cctools/chirp_multi.h
%{_includedir}/cctools/chirp_protocol.h
%{_includedir}/cctools/chirp_recursive.h
%{_includedir}/cctools/chirp_reli.h
%{_includedir}/cctools/chirp_stream.h
%{_includedir}/cctools/chirp_types.h
%{_libdir}/libchirp.a
%dir %{_libdir}/cctools/
%{_libdir}/cctools/libchirp_client.so
%{_docdir}/cctools/chirp.html
%{_docdir}/cctools/chirp_protocol.html

%files work_queue
%{_bindir}/condor_submit_workers
%{_bindir}/ec2_remove_workers
%{_bindir}/ec2_submit_workers
%{_bindir}/pbs_submit_workers
%{_bindir}/sge_submit_workers
%{_bindir}/torque_submit_workers
%{_bindir}/slurm_submit_workers
%{_bindir}/watchdog
%{_bindir}/work_queue_example
%{_bindir}/work_queue_pool
%{_bindir}/work_queue_status
%{_bindir}/work_queue_worker
%{python_sitelib}/work_queue.py
%{python_sitelib}/work_queue.pyc
%{python_sitelib}/work_queue.pyo
%{python_sitelib}/_work_queue.so
%{_includedir}/cctools/work_queue.h
%{_docdir}/cctools/COPYING
%{_docdir}/cctools/workqueue.html
%{_docdir}/cctools/watchdog.html
%{_docdir}/cctools/work_queue_example.c
%{_docdir}/cctools/work_queue_example.pl
%{_docdir}/cctools/work_queue_example.py
%{_docdir}/cctools/work_queue_example.pyc
%{_docdir}/cctools/work_queue_example.pyo
%{_libdir}/libwork_queue.a 
%{_libdir}/perl5/vendor_perl/work_queue.pm
%{_libdir}/perl5/vendor_perl/work_queue.so

%files dttools
%{_bindir}/catalog_server
%{_bindir}/catalog_update
%{_libdir}/libdttools.a
%{_includedir}/cctools/auth.h
%{_includedir}/cctools/auth_address.h
%{_includedir}/cctools/auth_all.h
%{_includedir}/cctools/auth_globus.h
%{_includedir}/cctools/auth_hostname.h
%{_includedir}/cctools/auth_kerberos.h
%{_includedir}/cctools/auth_ticket.h
%{_includedir}/cctools/auth_unix.h
%{_includedir}/cctools/batch_job.h
%{_includedir}/cctools/debug.h
%{_includedir}/cctools/int_sizes.h
#%{_includedir}/cctools/rmonitor_hooks.h  ## rmonitor_hooks.h isnt present in dttools/src, but the Makefile wants to move it to /include.
%{_includedir}/cctools/timestamp.h
%{_includedir}/cctools/buffer.h
%{_includedir}/cctools/md5.h

%changelog
* Tue Dec 10 2013 Edgar Fajardo <efajardo@cern.ch> - 4.0.2-4
- Added m4, doxygen and nroff so documentation is built.

* Tue Oct 15 2013 Brian Lin <blin@cs.wisc.edu> - 4.0.2-3
- Introduced to the OSG Software Stack

* Thu Oct 10 2013 Lincoln Bryant <lincolnb@hep.uchicago.edu> - 4.0.2-2
- B. Tovar patched segfault in Makeflow when using Condor submit
- Moved Perl from site_perl to vendor_perl

* Wed Sep 18 2013 Lincoln Bryant <lincolnb@hep.uchicago.edu> - 4.0.2-1
- Rebased to 4.0.2

* Mon Aug 19 2013 Lincoln Bryant <lincolnb@hep.uchicago.edu> - 4.0.1-1
- Added CVMFS and FUSE support.
