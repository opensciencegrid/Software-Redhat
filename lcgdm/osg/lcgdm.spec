%{!?perl_vendorarch: %global perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")}

%if %{?rhel}%{!?rhel:0} == 5
%global altpython python26
%global __altpython %{_bindir}/python2.6
# Disable the default python byte compilation
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%endif

%if %{?fedora}%{!?fedora:0} >= 13
%global altpython python3
%global __altpython %{_bindir}/python3
%endif

%if %{?altpython:1}%{!?altpython:0}
%global altpython_sitearch %(%{__altpython} -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")
%endif

%if %{?filter_setup:1}%{!?filter_setup:0}
%filter_provides_in %{python_sitearch}.*\.so$
%if %{?altpython:1}%{!?altpython:0}
%filter_provides_in %{altpython_sitearch}.*\.so$
%endif
%filter_setup
%endif

Name:		lcgdm
Version:	1.8.0.1
Release:	4%{?dist}
Summary:	LHC Computing Grid Data Management

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://glite.web.cern.ch/glite/
#		LANG=C svn co http://svnweb.cern.ch/guest/lcgdm/lcg-dm/tags/LCG-DM_R_1_8_0_1 lcgdm-1.8.0.1
#		tar --exclude .svn -z -c -f lcgdm-1.8.0.1.tar.gz lcgdm-1.8.0.1
Source0:	%{name}-%{version}.tar.gz
Source1:	README.Fedora.lfc-mysql
Source2:	README.Fedora.lfc-postgres
Source3:	README.Fedora.dpm-mysql
Source4:	README.Fedora.dpns-mysql
Source5:	README.Fedora.dpm-postgres
Source6:	README.Fedora.dpns-postgres
#		Fix non-standard installation path
#		https://savannah.cern.ch/bugs/?57526
Patch0:		%{name}-paths.patch
#		Link using $(CC)
#		https://savannah.cern.ch/bugs/?57527
Patch1:		%{name}-ld.patch
#		Fix soname issues
#		https://savannah.cern.ch/bugs/?57528
Patch2:		%{name}-withsoname.patch
#		Link binaries using shared libraries
#		https://savannah.cern.ch/bugs/?57529
Patch3:		%{name}-shliblink.patch
#		Link to gsoap library, fix parallel build
#		https://savannah.cern.ch/bugs/?57530
Patch4:		%{name}-gsoap.patch
#		Fix build on GNU/Hurd and GNU/kFreeBSD
#		https://savannah.cern.ch/bugs/?61071
Patch5:		%{name}-porting.patch
#		Fix race conditions in Makefile install rules:
#		https://savannah.cern.ch/bugs/?69233
Patch6:		%{name}-race.patch
#		Remove deprecated python function:
#		https://savannah.cern.ch/bugs/?69232
Patch7:		%{name}-python-exception.patch
#		Make condrestart work as expected
Patch8:		%{name}-condrestart.patch
#		Adapt upstream's hardcoded include and library paths for Fedora
Patch9:		%{name}-usr.patch
#		Allow moving plugins out of default library search path
Patch10:	%{name}-dlopen.patch
#		Use Fedora's imake instead of bundled version
Patch11:	%{name}-imake.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{?fedora}%{!?fedora:0} >= 5 || %{?rhel}%{!?rhel:0} >= 5
BuildRequires:	imake
%else
%if %{?fedora}%{!?fedora:0} >= 2 || %{?rhel}%{!?rhel:0} >= 4
BuildRequires:	xorg-x11-devel
%else
BuildRequires:	XFree86-devel
%endif
%endif
BuildRequires:	globus-gssapi-gsi-devel%{?_isa}
BuildRequires:	globus-gss-assist-devel%{?_isa}
BuildRequires:	globus-gsi-credential-devel%{?_isa}
BuildRequires:	globus-gsi-callback-devel%{?_isa}
BuildRequires:	globus-gass-copy-devel%{?_isa}
BuildRequires:	globus-ftp-client-devel%{?_isa}
BuildRequires:	globus-common-devel%{?_isa}
BuildRequires:	voms-devel%{?_isa}
BuildRequires:	gsoap-devel%{?_isa}
BuildRequires:	CGSI-gSOAP-devel%{?_isa} >= 1.3.4.0
BuildRequires:	mysql-devel%{?_isa}
BuildRequires:	postgresql-devel%{?_isa}
%if %{?fedora}%{!?fedora:0} >= 12 || %{?rhel}%{!?rhel:0} >= 6
BuildRequires:	libuuid-devel%{?_isa}
%else
BuildRequires:	e2fsprogs-devel%{?_isa}
%endif
BuildRequires:	swig
%if %{?fedora}%{!?fedora:0} >= 7 || %{?rhel}%{!?rhel:0} >= 6
BuildRequires:	perl-devel%{?_isa}
%else
BuildRequires:	perl
%endif
BuildRequires:	python-devel%{?_isa}
%if %{?altpython:1}%{!?altpython:0}
BuildRequires:	%{altpython}-devel%{?_isa}
%endif

%description
The lcgdm package contains common libraries for the LCG Data Management
components: the LFC (LCG File Catalog) and the DPM (Disk Pool Manager).

%package devel
Summary:	LCG Data Management common development files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains common development libraries and header files
for LCG Data Management

%package -n lfc
Summary:	LCG File Catalog (LFC)
Group:		System Environment/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n lfc
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package contains the runtime LFC client library.

%package -n lfc-devel
Summary:	LFC development libraries and header files
Group:		Development/Libraries
Requires:	lfc%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description -n lfc-devel
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package contains the development libraries and header files for LFC.

%package -n lfc-client
Summary:	LCG File Catalog (LFC) client
Group:		Applications/Internet
Requires:	lfc%{?_isa} = %{version}-%{release}

%description -n lfc-client
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package contains the command line interfaces for the LFC.

%package -n lfc-perl
Summary:	LCG File Catalog (LFC) perl bindings
Group:		Applications/Internet
Requires:	lfc%{?_isa} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n lfc-perl
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package provides Perl bindings for the LFC client library.

%package -n lfc-python
Summary:	LCG File Catalog (LFC) python bindings
Group:		Applications/Internet
Requires:	lfc%{?_isa} = %{version}-%{release}

%description -n lfc-python
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package provides Python bindings for the LFC client library.

%if %{?altpython:1}%{!?altpython:0}
%package -n lfc-%{altpython}
Summary:	LCG File Catalog (LFC) python bindings
Group:		Applications/Internet
Requires:	lfc%{?_isa} = %{version}-%{release}
%if %{?rhel}%{!?rhel:0} == 5
Requires:	python(abi) = 2.6
%endif

%description -n lfc-%{altpython}
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package provides Python bindings for the LFC client library.
%endif

%package -n lfc-mysql
Summary:	LCG File Catalog (LFC) server with MySQL database backend
Group:		Applications/Internet
Provides:	lfcdaemon = %{version}-%{release}
Requires:	lfc%{?_isa} = %{version}-%{release}

Requires(pre):		shadow-utils
Requires(post):		mysql
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n lfc-mysql
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package provides an LFC server that uses MySQL as its database
backend.

%package -n lfc-dli
Summary:	LCG File Catalog (LFC) data location interface (dli) server
Group:		Applications/Internet
Requires:	lfcdaemon = %{version}-%{release}

Requires(pre):		lfcdaemon
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n lfc-dli
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package provides the data location interface (dli) server for the LFC.

%package -n lfc-postgres
Summary:	LCG File Catalog (LFC) server with postgres database backend
Group:		Applications/Internet
Provides:	lfcdaemon = %{version}-%{release}
Requires:	lfc%{?_isa} = %{version}-%{release}

Requires(pre):		shadow-utils
Requires(post):		postgresql
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n lfc-postgres
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package provides an LFC server that uses postgres as its database
backend.

%package -n dpm
Summary:	Disk Pool Manager (DPM)
Group:		System Environment/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n dpm
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package contains the runtime DPM client library.

%package -n dpm-devel
Summary:	DPM development libraries and header files
Group:		Development/Libraries
Requires:	dpm%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description -n dpm-devel
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package contains the development libraries and header files for DPM.

%package -n dpm-client
Summary:	Disk Pool Manager (DPM) client
Group:		Applications/Internet
Requires:	dpm%{?_isa} = %{version}-%{release}

%description -n dpm-client
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package contains the command line interfaces for the DPM.

%package -n dpm-perl
Summary:	Disk Pool Manager (DPM) perl bindings
Group:		Applications/Internet
Requires:	dpm%{?_isa} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n dpm-perl
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides Perl bindings for the DPM client library.

%package -n dpm-python
Summary:	Disk Pool Manager (DPM) python bindings
Group:		Applications/Internet
Requires:	dpm%{?_isa} = %{version}-%{release}

%description -n dpm-python
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides Python bindings for the DPM client library.

%if %{?altpython:1}%{!?altpython:0}
%package -n dpm-%{altpython}
Summary:	Disk Pool Manager (DPM) python bindings
Group:		Applications/Internet
Requires:	dpm%{?_isa} = %{version}-%{release}
%if %{?rhel}%{!?rhel:0} == 5
Requires:	python(abi) = 2.6
%endif

%description -n dpm-%{altpython}
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides Python bindings for the DPM client library.
%endif

%package -n dpm-mysql
Summary:	Disk Pool Manager (DPM) server with MySQL database backend
Group:		Applications/Internet
Requires:	dpm%{?_isa} = %{version}-%{release}

Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-mysql
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM server that uses MySQL as its database
backend.

%package -n dpm-mysql-nameserver
Summary:	DPM nameserver with MySQL database backend
Group:		Applications/Internet
Requires:	dpm-mysql%{?_isa} = %{version}-%{release}

Requires(pre):		dpm-mysql
Requires(post):		mysql
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-mysql-nameserver
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM nameserver that uses MySQL as its database
backend.

%package -n dpm-mysql-copyd
Summary:	DPM copy server with MySQL database backend
Group:		Applications/Internet
Requires:	dpm-mysql%{?_isa} = %{version}-%{release}

Requires(pre):		dpm-mysql
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-mysql-copyd
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM copy server that uses MySQL as its
database backend.

%package -n dpm-mysql-srmv1
Summary:	DPM SRM version 1 server with MySQL database backend
Group:		Applications/Internet
Requires:	dpm-mysql%{?_isa} = %{version}-%{release}

Requires(pre):		dpm-mysql
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-mysql-srmv1
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM SRM version 1 server that uses MySQL as
its database backend.

%package -n dpm-mysql-srmv2
Summary:	DPM SRM version 2 server with MySQL database backend
Group:		Applications/Internet
Requires:	dpm-mysql%{?_isa} = %{version}-%{release}

Requires(pre):		dpm-mysql
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-mysql-srmv2
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM SRM version 2 server that uses MySQL as
its database backend.

%package -n dpm-mysql-srmv22
Summary:	DPM SRM version 2.2 server with MySQL database backend
Group:		Applications/Internet
Requires:	dpm-mysql%{?_isa} = %{version}-%{release}

Requires(pre):		dpm-mysql
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-mysql-srmv22
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM SRM version 2.2 server that uses MySQL as
its database backend.

%package -n dpm-rfiod
Summary:	DPM RFIO server
Group:		Applications/Internet
Requires:	dpm%{?_isa} = %{version}-%{release}

Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-rfiod
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a Remote File IO (RFIO) server for DPM.

%package -n dpm-postgres
Summary:	Disk Pool Manager (DPM) server with postgres database backend
Group:		Applications/Internet
Requires:	dpm%{?_isa} = %{version}-%{release}

Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-postgres
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM server that uses postgres as its database
backend.

%package -n dpm-postgres-nameserver
Summary:	DPM nameserver with postgres database backend
Group:		Applications/Internet
Requires:	dpm-postgres%{?_isa} = %{version}-%{release}

Requires(pre):		dpm-postgres
Requires(post):		postgresql
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-postgres-nameserver
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM nameserver that uses postgres as its
database backend.

%package -n dpm-postgres-copyd
Summary:	DPM copy server with postgres database backend
Group:		Applications/Internet
Requires:	dpm-postgres%{?_isa} = %{version}-%{release}

Requires(pre):		dpm-postgres
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-postgres-copyd
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM copy server that uses postgres as its
database backend.

%package -n dpm-postgres-srmv1
Summary:	DPM SRM version 1 server with postgres database backend
Group:		Applications/Internet
Requires:	dpm-postgres%{?_isa} = %{version}-%{release}

Requires(pre):		dpm-postgres
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-postgres-srmv1
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM SRM version 1 server that uses postgres as
its database backend.

%package -n dpm-postgres-srmv2
Summary:	DPM SRM version 2 server with postgres database backend
Group:		Applications/Internet
Requires:	dpm-postgres%{?_isa} = %{version}-%{release}

Requires(pre):		dpm-postgres
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-postgres-srmv2
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM SRM version 2 server that uses postgres as
its database backend.

%package -n dpm-postgres-srmv22
Summary:	DPM SRM version 2.2 server with postgres database backend
Group:		Applications/Internet
Requires:	dpm-postgres%{?_isa} = %{version}-%{release}

Requires(pre):		dpm-postgres
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-postgres-srmv22
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM SRM version 2.2 server that uses postgres
as its database backend.

%prep
%setup -T -q -c
%setup -q -c -n %{name}-%{version}/lfc-mysql
%setup -q -c -n %{name}-%{version}/lfc-postgres
%setup -q -c -n %{name}-%{version}/dpm-mysql
%setup -q -c -n %{name}-%{version}/dpm-postgres
%setup -D -T -q

for d in lfc-mysql lfc-postgres dpm-mysql dpm-postgres ; do

pushd $d/%{name}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

chmod 644 security/globus_gsi_gss_constants.h \
	  security/globus_i_gsi_credential.h \
	  security/gssapi_openssl.h
chmod 644 doc/lfc/INSTALL-*

sed 's!@@LIBDIR@@!%{_libdir}!' -i security/Csec_api_loader.c

# The code violates the strict aliasing rules all over the place...
# Need to use -fnostrict-aliasing so that the -O2 optimization in
# optflags doesn't try to use them.
sed 's/^CC +=/& %{optflags} -fno-strict-aliasing/' -i config/linux.cf

popd

done

install -m 644 -p %{SOURCE1} lfc-mysql/%{name}-%{version}/ns/README.Fedora
install -m 644 -p %{SOURCE2} lfc-postgres/%{name}-%{version}/ns/README.Fedora
install -m 644 -p %{SOURCE3} dpm-mysql/%{name}-%{version}/dpm/README.Fedora
install -m 644 -p %{SOURCE4} dpm-mysql/%{name}-%{version}/ns/README.Fedora
install -m 644 -p %{SOURCE5} dpm-postgres/%{name}-%{version}/dpm/README.Fedora
install -m 644 -p %{SOURCE6} dpm-postgres/%{name}-%{version}/ns/README.Fedora

%build
gsoapversion=`soapcpp2 -v 2>&1 | grep C++ | sed 's/.* //'`

pushd lfc-mysql/%{name}-%{version}

./configure lfc --with-mysql \
	--libdir=%{_lib} \
	--with-gsoap-location=%{_prefix} \
	--with-gsoap-version=$gsoapversion \
	--with-voms-location=%{_prefix} \
	--with-id-map-file=%{_sysconfdir}/lcgdm-mapfile \
	--with-ns-config-file=%{_sysconfdir}/NSCONFIG \
	--with-sysconf-dir='$(prefix)/../etc'

make -f Makefile.ini Makefiles

make %{?_smp_mflags} prefix=%{_prefix}

popd

pushd lfc-postgres/%{name}-%{version}

./configure lfc --with-postgres \
	--libdir=%{_lib} \
	--with-gsoap-location=%{_prefix} \
	--with-gsoap-version=$gsoapversion \
	--with-voms-location=%{_prefix} \
	--with-id-map-file=%{_sysconfdir}/lcgdm-mapfile \
	--with-ns-config-file=%{_sysconfdir}/NSCONFIG \
	--with-sysconf-dir='$(prefix)/../etc'

# Disable building things already built above
sed -e 's/\(BuildDLI	*\)YES/\1NO/' \
    -e 's/\(BuildInterfaces	*\)YES/\1NO/' \
    -e 's/\(BuildNameServerClient	*\)YES/\1NO/' \
    -e 's/\(BuildNameServerLibrary	*\)YES/\1NO/' -i config/site.def
sed '/^\#define.*YES/d' -i config/Project.tmpl config/Library.tmpl
sed '/^SECURITYDIR =/d' -i config/Project.tmpl

make -f Makefile.ini Makefiles

pushd shlib
ln -s ../../../lfc-mysql/%{name}-%{version}/shlib/liblcgdm.so* .
ln -s ../../../lfc-mysql/%{name}-%{version}/shlib/liblfc.so* .
popd

make %{?_smp_mflags} prefix=%{_prefix}

popd

pushd dpm-mysql/%{name}-%{version}

./configure dpm --with-mysql \
	--libdir=%{_lib} \
	--with-gsoap-location=%{_prefix} \
	--with-gsoap-version=$gsoapversion \
	--with-voms-location=%{_prefix} \
	--with-dpm-config-file=%{_sysconfdir}/DPMCONFIG \
	--with-id-map-file=%{_sysconfdir}/lcgdm-mapfile \
	--with-ns-config-file=%{_sysconfdir}/DPNSCONFIG \
	--with-sysconf-dir='$(prefix)/../etc'

# Disable building things already built above
sed -e '/^SECURITYDIR =/d' -e '/^COMMONDIR =/d' -i config/Project.tmpl
sed -e 's/:.*(lcgdm).*/:/' -i lib/Imakefile
sed -e 's/:.*(lcgdm).*/:/' -i shlib/Imakefile

make -f Makefile.ini Makefiles

pushd shlib
ln -s ../../../lfc-mysql/%{name}-%{version}/shlib/liblcgdm.so* .
popd

make %{?_smp_mflags} prefix=%{_prefix}

popd

pushd dpm-postgres/%{name}-%{version}

./configure dpm --with-postgres \
	--libdir=%{_lib} \
	--with-gsoap-location=%{_prefix} \
	--with-gsoap-version=$gsoapversion \
	--with-voms-location=%{_prefix} \
	--with-dpm-config-file=%{_sysconfdir}/DPMCONFIG \
	--with-id-map-file=%{_sysconfdir}/lcgdm-mapfile \
	--with-ns-config-file=%{_sysconfdir}/DPNSCONFIG \
	--with-sysconf-dir='$(prefix)/../etc'

# Disable building things already built above
sed -e 's/\(BuildDPMClient	*\)YES/\1NO/' \
    -e 's/\(BuildInterfaces	*\)YES/\1NO/' \
    -e 's/\(BuildNameServerClient	*\)YES/\1NO/' \
    -e 's/\(BuildNameServerLibrary	*\)YES/\1NO/' \
    -e 's/\(BuildRfioClient	*\)YES/\1NO/' \
    -e 's/\(BuildRfioServer	*\)YES/\1NO/' -i config/site.def
sed '/^\#define.*YES/d' -i config/Project.tmpl config/Library.tmpl
sed '/^SECURITYDIR =/d' -i config/Project.tmpl

make -f Makefile.ini Makefiles

pushd shlib
ln -s ../../../lfc-mysql/%{name}-%{version}/shlib/liblcgdm.so* .
ln -s ../../../dpm-mysql/%{name}-%{version}/shlib/libdpm.so* .
popd

make %{?_smp_mflags} prefix=%{_prefix}

popd

%if %{?altpython:1}%{!?altpython:0}
mkdir %{altpython}
pushd %{altpython}

INCLUDE_PYTHON=`%{__altpython} \
    -c "from distutils import sysconfig; \
	import sys; \
	sys.stdout.write('-I' + sysconfig.get_python_inc(0))"`
PYTHON_LIB=`%{__altpython} \
    -c "from distutils import sysconfig; \
	import sys; \
	sys.stdout.write('-L' + sysconfig.get_config_var('LIBDEST') + \
	'/config -lpython' + sys.version[:3] + ' ' + \
	sysconfig.get_config_var('LIBS') + ' ' + \
	sysconfig.get_config_var('SYSLIBS'))"`

for module in lfc lfcthr lfc2 lfc2thr ; do

gcc %{optflags} -fno-strict-aliasing -fPIC -D_LARGEFILE64_SOURCE -Dlinux \
    -c -pthread -DCTHREAD_LINUX -D_THREAD_SAFE -D_REENTRANT \
    -I../lfc-mysql/%{name}-%{version}/h -DNSTYPE_LFC \
    ${INCLUDE_PYTHON} ../lfc-mysql/%{name}-%{version}/ns/${module}_wrap.c
gcc %{optflags} -fno-strict-aliasing -fPIC -D_LARGEFILE64_SOURCE -Dlinux \
    -shared -o _${module}.so ${module}_wrap.o ${PYTHON_LIB} \
    -L../lfc-mysql/%{name}-%{version}/shlib -llfc -llcgdm

done

for module in dpm dpm2 ; do

gcc %{optflags} -fno-strict-aliasing -fPIC -D_LARGEFILE64_SOURCE -Dlinux \
    -c -pthread -DCTHREAD_LINUX -D_THREAD_SAFE -D_REENTRANT \
    -I../dpm-mysql/%{name}-%{version}/h -DNSTYPE_DPNS \
    ${INCLUDE_PYTHON} ../dpm-mysql/%{name}-%{version}/dpm/${module}_wrap.c
gcc %{optflags} -fno-strict-aliasing -fPIC -D_LARGEFILE64_SOURCE -Dlinux \
    -shared -o _${module}.so ${module}_wrap.o ${PYTHON_LIB} \
    -L../dpm-mysql/%{name}-%{version}/shlib -ldpm -llcgdm

done

popd
%endif

%install
rm -rf ${RPM_BUILD_ROOT}

pushd lfc-mysql/%{name}-%{version}

make prefix=${RPM_BUILD_ROOT}%{_prefix} install
make prefix=${RPM_BUILD_ROOT}%{_prefix} install.man

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/lfc
mv ${RPM_BUILD_ROOT}%{_datadir}/LFC/* ${RPM_BUILD_ROOT}%{_datadir}/lfc
rmdir ${RPM_BUILD_ROOT}%{_datadir}/LFC

mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/lfc-mysql
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-mysql

# lfcdaemon startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!/opt/lcg/bin!/usr/sbin!g' -e 's!/opt/lcg!!g' \
    -e 's!\(/var/lock/subsys/\).*!\1lfc-mysql!' \
    ${RPM_BUILD_ROOT}%{_datadir}/lfc/rc.lfcdaemon > \
    ${RPM_BUILD_ROOT}%{_initrddir}/lfc-mysql
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/lfc-mysql
rm ${RPM_BUILD_ROOT}%{_datadir}/lfc/rc.lfcdaemon

# lfcdaemon configuration file
sed -e 's!/opt/lcg!!g' \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/lfcdaemon.conf.templ > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-mysql/lfcdaemon.conf
rm ${RPM_BUILD_ROOT}%{_sysconfdir}/lfcdaemon.conf.templ
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/lfcdaemon

# lfcdaemon log directory and log rotation configuration
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/log/lfc
install -m 644 -p ns/lfcdaemon.logrotate \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-mysql/lfcdaemon.logrotate
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/lfcdaemon

# lfcdaemon binary and man page
mv ${RPM_BUILD_ROOT}%{_bindir}/lfcdaemon \
   ${RPM_BUILD_ROOT}%{_libdir}/lfc-mysql/lfcdaemon
touch ${RPM_BUILD_ROOT}%{_sbindir}/lfcdaemon
chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/lfcdaemon
sed -e 's/\(\.TH [^ ]* \)1/\18/' \
    -e 's!/opt/lcg!!g' \
    -e 's/lfc-shutdown(1)/lfc-shutdown(8)/g' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/lfcdaemon.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/lfc-mysql/lfcdaemon.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/lfcdaemon.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/lfcdaemon.8

mv ${RPM_BUILD_ROOT}%{_sysconfdir}/NSCONFIG.templ \
   ${RPM_BUILD_ROOT}%{_libdir}/lfc-mysql/NSCONFIG.templ
touch ${RPM_BUILD_ROOT}%{_datadir}/lfc/NSCONFIG.templ

# lfc-shutdown binary and man page
mv ${RPM_BUILD_ROOT}%{_bindir}/lfc-shutdown \
   ${RPM_BUILD_ROOT}%{_libdir}/lfc-mysql/lfc-shutdown
touch ${RPM_BUILD_ROOT}%{_sbindir}/lfc-shutdown
chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/lfc-shutdown
sed -e 's/\(\.TH [^ ]* \)1/\18/' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/lfc-shutdown.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/lfc-mysql/lfc-shutdown.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/lfc-shutdown.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/lfc-shutdown.8

# lfc-dli startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!/opt/lcg/bin!/usr/sbin!g' -e 's!/opt/lcg!!g' \
    -e 's!/var/log/dli!/var/log/lfc-dli!g' \
    ${RPM_BUILD_ROOT}%{_datadir}/lfc/rc.lfc-dli > \
    ${RPM_BUILD_ROOT}%{_initrddir}/lfc-dli
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/lfc-dli
rm ${RPM_BUILD_ROOT}%{_datadir}/lfc/rc.lfc-dli

# lfc-dli configuration file
sed -e 's!/var/log/dli!/var/log/lfc-dli!g' \
    -e 's/\(LFC_HOST=\).*/\1`hostname -f`/' \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-dli.conf.templ > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/lfc-dli
rm ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-dli.conf.templ

# lfc-dli log directory and log rotation configuration
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/log/lfc-dli
sed -e 's!/var/log/dli!/var/log/lfc-dli!g' dli/lfc-dli.logrotate > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/lfc-dli

# lfc-dli binary and man page
mv ${RPM_BUILD_ROOT}%{_bindir}/lfc-dli ${RPM_BUILD_ROOT}%{_sbindir}/lfc-dli
sed -e 's/\(\.TH [^ ]* \)1/\18/' \
    -e 's!/var/log/dli!/var/log/lfc-dli!g' \
    -e 's/lfcdaemon(1)/lfcdaemon(8)/g' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/lfc-dli.1 > \
    ${RPM_BUILD_ROOT}%{_mandir}/man8/lfc-dli.8
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/lfc-dli.1

sed 's/\(^LFC_VERSION=\).*/\1%{version}/' scripts/lcg-info-provider-lfc > \
    ${RPM_BUILD_ROOT}%{_datadir}/lfc/lcg-info-provider-lfc 
chmod 755 ${RPM_BUILD_ROOT}%{_datadir}/lfc/lcg-info-provider-lfc 

# Move plugins out of the default library search path
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{name}
mv ${RPM_BUILD_ROOT}%{_libdir}/libCsec_plugin_* \
   ${RPM_BUILD_ROOT}%{_libdir}/%{name}

# Create lfc user home and certificate directories
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/lfc
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/grid-security/lfcmgr

# Remove due to name conflict
rm ${RPM_BUILD_ROOT}%{_mandir}/man3/log.3*

# Remove static libraries
rm ${RPM_BUILD_ROOT}%{_libdir}/liblfc.a
rm ${RPM_BUILD_ROOT}%{_libdir}/liblcgdm.a

# Turn off services by default
sed -e 's/\(chkconfig: \)\w*/\1-/' \
    -e '/Default-Start/d' \
    -e 's/\(Default-Stop: *\).*/\10 1 2 3 4 5 6/' \
    -i ${RPM_BUILD_ROOT}%{_initrddir}/lfc-mysql \
       ${RPM_BUILD_ROOT}%{_initrddir}/lfc-dli

popd

pushd lfc-postgres/%{name}-%{version}

make prefix=${RPM_BUILD_ROOT}%{_prefix} install
make prefix=${RPM_BUILD_ROOT}%{_prefix} install.man

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/lfc
mv ${RPM_BUILD_ROOT}%{_datadir}/LFC/* ${RPM_BUILD_ROOT}%{_datadir}/lfc
rmdir ${RPM_BUILD_ROOT}%{_datadir}/LFC

mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/lfc-postgres
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-postgres

# lfcdaemon startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!/opt/lcg/bin!/usr/sbin!g' -e 's!/opt/lcg!!g' \
    -e 's!\(/var/lock/subsys/\).*!\1lfc-postgres!' \
    ${RPM_BUILD_ROOT}%{_datadir}/lfc/rc.lfcdaemon > \
    ${RPM_BUILD_ROOT}%{_initrddir}/lfc-postgres
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/lfc-postgres
rm ${RPM_BUILD_ROOT}%{_datadir}/lfc/rc.lfcdaemon

# lfcdaemon configuration file
sed -e 's!/opt/lcg!!g' \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/lfcdaemon.conf.templ > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-postgres/lfcdaemon.conf
rm ${RPM_BUILD_ROOT}%{_sysconfdir}/lfcdaemon.conf.templ
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/lfcdaemon

# lfcdaemon log directory and log rotation configuration
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/log/lfc
install -m 644 -p ns/lfcdaemon.logrotate \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-postgres/lfcdaemon.logrotate
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/lfcdaemon

# lfcdaemon binary and man page
mv ${RPM_BUILD_ROOT}%{_bindir}/lfcdaemon \
   ${RPM_BUILD_ROOT}%{_libdir}/lfc-postgres/lfcdaemon
touch ${RPM_BUILD_ROOT}%{_sbindir}/lfcdaemon
chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/lfcdaemon
sed -e 's/\(\.TH [^ ]* \)1/\18/' \
    -e 's!/opt/lcg!!g' \
    -e 's/lfc-shutdown(1)/lfc-shutdown(8)/g' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/lfcdaemon.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/lfc-postgres/lfcdaemon.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/lfcdaemon.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/lfcdaemon.8

mv ${RPM_BUILD_ROOT}%{_sysconfdir}/NSCONFIG.templ \
   ${RPM_BUILD_ROOT}%{_libdir}/lfc-postgres/NSCONFIG.templ
touch ${RPM_BUILD_ROOT}%{_datadir}/lfc/NSCONFIG.templ

# lfc-shutdown binary and man page
mv ${RPM_BUILD_ROOT}%{_bindir}/lfc-shutdown \
   ${RPM_BUILD_ROOT}%{_libdir}/lfc-postgres/lfc-shutdown
touch ${RPM_BUILD_ROOT}%{_sbindir}/lfc-shutdown
chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/lfc-shutdown
sed -e 's/\(\.TH [^ ]* \)1/\18/' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/lfc-shutdown.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/lfc-postgres/lfc-shutdown.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/lfc-shutdown.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/lfc-shutdown.8

# Create lfc user home and certificate directories
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/lfc
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/grid-security/lfcmgr

# This doesn't quite work...
sed '/CREATE DATABASE/d' -i \
    ${RPM_BUILD_ROOT}%{_datadir}/lfc/create_lfc_tables_postgres.sql

# Turn off services by default
sed -e 's/\(chkconfig: \)\w*/\1-/' \
    -e '/Default-Start/d' \
    -e 's/\(Default-Stop: *\).*/\10 1 2 3 4 5 6/' \
    -i ${RPM_BUILD_ROOT}%{_initrddir}/lfc-postgres

popd

pushd dpm-mysql/%{name}-%{version}

make prefix=${RPM_BUILD_ROOT}%{_prefix} install
make prefix=${RPM_BUILD_ROOT}%{_prefix} install.man

sed 's!/usr/bin/env python!/usr/bin/python!' \
    -i ${RPM_BUILD_ROOT}%{_bindir}/dpm-listspaces

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/dpm
mv ${RPM_BUILD_ROOT}%{_datadir}/DPM/* ${RPM_BUILD_ROOT}%{_datadir}/dpm
rmdir ${RPM_BUILD_ROOT}%{_datadir}/DPM

mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql

# dpm startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!/opt/lcg/bin!/usr/sbin!g' -e 's!/opt/lcg!!g' \
    -e 's!\(/var/lock/subsys/\).*!\1dpm-mysql!' \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpm > \
    ${RPM_BUILD_ROOT}%{_initrddir}/dpm-mysql
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpm-mysql
rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpm

# dpm configuration file
sed -e 's!/opt/lcg!!g' \
    -e 's/\(^DPNS_HOST=\).*/\1`hostname -f`/' \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm.conf.templ > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpm.conf
rm ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm.conf.templ
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/dpm

# dpm log directory and log rotation configuration
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/log/dpm
install -m 644 -p dpm/dpm.logrotate \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpm.logrotate
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/dpm

# dpm binary and man page
mv ${RPM_BUILD_ROOT}%{_bindir}/dpm \
   ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpm
touch ${RPM_BUILD_ROOT}%{_sbindir}/dpm
chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/dpm
sed -e 's/\(\.TH [^ ]* \)1/\18/' \
    -e 's/dpm-shutdown(1)/dpm-shutdown(8)/g' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/dpm.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpm.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/dpm.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpm.8

mv ${RPM_BUILD_ROOT}%{_sysconfdir}/DPMCONFIG.templ \
   ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/DPMCONFIG.templ
touch ${RPM_BUILD_ROOT}%{_datadir}/dpm/DPMCONFIG.templ

# dpm-shutdown binary and man page
mv ${RPM_BUILD_ROOT}%{_bindir}/dpm-shutdown \
   ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpm-shutdown
touch ${RPM_BUILD_ROOT}%{_sbindir}/dpm-shutdown
chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/dpm-shutdown
sed -e 's/\(\.TH [^ ]* \)1/\18/' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/dpm-shutdown.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpm-shutdown.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/dpm-shutdown.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpm-shutdown.8

# dpnsdaemon startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!/opt/lcg/bin!/usr/sbin!g' -e 's!/opt/lcg!!g' \
    -e 's!\(/var/lock/subsys/\).*!\1dpm-mysql-nameserver!' \
    -e 's!/etc/NSCONFIG!/etc/DPNSCONFIG!g' \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpnsdaemon > \
    ${RPM_BUILD_ROOT}%{_initrddir}/dpm-mysql-nameserver
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpm-mysql-nameserver
rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpnsdaemon

# dpnsdaemon configuration file
sed -e 's!/opt/lcg!!g' \
    -e 's!/etc/NSCONFIG!/etc/DPNSCONFIG!g' \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpnsdaemon.conf.templ > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpnsdaemon.conf
rm ${RPM_BUILD_ROOT}%{_sysconfdir}/dpnsdaemon.conf.templ
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/dpnsdaemon

# dpnsdaemon log directory and log rotation configuration
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/log/dpns
install -m 644 -p ns/dpnsdaemon.logrotate \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpnsdaemon.logrotate
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/dpnsdaemon

# dpnsdaemon binary and man page
mv ${RPM_BUILD_ROOT}%{_bindir}/dpnsdaemon \
   ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpnsdaemon
touch ${RPM_BUILD_ROOT}%{_sbindir}/dpnsdaemon
chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/dpnsdaemon
sed -e 's/\(\.TH [^ ]* \)1/\18/' \
    -e 's!/opt/lcg!!g' \
    -e 's!/etc/NSCONFIG!/etc/DPNSCONFIG!g' \
    -e 's/dpns-shutdown(1)/dpns-shutdown(8)/g' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/dpnsdaemon.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpnsdaemon.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/dpnsdaemon.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpnsdaemon.8

mv ${RPM_BUILD_ROOT}%{_sysconfdir}/NSCONFIG.templ \
   ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/DPNSCONFIG.templ
touch ${RPM_BUILD_ROOT}%{_datadir}/dpm/DPNSCONFIG.templ

# dpns-shutdown binary and man page
mv ${RPM_BUILD_ROOT}%{_bindir}/dpns-shutdown \
   ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpns-shutdown
touch ${RPM_BUILD_ROOT}%{_sbindir}/dpns-shutdown
chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/dpns-shutdown
sed -e 's/\(\.TH [^ ]* \)1/\18/' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/dpns-shutdown.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpns-shutdown.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/dpns-shutdown.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpns-shutdown.8

# dpmcopyd startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!/opt/lcg/bin!/usr/sbin!g' -e 's!/opt/lcg!!g' \
    -e 's!\(/var/lock/subsys/\).*!\1dpm-mysql-copyd!' \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpmcopyd > \
    ${RPM_BUILD_ROOT}%{_initrddir}/dpm-mysql-copyd
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpm-mysql-copyd
rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpmcopyd

# dpmcopyd configuration file
sed -e 's!/opt/lcg!!g' \
    -e 's/\(^DPNS_HOST=\).*/\1`hostname -f`/' \
    -e 's/\(^DPM_HOST=\).*/\1`hostname -f`/' \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpmcopyd.conf.templ > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpmcopyd.conf
rm ${RPM_BUILD_ROOT}%{_sysconfdir}/dpmcopyd.conf.templ
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/dpmcopyd

# dpmcopyd log directory and log rotation configuration
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/log/dpmcopy
install -m 644 -p dpmcopy/dpmcopyd.logrotate \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpmcopyd.logrotate
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/dpmcopyd

# dpmcopyd binary and log file
mv ${RPM_BUILD_ROOT}%{_bindir}/dpmcopyd \
   ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpmcopyd
touch ${RPM_BUILD_ROOT}%{_sbindir}/dpmcopyd
chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/dpmcopyd
sed -e 's/\(\.TH [^ ]*\) 1/\1 8/' \
    -e 's!/opt/lcg/lib/!!g' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/dpmcopyd.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpmcopyd.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/dpmcopyd.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpmcopyd.8

for svc in srmv1 srmv2 srmv2.2 ; do
    ssvc=`tr -d '.' <<< ${svc}`
    # startup script
    sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
	-e '/LD_LIBRARY_PATH/d' \
	-e 's!/opt/lcg/bin!/usr/sbin!g' -e 's!/opt/lcg!!g' \
	-e "s/${svc}/dpm-${svc}/g" \
	-e "s!\(/var/lock/subsys/\).*!\1dpm-mysql-${ssvc}!" \
	${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.${svc} > \
	${RPM_BUILD_ROOT}%{_initrddir}/dpm-mysql-${ssvc}
    chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpm-mysql-${ssvc}
    rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.${svc}

    # configuration file
    sed -e "s/${svc}/dpm-${svc}/g" -e 's!/opt/lcg!!g' \
	-e 's/\(^DPNS_HOST=\).*/\1`hostname -f`/' \
	-e 's/\(^DPM_HOST=\).*/\1`hostname -f`/' \
	-e 's/\(^RUN_SRMV2DAEMON=\).*/\1"yes"/' \
	${RPM_BUILD_ROOT}%{_sysconfdir}/${svc}.conf.templ > \
	${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpm-${svc}.conf
    rm ${RPM_BUILD_ROOT}%{_sysconfdir}/${svc}.conf.templ
    touch ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/dpm-${svc}

    # log directory and log rotation configuration
    mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/log/dpm-${svc}
    sed -e "s/${svc}/dpm-${svc}/g" ${svc}/${svc}.logrotate > \
	${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpm-${svc}.logrotate
    touch ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/dpm-${svc}

    # binary and makefile
    mv ${RPM_BUILD_ROOT}%{_bindir}/${svc} \
       ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpm-${svc}
    touch ${RPM_BUILD_ROOT}%{_sbindir}/dpm-${svc}
    chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/dpm-${svc}
    sed -e 's/\.TH \([^ ]*\) 1/.TH DPM-\1 8/' \
	-e 's/dpm(1)/dpm(8)/g' \
	${RPM_BUILD_ROOT}%{_mandir}/man1/${svc}.1 | gzip -9 -n -c > \
	${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpm-${svc}.8.gz
    rm ${RPM_BUILD_ROOT}%{_mandir}/man1/${svc}.1
    touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpm-${svc}.8
done

# dpm-rfiod startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!/opt/lcg/bin!/usr/sbin!g' -e 's!/opt/lcg!!g' \
    -e 's/rfiod/dpm-rfiod/g' \
    -e 's!/var/log/rfio!/var/log/dpm-rfio!g' \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.rfiod > \
    ${RPM_BUILD_ROOT}%{_initrddir}/dpm-rfiod
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpm-rfiod
rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.rfiod

# dpm-rfiod configuration file
sed -e 's/rfiod/dpm-rfiod/g' -e 's!/opt/lcg!!g' \
    -e 's!/var/log/rfio!/var/log/dpm-rfio!g' \
    -e 's/\(^DPNS_HOST=\).*/\1`hostname -f`/' \
    -e 's/\(^DPM_HOST=\).*/\1`hostname -f`/' \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/rfiod.conf.templ > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/dpm-rfiod
rm ${RPM_BUILD_ROOT}%{_sysconfdir}/rfiod.conf.templ

# dpm-rfiod log directory and log rotation configuration
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/log/dpm-rfio
sed -e 's!/var/log/rfio!/var/log/dpm-rfio!g' rfio/rfiod.logrotate > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/dpm-rfiod

# dpm-rfiod binary and man page
mv ${RPM_BUILD_ROOT}%{_bindir}/rfiod \
   ${RPM_BUILD_ROOT}%{_sbindir}/dpm-rfiod
sed -e 's/\.TH \([^ ]* \)1/.TH DPM-\18/' \
    -e 's/rfiod/dpm-rfiod/g' \
    -e 's!/usr/local/bin!/usr/sbin!g' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/rfiod.1 > \
    ${RPM_BUILD_ROOT}%{_mandir}/man8/dpm-rfiod.8
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/rfiod.1

# Create dpm user home and certificate directories
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/dpm
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/grid-security/dpmmgr

# Remove static library
rm ${RPM_BUILD_ROOT}%{_libdir}/libdpm.a

# Turn off services by default
sed -e 's/\(chkconfig: \)\w*/\1-/' \
    -e '/Default-Start/d' \
    -e 's/\(Default-Stop: *\).*/\10 1 2 3 4 5 6/' \
    -i ${RPM_BUILD_ROOT}%{_initrddir}/dpm-mysql* \
       ${RPM_BUILD_ROOT}%{_initrddir}/dpm-rfiod

popd

pushd dpm-postgres/%{name}-%{version}

make prefix=${RPM_BUILD_ROOT}%{_prefix} install
make prefix=${RPM_BUILD_ROOT}%{_prefix} install.man

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/dpm
mv ${RPM_BUILD_ROOT}%{_datadir}/DPM/* ${RPM_BUILD_ROOT}%{_datadir}/dpm
rmdir ${RPM_BUILD_ROOT}%{_datadir}/DPM

mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres

# dpm startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!/opt/lcg/bin!/usr/sbin!g' -e 's!/opt/lcg!!g' \
    -e 's!\(/var/lock/subsys/\).*!\1dpm-postgres!' \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpm > \
    ${RPM_BUILD_ROOT}%{_initrddir}/dpm-postgres
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpm-postgres
rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpm

# dpm configuration file
sed -e 's!/opt/lcg!!g' \
    -e 's/\(^DPNS_HOST=\).*/\1`hostname -f`/' \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm.conf.templ > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpm.conf
rm ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm.conf.templ
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/dpm

# dpm log directory and log rotation configuration
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/log/dpm
install -m 644 -p dpm/dpm.logrotate \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpm.logrotate
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/dpm

# dpm binary and man page
mv ${RPM_BUILD_ROOT}%{_bindir}/dpm \
   ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/dpm
touch ${RPM_BUILD_ROOT}%{_sbindir}/dpm
chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/dpm
sed -e 's/\(\.TH [^ ]* \)1/\18/' \
    -e 's/dpm-shutdown(1)/dpm-shutdown(8)/g' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/dpm.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/dpm.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/dpm.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpm.8

mv ${RPM_BUILD_ROOT}%{_sysconfdir}/DPMCONFIG.templ \
   ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/DPMCONFIG.templ
touch ${RPM_BUILD_ROOT}%{_datadir}/dpm/DPMCONFIG.templ

# dpm-shutdown binary and man page
mv ${RPM_BUILD_ROOT}%{_bindir}/dpm-shutdown \
   ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/dpm-shutdown
touch ${RPM_BUILD_ROOT}%{_sbindir}/dpm-shutdown
chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/dpm-shutdown
sed -e 's/\(\.TH [^ ]* \)1/\18/' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/dpm-shutdown.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/dpm-shutdown.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/dpm-shutdown.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpm-shutdown.8

# dpnsdaemon startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!/opt/lcg/bin!/usr/sbin!g' -e 's!/opt/lcg!!g' \
    -e 's!\(/var/lock/subsys/\).*!\1dpm-postgres-nameserver!' \
    -e 's!/etc/NSCONFIG!/etc/DPNSCONFIG!g' \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpnsdaemon > \
    ${RPM_BUILD_ROOT}%{_initrddir}/dpm-postgres-nameserver
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpm-postgres-nameserver
rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpnsdaemon

# dpnsdaemon configuration file
sed -e 's!/opt/lcg!!g' \
    -e 's!/etc/NSCONFIG!/etc/DPNSCONFIG!g' \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpnsdaemon.conf.templ > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpnsdaemon.conf
rm ${RPM_BUILD_ROOT}%{_sysconfdir}/dpnsdaemon.conf.templ
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/dpnsdaemon

# dpnsdaemon log directory and log rotation configuration
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/log/dpns
install -m 644 -p ns/dpnsdaemon.logrotate \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpnsdaemon.logrotate
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/dpnsdaemon

# dpnsdaemon binary and man page
mv ${RPM_BUILD_ROOT}%{_bindir}/dpnsdaemon \
   ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/dpnsdaemon
touch ${RPM_BUILD_ROOT}%{_sbindir}/dpnsdaemon
chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/dpnsdaemon
sed -e 's/\(\.TH [^ ]* \)1/\18/' \
    -e 's!/opt/lcg!!g' \
    -e 's!/etc/NSCONFIG!/etc/DPNSCONFIG!g' \
    -e 's/dpns-shutdown(1)/dpns-shutdown(8)/g' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/dpnsdaemon.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/dpnsdaemon.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/dpnsdaemon.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpnsdaemon.8

mv ${RPM_BUILD_ROOT}%{_sysconfdir}/NSCONFIG.templ \
   ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/DPNSCONFIG.templ
touch ${RPM_BUILD_ROOT}%{_datadir}/dpm/DPNSCONFIG.templ

# dpns-shutdown binary and man page
mv ${RPM_BUILD_ROOT}%{_bindir}/dpns-shutdown \
   ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/dpns-shutdown
touch ${RPM_BUILD_ROOT}%{_sbindir}/dpns-shutdown
chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/dpns-shutdown
sed -e 's/\(\.TH [^ ]* \)1/\18/' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/dpns-shutdown.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/dpns-shutdown.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/dpns-shutdown.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpns-shutdown.8

# dpmcopyd startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!/opt/lcg/bin!/usr/sbin!g' -e 's!/opt/lcg!!g' \
    -e 's!\(/var/lock/subsys/\).*!\1dpm-postgres-copyd!' \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpmcopyd > \
    ${RPM_BUILD_ROOT}%{_initrddir}/dpm-postgres-copyd
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpm-postgres-copyd
rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpmcopyd

# dpmcopyd configuration file
sed -e 's!/opt/lcg!!g' \
    -e 's/\(^DPNS_HOST=\).*/\1`hostname -f`/' \
    -e 's/\(^DPM_HOST=\).*/\1`hostname -f`/' \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpmcopyd.conf.templ > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpmcopyd.conf
rm ${RPM_BUILD_ROOT}%{_sysconfdir}/dpmcopyd.conf.templ
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/dpmcopyd

# dpmcopyd log directory and log rotation configuration
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/log/dpmcopy
install -m 644 -p dpmcopy/dpmcopyd.logrotate \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpmcopyd.logrotate
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/dpmcopyd

# dpmcopyd binary and log file
mv ${RPM_BUILD_ROOT}%{_bindir}/dpmcopyd \
   ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/dpmcopyd
touch ${RPM_BUILD_ROOT}%{_sbindir}/dpmcopyd
chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/dpmcopyd
sed -e 's/\(\.TH [^ ]*\) 1/\1 8/' \
    -e 's!/opt/lcg/lib/!!g' \
    ${RPM_BUILD_ROOT}%{_mandir}/man1/dpmcopyd.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/dpmcopyd.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/dpmcopyd.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpmcopyd.8

for svc in srmv1 srmv2 srmv2.2 ; do
    ssvc=`tr -d '.' <<< ${svc}`
    # startup script
    sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
	-e '/LD_LIBRARY_PATH/d' \
	-e 's!/opt/lcg/bin!/usr/sbin!g' -e 's!/opt/lcg!!g' \
	-e "s/${svc}/dpm-${svc}/g" \
	-e "s!\(/var/lock/subsys/\).*!\1dpm-postgres-${ssvc}!" \
	${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.${svc} > \
	${RPM_BUILD_ROOT}%{_initrddir}/dpm-postgres-${ssvc}
    chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpm-postgres-${ssvc}
    rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.${svc}

    # configuration file
    sed -e "s/${svc}/dpm-${svc}/g" -e 's!/opt/lcg!!g' \
	-e 's/\(^DPNS_HOST=\).*/\1`hostname -f`/' \
	-e 's/\(^DPM_HOST=\).*/\1`hostname -f`/' \
	-e 's/\(^RUN_SRMV2DAEMON=\).*/\1"yes"/' \
	${RPM_BUILD_ROOT}%{_sysconfdir}/${svc}.conf.templ > \
	${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpm-${svc}.conf
    rm ${RPM_BUILD_ROOT}%{_sysconfdir}/${svc}.conf.templ
    touch ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/dpm-${svc}

    # log directory and log rotation configuration
    mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/log/dpm-${svc}
    sed -e "s/${svc}/dpm-${svc}/g" ${svc}/${svc}.logrotate > \
	${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpm-${svc}.logrotate
    touch ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/dpm-${svc}

    # binary and makefile
    mv ${RPM_BUILD_ROOT}%{_bindir}/${svc} \
       ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/dpm-${svc}
    touch ${RPM_BUILD_ROOT}%{_sbindir}/dpm-${svc}
    chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/dpm-${svc}
    sed -e 's/\.TH \([^ ]*\) 1/.TH DPM-\1 8/' \
	-e 's/dpm(1)/dpm(8)/g' \
	${RPM_BUILD_ROOT}%{_mandir}/man1/${svc}.1 | gzip -9 -n -c > \
	${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/dpm-${svc}.8.gz
    rm ${RPM_BUILD_ROOT}%{_mandir}/man1/${svc}.1
    touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpm-${svc}.8
done

# Create dpm user home and certificate directories
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/dpm
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/grid-security/dpmmgr

# This doesn't quite work...
sed '/CREATE DATABASE/d' -i \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/create_dpm_tables_postgres.sql \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/create_dpns_tables_postgres.sql

# Turn off services by default
sed -e 's/\(chkconfig: \)\w*/\1-/' \
    -e '/Default-Start/d' \
    -e 's/\(Default-Stop: *\).*/\10 1 2 3 4 5 6/' \
    -i ${RPM_BUILD_ROOT}%{_initrddir}/dpm-postgres*

popd

%if %{?altpython:1}%{!?altpython:0}
mkdir -p ${RPM_BUILD_ROOT}%{altpython_sitearch}
install -m 644 lfc-mysql/%{name}-%{version}/ns/*.py \
	       dpm-mysql/%{name}-%{version}/dpm/*.py \
	       ${RPM_BUILD_ROOT}%{altpython_sitearch}
install %{altpython}/*.so ${RPM_BUILD_ROOT}%{altpython_sitearch}
%endif

%if %{?fedora}%{!?fedora:0} < 5 && %{?rhel}%{!?rhel:0} < 6
%{__python}    -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT"'", 10, "%{python_sitearch}", 1)' > /dev/null
%{__python} -O -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT"'", 10, "%{python_sitearch}", 1)' > /dev/null
%if %{?altpython:1}%{!?altpython:0}
%{__altpython}    -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{altpython_sitearch}"'", 10, "%{altpython_sitearch}", 1)' > /dev/null
%{__altpython} -O -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{altpython_sitearch}"'", 10, "%{altpython_sitearch}", 1)' > /dev/null
%endif
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n lfc -p /sbin/ldconfig

%postun -n lfc -p /sbin/ldconfig

%post -n dpm -p /sbin/ldconfig

%postun -n dpm -p /sbin/ldconfig

%pre -n lfc-mysql
getent group lfcmgr > /dev/null || groupadd -r lfcmgr
getent passwd lfcmgr > /dev/null || useradd -r -g lfcmgr \
    -d %{_localstatedir}/lib/lfc -s /bin/bash -c "LFC Manager" lfcmgr
exit 0

%post -n lfc-mysql
updatelfc () {
    [ -r /etc/sysconfig/lfcdaemon ] && . /etc/sysconfig/lfcdaemon
    [ -z "$NSCONFIGFILE" ] && NSCONFIGFILE=/etc/NSCONFIG
    [ -r $NSCONFIGFILE ] || return 0

    nscfg=$(cat $NSCONFIGFILE)

    cfg1=$(echo $nscfg | cut -f1 -d@)
    cfg2=$(echo $nscfg | cut -f2 -d@ -s)

    user=$(echo $cfg1 | cut -f1 -d/)
    passwd=$(echo $cfg1 | cut -f2 -d/ -s)
    host=$(echo $cfg2 | cut -f1 -d/)
    db=$(echo $cfg2 | cut -f2 -d/ -s)

    [ -z "$user" ] && return 0
    [ -z "$passwd" ] && return 0
    [ -z "$host" ] && return 0
    [ -z "$db" ] && db=cns_db

    mycfg=$(mktemp)
    cat > $mycfg <<-EOF
	[client]
	user=$user
	password=$passwd
	EOF

    mysql="mysql --defaults-file=$mycfg --skip-column-names $db"

    vmajor=$($mysql -e "select major from schema_version" 2>/dev/null)
    vminor=$($mysql -e "select minor from schema_version" 2>/dev/null)
    vpatch=$($mysql -e "select patch from schema_version" 2>/dev/null)

    if [ -z "$vmajor" -o -z "$vminor" -o -z "$vpatch" ] ; then
	rm $mycfg
	return 0
    fi

    if [ $vmajor -eq 3 -a $vminor -eq 0 -a $vpatch -eq 0 ] ; then
	$mysql <<-EOF
	ALTER TABLE Cns_groupinfo ADD banned INTEGER;
	ALTER TABLE Cns_userinfo ADD user_ca VARCHAR(255) BINARY;
	ALTER TABLE Cns_userinfo ADD banned INTEGER;
	CREATE INDEX linkname_idx ON Cns_symlinks(linkname(255));
	UPDATE schema_version SET major = 3, minor = 1, patch = 0;
	EOF
    fi

    rm $mycfg
    return 0
}

updatelfc

if [ $1 = 1 ]; then
    /sbin/chkconfig --add lfc-mysql
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/lfcdaemon lfcdaemon \
	  %{_libdir}/lfc-mysql/lfcdaemon 20 \
  --slave %{_mandir}/man8/lfcdaemon.8.gz lfcdaemon.8.gz \
	  %{_libdir}/lfc-mysql/lfcdaemon.8.gz \
  --slave %{_datadir}/lfc/NSCONFIG.templ NSCONFIG.templ \
	  %{_libdir}/lfc-mysql/NSCONFIG.templ \
  --slave %{_sysconfdir}/sysconfig/lfcdaemon lfcdaemon.conf \
	  %{_sysconfdir}/lfc-mysql/lfcdaemon.conf \
  --slave %{_sysconfdir}/logrotate.d/lfcdaemon lfcdaemon.logrotate \
	  %{_sysconfdir}/lfc-mysql/lfcdaemon.logrotate \
  --slave %{_sbindir}/lfc-shutdown lfc-shutdown \
	  %{_libdir}/lfc-mysql/lfc-shutdown \
  --slave %{_mandir}/man8/lfc-shutdown.8.gz lfc-shutdown.8.gz \
	  %{_libdir}/lfc-mysql/lfc-shutdown.8.gz \
  --initscript lfc-mysql

%preun -n lfc-mysql
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display lfcdaemon | \
	grep currently | grep -q lfc-mysql && \
	/sbin/service lfc-mysql stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove lfcdaemon \
	%{_libdir}/lfc-mysql/lfcdaemon
    /sbin/chkconfig --del lfc-mysql
fi

%postun -n lfc-mysql
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display lfcdaemon | \
	grep currently | grep -q lfc-mysql && \
	/sbin/service lfc-mysql condrestart > /dev/null 2>&1 || :
fi

%post -n lfc-dli
if [ $1 = 1 ]; then
    /sbin/chkconfig --add lfc-dli
fi

%preun -n lfc-dli
if [ $1 = 0 ]; then
    /sbin/service lfc-dli stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del lfc-dli
fi

%postun -n lfc-dli
if [ $1 -ge 1 ]; then
    /sbin/service lfc-dli condrestart > /dev/null 2>&1 || :
fi

%pre -n lfc-postgres
getent group lfcmgr > /dev/null || groupadd -r lfcmgr
getent passwd lfcmgr > /dev/null || useradd -r -g lfcmgr \
    -d %{_localstatedir}/lib/lfc -s /bin/bash -c "LFC Manager" lfcmgr
exit 0

%post -n lfc-postgres
updatelfc () {
    [ -r /etc/sysconfig/lfcdaemon ] && . /etc/sysconfig/lfcdaemon
    [ -z "$NSCONFIGFILE" ] && NSCONFIGFILE=/etc/NSCONFIG
    [ -r $NSCONFIGFILE ] || return 0

    nscfg=$(cat $NSCONFIGFILE)

    cfg1=$(echo $nscfg | cut -f1 -d@)
    cfg2=$(echo $nscfg | cut -f2 -d@ -s)

    user=$(echo $cfg1 | cut -f1 -d/)
    passwd=$(echo $cfg1 | cut -f2 -d/ -s)
    host=$(echo $cfg2 | cut -f1 -d/)
    db=$(echo $cfg2 | cut -f2 -d/ -s)

    [ -z "$user" ] && return 0
    [ -z "$passwd" ] && return 0
    [ -z "$host" ] && return 0
    [ -z "$db" ] && db=cns_db

    export PGPASSWORD=$passwd
    psql="psql -t -q -U $user $db"

    vmajor=$($psql -c "select major from schema_version" 2>/dev/null)
    vminor=$($psql -c "select minor from schema_version" 2>/dev/null)
    vpatch=$($psql -c "select patch from schema_version" 2>/dev/null)

    if [ -z "$vmajor" -o -z "$vminor" -o -z "$vpatch" ] ; then
	return 0
    fi

    if [ $vmajor -eq 3 -a $vminor -eq 0 -a $vpatch -eq 0 ] ; then
	$psql <<-EOF
	ALTER TABLE Cns_groupinfo ADD banned INTEGER;
	ALTER TABLE Cns_userinfo ADD user_ca VARCHAR(255);
	ALTER TABLE Cns_userinfo ADD banned INTEGER;
	CREATE INDEX linkname_idx ON Cns_symlinks(linkname);
	UPDATE schema_version SET major = 3, minor = 1, patch = 0;
	EOF
    fi

    return 0
}

updatelfc

if [ $1 = 1 ]; then
    /sbin/chkconfig --add lfc-postgres
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/lfcdaemon lfcdaemon \
	  %{_libdir}/lfc-postgres/lfcdaemon 10 \
  --slave %{_mandir}/man8/lfcdaemon.8.gz lfcdaemon.8.gz \
	  %{_libdir}/lfc-postgres/lfcdaemon.8.gz \
  --slave %{_datadir}/lfc/NSCONFIG.templ NSCONFIG.templ \
	  %{_libdir}/lfc-postgres/NSCONFIG.templ \
  --slave %{_sysconfdir}/sysconfig/lfcdaemon lfcdaemon.conf \
	  %{_sysconfdir}/lfc-postgres/lfcdaemon.conf \
  --slave %{_sysconfdir}/logrotate.d/lfcdaemon lfcdaemon.logrotate \
	  %{_sysconfdir}/lfc-postgres/lfcdaemon.logrotate \
  --slave %{_sbindir}/lfc-shutdown lfc-shutdown \
	  %{_libdir}/lfc-postgres/lfc-shutdown \
  --slave %{_mandir}/man8/lfc-shutdown.8.gz lfc-shutdown.8.gz \
	  %{_libdir}/lfc-postgres/lfc-shutdown.8.gz \
  --initscript lfc-postgres

%preun -n lfc-postgres
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display lfcdaemon | \
	grep currently | grep -q lfc-postgres && \
	/sbin/service lfc-postgres stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove lfcdaemon \
	%{_libdir}/lfc-postgres/lfcdaemon
    /sbin/chkconfig --del lfc-postgres
fi

%postun -n lfc-postgres
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display lfcdaemon | \
	grep currently | grep -q lfc-postgres && \
	/sbin/service lfc-postgres condrestart > /dev/null 2>&1 || :
fi

%pre -n dpm-mysql
getent group dpmmgr > /dev/null || groupadd -r dpmmgr
getent passwd dpmmgr > /dev/null || useradd -r -g dpmmgr \
    -d %{_localstatedir}/lib/dpm -s /bin/bash -c "DPM Manager" dpmmgr
exit 0

%post -n dpm-mysql
if [ $1 = 1 ]; then
    /sbin/chkconfig --add dpm-mysql
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm dpm \
	  %{_libdir}/dpm-mysql/dpm 20 \
  --slave %{_mandir}/man8/dpm.8.gz dpm.8.gz \
	  %{_libdir}/dpm-mysql/dpm.8.gz \
  --slave %{_datadir}/dpm/DPMCONFIG.templ DPMCONFIG.templ \
	  %{_libdir}/dpm-mysql/DPMCONFIG.templ \
  --slave %{_sysconfdir}/sysconfig/dpm dpm.conf \
	  %{_sysconfdir}/dpm-mysql/dpm.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm dpm.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpm.logrotate \
  --slave %{_sbindir}/dpm-shutdown dpm-shutdown \
	  %{_libdir}/dpm-mysql/dpm-shutdown \
  --slave %{_mandir}/man8/dpm-shutdown.8.gz dpm-shutdown.8.gz \
	  %{_libdir}/dpm-mysql/dpm-shutdown.8.gz \
  --initscript dpm-mysql

%preun -n dpm-mysql
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpm | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-mysql stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm \
	%{_libdir}/dpm-mysql/dpm
    /sbin/chkconfig --del dpm-mysql
fi

%postun -n dpm-mysql
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpm | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-mysql condrestart > /dev/null 2>&1 || :
fi

%post -n dpm-mysql-nameserver
updatedpns () {
    [ -r /etc/sysconfig/dpnsdaemon ] && . /etc/sysconfig/dpnsdaemon
    [ -z "$NSCONFIGFILE" ] && NSCONFIGFILE=/etc/DPNSCONFIG
    [ -r $NSCONFIGFILE ] || return 0

    nscfg=$(cat $NSCONFIGFILE)

    cfg1=$(echo $nscfg | cut -f1 -d@)
    cfg2=$(echo $nscfg | cut -f2 -d@ -s)

    user=$(echo $cfg1 | cut -f1 -d/)
    passwd=$(echo $cfg1 | cut -f2 -d/ -s)
    host=$(echo $cfg2 | cut -f1 -d/)
    db=$(echo $cfg2 | cut -f2 -d/ -s)

    [ -z "$user" ] && return 0
    [ -z "$passwd" ] && return 0
    [ -z "$host" ] && return 0
    [ -z "$db" ] && db=cns_db

    mycfg=$(mktemp)
    cat > $mycfg <<-EOF
	[client]
	user=$user
	password=$passwd
	EOF

    mysql="mysql --defaults-file=$mycfg --skip-column-names $db"

    vmajor=$($mysql -e "select major from schema_version" 2>/dev/null)
    vminor=$($mysql -e "select minor from schema_version" 2>/dev/null)
    vpatch=$($mysql -e "select patch from schema_version" 2>/dev/null)

    if [ -z "$vmajor" -o -z "$vminor" -o -z "$vpatch" ] ; then
	rm $mycfg
	return 0
    fi

    if [ $vmajor -eq 3 -a $vminor -eq 0 -a $vpatch -eq 0 ] ; then
	$mysql <<-EOF
	ALTER TABLE Cns_groupinfo ADD banned INTEGER;
	ALTER TABLE Cns_userinfo ADD user_ca VARCHAR(255) BINARY;
	ALTER TABLE Cns_userinfo ADD banned INTEGER;
	CREATE INDEX linkname_idx ON Cns_symlinks(linkname(255));
	UPDATE schema_version SET major = 3, minor = 1, patch = 0;
	EOF
    fi

    rm $mycfg
    return 0
}

updatedpns

if [ $1 = 1 ]; then
    /sbin/chkconfig --add dpm-mysql-nameserver
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/dpnsdaemon dpnsdaemon \
	  %{_libdir}/dpm-mysql/dpnsdaemon 20 \
  --slave %{_mandir}/man8/dpnsdaemon.8.gz dpnsdaemon.8.gz \
	  %{_libdir}/dpm-mysql/dpnsdaemon.8.gz \
  --slave %{_datadir}/dpm/DPNSCONFIG.templ DPNSCONFIG.templ \
	  %{_libdir}/dpm-mysql/DPNSCONFIG.templ \
  --slave %{_sysconfdir}/sysconfig/dpnsdaemon dpnsdaemon.conf \
	  %{_sysconfdir}/dpm-mysql/dpnsdaemon.conf \
  --slave %{_sysconfdir}/logrotate.d/dpnsdaemon dpnsdaemon.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpnsdaemon.logrotate \
  --slave %{_sbindir}/dpns-shutdown dpns-shutdown \
	  %{_libdir}/dpm-mysql/dpns-shutdown \
  --slave %{_mandir}/man8/dpns-shutdown.8.gz dpns-shutdown.8.gz \
	  %{_libdir}/dpm-mysql/dpns-shutdown.8.gz \
  --initscript dpm-mysql-nameserver

%preun -n dpm-mysql-nameserver
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpnsdaemon | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-mysql-nameserver stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpnsdaemon \
	%{_libdir}/dpm-mysql/dpnsdaemon
    /sbin/chkconfig --del dpm-mysql-nameserver
fi

%postun -n dpm-mysql-nameserver
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpnsdaemon | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-mysql-nameserver condrestart > /dev/null 2>&1 || :
fi

%post -n dpm-mysql-copyd
if [ $1 = 1 ]; then
    /sbin/chkconfig --add dpm-mysql-copyd
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/dpmcopyd dpmcopyd \
	  %{_libdir}/dpm-mysql/dpmcopyd 20 \
  --slave %{_mandir}/man8/dpmcopyd.8.gz dpmcopyd.8.gz \
	  %{_libdir}/dpm-mysql/dpmcopyd.8.gz \
  --slave %{_sysconfdir}/sysconfig/dpmcopyd dpmcopyd.conf \
	  %{_sysconfdir}/dpm-mysql/dpmcopyd.conf \
  --slave %{_sysconfdir}/logrotate.d/dpmcopyd dpmcopyd.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpmcopyd.logrotate \
  --initscript dpm-mysql-copyd

%preun -n dpm-mysql-copyd
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpmcopyd | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-mysql-copyd stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpmcopyd \
	%{_libdir}/dpm-mysql/dpmcopyd
    /sbin/chkconfig --del dpm-mysql-copyd
fi

%postun -n dpm-mysql-copyd
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpmcopyd | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-mysql-copyd condrestart > /dev/null 2>&1 || :
fi

%post -n dpm-mysql-srmv1
if [ $1 = 1 ]; then
    /sbin/chkconfig --add dpm-mysql-srmv1
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv1 dpm-srmv1 \
	  %{_libdir}/dpm-mysql/dpm-srmv1 20 \
  --slave %{_mandir}/man8/dpm-srmv1.8.gz dpm-srmv1.8.gz \
	  %{_libdir}/dpm-mysql/dpm-srmv1.8.gz \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv1 dpm-srmv1.conf \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv1.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv1 dpm-srmv1.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv1.logrotate \
  --initscript dpm-mysql-srmv1

%preun -n dpm-mysql-srmv1
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv1 | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-mysql-srmv1 stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm-srmv1 \
	%{_libdir}/dpm-mysql/dpm-srmv1
    /sbin/chkconfig --del dpm-mysql-srmv1
fi

%postun -n dpm-mysql-srmv1
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv1 | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-mysql-srmv1 condrestart > /dev/null 2>&1 || :
fi

%post -n dpm-mysql-srmv2
if [ $1 = 1 ]; then
    /sbin/chkconfig --add dpm-mysql-srmv2
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv2 dpm-srmv2 \
	  %{_libdir}/dpm-mysql/dpm-srmv2 20 \
  --slave %{_mandir}/man8/dpm-srmv2.8.gz dpm-srmv2.8.gz \
	  %{_libdir}/dpm-mysql/dpm-srmv2.8.gz \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv2 dpm-srmv2.conf \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv2 dpm-srmv2.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.logrotate \
  --initscript dpm-mysql-srmv2

%preun -n dpm-mysql-srmv2
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv2 | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-mysql-srmv2 stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm-srmv2 \
	%{_libdir}/dpm-mysql/dpm-srmv2
    /sbin/chkconfig --del dpm-mysql-srmv2
fi

%postun -n dpm-mysql-srmv2
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv2 | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-mysql-srmv2 condrestart > /dev/null 2>&1 || :
fi

%post -n dpm-mysql-srmv22
if [ $1 = 1 ]; then
    /sbin/chkconfig --add dpm-mysql-srmv22
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv2.2 dpm-srmv2.2 \
	  %{_libdir}/dpm-mysql/dpm-srmv2.2 20 \
  --slave %{_mandir}/man8/dpm-srmv2.2.8.gz dpm-srmv2.2.8.gz \
	  %{_libdir}/dpm-mysql/dpm-srmv2.2.8.gz \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv2.2 dpm-srmv2.2.conf \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.2.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv2.2 dpm-srmv2.2.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.2.logrotate \
  --initscript dpm-mysql-srmv22

%preun -n dpm-mysql-srmv22
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv2.2 | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-mysql-srmv22 stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm-srmv2.2 \
	%{_libdir}/dpm-mysql/dpm-srmv2.2
    /sbin/chkconfig --del dpm-mysql-srmv22
fi

%postun -n dpm-mysql-srmv22
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv2.2 | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-mysql-srmv22 condrestart > /dev/null 2>&1 || :
fi

%post -n dpm-rfiod
if [ $1 = 1 ]; then
    /sbin/chkconfig --add dpm-rfiod
fi

%preun -n dpm-rfiod
if [ $1 = 0 ]; then
    /sbin/service dpm-rfiod stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del dpm-rfiod
fi

%postun -n dpm-rfiod
if [ $1 -ge 1 ]; then
    /sbin/service dpm-rfiod condrestart > /dev/null 2>&1 || :
fi


%pre -n dpm-postgres
getent group dpmmgr > /dev/null || groupadd -r dpmmgr
getent passwd dpmmgr > /dev/null || useradd -r -g dpmmgr \
    -d %{_localstatedir}/lib/dpm -s /bin/bash -c "DPM Manager" dpmmgr
exit 0

%post -n dpm-postgres
if [ $1 = 1 ]; then
    /sbin/chkconfig --add dpm-postgres
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm dpm \
	  %{_libdir}/dpm-postgres/dpm 10 \
  --slave %{_mandir}/man8/dpm.8.gz dpm.8.gz \
	  %{_libdir}/dpm-postgres/dpm.8.gz \
  --slave %{_datadir}/dpm/DPMCONFIG.templ DPMCONFIG.templ \
	  %{_libdir}/dpm-postgres/DPMCONFIG.templ \
  --slave %{_sysconfdir}/sysconfig/dpm dpm.conf \
	  %{_sysconfdir}/dpm-postgres/dpm.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm dpm.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpm.logrotate \
  --slave %{_sbindir}/dpm-shutdown dpm-shutdown \
	  %{_libdir}/dpm-postgres/dpm-shutdown \
  --slave %{_mandir}/man8/dpm-shutdown.8.gz dpm-shutdown.8.gz \
	  %{_libdir}/dpm-postgres/dpm-shutdown.8.gz \
  --initscript dpm-postgres

%preun -n dpm-postgres
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpm | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-postgres stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm \
	%{_libdir}/dpm-postgres/dpm
    /sbin/chkconfig --del dpm-postgres
fi

%postun -n dpm-postgres
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpm | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-postgres condrestart > /dev/null 2>&1 || :
fi

%post -n dpm-postgres-nameserver
updatedpns () {
    [ -r /etc/sysconfig/dpnsdaemon ] && . /etc/sysconfig/dpnsdaemon
    [ -z "$NSCONFIGFILE" ] && NSCONFIGFILE=/etc/DPNSCONFIG
    [ -r $NSCONFIGFILE ] || return 0

    nscfg=$(cat $NSCONFIGFILE)

    cfg1=$(echo $nscfg | cut -f1 -d@)
    cfg2=$(echo $nscfg | cut -f2 -d@ -s)

    user=$(echo $cfg1 | cut -f1 -d/)
    passwd=$(echo $cfg1 | cut -f2 -d/ -s)
    host=$(echo $cfg2 | cut -f1 -d/)
    db=$(echo $cfg2 | cut -f2 -d/ -s)

    [ -z "$user" ] && return 0
    [ -z "$passwd" ] && return 0
    [ -z "$host" ] && return 0
    [ -z "$db" ] && db=cns_db

    export PGPASSWORD=$passwd
    psql="psql -t -q -U $user $db"

    vmajor=$($psql -c "select major from schema_version" 2>/dev/null)
    vminor=$($psql -c "select minor from schema_version" 2>/dev/null)
    vpatch=$($psql -c "select patch from schema_version" 2>/dev/null)

    if [ -z "$vmajor" -o -z "$vminor" -o -z "$vpatch" ] ; then
	return 0
    fi

    if [ $vmajor -eq 3 -a $vminor -eq 0 -a $vpatch -eq 0 ] ; then
	$psql <<-EOF
	ALTER TABLE Cns_groupinfo ADD banned INTEGER;
	ALTER TABLE Cns_userinfo ADD user_ca VARCHAR(255);
	ALTER TABLE Cns_userinfo ADD banned INTEGER;
	CREATE INDEX linkname_idx ON Cns_symlinks(linkname);
	UPDATE schema_version SET major = 3, minor = 1, patch = 0;
	EOF
    fi

    return 0
}

updatedpns

if [ $1 = 1 ]; then
    /sbin/chkconfig --add dpm-postgres-nameserver
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/dpnsdaemon dpnsdaemon \
	  %{_libdir}/dpm-postgres/dpnsdaemon 10 \
  --slave %{_mandir}/man8/dpnsdaemon.8.gz dpnsdaemon.8.gz \
	  %{_libdir}/dpm-postgres/dpnsdaemon.8.gz \
  --slave %{_datadir}/dpm/DPNSCONFIG.templ DPNSCONFIG.templ \
	  %{_libdir}/dpm-postgres/DPNSCONFIG.templ \
  --slave %{_sysconfdir}/sysconfig/dpnsdaemon dpnsdaemon.conf \
	  %{_sysconfdir}/dpm-postgres/dpnsdaemon.conf \
  --slave %{_sysconfdir}/logrotate.d/dpnsdaemon dpnsdaemon.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpnsdaemon.logrotate \
  --slave %{_sbindir}/dpns-shutdown dpns-shutdown \
	  %{_libdir}/dpm-postgres/dpns-shutdown \
  --slave %{_mandir}/man8/dpns-shutdown.8.gz dpns-shutdown.8.gz \
	  %{_libdir}/dpm-postgres/dpns-shutdown.8.gz \
  --initscript dpm-postgres-nameserver

%preun -n dpm-postgres-nameserver
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpnsdaemon | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-postgres-nameserver stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpnsdaemon \
	%{_libdir}/dpm-postgres/dpnsdaemon
    /sbin/chkconfig --del dpm-postgres-nameserver
fi

%postun -n dpm-postgres-nameserver
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpnsdaemon | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-postgres-nameserver condrestart > /dev/null 2>&1 || :
fi

%post -n dpm-postgres-copyd
if [ $1 = 1 ]; then
    /sbin/chkconfig --add dpm-postgres-copyd
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/dpmcopyd dpmcopyd \
	  %{_libdir}/dpm-postgres/dpmcopyd 10 \
  --slave %{_mandir}/man8/dpmcopyd.8.gz dpmcopyd.8.gz \
	  %{_libdir}/dpm-postgres/dpmcopyd.8.gz \
  --slave %{_sysconfdir}/sysconfig/dpmcopyd dpmcopyd.conf \
	  %{_sysconfdir}/dpm-postgres/dpmcopyd.conf \
  --slave %{_sysconfdir}/logrotate.d/dpmcopyd dpmcopyd.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpmcopyd.logrotate \
  --initscript dpm-postgres-copyd

%preun -n dpm-postgres-copyd
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpmcopyd | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-postgres-copyd stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpmcopyd \
	%{_libdir}/dpm-postgres/dpmcopyd
    /sbin/chkconfig --del dpm-postgres-copyd
fi

%postun -n dpm-postgres-copyd
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpmcopyd | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-postgres-copyd condrestart > /dev/null 2>&1 || :
fi

%post -n dpm-postgres-srmv1
if [ $1 = 1 ]; then
    /sbin/chkconfig --add dpm-postgres-srmv1
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv1 dpm-srmv1 \
	  %{_libdir}/dpm-postgres/dpm-srmv1 10 \
  --slave %{_mandir}/man8/dpm-srmv1.8.gz dpm-srmv1.8.gz \
	  %{_libdir}/dpm-postgres/dpm-srmv1.8.gz \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv1 dpm-srmv1.conf \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv1.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv1 dpm-srmv1.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv1.logrotate \
  --initscript dpm-postgres-srmv1

%preun -n dpm-postgres-srmv1
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv1 | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-postgres-srmv1 stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm-srmv1 \
	%{_libdir}/dpm-postgres/dpm-srmv1
    /sbin/chkconfig --del dpm-postgres-srmv1
fi

%postun -n dpm-postgres-srmv1
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv1 | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-postgres-srmv1 condrestart > /dev/null 2>&1 || :
fi

%post -n dpm-postgres-srmv2
if [ $1 = 1 ]; then
    /sbin/chkconfig --add dpm-postgres-srmv2
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv2 dpm-srmv2 \
	  %{_libdir}/dpm-postgres/dpm-srmv2 10 \
  --slave %{_mandir}/man8/dpm-srmv2.8.gz dpm-srmv2.8.gz \
	  %{_libdir}/dpm-postgres/dpm-srmv2.8.gz \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv2 dpm-srmv2.conf \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv2 dpm-srmv2.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.logrotate \
  --initscript dpm-postgres-srmv2

%preun -n dpm-postgres-srmv2
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv2 | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-postgres-srmv2 stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm-srmv2 \
	%{_libdir}/dpm-postgres/dpm-srmv2
    /sbin/chkconfig --del dpm-postgres-srmv2
fi

%postun -n dpm-postgres-srmv2
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv2 | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-postgres-srmv2 condrestart > /dev/null 2>&1 || :
fi

%post -n dpm-postgres-srmv22
if [ $1 = 1 ]; then
    /sbin/chkconfig --add dpm-postgres-srmv22
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv2.2 dpm-srmv2.2 \
	  %{_libdir}/dpm-postgres/dpm-srmv2.2 10 \
  --slave %{_mandir}/man8/dpm-srmv2.2.8.gz dpm-srmv2.2.8.gz \
	  %{_libdir}/dpm-postgres/dpm-srmv2.2.8.gz \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv2.2 dpm-srmv2.2.conf \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.2.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv2.2 dpm-srmv2.2.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.2.logrotate \
  --initscript dpm-postgres-srmv22

%preun -n dpm-postgres-srmv22
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv2.2 | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-postgres-srmv22 stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm-srmv2.2 \
	%{_libdir}/dpm-postgres/dpm-srmv2.2
    /sbin/chkconfig --del dpm-postgres-srmv22
fi

%postun -n dpm-postgres-srmv22
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv2.2 | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-postgres-srmv22 condrestart > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%{_libdir}/liblcgdm.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libCsec_plugin_GSI.so
%{_libdir}/%{name}/libCsec_plugin_GSI_thread.so
%{_libdir}/%{name}/libCsec_plugin_ID.so
%doc lfc-mysql/%{name}-%{version}/LICENSE

%files devel
%defattr(-,root,root,-)
%{_libdir}/liblcgdm.so
%doc %{_mandir}/man3/C*.3*
%doc %{_mandir}/man3/getconfent.3*
%doc %{_mandir}/man3/netclose.3*
%doc %{_mandir}/man3/netread.3*
%doc %{_mandir}/man3/netwrite.3*
%doc %{_mandir}/man3/serrno.3*
%doc %{_mandir}/man4/Castor_limits.4*

%files -n lfc
%defattr(-,root,root,-)
%{_libdir}/liblfc.so.*
%doc lfc-mysql/%{name}-%{version}/doc/lfc/README

%files -n lfc-devel
%defattr(-,root,root,-)
%{_includedir}/lfc
%{_libdir}/liblfc.so
%doc %{_mandir}/man3/lfc_[a-o]*.3*
%doc %{_mandir}/man3/lfc_ping.3*
%doc %{_mandir}/man3/lfc_[q-z]*.3*

%files -n lfc-client
%defattr(-,root,root,-)
%{_bindir}/lfc-*
%doc %{_mandir}/man1/lfc-*

%files -n lfc-perl
%defattr(-,root,root,-)
%{perl_vendorarch}/lfc.so
%{perl_vendorarch}/lfc.pm
%doc %{_mandir}/man3/lfc_perl.3*

%files -n lfc-python
%defattr(-,root,root,-)
%{python_sitearch}/_lfc.so
%{python_sitearch}/lfc.py*
%{python_sitearch}/_lfcthr.so
%{python_sitearch}/lfcthr.py*
%{python_sitearch}/_lfc2.so
%{python_sitearch}/lfc2.py*
%{python_sitearch}/_lfc2thr.so
%{python_sitearch}/lfc2thr.py*
%doc %{_mandir}/man3/lfc_python.3*
%doc %{_mandir}/man3/lfc2_python.3*

%if %{?altpython:1}%{!?altpython:0}
%files -n lfc-%{altpython}
%defattr(-,root,root,-)
%{altpython_sitearch}/_lfc.so
%{altpython_sitearch}/lfc.py*
%{altpython_sitearch}/_lfcthr.so
%{altpython_sitearch}/lfcthr.py*
%{altpython_sitearch}/_lfc2.so
%{altpython_sitearch}/lfc2.py*
%{altpython_sitearch}/_lfc2thr.so
%{altpython_sitearch}/lfc2thr.py*
%if %{?fedora}%{!?fedora:0} >= 15
%{altpython_sitearch}/__pycache__/lfc*
%endif
%endif

%files -n lfc-mysql
%defattr(-,root,root,-)
%dir %{_libdir}/lfc-mysql
%{_libdir}/lfc-mysql/lfcdaemon
%ghost %{_sbindir}/lfcdaemon
%{_libdir}/lfc-mysql/lfc-shutdown
%ghost %{_sbindir}/lfc-shutdown
%{_libdir}/lfc-mysql/NSCONFIG.templ
%ghost %{_datadir}/lfc/NSCONFIG.templ
%doc %{_libdir}/lfc-mysql/lfcdaemon.8*
%ghost %{_mandir}/man8/lfcdaemon.8*
%doc %{_libdir}/lfc-mysql/lfc-shutdown.8*
%ghost %{_mandir}/man8/lfc-shutdown.8*
%dir %{_sysconfdir}/lfc-mysql
%config(noreplace) %{_sysconfdir}/lfc-mysql/lfcdaemon.conf
%ghost %{_sysconfdir}/sysconfig/lfcdaemon
%config(noreplace) %{_sysconfdir}/lfc-mysql/lfcdaemon.logrotate
%ghost %{_sysconfdir}/logrotate.d/lfcdaemon
%{_initrddir}/lfc-mysql
%dir %{_datadir}/lfc
%{_datadir}/lfc/create_lfc_tables_mysql.sql
%attr(-,lfcmgr,lfcmgr) %{_localstatedir}/log/lfc
%attr(-,lfcmgr,lfcmgr) %{_localstatedir}/lib/lfc
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/lfcmgr
%doc lfc-mysql/%{name}-%{version}/ns/README.Fedora

%files -n lfc-dli
%defattr(-,root,root,-)
%{_sbindir}/lfc-dli
%doc %{_mandir}/man8/lfc-dli.8*
%{_initrddir}/lfc-dli
%config(noreplace) %{_sysconfdir}/sysconfig/lfc-dli
%config(noreplace) %{_sysconfdir}/logrotate.d/lfc-dli
%{_datadir}/lfc/lcg-info-provider-lfc
%attr(-,lfcmgr,lfcmgr) %{_localstatedir}/log/lfc-dli

%files -n lfc-postgres
%defattr(-,root,root,-)
%dir %{_libdir}/lfc-postgres
%{_libdir}/lfc-postgres/lfcdaemon
%ghost %{_sbindir}/lfcdaemon
%{_libdir}/lfc-postgres/lfc-shutdown
%ghost %{_sbindir}/lfc-shutdown
%{_libdir}/lfc-postgres/NSCONFIG.templ
%ghost %{_datadir}/lfc/NSCONFIG.templ
%doc %{_libdir}/lfc-postgres/lfcdaemon.8*
%ghost %{_mandir}/man8/lfcdaemon.8*
%doc %{_libdir}/lfc-postgres/lfc-shutdown.8*
%ghost %{_mandir}/man8/lfc-shutdown.8*
%dir %{_sysconfdir}/lfc-postgres
%config(noreplace) %{_sysconfdir}/lfc-postgres/lfcdaemon.conf
%ghost %{_sysconfdir}/sysconfig/lfcdaemon
%config(noreplace) %{_sysconfdir}/lfc-postgres/lfcdaemon.logrotate
%ghost %{_sysconfdir}/logrotate.d/lfcdaemon
%{_initrddir}/lfc-postgres
%dir %{_datadir}/lfc
%{_datadir}/lfc/create_lfc_tables_postgres.sql
%attr(-,lfcmgr,lfcmgr) %{_localstatedir}/log/lfc
%attr(-,lfcmgr,lfcmgr) %{_localstatedir}/lib/lfc
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/lfcmgr
%doc lfc-postgres/%{name}-%{version}/ns/README.Fedora

%files -n dpm
%defattr(-,root,root,-)
%{_libdir}/libdpm.so.*
%doc dpm-mysql/%{name}-%{version}/dpm/README

%files -n dpm-devel
%defattr(-,root,root,-)
%{_includedir}/dpm
%{_libdir}/libdpm.so
%doc %{_mandir}/man3/dpm_[a-o]*.3*
%doc %{_mandir}/man3/dpm_ping.3*
%doc %{_mandir}/man3/dpm_put.3*
%doc %{_mandir}/man3/dpm_putdone.3*
%doc %{_mandir}/man3/dpm_[q-z]*.3*
%doc %{_mandir}/man3/dpns_*.3*
%doc %{_mandir}/man3/rfio*.3*

%files -n dpm-client
%defattr(-,root,root,-)
%{_bindir}/dpm-[a-k]*
%{_bindir}/dpm-[m-z]*
%{_bindir}/dpns-*
%{_bindir}/rf*
%doc %{_mandir}/man1/dpm-[a-k]*
%doc %{_mandir}/man1/dpm-[m-z]*
%doc %{_mandir}/man1/dpns-*
%doc %{_mandir}/man1/rf*

%files -n dpm-perl
%defattr(-,root,root,-)
%{perl_vendorarch}/dpm.so
%{perl_vendorarch}/dpm.pm

%files -n dpm-python
%defattr(-,root,root,-)
%{_bindir}/dpm-listspaces
%{python_sitearch}/_dpm.so
%{python_sitearch}/dpm.py*
%{python_sitearch}/_dpm2.so
%{python_sitearch}/dpm2.py*
%doc %{_mandir}/man1/dpm-listspaces.1*
%doc %{_mandir}/man3/dpm_python.3*
%doc %{_mandir}/man3/dpm2_python.3*

%if %{?altpython:1}%{!?altpython:0}
%files -n dpm-%{altpython}
%defattr(-,root,root,-)
%{altpython_sitearch}/_dpm.so
%{altpython_sitearch}/dpm.py*
%{altpython_sitearch}/_dpm2.so
%{altpython_sitearch}/dpm2.py*
%if %{?fedora}%{!?fedora:0} >= 15
%{altpython_sitearch}/__pycache__/dpm*
%endif
%endif

%files -n dpm-mysql
%defattr(-,root,root,-)
%dir %{_libdir}/dpm-mysql
%{_libdir}/dpm-mysql/dpm
%ghost %{_sbindir}/dpm
%{_libdir}/dpm-mysql/dpm-shutdown
%ghost %{_sbindir}/dpm-shutdown
%doc %{_libdir}/dpm-mysql/dpm.8*
%ghost %{_mandir}/man8/dpm.8*
%doc %{_libdir}/dpm-mysql/dpm-shutdown.8*
%ghost %{_mandir}/man8/dpm-shutdown.8*
%{_libdir}/dpm-mysql/DPMCONFIG.templ
%ghost %{_datadir}/dpm/DPMCONFIG.templ
%dir %{_sysconfdir}/dpm-mysql
%{_initrddir}/dpm-mysql
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpm.conf
%ghost %{_sysconfdir}/sysconfig/dpm
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpm.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpm
%dir %{_datadir}/dpm
%{_datadir}/dpm/create_dpm_tables_mysql.sql
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpm
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/lib/dpm
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/dpmmgr
%doc dpm-mysql/%{name}-%{version}/dpm/README.Fedora

%files -n dpm-mysql-nameserver
%defattr(-,root,root,-)
%{_libdir}/dpm-mysql/dpnsdaemon
%ghost %{_sbindir}/dpnsdaemon
%{_libdir}/dpm-mysql/dpns-shutdown
%ghost %{_sbindir}/dpns-shutdown
%doc %{_libdir}/dpm-mysql/dpnsdaemon.8*
%ghost %{_mandir}/man8/dpnsdaemon.8*
%doc %{_libdir}/dpm-mysql/dpns-shutdown.8*
%ghost %{_mandir}/man8/dpns-shutdown.8*
%{_libdir}/dpm-mysql/DPNSCONFIG.templ
%ghost %{_datadir}/dpm/DPNSCONFIG.templ
%{_initrddir}/dpm-mysql-nameserver
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpnsdaemon.conf
%ghost %{_sysconfdir}/sysconfig/dpnsdaemon
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpnsdaemon.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpnsdaemon
%{_datadir}/dpm/create_dpns_tables_mysql.sql
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpns
%doc dpm-mysql/%{name}-%{version}/ns/README.Fedora

%files -n dpm-mysql-copyd
%defattr(-,root,root,-)
%{_libdir}/dpm-mysql/dpmcopyd
%ghost %{_sbindir}/dpmcopyd
%doc %{_libdir}/dpm-mysql/dpmcopyd.8*
%ghost %{_mandir}/man8/dpmcopyd.8*
%{_initrddir}/dpm-mysql-copyd
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpmcopyd.conf
%ghost %{_sysconfdir}/sysconfig/dpmcopyd
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpmcopyd.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpmcopyd
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpmcopy

%files -n dpm-mysql-srmv1
%defattr(-,root,root,-)
%{_libdir}/dpm-mysql/dpm-srmv1
%ghost %{_sbindir}/dpm-srmv1
%doc %{_libdir}/dpm-mysql/dpm-srmv1.8*
%ghost %{_mandir}/man8/dpm-srmv1.8*
%{_initrddir}/dpm-mysql-srmv1
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpm-srmv1.conf
%ghost %{_sysconfdir}/sysconfig/dpm-srmv1
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpm-srmv1.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpm-srmv1
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpm-srmv1

%files -n dpm-mysql-srmv2
%defattr(-,root,root,-)
%{_libdir}/dpm-mysql/dpm-srmv2
%ghost %{_sbindir}/dpm-srmv2
%doc %{_libdir}/dpm-mysql/dpm-srmv2.8*
%ghost %{_mandir}/man8/dpm-srmv2.8*
%{_initrddir}/dpm-mysql-srmv2
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpm-srmv2.conf
%ghost %{_sysconfdir}/sysconfig/dpm-srmv2
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpm-srmv2.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpm-srmv2
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpm-srmv2

%files -n dpm-mysql-srmv22
%defattr(-,root,root,-)
%{_libdir}/dpm-mysql/dpm-srmv2.2
%ghost %{_sbindir}/dpm-srmv2.2
%doc %{_libdir}/dpm-mysql/dpm-srmv2.2.8*
%ghost %{_mandir}/man8/dpm-srmv2.2.8*
%{_initrddir}/dpm-mysql-srmv22
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpm-srmv2.2.conf
%ghost %{_sysconfdir}/sysconfig/dpm-srmv2.2
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpm-srmv2.2.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpm-srmv2.2
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpm-srmv2.2

%files -n dpm-rfiod
%defattr(-,root,root,-)
%{_sbindir}/dpm-rfiod
%{_initrddir}/dpm-rfiod
%config(noreplace) %{_sysconfdir}/sysconfig/dpm-rfiod
%config(noreplace) %{_sysconfdir}/logrotate.d/dpm-rfiod
%{_localstatedir}/log/dpm-rfio
%doc %{_mandir}/man8/dpm-rfiod.8*

%files -n dpm-postgres
%defattr(-,root,root,-)
%dir %{_libdir}/dpm-postgres
%{_libdir}/dpm-postgres/dpm
%ghost %{_sbindir}/dpm
%{_libdir}/dpm-postgres/dpm-shutdown
%ghost %{_sbindir}/dpm-shutdown
%doc %{_libdir}/dpm-postgres/dpm.8*
%ghost %{_mandir}/man8/dpm.8*
%doc %{_libdir}/dpm-postgres/dpm-shutdown.8*
%ghost %{_mandir}/man8/dpm-shutdown.8*
%{_libdir}/dpm-postgres/DPMCONFIG.templ
%ghost %{_datadir}/dpm/DPMCONFIG.templ
%dir %{_sysconfdir}/dpm-postgres
%{_initrddir}/dpm-postgres
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpm.conf
%ghost %{_sysconfdir}/sysconfig/dpm
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpm.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpm
%dir %{_datadir}/dpm
%{_datadir}/dpm/create_dpm_tables_postgres.sql
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpm
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/lib/dpm
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/dpmmgr
%doc dpm-postgres/%{name}-%{version}/dpm/README.Fedora

%files -n dpm-postgres-nameserver
%defattr(-,root,root,-)
%{_libdir}/dpm-postgres/dpnsdaemon
%ghost %{_sbindir}/dpnsdaemon
%{_libdir}/dpm-postgres/dpns-shutdown
%ghost %{_sbindir}/dpns-shutdown
%doc %{_libdir}/dpm-postgres/dpnsdaemon.8*
%ghost %{_mandir}/man8/dpnsdaemon.8*
%doc %{_libdir}/dpm-postgres/dpns-shutdown.8*
%ghost %{_mandir}/man8/dpns-shutdown.8*
%{_libdir}/dpm-postgres/DPNSCONFIG.templ
%ghost %{_datadir}/dpm/DPNSCONFIG.templ
%{_initrddir}/dpm-postgres-nameserver
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpnsdaemon.conf
%ghost %{_sysconfdir}/sysconfig/dpnsdaemon
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpnsdaemon.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpnsdaemon
%{_datadir}/dpm/create_dpns_tables_postgres.sql
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpns
%doc dpm-postgres/%{name}-%{version}/ns/README.Fedora

%files -n dpm-postgres-copyd
%defattr(-,root,root,-)
%{_libdir}/dpm-postgres/dpmcopyd
%ghost %{_sbindir}/dpmcopyd
%doc %{_libdir}/dpm-postgres/dpmcopyd.8*
%ghost %{_mandir}/man8/dpmcopyd.8*
%{_initrddir}/dpm-postgres-copyd
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpmcopyd.conf
%ghost %{_sysconfdir}/sysconfig/dpmcopyd
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpmcopyd.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpmcopyd
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpmcopy

%files -n dpm-postgres-srmv1
%defattr(-,root,root,-)
%{_libdir}/dpm-postgres/dpm-srmv1
%ghost %{_sbindir}/dpm-srmv1
%doc %{_libdir}/dpm-postgres/dpm-srmv1.8*
%ghost %{_mandir}/man8/dpm-srmv1.8*
%{_initrddir}/dpm-postgres-srmv1
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpm-srmv1.conf
%ghost %{_sysconfdir}/sysconfig/dpm-srmv1
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpm-srmv1.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpm-srmv1
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpm-srmv1

%files -n dpm-postgres-srmv2
%defattr(-,root,root,-)
%{_libdir}/dpm-postgres/dpm-srmv2
%ghost %{_sbindir}/dpm-srmv2
%doc %{_libdir}/dpm-postgres/dpm-srmv2.8*
%ghost %{_mandir}/man8/dpm-srmv2.8*
%{_initrddir}/dpm-postgres-srmv2
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpm-srmv2.conf
%ghost %{_sysconfdir}/sysconfig/dpm-srmv2
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpm-srmv2.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpm-srmv2
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpm-srmv2

%files -n dpm-postgres-srmv22
%defattr(-,root,root,-)
%{_libdir}/dpm-postgres/dpm-srmv2.2
%ghost %{_sbindir}/dpm-srmv2.2
%doc %{_libdir}/dpm-postgres/dpm-srmv2.2.8*
%ghost %{_mandir}/man8/dpm-srmv2.2.8*
%{_initrddir}/dpm-postgres-srmv22
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpm-srmv2.2.conf
%ghost %{_sysconfdir}/sysconfig/dpm-srmv2.2
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpm-srmv2.2.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpm-srmv2.2
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpm-srmv2.2

%changelog
* Tue Sep 13 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.8.0.1-4
- Rebuilt against updated Globus libraries

* Mon Dec 27 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.8.0.1-3
- Add database schema migration to scriptlets
- Fix broken condrestart action in start-up scripts

* Mon Dec 20 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.8.0.1-2
- Filter private provides from python

* Mon Dec 20 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.8.0.1-1
- Update to version 1.8.0.1
- Drop patch lcgdm-bashisms.patch (fixed upstream)

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.7.4.7-4
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.7.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jun 27 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7.4.7-2
- Fix race conditions during make install
- Build python modules for alternative python versions

* Sun Jun 06 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7.4.7-1
- Update to version 1.7.4.7
- This version works with gsoap versions > 2.7.15
- Dropped patches lcgdm-typo.patch and lcgdm-man.patch (fixed upstream)

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.7.4.4-3
- Mass rebuild with perl-5.12.0

* Thu Apr 08 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7.4.4-2
- Fix priorities for alternatives
- Add -p flag to install commands

* Mon Mar 29 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7.4.4-1
- Update to version 1.7.4.4
- Dropped patches lcgdm-installpermissions.patch, lcgdm-rules.patch,
  lcgdm-initscripts.patch and lcgdm-posinc.patch (fixed upstream)

* Mon Jan 04 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7.4.1-1
- Update to version 1.7.4.1
- Dropped patch lcgdm-missing-swig-includes.patch (fixed upstream)

* Thu Dec 10 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7.3.1-5
- Merge LFC and DPM to one specfile

* Mon Dec 07 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7.3.1-4
- Add missing swig includes

* Tue Nov 24 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7.3.1-3
- Don't use /sbin/nologin as shell - doesn't work with su

* Mon Nov 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7.3.1-2
- Make dlopening work for standalone

* Tue Sep 22 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7.3.1-1
- Update to version 1.7.3.1

* Wed Aug 19 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7.2.5-2
- Patch refactoring
- Add alternatives support

* Fri Aug 14 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7.2.5-1
- Update to version 1.7.2.5
- Dropped patch LFC-nofunctions.patch (fixed upstream)

* Wed Jan 14 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7.0.6-1
- Update to version 1.7.0.6
- Dropped patch LFC-glibc28.patch (fixed upstream)
- Dropped patch LFC-perlbug.patch (no longer needed)

* Sun Oct 26 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7.0.2-1ng
- Update to version 1.7.0.2
- Dropped patch LFC-spelling.patch (fixed upstream)

* Fri May 16 2008 Anders Wäänänen <waananen@nbi.dk> - 1.6.9.1-5ng
- Support Alpha architecture
- Added patch LFC-glibc28.patch for glibc-2.8 support
- Added patch LFC-perlbug.patch for work-around on Fedora 9 x86_64

* Tue Apr 02 2008 Anders Wäänänen <waananen@nbi.dk> - 1.6.9.1-4ng
- Added patch from Mattias Ellert <mattias.ellert@fysast.uu.se>:
    LFC-shliblink.patch - Make clients link dynamically against library 

* Tue Mar 18 2008 Anders Wäänänen <waananen@nbi.dk> - 1.6.9.1-3ng
- Added ng to release tag
- Added patches:
    LFC-withsoname.patch - Add sonames libraries (helps package dependencies)
    LFC-nofunctions.patch - Support systems without /etc/init.d/functions
    LFC-spelling.patch - Spelling corrections

* Sat Jan 12 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.6.9.1-2
- Fixing some file permissions in the server package

* Sat Jan 12 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.6.9.1-1
- Update.

* Wed Jul 25 2007 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.6.6.1-1
- Update.

* Thu May 10 2007 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.6.4.3-1
- Initial build.
