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
%filter_provides_in %{_libdir}/lcgdm/.*\.so$
%filter_provides_in %{perl_vendorarch}/.*\.so$
%filter_provides_in %{python_sitearch}/.*\.so$
%if %{?altpython:1}%{!?altpython:0}
%filter_provides_in %{altpython_sitearch}/.*\.so$
%endif
%filter_setup
%endif

Name:		lcgdm
Version:	1.8.1.2
Release:	6%{?dist}
Summary:	LHC Computing Grid Data Management

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://glite.web.cern.ch/glite/
#		LANG=C svn co http://svnweb.cern.ch/guest/lcgdm/lcg-dm/tags/LCG-DM_R_1_8_1_2_emi lcgdm-1.8.1.2
#		tar --exclude .svn -z -c -f lcgdm-1.8.1.2.tar.gz lcgdm-1.8.1.2
Source0:	%{name}-%{version}.tar.gz
Source1:	README.Fedora.lfc-mysql
Source2:	README.Fedora.lfc-postgres
Source3:	README.Fedora.dpm-mysql
Source4:	README.Fedora.dpns-mysql
Source5:	README.Fedora.dpm-postgres
Source6:	README.Fedora.dpns-postgres
#		Link binaries using shared libraries
#		https://savannah.cern.ch/bugs/?57529
Patch0:		%{name}-shliblink.patch
#		Fix build on GNU/Hurd and GNU/kFreeBSD
#		https://savannah.cern.ch/bugs/?61071
Patch1:		%{name}-porting.patch
#		Fix race conditions in Makefile install rules:
#		https://savannah.cern.ch/bugs/?69233
Patch2:		%{name}-race.patch
#		Remove deprecated python function:
#		https://savannah.cern.ch/bugs/?69232
Patch3:		%{name}-python-exception.patch
#		Make condrestart work as expected
#		https://savannah.cern.ch/bugs/?76695
Patch4:		%{name}-condrestart.patch
#		Add service dependencies to start-up scripts
Patch5:		%{name}-start-deps.patch
#		Get rid of -L/usr/lib(64)
Patch6:		%{name}-usr.patch
#		Fix python and perl installation paths and linking
Patch7:		%{name}-paths.patch
#		Allow moving plugins out of default library search path
Patch8:		%{name}-dlopen.patch
#		Use Fedora's imake instead of bundled version
Patch9:		%{name}-imake.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{?fedora}%{!?fedora:0} >= 5 || %{?rhel}%{!?rhel:0} >= 5
BuildRequires:	imake
%else
BuildRequires:	xorg-x11-devel
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
The lcgdm package provides the LCG Data Management components: the LFC
(LCG File Catalog) and the DPM (Disk Pool Manager).

%package libs
Summary:	LHC Computing Grid Data Management common libraries
Group:		System Environment/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name} < 1.8.1.2-4

%description libs
The lcgdm-libs package contains common libraries for the LCG Data Management
components: the LFC (LCG File Catalog) and the DPM (Disk Pool Manager).

%package devel
Summary:	LCG Data Management common development files
Group:		Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains common development libraries and header files
for LCG Data Management.

%package -n lfc-libs
Summary:	LCG File Catalog (LFC) libraries
Group:		System Environment/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes:	lfc < 1.8.1.2-4

%description -n lfc-libs
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package contains the runtime LFC client library.

%package -n lfc-devel
Summary:	LFC development libraries and header files
Group:		Development/Libraries
Requires:	lfc-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description -n lfc-devel
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package contains the development libraries and header files for LFC.

%package -n lfc
Summary:	LCG File Catalog (LFC) client
Group:		Applications/Internet
Requires:	lfc-libs%{?_isa} = %{version}-%{release}
Provides:	lfc-client = %{version}-%{release}
Obsoletes:	lfc-client < 1.8.1.2-4

%description -n lfc
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package contains the command line interfaces for the LFC.

%package -n lfc-perl
Summary:	LCG File Catalog (LFC) perl bindings
Group:		Applications/Internet
Requires:	lfc-libs%{?_isa} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n lfc-perl
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package provides Perl bindings for the LFC client library.

%package -n lfc-python
Summary:	LCG File Catalog (LFC) python bindings
Group:		Applications/Internet
Requires:	lfc-libs%{?_isa} = %{version}-%{release}

%description -n lfc-python
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package provides Python bindings for the LFC client library.

%if %{?altpython:1}%{!?altpython:0}
%package -n lfc-%{altpython}
Summary:	LCG File Catalog (LFC) python bindings
Group:		Applications/Internet
Requires:	lfc-libs%{?_isa} = %{version}-%{release}
%if %{?rhel}%{!?rhel:0} == 5
Requires:	python(abi) = 2.6
%endif

%description -n lfc-%{altpython}
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package provides Python bindings for the LFC client library.
%endif

%package -n lfc-server-mysql
Summary:	LCG File Catalog (LFC) server with MySQL database backend
Group:		Applications/Internet
Requires:	lfc-libs%{?_isa} = %{version}-%{release}
Provides:	lfc-mysql = %{version}-%{release}
Obsoletes:	lfc-mysql < 1.8.1.2-4

Requires(pre):		shadow-utils
Requires(post):		mysql
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n lfc-server-mysql
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package provides an LFC server that uses MySQL as its database
backend.

%package -n lfc-server-postgres
Summary:	LCG File Catalog (LFC) server with postgres database backend
Group:		Applications/Internet
Requires:	lfc-libs%{?_isa} = %{version}-%{release}
Provides:	lfc-postgres = %{version}-%{release}
Obsoletes:	lfc-postgres < 1.8.1.2-4

Requires(pre):		shadow-utils
Requires(post):		postgresql
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n lfc-server-postgres
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package provides an LFC server that uses postgres as its database
backend.

%package -n lfc-dli
Summary:	LCG File Catalog (LFC) data location interface (dli) server
Group:		Applications/Internet
Requires:	lfc-libs%{?_isa} = %{version}-%{release}

Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n lfc-dli
The LCG File Catalog (LFC) keeps track of the locations of the physical
replicas of the logical files in a distributed storage system.
This package provides the data location interface (dli) server for the LFC.

%package -n dpm-libs
Summary:	Disk Pool Manager (DPM) libraries
Group:		System Environment/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes:	dpm < 1.8.1.2-4

%description -n dpm-libs
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package contains the runtime DPM client library.

%package -n dpm-devel
Summary:	DPM development libraries and header files
Group:		Development/Libraries
Requires:	dpm-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description -n dpm-devel
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package contains the development libraries and header files for DPM.

%package -n dpm
Summary:	Disk Pool Manager (DPM) client
Group:		Applications/Internet
Requires:	dpm-libs%{?_isa} = %{version}-%{release}
Provides:	dpm-client = %{version}-%{release}
Obsoletes:	dpm-client < 1.8.1.2-4

%description -n dpm
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package contains the command line interfaces for the DPM.

%package -n dpm-perl
Summary:	Disk Pool Manager (DPM) perl bindings
Group:		Applications/Internet
Requires:	dpm-libs%{?_isa} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n dpm-perl
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides Perl bindings for the DPM client library.

%package -n dpm-python
Summary:	Disk Pool Manager (DPM) python bindings
Group:		Applications/Internet
Requires:	dpm-libs%{?_isa} = %{version}-%{release}

%description -n dpm-python
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides Python bindings for the DPM client library.

%if %{?altpython:1}%{!?altpython:0}
%package -n dpm-%{altpython}
Summary:	Disk Pool Manager (DPM) python bindings
Group:		Applications/Internet
Requires:	dpm-libs%{?_isa} = %{version}-%{release}
%if %{?rhel}%{!?rhel:0} == 5
Requires:	python(abi) = 2.6
%endif

%description -n dpm-%{altpython}
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides Python bindings for the DPM client library.
%endif

%package -n dpm-server-mysql
Summary:	Disk Pool Manager (DPM) server with MySQL database backend
Group:		Applications/Internet
Requires:	dpm-libs%{?_isa} = %{version}-%{release}
Provides:	dpm-mysql = %{version}-%{release}
Obsoletes:	dpm-mysql < 1.8.1.2-4

Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-server-mysql
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM server that uses MySQL as its database
backend.

%package -n dpm-server-postgres
Summary:	Disk Pool Manager (DPM) server with postgres database backend
Group:		Applications/Internet
Requires:	dpm-libs%{?_isa} = %{version}-%{release}
Provides:	dpm-postgres = %{version}-%{release}
Obsoletes:	dpm-postgres < 1.8.1.2-4

Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-server-postgres
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM server that uses postgres as its database
backend.

%package -n dpm-name-server-mysql
Summary:	DPM name server with MySQL database backend
Group:		Applications/Internet
Requires:	dpm-libs%{?_isa} = %{version}-%{release}
Provides:	dpm-mysql-nameserver = %{version}-%{release}
Obsoletes:	dpm-mysql-nameserver < 1.8.1.2-4

Requires(pre):		shadow-utils
Requires(post):		mysql
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-name-server-mysql
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM nameserver that uses MySQL as its database
backend.

%package -n dpm-name-server-postgres
Summary:	DPM nameserver with postgres database backend
Group:		Applications/Internet
Requires:	dpm-libs%{?_isa} = %{version}-%{release}
Provides:	dpm-postgres-nameserver = %{version}-%{release}
Obsoletes:	dpm-postgres-nameserver < 1.8.1.2-4

Requires(pre):		shadow-utils
Requires(post):		postgresql
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-name-server-postgres
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM nameserver that uses postgres as its
database backend.

%package -n dpm-copy-server-mysql
Summary:	DPM copy server with MySQL database backend
Group:		Applications/Internet
Requires:	dpm-libs%{?_isa} = %{version}-%{release}
Provides:	dpm-mysql-copyd = %{version}-%{release}
Obsoletes:	dpm-mysql-copyd < 1.8.1.2-4

Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-copy-server-mysql
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM copy server that uses MySQL as its
database backend.

%package -n dpm-copy-server-postgres
Summary:	DPM copy server with postgres database backend
Group:		Applications/Internet
Requires:	dpm-libs%{?_isa} = %{version}-%{release}
Provides:	dpm-postgres-copyd = %{version}-%{release}
Obsoletes:	dpm-postgres-copyd < 1.8.1.2-4

Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-copy-server-postgres
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM copy server that uses postgres as its
database backend.

%package -n dpm-srm-server-mysql
Summary:	DPM SRM server with MySQL database backend
Group:		Applications/Internet
Requires:	dpm-libs%{?_isa} = %{version}-%{release}
Provides:	dpm-mysql-srmv1 = %{version}-%{release}
Obsoletes:	dpm-mysql-srmv1 < 1.8.1.2-4
Provides:	dpm-mysql-srmv2 = %{version}-%{release}
Obsoletes:	dpm-mysql-srmv2 < 1.8.1.2-4
Provides:	dpm-mysql-srmv22 = %{version}-%{release}
Obsoletes:	dpm-mysql-srmv22 < 1.8.1.2-4

Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-srm-server-mysql
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM SRM server that uses MySQL as its
database backend.

%package -n dpm-srm-server-postgres
Summary:	DPM SRM server with postgres database backend
Group:		Applications/Internet
Requires:	dpm-libs%{?_isa} = %{version}-%{release}
Provides:	dpm-postgres-srmv1 = %{version}-%{release}
Obsoletes:	dpm-postgres-srmv1 < 1.8.1.2-4
Provides:	dpm-postgres-srmv2 = %{version}-%{release}
Obsoletes:	dpm-postgres-srmv2 < 1.8.1.2-4
Provides:	dpm-postgres-srmv22 = %{version}-%{release}
Obsoletes:	dpm-postgres-srmv22 < 1.8.1.2-4

Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-srm-server-postgres
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a DPM SRM server that uses postgres as its
database backend.

%package -n dpm-rfio-server
Summary:	DPM RFIO server
Group:		Applications/Internet
Requires:	dpm-libs%{?_isa} = %{version}-%{release}
Provides:	dpm-rfiod = %{version}-%{release}
Obsoletes:	dpm-rfiod < 1.8.1.2-4

Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description -n dpm-rfio-server
The LCG Disk Pool Manager (DPM) creates a storage element from a set
of disks. It provides several interfaces for storing and retrieving
data such as RFIO and SRM version 1, version 2 and version 2.2.
This package provides a Remote File IO (RFIO) server for DPM.

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

chmod 644 security/globus_gsi_gss_constants.h \
	  security/globus_i_gsi_credential.h \
	  security/gssapi_openssl.h
chmod 644 doc/lfc/INSTALL-*

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
	--with-gsoap-version=$gsoapversion \
	--with-id-map-file=%{_sysconfdir}/lcgdm-mapfile \
	--with-ns-config-file=%{_sysconfdir}/NSCONFIG \
	--with-emi \
	--without-argus

make -f Makefile.ini Makefiles

make %{?_smp_mflags} SOAPFLG="`pkg-config --cflags gsoap`" \
     SYSCONFDIR=%{_sysconfdir} \
     LDFLAGS="%{?__global_ldflags}"

popd

pushd lfc-postgres/%{name}-%{version}

./configure lfc --with-postgres \
	--libdir=%{_lib} \
	--with-gsoap-version=$gsoapversion \
	--with-id-map-file=%{_sysconfdir}/lcgdm-mapfile \
	--with-ns-config-file=%{_sysconfdir}/NSCONFIG \
	--with-emi \
	--without-argus

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

make %{?_smp_mflags} SOAPFLG="`pkg-config --cflags gsoap`" \
     SYSCONFDIR=%{_sysconfdir} \
     LDFLAGS="%{?__global_ldflags}"

popd

pushd dpm-mysql/%{name}-%{version}

./configure dpm --with-mysql \
	--libdir=%{_lib} \
	--with-gsoap-version=$gsoapversion \
	--with-dpm-config-file=%{_sysconfdir}/DPMCONFIG \
	--with-id-map-file=%{_sysconfdir}/lcgdm-mapfile \
	--with-ns-config-file=%{_sysconfdir}/DPNSCONFIG \
	--with-emi \
	--without-argus

# Disable building things already built above
sed -e '/^SECURITYDIR =/d' -e '/^COMMONDIR =/d' -i config/Project.tmpl
sed -e 's/:.*(lcgdm).*/:/' -i lib/Imakefile
sed -e 's/:.*(lcgdm).*/:/' -i shlib/Imakefile

make -f Makefile.ini Makefiles

pushd shlib
ln -s ../../../lfc-mysql/%{name}-%{version}/shlib/liblcgdm.so* .
popd

make %{?_smp_mflags} SOAPFLG="`pkg-config --cflags gsoap`" \
     SYSCONFDIR=%{_sysconfdir} \
     LDFLAGS="%{?__global_ldflags}"

popd

pushd dpm-postgres/%{name}-%{version}

./configure dpm --with-postgres \
	--libdir=%{_lib} \
	--with-gsoap-version=$gsoapversion \
	--with-dpm-config-file=%{_sysconfdir}/DPMCONFIG \
	--with-id-map-file=%{_sysconfdir}/lcgdm-mapfile \
	--with-ns-config-file=%{_sysconfdir}/DPNSCONFIG \
	--with-emi \
	--without-argus

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

make %{?_smp_mflags} SOAPFLG="`pkg-config --cflags gsoap`" \
     SYSCONFDIR=%{_sysconfdir} \
     LDFLAGS="%{?__global_ldflags}"

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
	'/config -lpython' + sys.version[:3] \
	   + sys.abiflags if hasattr(sys, 'abiflags') else '' \
	   + ' ' + \
	sysconfig.get_config_var('LIBS') + ' ' + \
	sysconfig.get_config_var('SYSLIBS'))"`
PYTHON_MODULE_SUFFIX=`%{__altpython} \
    -c "from distutils import sysconfig; \
	print(sysconfig.get_config_var('SO'))"`

for module in lfc lfcthr lfc2 lfc2thr ; do

gcc %{optflags} -fno-strict-aliasing -fPIC -D_LARGEFILE64_SOURCE -Dlinux \
    -c -pthread -DCTHREAD_LINUX -D_THREAD_SAFE -D_REENTRANT \
    -I../lfc-mysql/%{name}-%{version}/h -DNSTYPE_LFC \
    ${INCLUDE_PYTHON} ../lfc-mysql/%{name}-%{version}/ns/${module}_wrap.c
gcc %{optflags} -fno-strict-aliasing -fPIC -D_LARGEFILE64_SOURCE -Dlinux \
    -shared -o _${module}${PYTHON_MODULE_SUFFIX} ${module}_wrap.o ${PYTHON_LIB} \
    -L../lfc-mysql/%{name}-%{version}/shlib -llfc -llcgdm

done

for module in dpm dpm2 ; do

gcc %{optflags} -fno-strict-aliasing -fPIC -D_LARGEFILE64_SOURCE -Dlinux \
    -c -pthread -DCTHREAD_LINUX -D_THREAD_SAFE -D_REENTRANT \
    -I../dpm-mysql/%{name}-%{version}/h -DNSTYPE_DPNS \
    ${INCLUDE_PYTHON} ../dpm-mysql/%{name}-%{version}/dpm/${module}_wrap.c
gcc %{optflags} -fno-strict-aliasing -fPIC -D_LARGEFILE64_SOURCE -Dlinux \
    -shared -o _${module}${PYTHON_MODULE_SUFFIX} ${module}_wrap.o ${PYTHON_LIB} \
    -L../dpm-mysql/%{name}-%{version}/shlib -ldpm -llcgdm

done

popd
%endif

%install
rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8

pushd lfc-mysql/%{name}-%{version}

make SOAPFLG="`pkg-config --cflags gsoap`" \
     SYSCONFDIR=${RPM_BUILD_ROOT}%{_sysconfdir} \
     LDFLAGS="%{?__global_ldflags}" \
     prefix=${RPM_BUILD_ROOT}%{_prefix} install install.man

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/lfc
mv ${RPM_BUILD_ROOT}%{_datadir}/LFC/* ${RPM_BUILD_ROOT}%{_datadir}/lfc
rmdir ${RPM_BUILD_ROOT}%{_datadir}/LFC

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/lfc-mysql
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-mysql

# lfcdaemon startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!\$PREFIX/bin!\$PREFIX/sbin!' \
    -e 's!\$PREFIX/etc!/etc!' \
    ${RPM_BUILD_ROOT}%{_datadir}/lfc/rc.lfcdaemon > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-mysql/lfcdaemon.init
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-mysql/lfcdaemon.init
rm ${RPM_BUILD_ROOT}%{_datadir}/lfc/rc.lfcdaemon
touch ${RPM_BUILD_ROOT}%{_initrddir}/lfcdaemon
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/lfcdaemon

# lfcdaemon configuration file
cp -p ${RPM_BUILD_ROOT}%{_sysconfdir}/lfcdaemon.conf.templ \
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
    -e 's!\$PREFIX/bin!\$PREFIX/sbin!' \
    -e 's!\$PREFIX/etc!/etc!' \
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
    -i ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-mysql/lfcdaemon.init \
       ${RPM_BUILD_ROOT}%{_initrddir}/lfc-dli

popd

pushd lfc-postgres/%{name}-%{version}

make SOAPFLG="`pkg-config --cflags gsoap`" \
     SYSCONFDIR=${RPM_BUILD_ROOT}%{_sysconfdir} \
     LDFLAGS="%{?__global_ldflags}" \
     prefix=${RPM_BUILD_ROOT}%{_prefix} install install.man

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/lfc
mv ${RPM_BUILD_ROOT}%{_datadir}/LFC/* ${RPM_BUILD_ROOT}%{_datadir}/lfc
rmdir ${RPM_BUILD_ROOT}%{_datadir}/LFC

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/lfc-postgres
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-postgres

# lfcdaemon startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!\$PREFIX/bin!\$PREFIX/sbin!' \
    -e 's!\$PREFIX/etc!/etc!' \
    ${RPM_BUILD_ROOT}%{_datadir}/lfc/rc.lfcdaemon > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-postgres/lfcdaemon.init
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-postgres/lfcdaemon.init
rm ${RPM_BUILD_ROOT}%{_datadir}/lfc/rc.lfcdaemon
touch ${RPM_BUILD_ROOT}%{_initrddir}/lfcdaemon
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/lfcdaemon

# lfcdaemon configuration file
cp -p ${RPM_BUILD_ROOT}%{_sysconfdir}/lfcdaemon.conf.templ \
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
    -i ${RPM_BUILD_ROOT}%{_sysconfdir}/lfc-postgres/lfcdaemon.init

popd

pushd dpm-mysql/%{name}-%{version}

make SOAPFLG="`pkg-config --cflags gsoap`" \
     SYSCONFDIR=${RPM_BUILD_ROOT}%{_sysconfdir} \
     LDFLAGS="%{?__global_ldflags}" \
     prefix=${RPM_BUILD_ROOT}%{_prefix} install install.man

sed 's!/usr/bin/env python!/usr/bin/python!' \
    -i ${RPM_BUILD_ROOT}%{_bindir}/dpm-listspaces

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/dpm
mv ${RPM_BUILD_ROOT}%{_datadir}/DPM/* ${RPM_BUILD_ROOT}%{_datadir}/dpm
rmdir ${RPM_BUILD_ROOT}%{_datadir}/DPM

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql

# dpm startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!\$PREFIX/bin!\$PREFIX/sbin!' \
    -e 's!\$PREFIX/etc!/etc!' \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpm > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpm.init
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpm.init
rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpm
touch ${RPM_BUILD_ROOT}%{_initrddir}/dpm
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpm

# dpm configuration file
sed -e 's/\(^DPNS_HOST=\).*/\1`hostname -f`/' \
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
    -e 's!\$PREFIX/bin!\$PREFIX/sbin!' \
    -e 's!\$PREFIX/etc!/etc!' \
    -e 's!/etc/NSCONFIG!/etc/DPNSCONFIG!g' \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpnsdaemon > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpnsdaemon.init
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpnsdaemon.init
rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpnsdaemon
touch ${RPM_BUILD_ROOT}%{_initrddir}/dpnsdaemon
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpnsdaemon

# dpnsdaemon configuration file
sed -e 's!/etc/NSCONFIG!/etc/DPNSCONFIG!g' \
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
    -e 's!\$PREFIX/bin!\$PREFIX/sbin!' \
    -e 's!\$PREFIX/etc!/etc!' \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpmcopyd > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpmcopyd.init
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpmcopyd.init
rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpmcopyd
touch ${RPM_BUILD_ROOT}%{_initrddir}/dpmcopyd
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpmcopyd

# dpmcopyd configuration file
sed -e 's/\(^DPNS_HOST=\).*/\1`hostname -f`/' \
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
    ${RPM_BUILD_ROOT}%{_mandir}/man1/dpmcopyd.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpmcopyd.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/dpmcopyd.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpmcopyd.8

for svc in srmv1 srmv2 srmv2.2 ; do
    # startup script
    sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
	-e '/LD_LIBRARY_PATH/d' \
	-e 's!\$PREFIX/bin!\$PREFIX/sbin!' \
	-e 's!\$PREFIX/etc!/etc!' \
	-e "s/${svc}/dpm-${svc}/g" \
	${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.${svc} > \
	${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpm-${svc}.init
    chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/dpm-${svc}.init
    rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.${svc}
    touch ${RPM_BUILD_ROOT}%{_initrddir}/dpm-${svc}
    chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpm-${svc}

    # configuration file
    sed -e "s/${svc}/dpm-${svc}/g" \
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

    # binary and man page
    mv ${RPM_BUILD_ROOT}%{_bindir}/${svc} \
       ${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpm-${svc}
    touch ${RPM_BUILD_ROOT}%{_sbindir}/dpm-${svc}
    chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/dpm-${svc}
    sed -e 's/\.TH \([^ ]*\) 1/.TH DPM-\1 8/' \
	-e "s/${svc}/dpm-${svc}/g" \
	-e 's/dpm(1)/dpm(8)/g' \
	${RPM_BUILD_ROOT}%{_mandir}/man1/${svc}.1 | gzip -9 -n -c > \
	${RPM_BUILD_ROOT}%{_libdir}/dpm-mysql/dpm-${svc}.8.gz
    rm ${RPM_BUILD_ROOT}%{_mandir}/man1/${svc}.1
    touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpm-${svc}.8
done

# dpm-rfiod startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!\$PREFIX/bin!\$PREFIX/sbin!' \
    -e 's!\$PREFIX/etc!/etc!' \
    -e 's/rfiod/dpm-rfiod/g' \
    -e 's!/var/log/rfio!/var/log/dpm-rfio!g' \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.rfiod > \
    ${RPM_BUILD_ROOT}%{_initrddir}/dpm-rfiod
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpm-rfiod
rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.rfiod

# dpm-rfiod configuration file
sed -e 's/rfiod/dpm-rfiod/g' \
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
    -i ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-mysql/*.init \
       ${RPM_BUILD_ROOT}%{_initrddir}/dpm-rfiod

popd

pushd dpm-postgres/%{name}-%{version}

make SOAPFLG="`pkg-config --cflags gsoap`" \
     SYSCONFDIR=${RPM_BUILD_ROOT}%{_sysconfdir} \
     LDFLAGS="%{?__global_ldflags}" \
     prefix=${RPM_BUILD_ROOT}%{_prefix} install install.man

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/dpm
mv ${RPM_BUILD_ROOT}%{_datadir}/DPM/* ${RPM_BUILD_ROOT}%{_datadir}/dpm
rmdir ${RPM_BUILD_ROOT}%{_datadir}/DPM

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres

# dpm startup script
sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
    -e '/LD_LIBRARY_PATH/d' \
    -e 's!\$PREFIX/bin!\$PREFIX/sbin!' \
    -e 's!\$PREFIX/etc!/etc!' \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpm > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpm.init
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpm.init
rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpm
touch ${RPM_BUILD_ROOT}%{_initrddir}/dpm
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpm

# dpm configuration file
sed -e 's/\(^DPNS_HOST=\).*/\1`hostname -f`/' \
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
    -e 's!\$PREFIX/bin!\$PREFIX/sbin!' \
    -e 's!\$PREFIX/etc!/etc!' \
    -e 's!/etc/NSCONFIG!/etc/DPNSCONFIG!g' \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpnsdaemon > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpnsdaemon.init
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpnsdaemon.init
rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpnsdaemon
touch ${RPM_BUILD_ROOT}%{_initrddir}/dpnsdaemon
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpnsdaemon

# dpnsdaemon configuration file
sed -e 's!/etc/NSCONFIG!/etc/DPNSCONFIG!g' \
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
    -e 's!\$PREFIX/bin!\$PREFIX/sbin!' \
    -e 's!\$PREFIX/etc!/etc!' \
    ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpmcopyd > \
    ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpmcopyd.init
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpmcopyd.init
rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.dpmcopyd
touch ${RPM_BUILD_ROOT}%{_initrddir}/dpmcopyd
chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpmcopyd

# dpmcopyd configuration file
sed -e 's/\(^DPNS_HOST=\).*/\1`hostname -f`/' \
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
    ${RPM_BUILD_ROOT}%{_mandir}/man1/dpmcopyd.1 | gzip -9 -n -c > \
    ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/dpmcopyd.8.gz
rm ${RPM_BUILD_ROOT}%{_mandir}/man1/dpmcopyd.1
touch ${RPM_BUILD_ROOT}%{_mandir}/man8/dpmcopyd.8

for svc in srmv1 srmv2 srmv2.2 ; do
    # startup script
    sed -e 's/LD_LIBRARY_PATH=$LD_LIBRARY_PATH //' \
	-e '/LD_LIBRARY_PATH/d' \
	-e 's!\$PREFIX/bin!\$PREFIX/sbin!' \
	-e 's!\$PREFIX/etc!/etc!' \
	-e "s/${svc}/dpm-${svc}/g" \
	${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.${svc} > \
	${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpm-${svc}.init
    chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/dpm-${svc}.init
    rm ${RPM_BUILD_ROOT}%{_datadir}/dpm/rc.${svc}
    touch ${RPM_BUILD_ROOT}%{_initrddir}/dpm-${svc}
    chmod 755 ${RPM_BUILD_ROOT}%{_initrddir}/dpm-${svc}

    # configuration file
    sed -e "s/${svc}/dpm-${svc}/g" \
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

    # binary and man page
    mv ${RPM_BUILD_ROOT}%{_bindir}/${svc} \
       ${RPM_BUILD_ROOT}%{_libdir}/dpm-postgres/dpm-${svc}
    touch ${RPM_BUILD_ROOT}%{_sbindir}/dpm-${svc}
    chmod 755 ${RPM_BUILD_ROOT}%{_sbindir}/dpm-${svc}
    sed -e 's/\.TH \([^ ]*\) 1/.TH DPM-\1 8/' \
	-e "s/${svc}/dpm-${svc}/g" \
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
    -i ${RPM_BUILD_ROOT}%{_sysconfdir}/dpm-postgres/*.init

popd

%if %{?altpython:1}%{!?altpython:0}
mkdir -p ${RPM_BUILD_ROOT}%{altpython_sitearch}
install -m 644 lfc-mysql/%{name}-%{version}/ns/*.py \
	       dpm-mysql/%{name}-%{version}/dpm/*.py \
	       ${RPM_BUILD_ROOT}%{altpython_sitearch}
install %{altpython}/*.so ${RPM_BUILD_ROOT}%{altpython_sitearch}

# make a dummy ld.so.conf file so lfc-python26 will be considered multilib
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/ld.so.conf.d
echo "# this file is intentionally left blank" > ${RPM_BUILD_ROOT}%{_sysconfdir}/ld.so.conf.d/lfc-%{altpython}.conf
%endif

%if %{?fedora}%{!?fedora:0} < 5 && %{?rhel}%{!?rhel:0} < 6
%{__python}    -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT"'", 10, "%{python_sitearch}", 1)' > /dev/null
%{__python} -O -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT"'", 10, "%{python_sitearch}", 1)' > /dev/null

%if %{?altpython:1}%{!?altpython:0}
%{__altpython}	  -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{altpython_sitearch}"'", 10, "%{altpython_sitearch}", 1)' > /dev/null
%{__altpython} -O -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{altpython_sitearch}"'", 10, "%{altpython_sitearch}", 1)' > /dev/null
%endif
%endif

# make a dummy ld.so.conf file so lfc-python will be considered multilib
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/ld.so.conf.d
echo "# this file is intentionally left blank" > ${RPM_BUILD_ROOT}%{_sysconfdir}/ld.so.conf.d/lfc-python.conf


%clean
rm -rf ${RPM_BUILD_ROOT}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post -n lfc-libs -p /sbin/ldconfig

%postun -n lfc-libs -p /sbin/ldconfig

%post -n dpm-libs -p /sbin/ldconfig

%postun -n dpm-libs -p /sbin/ldconfig

%pre -n lfc-server-mysql
getent group lfcmgr > /dev/null || groupadd -r lfcmgr
getent passwd lfcmgr > /dev/null || useradd -r -g lfcmgr \
    -d %{_localstatedir}/lib/lfc -s /bin/bash -c "LFC Manager" lfcmgr
exit 0

%pre -n lfc-server-postgres
getent group lfcmgr > /dev/null || groupadd -r lfcmgr
getent passwd lfcmgr > /dev/null || useradd -r -g lfcmgr \
    -d %{_localstatedir}/lib/lfc -s /bin/bash -c "LFC Manager" lfcmgr
exit 0

%post -n lfc-server-mysql
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

%{_sbindir}/update-alternatives --install %{_sbindir}/lfcdaemon lfcdaemon \
	  %{_libdir}/lfc-mysql/lfcdaemon 20 \
  --slave %{_mandir}/man8/lfcdaemon.8.gz lfcdaemon.8.gz \
	  %{_libdir}/lfc-mysql/lfcdaemon.8.gz \
  --slave %{_datadir}/lfc/NSCONFIG.templ NSCONFIG.templ \
	  %{_libdir}/lfc-mysql/NSCONFIG.templ \
  --slave %{_initrddir}/lfcdaemon lfcdaemon.init \
	  %{_sysconfdir}/lfc-mysql/lfcdaemon.init \
  --slave %{_sysconfdir}/sysconfig/lfcdaemon lfcdaemon.conf \
	  %{_sysconfdir}/lfc-mysql/lfcdaemon.conf \
  --slave %{_sysconfdir}/logrotate.d/lfcdaemon lfcdaemon.logrotate \
	  %{_sysconfdir}/lfc-mysql/lfcdaemon.logrotate \
  --slave %{_sbindir}/lfc-shutdown lfc-shutdown \
	  %{_libdir}/lfc-mysql/lfc-shutdown \
  --slave %{_mandir}/man8/lfc-shutdown.8.gz lfc-shutdown.8.gz \
	  %{_libdir}/lfc-mysql/lfc-shutdown.8.gz

if [ $1 = 1 ]; then
    if [ -r %{_initrddir}/lfcdaemon ]; then
	/sbin/chkconfig --add lfcdaemon
    fi
fi

%post -n lfc-server-postgres
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

%{_sbindir}/update-alternatives --install %{_sbindir}/lfcdaemon lfcdaemon \
	  %{_libdir}/lfc-postgres/lfcdaemon 10 \
  --slave %{_mandir}/man8/lfcdaemon.8.gz lfcdaemon.8.gz \
	  %{_libdir}/lfc-postgres/lfcdaemon.8.gz \
  --slave %{_datadir}/lfc/NSCONFIG.templ NSCONFIG.templ \
	  %{_libdir}/lfc-postgres/NSCONFIG.templ \
  --slave %{_initrddir}/lfcdaemon lfcdaemon.init \
	  %{_sysconfdir}/lfc-postgres/lfcdaemon.init \
  --slave %{_sysconfdir}/sysconfig/lfcdaemon lfcdaemon.conf \
	  %{_sysconfdir}/lfc-postgres/lfcdaemon.conf \
  --slave %{_sysconfdir}/logrotate.d/lfcdaemon lfcdaemon.logrotate \
	  %{_sysconfdir}/lfc-postgres/lfcdaemon.logrotate \
  --slave %{_sbindir}/lfc-shutdown lfc-shutdown \
	  %{_libdir}/lfc-postgres/lfc-shutdown \
  --slave %{_mandir}/man8/lfc-shutdown.8.gz lfc-shutdown.8.gz \
	  %{_libdir}/lfc-postgres/lfc-shutdown.8.gz

if [ $1 = 1 ]; then
    if [ -r %{_initrddir}/lfcdaemon ]; then
	/sbin/chkconfig --add lfcdaemon
    fi
fi

%preun -n lfc-server-mysql
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display lfcdaemon | \
	grep currently | grep -q lfc-mysql && \
	/sbin/service lfcdaemon stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove lfcdaemon \
	%{_libdir}/lfc-mysql/lfcdaemon
    %{_sbindir}/update-alternatives --display lfcdaemon > /dev/null || \
	/sbin/chkconfig --del lfcdaemon > /dev/null 2>&1 || :
fi

%preun -n lfc-server-postgres
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display lfcdaemon | \
	grep currently | grep -q lfc-postgres && \
	/sbin/service lfcdaemon stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove lfcdaemon \
	%{_libdir}/lfc-postgres/lfcdaemon
    %{_sbindir}/update-alternatives --display lfcdaemon > /dev/null || \
	/sbin/chkconfig --del lfcdaemon > /dev/null 2>&1 || :
fi

%postun -n lfc-server-mysql
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display lfcdaemon | \
	grep currently | grep -q lfc-mysql && \
	/sbin/service lfcdaemon condrestart > /dev/null 2>&1 || :
fi

%postun -n lfc-server-postgres
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display lfcdaemon | \
	grep currently | grep -q lfc-postgres && \
	/sbin/service lfcdaemon condrestart > /dev/null 2>&1 || :
fi

%triggerpostun -n lfc-server-mysql -- lfc-mysql < 1.8.1.2-4
# Restore alternatives removed by lfc-mysql preun
%{_sbindir}/update-alternatives --install %{_sbindir}/lfcdaemon lfcdaemon \
	  %{_libdir}/lfc-mysql/lfcdaemon 20 \
  --slave %{_mandir}/man8/lfcdaemon.8.gz lfcdaemon.8.gz \
	  %{_libdir}/lfc-mysql/lfcdaemon.8.gz \
  --slave %{_datadir}/lfc/NSCONFIG.templ NSCONFIG.templ \
	  %{_libdir}/lfc-mysql/NSCONFIG.templ \
  --slave %{_initrddir}/lfcdaemon lfcdaemon.init \
	  %{_sysconfdir}/lfc-mysql/lfcdaemon.init \
  --slave %{_sysconfdir}/sysconfig/lfcdaemon lfcdaemon.conf \
	  %{_sysconfdir}/lfc-mysql/lfcdaemon.conf \
  --slave %{_sysconfdir}/logrotate.d/lfcdaemon lfcdaemon.logrotate \
	  %{_sysconfdir}/lfc-mysql/lfcdaemon.logrotate \
  --slave %{_sbindir}/lfc-shutdown lfc-shutdown \
	  %{_libdir}/lfc-mysql/lfc-shutdown \
  --slave %{_mandir}/man8/lfc-shutdown.8.gz lfc-shutdown.8.gz \
	  %{_libdir}/lfc-mysql/lfc-shutdown.8.gz

%triggerpostun -n lfc-server-postgres -- lfc-postgres < 1.8.1.2-4
# Restore alternatives removed by lfc-postgres preun
%{_sbindir}/update-alternatives --install %{_sbindir}/lfcdaemon lfcdaemon \
	  %{_libdir}/lfc-postgres/lfcdaemon 10 \
  --slave %{_mandir}/man8/lfcdaemon.8.gz lfcdaemon.8.gz \
	  %{_libdir}/lfc-postgres/lfcdaemon.8.gz \
  --slave %{_datadir}/lfc/NSCONFIG.templ NSCONFIG.templ \
	  %{_libdir}/lfc-postgres/NSCONFIG.templ \
  --slave %{_initrddir}/lfcdaemon lfcdaemon.init \
	  %{_sysconfdir}/lfc-postgres/lfcdaemon.init \
  --slave %{_sysconfdir}/sysconfig/lfcdaemon lfcdaemon.conf \
	  %{_sysconfdir}/lfc-postgres/lfcdaemon.conf \
  --slave %{_sysconfdir}/logrotate.d/lfcdaemon lfcdaemon.logrotate \
	  %{_sysconfdir}/lfc-postgres/lfcdaemon.logrotate \
  --slave %{_sbindir}/lfc-shutdown lfc-shutdown \
	  %{_libdir}/lfc-postgres/lfc-shutdown \
  --slave %{_mandir}/man8/lfc-shutdown.8.gz lfc-shutdown.8.gz \
	  %{_libdir}/lfc-postgres/lfc-shutdown.8.gz

%pre -n lfc-dli
getent group lfcmgr > /dev/null || groupadd -r lfcmgr
getent passwd lfcmgr > /dev/null || useradd -r -g lfcmgr \
    -d %{_localstatedir}/lib/lfc -s /bin/bash -c "LFC Manager" lfcmgr
exit 0

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

%pre -n dpm-server-mysql
getent group dpmmgr > /dev/null || groupadd -r dpmmgr
getent passwd dpmmgr > /dev/null || useradd -r -g dpmmgr \
    -d %{_localstatedir}/lib/dpm -s /bin/bash -c "DPM Manager" dpmmgr
exit 0

%pre -n dpm-server-postgres
getent group dpmmgr > /dev/null || groupadd -r dpmmgr
getent passwd dpmmgr > /dev/null || useradd -r -g dpmmgr \
    -d %{_localstatedir}/lib/dpm -s /bin/bash -c "DPM Manager" dpmmgr
exit 0

%post -n dpm-server-mysql
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm dpm \
	  %{_libdir}/dpm-mysql/dpm 20 \
  --slave %{_mandir}/man8/dpm.8.gz dpm.8.gz \
	  %{_libdir}/dpm-mysql/dpm.8.gz \
  --slave %{_datadir}/dpm/DPMCONFIG.templ DPMCONFIG.templ \
	  %{_libdir}/dpm-mysql/DPMCONFIG.templ \
  --slave %{_initrddir}/dpm dpm.init \
	  %{_sysconfdir}/dpm-mysql/dpm.init \
  --slave %{_sysconfdir}/sysconfig/dpm dpm.conf \
	  %{_sysconfdir}/dpm-mysql/dpm.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm dpm.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpm.logrotate \
  --slave %{_sbindir}/dpm-shutdown dpm-shutdown \
	  %{_libdir}/dpm-mysql/dpm-shutdown \
  --slave %{_mandir}/man8/dpm-shutdown.8.gz dpm-shutdown.8.gz \
	  %{_libdir}/dpm-mysql/dpm-shutdown.8.gz

if [ $1 = 1 ]; then
    if [ -r %{_initrddir}/dpm ]; then
	/sbin/chkconfig --add dpm
    fi
fi

%post -n dpm-server-postgres
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm dpm \
	  %{_libdir}/dpm-postgres/dpm 10 \
  --slave %{_mandir}/man8/dpm.8.gz dpm.8.gz \
	  %{_libdir}/dpm-postgres/dpm.8.gz \
  --slave %{_datadir}/dpm/DPMCONFIG.templ DPMCONFIG.templ \
	  %{_libdir}/dpm-postgres/DPMCONFIG.templ \
  --slave %{_initrddir}/dpm dpm.init \
	  %{_sysconfdir}/dpm-postgres/dpm.init \
  --slave %{_sysconfdir}/sysconfig/dpm dpm.conf \
	  %{_sysconfdir}/dpm-postgres/dpm.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm dpm.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpm.logrotate \
  --slave %{_sbindir}/dpm-shutdown dpm-shutdown \
	  %{_libdir}/dpm-postgres/dpm-shutdown \
  --slave %{_mandir}/man8/dpm-shutdown.8.gz dpm-shutdown.8.gz \
	  %{_libdir}/dpm-postgres/dpm-shutdown.8.gz

if [ $1 = 1 ]; then
    if [ -r %{_initrddir}/dpm ]; then
	/sbin/chkconfig --add dpm
    fi
fi

%triggerpostun -n dpm-server-mysql -- dpm-mysql < 1.8.1.2-4
# Restore alternatives removed by dpm-mysql preun
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm dpm \
	  %{_libdir}/dpm-mysql/dpm 20 \
  --slave %{_mandir}/man8/dpm.8.gz dpm.8.gz \
	  %{_libdir}/dpm-mysql/dpm.8.gz \
  --slave %{_datadir}/dpm/DPMCONFIG.templ DPMCONFIG.templ \
	  %{_libdir}/dpm-mysql/DPMCONFIG.templ \
  --slave %{_initrddir}/dpm dpm.init \
	  %{_sysconfdir}/dpm-mysql/dpm.init \
  --slave %{_sysconfdir}/sysconfig/dpm dpm.conf \
	  %{_sysconfdir}/dpm-mysql/dpm.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm dpm.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpm.logrotate \
  --slave %{_sbindir}/dpm-shutdown dpm-shutdown \
	  %{_libdir}/dpm-mysql/dpm-shutdown \
  --slave %{_mandir}/man8/dpm-shutdown.8.gz dpm-shutdown.8.gz \
	  %{_libdir}/dpm-mysql/dpm-shutdown.8.gz

%triggerpostun -n dpm-server-postgres -- dpm-postgres < 1.8.1.2-4
# Restore alternatives removed by dpm-postgres preun
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm dpm \
	  %{_libdir}/dpm-postgres/dpm 10 \
  --slave %{_mandir}/man8/dpm.8.gz dpm.8.gz \
	  %{_libdir}/dpm-postgres/dpm.8.gz \
  --slave %{_datadir}/dpm/DPMCONFIG.templ DPMCONFIG.templ \
	  %{_libdir}/dpm-postgres/DPMCONFIG.templ \
  --slave %{_initrddir}/dpm dpm.init \
	  %{_sysconfdir}/dpm-postgres/dpm.init \
  --slave %{_sysconfdir}/sysconfig/dpm dpm.conf \
	  %{_sysconfdir}/dpm-postgres/dpm.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm dpm.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpm.logrotate \
  --slave %{_sbindir}/dpm-shutdown dpm-shutdown \
	  %{_libdir}/dpm-postgres/dpm-shutdown \
  --slave %{_mandir}/man8/dpm-shutdown.8.gz dpm-shutdown.8.gz \
	  %{_libdir}/dpm-postgres/dpm-shutdown.8.gz

%preun -n dpm-server-mysql
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpm | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm \
	%{_libdir}/dpm-mysql/dpm
    %{_sbindir}/update-alternatives --display dpm > /dev/null || \
	/sbin/chkconfig --del dpm > /dev/null 2>&1 || :
fi

%preun -n dpm-server-postgres
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpm | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm \
	%{_libdir}/dpm-postgres/dpm
    %{_sbindir}/update-alternatives --display dpm > /dev/null || \
	/sbin/chkconfig --del dpm > /dev/null 2>&1 || :
fi

%postun -n dpm-server-mysql
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpm | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm condrestart > /dev/null 2>&1 || :
fi

%postun -n dpm-server-postgres
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpm | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm condrestart > /dev/null 2>&1 || :
fi

%pre -n dpm-name-server-mysql
getent group dpmmgr > /dev/null || groupadd -r dpmmgr
getent passwd dpmmgr > /dev/null || useradd -r -g dpmmgr \
    -d %{_localstatedir}/lib/dpm -s /bin/bash -c "DPM Manager" dpmmgr
exit 0

%pre -n dpm-name-server-postgres
getent group dpmmgr > /dev/null || groupadd -r dpmmgr
getent passwd dpmmgr > /dev/null || useradd -r -g dpmmgr \
    -d %{_localstatedir}/lib/dpm -s /bin/bash -c "DPM Manager" dpmmgr
exit 0

%post -n dpm-name-server-mysql
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

%{_sbindir}/update-alternatives --install %{_sbindir}/dpnsdaemon dpnsdaemon \
	  %{_libdir}/dpm-mysql/dpnsdaemon 20 \
  --slave %{_mandir}/man8/dpnsdaemon.8.gz dpnsdaemon.8.gz \
	  %{_libdir}/dpm-mysql/dpnsdaemon.8.gz \
  --slave %{_datadir}/dpm/DPNSCONFIG.templ DPNSCONFIG.templ \
	  %{_libdir}/dpm-mysql/DPNSCONFIG.templ \
  --slave %{_initrddir}/dpnsdaemon dpnsdaemon.init \
	  %{_sysconfdir}/dpm-mysql/dpnsdaemon.init \
  --slave %{_sysconfdir}/sysconfig/dpnsdaemon dpnsdaemon.conf \
	  %{_sysconfdir}/dpm-mysql/dpnsdaemon.conf \
  --slave %{_sysconfdir}/logrotate.d/dpnsdaemon dpnsdaemon.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpnsdaemon.logrotate \
  --slave %{_sbindir}/dpns-shutdown dpns-shutdown \
	  %{_libdir}/dpm-mysql/dpns-shutdown \
  --slave %{_mandir}/man8/dpns-shutdown.8.gz dpns-shutdown.8.gz \
	  %{_libdir}/dpm-mysql/dpns-shutdown.8.gz

if [ $1 = 1 ]; then
    if [ -r %{_initrddir}/dpnsdaemon ]; then
	/sbin/chkconfig --add dpnsdaemon
    fi
fi

%post -n dpm-name-server-postgres
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

%{_sbindir}/update-alternatives --install %{_sbindir}/dpnsdaemon dpnsdaemon \
	  %{_libdir}/dpm-postgres/dpnsdaemon 10 \
  --slave %{_mandir}/man8/dpnsdaemon.8.gz dpnsdaemon.8.gz \
	  %{_libdir}/dpm-postgres/dpnsdaemon.8.gz \
  --slave %{_datadir}/dpm/DPNSCONFIG.templ DPNSCONFIG.templ \
	  %{_libdir}/dpm-postgres/DPNSCONFIG.templ \
  --slave %{_initrddir}/dpnsdaemon dpnsdaemon.init \
	  %{_sysconfdir}/dpm-postgres/dpnsdaemon.init \
  --slave %{_sysconfdir}/sysconfig/dpnsdaemon dpnsdaemon.conf \
	  %{_sysconfdir}/dpm-postgres/dpnsdaemon.conf \
  --slave %{_sysconfdir}/logrotate.d/dpnsdaemon dpnsdaemon.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpnsdaemon.logrotate \
  --slave %{_sbindir}/dpns-shutdown dpns-shutdown \
	  %{_libdir}/dpm-postgres/dpns-shutdown \
  --slave %{_mandir}/man8/dpns-shutdown.8.gz dpns-shutdown.8.gz \
	  %{_libdir}/dpm-postgres/dpns-shutdown.8.gz

if [ $1 = 1 ]; then
    if [ -r %{_initrddir}/dpnsdaemon ]; then
	/sbin/chkconfig --add dpnsdaemon
    fi
fi

%triggerpostun -n dpm-name-server-mysql -- dpm-mysql-nameserver < 1.8.1.2-4
# Restore alternatives removed by dpm-mysql-nameserver preun
%{_sbindir}/update-alternatives --install %{_sbindir}/dpnsdaemon dpnsdaemon \
	  %{_libdir}/dpm-mysql/dpnsdaemon 20 \
  --slave %{_mandir}/man8/dpnsdaemon.8.gz dpnsdaemon.8.gz \
	  %{_libdir}/dpm-mysql/dpnsdaemon.8.gz \
  --slave %{_datadir}/dpm/DPNSCONFIG.templ DPNSCONFIG.templ \
	  %{_libdir}/dpm-mysql/DPNSCONFIG.templ \
  --slave %{_initrddir}/dpnsdaemon dpnsdaemon.init \
	  %{_sysconfdir}/dpm-mysql/dpnsdaemon.init \
  --slave %{_sysconfdir}/sysconfig/dpnsdaemon dpnsdaemon.conf \
	  %{_sysconfdir}/dpm-mysql/dpnsdaemon.conf \
  --slave %{_sysconfdir}/logrotate.d/dpnsdaemon dpnsdaemon.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpnsdaemon.logrotate \
  --slave %{_sbindir}/dpns-shutdown dpns-shutdown \
	  %{_libdir}/dpm-mysql/dpns-shutdown \
  --slave %{_mandir}/man8/dpns-shutdown.8.gz dpns-shutdown.8.gz \
	  %{_libdir}/dpm-mysql/dpns-shutdown.8.gz

%triggerpostun -n dpm-name-server-postgres -- dpm-postgres-nameserver < 1.8.1.2-4
# Restore alternatives removed by dpm-postgres-nameserver preun
%{_sbindir}/update-alternatives --install %{_sbindir}/dpnsdaemon dpnsdaemon \
	  %{_libdir}/dpm-postgres/dpnsdaemon 10 \
  --slave %{_mandir}/man8/dpnsdaemon.8.gz dpnsdaemon.8.gz \
	  %{_libdir}/dpm-postgres/dpnsdaemon.8.gz \
  --slave %{_datadir}/dpm/DPNSCONFIG.templ DPNSCONFIG.templ \
	  %{_libdir}/dpm-postgres/DPNSCONFIG.templ \
  --slave %{_initrddir}/dpnsdaemon dpnsdaemon.init \
	  %{_sysconfdir}/dpm-postgres/dpnsdaemon.init \
  --slave %{_sysconfdir}/sysconfig/dpnsdaemon dpnsdaemon.conf \
	  %{_sysconfdir}/dpm-postgres/dpnsdaemon.conf \
  --slave %{_sysconfdir}/logrotate.d/dpnsdaemon dpnsdaemon.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpnsdaemon.logrotate \
  --slave %{_sbindir}/dpns-shutdown dpns-shutdown \
	  %{_libdir}/dpm-postgres/dpns-shutdown \
  --slave %{_mandir}/man8/dpns-shutdown.8.gz dpns-shutdown.8.gz \
	  %{_libdir}/dpm-postgres/dpns-shutdown.8.gz

%preun -n dpm-name-server-mysql
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpnsdaemon | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpnsdaemon stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpnsdaemon \
	%{_libdir}/dpm-mysql/dpnsdaemon
    %{_sbindir}/update-alternatives --display dpnsdaemon > /dev/null || \
	/sbin/chkconfig --del dpnsdaemon > /dev/null 2>&1 || :
fi

%preun -n dpm-name-server-postgres
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpnsdaemon | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpnsdaemon stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpnsdaemon \
	%{_libdir}/dpm-postgres/dpnsdaemon
    %{_sbindir}/update-alternatives --display dpnsdaemon > /dev/null || \
	/sbin/chkconfig --del dpnsdaemon > /dev/null 2>&1 || :
fi

%postun -n dpm-name-server-mysql
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpnsdaemon | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpnsdaemon condrestart > /dev/null 2>&1 || :
fi

%postun -n dpm-name-server-postgres
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpnsdaemon | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpnsdaemon condrestart > /dev/null 2>&1 || :
fi

%pre -n dpm-copy-server-mysql
getent group dpmmgr > /dev/null || groupadd -r dpmmgr
getent passwd dpmmgr > /dev/null || useradd -r -g dpmmgr \
    -d %{_localstatedir}/lib/dpm -s /bin/bash -c "DPM Manager" dpmmgr
exit 0

%pre -n dpm-copy-server-postgres
getent group dpmmgr > /dev/null || groupadd -r dpmmgr
getent passwd dpmmgr > /dev/null || useradd -r -g dpmmgr \
    -d %{_localstatedir}/lib/dpm -s /bin/bash -c "DPM Manager" dpmmgr
exit 0

%post -n dpm-copy-server-mysql
%{_sbindir}/update-alternatives --install %{_sbindir}/dpmcopyd dpmcopyd \
	  %{_libdir}/dpm-mysql/dpmcopyd 20 \
  --slave %{_mandir}/man8/dpmcopyd.8.gz dpmcopyd.8.gz \
	  %{_libdir}/dpm-mysql/dpmcopyd.8.gz \
  --slave %{_initrddir}/dpmcopyd dpmcopyd.init \
	  %{_sysconfdir}/dpm-mysql/dpmcopyd.init \
  --slave %{_sysconfdir}/sysconfig/dpmcopyd dpmcopyd.conf \
	  %{_sysconfdir}/dpm-mysql/dpmcopyd.conf \
  --slave %{_sysconfdir}/logrotate.d/dpmcopyd dpmcopyd.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpmcopyd.logrotate

if [ $1 = 1 ]; then
    if [ -r %{_initrddir}/dpmcopyd ]; then
	/sbin/chkconfig --add dpmcopyd
    fi
fi

%post -n dpm-copy-server-postgres
%{_sbindir}/update-alternatives --install %{_sbindir}/dpmcopyd dpmcopyd \
	  %{_libdir}/dpm-postgres/dpmcopyd 10 \
  --slave %{_mandir}/man8/dpmcopyd.8.gz dpmcopyd.8.gz \
	  %{_libdir}/dpm-postgres/dpmcopyd.8.gz \
  --slave %{_initrddir}/dpmcopyd dpmcopyd.init \
	  %{_sysconfdir}/dpm-postgres/dpmcopyd.init \
  --slave %{_sysconfdir}/sysconfig/dpmcopyd dpmcopyd.conf \
	  %{_sysconfdir}/dpm-postgres/dpmcopyd.conf \
  --slave %{_sysconfdir}/logrotate.d/dpmcopyd dpmcopyd.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpmcopyd.logrotate

if [ $1 = 1 ]; then
    if [ -r %{_initrddir}/dpmcopyd ]; then
	/sbin/chkconfig --add dpmcopyd
    fi
fi

%triggerpostun -n dpm-copy-server-mysql -- dpm-mysql-copyd < 1.8.1.2-4
# Restore alternatives removed by dpm-mysql-copyd preun
%{_sbindir}/update-alternatives --install %{_sbindir}/dpmcopyd dpmcopyd \
	  %{_libdir}/dpm-mysql/dpmcopyd 20 \
  --slave %{_mandir}/man8/dpmcopyd.8.gz dpmcopyd.8.gz \
	  %{_libdir}/dpm-mysql/dpmcopyd.8.gz \
  --slave %{_initrddir}/dpmcopyd dpmcopyd.init \
	  %{_sysconfdir}/dpm-mysql/dpmcopyd.init \
  --slave %{_sysconfdir}/sysconfig/dpmcopyd dpmcopyd.conf \
	  %{_sysconfdir}/dpm-mysql/dpmcopyd.conf \
  --slave %{_sysconfdir}/logrotate.d/dpmcopyd dpmcopyd.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpmcopyd.logrotate

%triggerpostun -n dpm-copy-server-postgres -- dpm-postgres-copyd < 1.8.1.2-4
# Restore alternatives removed by dpm-postgres-copyd preun
%{_sbindir}/update-alternatives --install %{_sbindir}/dpmcopyd dpmcopyd \
	  %{_libdir}/dpm-postgres/dpmcopyd 10 \
  --slave %{_mandir}/man8/dpmcopyd.8.gz dpmcopyd.8.gz \
	  %{_libdir}/dpm-postgres/dpmcopyd.8.gz \
  --slave %{_initrddir}/dpmcopyd dpmcopyd.init \
	  %{_sysconfdir}/dpm-postgres/dpmcopyd.init \
  --slave %{_sysconfdir}/sysconfig/dpmcopyd dpmcopyd.conf \
	  %{_sysconfdir}/dpm-postgres/dpmcopyd.conf \
  --slave %{_sysconfdir}/logrotate.d/dpmcopyd dpmcopyd.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpmcopyd.logrotate

if [ $1 = 1 ]; then
    if [ -r %{_initrddir}/dpmcopyd ]; then
	/sbin/chkconfig --add dpmcopyd
    fi
fi

%preun -n dpm-copy-server-mysql
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpmcopyd | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpmcopyd stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpmcopyd \
	%{_libdir}/dpm-mysql/dpmcopyd
    %{_sbindir}/update-alternatives --display dpmcopyd > /dev/null || \
	/sbin/chkconfig --del dpmcopyd > /dev/null 2>&1 || :
fi

%preun -n dpm-copy-server-postgres
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpmcopyd | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpmcopyd stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpmcopyd \
	%{_libdir}/dpm-postgres/dpmcopyd
    %{_sbindir}/update-alternatives --display dpmcopyd > /dev/null || \
	/sbin/chkconfig --del dpmcopyd > /dev/null 2>&1 || :
fi

%postun -n dpm-copy-server-mysql
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpmcopyd | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpmcopyd condrestart > /dev/null 2>&1 || :
fi

%postun -n dpm-copy-server-postgres
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpmcopyd | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpmcopyd condrestart > /dev/null 2>&1 || :
fi

%pre -n dpm-srm-server-mysql
getent group dpmmgr > /dev/null || groupadd -r dpmmgr
getent passwd dpmmgr > /dev/null || useradd -r -g dpmmgr \
    -d %{_localstatedir}/lib/dpm -s /bin/bash -c "DPM Manager" dpmmgr
exit 0

%pre -n dpm-srm-server-postgres
getent group dpmmgr > /dev/null || groupadd -r dpmmgr
getent passwd dpmmgr > /dev/null || useradd -r -g dpmmgr \
    -d %{_localstatedir}/lib/dpm -s /bin/bash -c "DPM Manager" dpmmgr
exit 0

%post -n dpm-srm-server-mysql
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv1 dpm-srmv1 \
	  %{_libdir}/dpm-mysql/dpm-srmv1 20 \
  --slave %{_mandir}/man8/dpm-srmv1.8.gz dpm-srmv1.8.gz \
	  %{_libdir}/dpm-mysql/dpm-srmv1.8.gz \
  --slave %{_initrddir}/dpm-srmv1 dpm-srmv1.init \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv1.init \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv1 dpm-srmv1.conf \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv1.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv1 dpm-srmv1.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv1.logrotate

%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv2 dpm-srmv2 \
	  %{_libdir}/dpm-mysql/dpm-srmv2 20 \
  --slave %{_mandir}/man8/dpm-srmv2.8.gz dpm-srmv2.8.gz \
	  %{_libdir}/dpm-mysql/dpm-srmv2.8.gz \
  --slave %{_initrddir}/dpm-srmv2 dpm-srmv2.init \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.init \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv2 dpm-srmv2.conf \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv2 dpm-srmv2.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.logrotate

%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv2.2 dpm-srmv2.2 \
	  %{_libdir}/dpm-mysql/dpm-srmv2.2 20 \
  --slave %{_mandir}/man8/dpm-srmv2.2.8.gz dpm-srmv2.2.8.gz \
	  %{_libdir}/dpm-mysql/dpm-srmv2.2.8.gz \
  --slave %{_initrddir}/dpm-srmv2.2 dpm-srmv2.2.init \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.2.init \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv2.2 dpm-srmv2.2.conf \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.2.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv2.2 dpm-srmv2.2.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.2.logrotate

if [ $1 = 1 ]; then
    if [ -r %{_initrddir}/dpm-srmv1 ]; then
	/sbin/chkconfig --add dpm-srmv1;
    fi
    if [ -r %{_initrddir}/dpm-srmv2 ]; then
	/sbin/chkconfig --add dpm-srmv2
    fi
    if [ -r %{_initrddir}/dpm-srmv2.2 ]; then
	/sbin/chkconfig --add dpm-srmv2.2
    fi
fi

%post -n dpm-srm-server-postgres
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv1 dpm-srmv1 \
	  %{_libdir}/dpm-postgres/dpm-srmv1 10 \
  --slave %{_mandir}/man8/dpm-srmv1.8.gz dpm-srmv1.8.gz \
	  %{_libdir}/dpm-postgres/dpm-srmv1.8.gz \
  --slave %{_initrddir}/dpm-srmv1 dpm-srmv1.init \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv1.init \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv1 dpm-srmv1.conf \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv1.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv1 dpm-srmv1.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv1.logrotate

%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv2 dpm-srmv2 \
	  %{_libdir}/dpm-postgres/dpm-srmv2 10 \
  --slave %{_mandir}/man8/dpm-srmv2.8.gz dpm-srmv2.8.gz \
	  %{_libdir}/dpm-postgres/dpm-srmv2.8.gz \
  --slave %{_initrddir}/dpm-srmv2 dpm-srmv2.init \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.init \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv2 dpm-srmv2.conf \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv2 dpm-srmv2.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.logrotate

%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv2.2 dpm-srmv2.2 \
	  %{_libdir}/dpm-postgres/dpm-srmv2.2 10 \
  --slave %{_mandir}/man8/dpm-srmv2.2.8.gz dpm-srmv2.2.8.gz \
	  %{_libdir}/dpm-postgres/dpm-srmv2.2.8.gz \
  --slave %{_initrddir}/dpm-srmv2.2 dpm-srmv2.2.init \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.2.init \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv2.2 dpm-srmv2.2.conf \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.2.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv2.2 dpm-srmv2.2.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.2.logrotate

if [ $1 = 1 ]; then
    if [ -r %{_initrddir}/dpm-srmv1 ]; then
	/sbin/chkconfig --add dpm-srmv1;
    fi
    if [ -r %{_initrddir}/dpm-srmv2 ]; then
	/sbin/chkconfig --add dpm-srmv2
    fi
    if [ -r %{_initrddir}/dpm-srmv2.2 ]; then
	/sbin/chkconfig --add dpm-srmv2.2
    fi
fi

%triggerpostun -n dpm-srm-server-mysql -- dpm-mysql-srmv1 < 1.8.1.2-4
# Restore alternatives removed by dpm-mysql-srmv1 preun
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv1 dpm-srmv1 \
	  %{_libdir}/dpm-mysql/dpm-srmv1 20 \
  --slave %{_mandir}/man8/dpm-srmv1.8.gz dpm-srmv1.8.gz \
	  %{_libdir}/dpm-mysql/dpm-srmv1.8.gz \
  --slave %{_initrddir}/dpm-srmv1 dpm-srmv1.init \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv1.init \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv1 dpm-srmv1.conf \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv1.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv1 dpm-srmv1.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv1.logrotate

%triggerpostun -n dpm-srm-server-mysql -- dpm-mysql-srmv2 < 1.8.1.2-4
# Restore alternatives removed by dpm-mysql-srmv2 preun
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv2 dpm-srmv2 \
	  %{_libdir}/dpm-mysql/dpm-srmv2 20 \
  --slave %{_mandir}/man8/dpm-srmv2.8.gz dpm-srmv2.8.gz \
	  %{_libdir}/dpm-mysql/dpm-srmv2.8.gz \
  --slave %{_initrddir}/dpm-srmv2 dpm-srmv2.init \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.init \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv2 dpm-srmv2.conf \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv2 dpm-srmv2.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.logrotate

%triggerpostun -n dpm-srm-server-mysql -- dpm-mysql-srmv2.2 < 1.8.1.2-4
# Restore alternatives removed by dpm-mysql-srmv22 preun
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv2.2 dpm-srmv2.2 \
	  %{_libdir}/dpm-mysql/dpm-srmv2.2 20 \
  --slave %{_mandir}/man8/dpm-srmv2.2.8.gz dpm-srmv2.2.8.gz \
	  %{_libdir}/dpm-mysql/dpm-srmv2.2.8.gz \
  --slave %{_initrddir}/dpm-srmv2.2 dpm-srmv2.2.init \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.2.init \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv2.2 dpm-srmv2.2.conf \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.2.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv2.2 dpm-srmv2.2.logrotate \
	  %{_sysconfdir}/dpm-mysql/dpm-srmv2.2.logrotate

%triggerpostun -n dpm-srm-server-postgres -- dpm-postgres-srmv1 < 1.8.1.2-4
# Restore alternatives removed by dpm-postgres-srmv1 preun
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv1 dpm-srmv1 \
	  %{_libdir}/dpm-postgres/dpm-srmv1 10 \
  --slave %{_mandir}/man8/dpm-srmv1.8.gz dpm-srmv1.8.gz \
	  %{_libdir}/dpm-postgres/dpm-srmv1.8.gz \
  --slave %{_initrddir}/dpm-srmv1 dpm-srmv1.init \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv1.init \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv1 dpm-srmv1.conf \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv1.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv1 dpm-srmv1.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv1.logrotate

%triggerpostun -n dpm-srm-server-postgres -- dpm-postgres-srmv2 < 1.8.1.2-4
# Restore alternatives removed by dpm-postgres-srmv2 preun
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv2 dpm-srmv2 \
	  %{_libdir}/dpm-postgres/dpm-srmv2 10 \
  --slave %{_mandir}/man8/dpm-srmv2.8.gz dpm-srmv2.8.gz \
	  %{_libdir}/dpm-postgres/dpm-srmv2.8.gz \
  --slave %{_initrddir}/dpm-srmv2 dpm-srmv2.init \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.init \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv2 dpm-srmv2.conf \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv2 dpm-srmv2.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.logrotate

%triggerpostun -n dpm-srm-server-postgres -- dpm-postgres-srmv2.2 < 1.8.1.2-4
# Restore alternatives removed by dpm-postgres-srmv22 preun
%{_sbindir}/update-alternatives --install %{_sbindir}/dpm-srmv2.2 dpm-srmv2.2 \
	  %{_libdir}/dpm-postgres/dpm-srmv2.2 10 \
  --slave %{_mandir}/man8/dpm-srmv2.2.8.gz dpm-srmv2.2.8.gz \
	  %{_libdir}/dpm-postgres/dpm-srmv2.2.8.gz \
  --slave %{_initrddir}/dpm-srmv2.2 dpm-srmv2.2.init \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.2.init \
  --slave %{_sysconfdir}/sysconfig/dpm-srmv2.2 dpm-srmv2.2.conf \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.2.conf \
  --slave %{_sysconfdir}/logrotate.d/dpm-srmv2.2 dpm-srmv2.2.logrotate \
	  %{_sysconfdir}/dpm-postgres/dpm-srmv2.2.logrotate

%preun -n dpm-srm-server-mysql
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv1 | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-srmv1 stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm-srmv1 \
	%{_libdir}/dpm-mysql/dpm-srmv1
    %{_sbindir}/update-alternatives --display dpm-srmv1 > /dev/null || \
	/sbin/chkconfig --del dpm-srmv1 > /dev/null 2>&1 || :

    %{_sbindir}/update-alternatives --display dpm-srmv2 | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-srmv2 stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm-srmv2 \
	%{_libdir}/dpm-mysql/dpm-srmv2
    %{_sbindir}/update-alternatives --display dpm-srmv2 > /dev/null || \
	/sbin/chkconfig --del dpm-srmv2 > /dev/null 2>&1 || :

    %{_sbindir}/update-alternatives --display dpm-srmv2.2 | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-srmv2.2 stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm-srmv2.2 \
	%{_libdir}/dpm-mysql/dpm-srmv2.2
    %{_sbindir}/update-alternatives --display dpm-srmv2.2 > /dev/null || \
	/sbin/chkconfig --del dpm-srmv2.2 > /dev/null 2>&1 || :
fi

%preun -n dpm-srm-server-postgres
export LANG=C

if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv1 | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-srmv1 stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm-srmv1 \
	%{_libdir}/dpm-postgres/dpm-srmv1
    %{_sbindir}/update-alternatives --display dpm-srmv1 > /dev/null || \
	/sbin/chkconfig --del dpm-srmv1 > /dev/null 2>&1 || :

    %{_sbindir}/update-alternatives --display dpm-srmv2 | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-srmv2 stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm-srmv2 \
	%{_libdir}/dpm-postgres/dpm-srmv2
    %{_sbindir}/update-alternatives --display dpm-srmv2 > /dev/null || \
	/sbin/chkconfig --del dpm-srmv2 > /dev/null 2>&1 || :

    %{_sbindir}/update-alternatives --display dpm-srmv2.2 | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-srmv2.2 stop > /dev/null 2>&1 || :
    %{_sbindir}/update-alternatives --remove dpm-srmv2.2 \
	%{_libdir}/dpm-postgres/dpm-srmv2.2
    %{_sbindir}/update-alternatives --display dpm-srmv2.2 > /dev/null || \
	/sbin/chkconfig --del dpm-srmv2.2 > /dev/null 2>&1 || :
fi

%postun -n dpm-srm-server-mysql
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv1 | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-srmv1 condrestart > /dev/null 2>&1 || :

    %{_sbindir}/update-alternatives --display dpm-srmv2 | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-srmv2 condrestart > /dev/null 2>&1 || :

    %{_sbindir}/update-alternatives --display dpm-srmv2.2 | \
	grep currently | grep -q dpm-mysql && \
	/sbin/service dpm-srmv2.2 condrestart > /dev/null 2>&1 || :
fi

%postun -n dpm-srm-server-postgres
export LANG=C

if [ $1 -ge 1 ]; then
    %{_sbindir}/update-alternatives --display dpm-srmv1 | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-srmv1 condrestart > /dev/null 2>&1 || :

    %{_sbindir}/update-alternatives --display dpm-srmv2 | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-srmv2 condrestart > /dev/null 2>&1 || :

    %{_sbindir}/update-alternatives --display dpm-srmv2.2 | \
	grep currently | grep -q dpm-postgres && \
	/sbin/service dpm-srmv2.2 condrestart > /dev/null 2>&1 || :
fi

%post -n dpm-rfio-server
if [ $1 = 1 ]; then
    /sbin/chkconfig --add dpm-rfiod
fi

%preun -n dpm-rfio-server
if [ $1 = 0 ]; then
    /sbin/service dpm-rfiod stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del dpm-rfiod
fi

%postun -n dpm-rfio-server
if [ $1 -ge 1 ]; then
    /sbin/service dpm-rfiod condrestart > /dev/null 2>&1 || :
fi

%files libs
%defattr(-,root,root,-)
%{_libdir}/liblcgdm.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libCsec_plugin_GSI.so
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

%files -n lfc-libs
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

%files -n lfc
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
%verify() %{_sysconfdir}/ld.so.conf.d/lfc-python.conf

%if %{?altpython:1}%{!?altpython:0}
%files -n lfc-%{altpython}
%defattr(-,root,root,-)
%{altpython_sitearch}/_lfc.*so
%{altpython_sitearch}/lfc.py*
%{altpython_sitearch}/_lfcthr.*so
%{altpython_sitearch}/lfcthr.py*
%{altpython_sitearch}/_lfc2.*so
%{altpython_sitearch}/lfc2.py*
%{altpython_sitearch}/_lfc2thr.*so
%{altpython_sitearch}/lfc2thr.py*
%if %{?fedora}%{!?fedora:0} >= 15
%{altpython_sitearch}/__pycache__/lfc*
%endif
%verify() %{_sysconfdir}/ld.so.conf.d/lfc-%{altpython}.conf
%endif

%files -n lfc-server-mysql
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
%{_sysconfdir}/lfc-mysql/lfcdaemon.init
%ghost %{_initrddir}/lfcdaemon
%config(noreplace) %{_sysconfdir}/lfc-mysql/lfcdaemon.conf
%ghost %{_sysconfdir}/sysconfig/lfcdaemon
%config(noreplace) %{_sysconfdir}/lfc-mysql/lfcdaemon.logrotate
%ghost %{_sysconfdir}/logrotate.d/lfcdaemon
%dir %{_datadir}/lfc
%{_datadir}/lfc/create_lfc_tables_mysql.sql
%attr(-,lfcmgr,lfcmgr) %{_localstatedir}/log/lfc
%attr(-,lfcmgr,lfcmgr) %{_localstatedir}/lib/lfc
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/lfcmgr
%doc lfc-mysql/%{name}-%{version}/ns/README.Fedora

%files -n lfc-server-postgres
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
%{_sysconfdir}/lfc-postgres/lfcdaemon.init
%ghost %{_initrddir}/lfcdaemon
%config(noreplace) %{_sysconfdir}/lfc-postgres/lfcdaemon.conf
%ghost %{_sysconfdir}/sysconfig/lfcdaemon
%config(noreplace) %{_sysconfdir}/lfc-postgres/lfcdaemon.logrotate
%ghost %{_sysconfdir}/logrotate.d/lfcdaemon
%dir %{_datadir}/lfc
%{_datadir}/lfc/create_lfc_tables_postgres.sql
%attr(-,lfcmgr,lfcmgr) %{_localstatedir}/log/lfc
%attr(-,lfcmgr,lfcmgr) %{_localstatedir}/lib/lfc
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/lfcmgr
%doc lfc-postgres/%{name}-%{version}/ns/README.Fedora

%files -n lfc-dli
%defattr(-,root,root,-)
%{_sbindir}/lfc-dli
%doc %{_mandir}/man8/lfc-dli.8*
%{_initrddir}/lfc-dli
%config(noreplace) %{_sysconfdir}/sysconfig/lfc-dli
%config(noreplace) %{_sysconfdir}/logrotate.d/lfc-dli
%dir %{_datadir}/lfc
%{_datadir}/lfc/lcg-info-provider-lfc
%attr(-,lfcmgr,lfcmgr) %{_localstatedir}/log/lfc-dli
%attr(-,lfcmgr,lfcmgr) %{_localstatedir}/lib/lfc

%files -n dpm-libs
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

%files -n dpm
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
%{altpython_sitearch}/_dpm.*so
%{altpython_sitearch}/dpm.py*
%{altpython_sitearch}/_dpm2.*so
%{altpython_sitearch}/dpm2.py*
%if %{?fedora}%{!?fedora:0} >= 15
%{altpython_sitearch}/__pycache__/dpm*
%endif
%endif

%files -n dpm-server-mysql
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
%{_sysconfdir}/dpm-mysql/dpm.init
%ghost %{_initrddir}/dpm
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

%files -n dpm-server-postgres
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
%{_sysconfdir}/dpm-postgres/dpm.init
%ghost %{_initrddir}/dpm
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

%files -n dpm-name-server-mysql
%defattr(-,root,root,-)
%dir %{_libdir}/dpm-mysql
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
%dir %{_sysconfdir}/dpm-mysql
%{_sysconfdir}/dpm-mysql/dpnsdaemon.init
%ghost %{_initrddir}/dpnsdaemon
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpnsdaemon.conf
%ghost %{_sysconfdir}/sysconfig/dpnsdaemon
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpnsdaemon.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpnsdaemon
%dir %{_datadir}/dpm
%{_datadir}/dpm/create_dpns_tables_mysql.sql
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpns
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/lib/dpm
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/dpmmgr
%doc dpm-mysql/%{name}-%{version}/ns/README.Fedora

%files -n dpm-name-server-postgres
%defattr(-,root,root,-)
%dir %{_libdir}/dpm-postgres
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
%dir %{_sysconfdir}/dpm-postgres
%{_sysconfdir}/dpm-postgres/dpnsdaemon.init
%ghost %{_initrddir}/dpnsdaemon
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpnsdaemon.conf
%ghost %{_sysconfdir}/sysconfig/dpnsdaemon
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpnsdaemon.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpnsdaemon
%dir %{_datadir}/dpm
%{_datadir}/dpm/create_dpns_tables_postgres.sql
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpns
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/lib/dpm
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/dpmmgr
%doc dpm-postgres/%{name}-%{version}/ns/README.Fedora

%files -n dpm-copy-server-mysql
%defattr(-,root,root,-)
%dir %{_libdir}/dpm-mysql
%{_libdir}/dpm-mysql/dpmcopyd
%ghost %{_sbindir}/dpmcopyd
%doc %{_libdir}/dpm-mysql/dpmcopyd.8*
%ghost %{_mandir}/man8/dpmcopyd.8*
%dir %{_sysconfdir}/dpm-mysql
%{_sysconfdir}/dpm-mysql/dpmcopyd.init
%ghost %{_initrddir}/dpmcopyd
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpmcopyd.conf
%ghost %{_sysconfdir}/sysconfig/dpmcopyd
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpmcopyd.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpmcopyd
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpmcopy
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/lib/dpm
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/dpmmgr

%files -n dpm-copy-server-postgres
%defattr(-,root,root,-)
%dir %{_libdir}/dpm-postgres
%{_libdir}/dpm-postgres/dpmcopyd
%ghost %{_sbindir}/dpmcopyd
%doc %{_libdir}/dpm-postgres/dpmcopyd.8*
%ghost %{_mandir}/man8/dpmcopyd.8*
%dir %{_sysconfdir}/dpm-postgres
%{_sysconfdir}/dpm-postgres/dpmcopyd.init
%ghost %{_initrddir}/dpmcopyd
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpmcopyd.conf
%ghost %{_sysconfdir}/sysconfig/dpmcopyd
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpmcopyd.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpmcopyd
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpmcopy
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/lib/dpm
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/dpmmgr

%files -n dpm-srm-server-mysql
%defattr(-,root,root,-)
%dir %{_libdir}/dpm-mysql
%{_libdir}/dpm-mysql/dpm-srmv1
%{_libdir}/dpm-mysql/dpm-srmv2
%{_libdir}/dpm-mysql/dpm-srmv2.2
%ghost %{_sbindir}/dpm-srmv1
%ghost %{_sbindir}/dpm-srmv2
%ghost %{_sbindir}/dpm-srmv2.2
%doc %{_libdir}/dpm-mysql/dpm-srmv1.8*
%doc %{_libdir}/dpm-mysql/dpm-srmv2.8*
%doc %{_libdir}/dpm-mysql/dpm-srmv2.2.8*
%ghost %{_mandir}/man8/dpm-srmv1.8*
%ghost %{_mandir}/man8/dpm-srmv2.8*
%ghost %{_mandir}/man8/dpm-srmv2.2.8*
%dir %{_sysconfdir}/dpm-mysql
%{_sysconfdir}/dpm-mysql/dpm-srmv1.init
%{_sysconfdir}/dpm-mysql/dpm-srmv2.init
%{_sysconfdir}/dpm-mysql/dpm-srmv2.2.init
%ghost %{_initrddir}/dpm-srmv1
%ghost %{_initrddir}/dpm-srmv2
%ghost %{_initrddir}/dpm-srmv2.2
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpm-srmv1.conf
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpm-srmv2.conf
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpm-srmv2.2.conf
%ghost %{_sysconfdir}/sysconfig/dpm-srmv1
%ghost %{_sysconfdir}/sysconfig/dpm-srmv2
%ghost %{_sysconfdir}/sysconfig/dpm-srmv2.2
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpm-srmv1.logrotate
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpm-srmv2.logrotate
%config(noreplace) %{_sysconfdir}/dpm-mysql/dpm-srmv2.2.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpm-srmv1
%ghost %{_sysconfdir}/logrotate.d/dpm-srmv2
%ghost %{_sysconfdir}/logrotate.d/dpm-srmv2.2
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpm-srmv1
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpm-srmv2
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpm-srmv2.2
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/lib/dpm
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/dpmmgr

%files -n dpm-srm-server-postgres
%defattr(-,root,root,-)
%dir %{_libdir}/dpm-postgres
%{_libdir}/dpm-postgres/dpm-srmv1
%{_libdir}/dpm-postgres/dpm-srmv2
%{_libdir}/dpm-postgres/dpm-srmv2.2
%ghost %{_sbindir}/dpm-srmv1
%ghost %{_sbindir}/dpm-srmv2
%ghost %{_sbindir}/dpm-srmv2.2
%doc %{_libdir}/dpm-postgres/dpm-srmv1.8*
%doc %{_libdir}/dpm-postgres/dpm-srmv2.8*
%doc %{_libdir}/dpm-postgres/dpm-srmv2.2.8*
%ghost %{_mandir}/man8/dpm-srmv1.8*
%ghost %{_mandir}/man8/dpm-srmv2.8*
%ghost %{_mandir}/man8/dpm-srmv2.2.8*
%dir %{_sysconfdir}/dpm-postgres
%{_sysconfdir}/dpm-postgres/dpm-srmv1.init
%{_sysconfdir}/dpm-postgres/dpm-srmv2.init
%{_sysconfdir}/dpm-postgres/dpm-srmv2.2.init
%ghost %{_initrddir}/dpm-srmv1
%ghost %{_initrddir}/dpm-srmv2
%ghost %{_initrddir}/dpm-srmv2.2
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpm-srmv1.conf
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpm-srmv2.conf
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpm-srmv2.2.conf
%ghost %{_sysconfdir}/sysconfig/dpm-srmv1
%ghost %{_sysconfdir}/sysconfig/dpm-srmv2
%ghost %{_sysconfdir}/sysconfig/dpm-srmv2.2
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpm-srmv1.logrotate
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpm-srmv2.logrotate
%config(noreplace) %{_sysconfdir}/dpm-postgres/dpm-srmv2.2.logrotate
%ghost %{_sysconfdir}/logrotate.d/dpm-srmv1
%ghost %{_sysconfdir}/logrotate.d/dpm-srmv2
%ghost %{_sysconfdir}/logrotate.d/dpm-srmv2.2
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpm-srmv1
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpm-srmv2
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/log/dpm-srmv2.2
%attr(-,dpmmgr,dpmmgr) %{_localstatedir}/lib/dpm
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/dpmmgr

%files -n dpm-rfio-server
%defattr(-,root,root,-)
%{_sbindir}/dpm-rfiod
%{_initrddir}/dpm-rfiod
%config(noreplace) %{_sysconfdir}/sysconfig/dpm-rfiod
%config(noreplace) %{_sysconfdir}/logrotate.d/dpm-rfiod
%{_localstatedir}/log/dpm-rfio
%doc %{_mandir}/man8/dpm-rfiod.8*

%changelog
* Thu Apr 12 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.8.1.2-6
- Fix dummy /etc/ld.so.conf.d file on el6

* Mon Mar 05 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.8.1.2-5
- Add dummy /etc/ld.so.conf.d files so the package will be considered multilib.

* Wed Dec 1 2011 Alain Roy <roy@cs.wisc.edu> - 1.8.1.2-4
- Packaging change only: fixed "Obsoletes"

* Wed Nov 30 2011 Alain Roy <roy@cs.wisc.edu> - 1.8.1.2-3
- Rebuilt. We had already used -2 internally for a rebuild, so bumped version. No other changes.

* Thu Nov 10 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.8.1.2-2
- Implement new package names agreed with upstream

* Fri Sep 02 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.8.1.2-1
- Update to version 1.8.1.2
- Drop patches lcgdm-withsoname.patch and lcgdm-gsoap.patch (upstream)

* Mon Jun 20 2011 Petr Sabata <contyk@redhat.com> - 1.8.0.1-8
- Perl mass rebuild

* Wed Mar 23 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.8.0.1-7
- Rebuild for mysql 5.5.10

* Sat Feb 12 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.8.0.1-6
- Fix duplicate files introduced by the PEP 3149 update

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 David Malcolm <dmalcolm@redhat.com> - 1.8.0.1-4
- update build of python bindings to reflect PEP 3149 in the latest python 3.2,
  which changes the extension of python modules, and the library SONAME

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
