%ifarch alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64pthr
%else
%global flavor gcc32pthr
%endif

Name:		globus-gatekeeper
%global _name %(tr - _ <<< %{name})
Version:	5.7
%global setupversion 2.2
Release:	5%{?dist}
Summary:	Globus Toolkit - Globus Gatekeeper

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
#		Source is extracted from the globus toolkit installer:
#		wget -N http://www-unix.globus.org/ftppub/gt5/5.0/5.0.3/installers/src/gt5.0.3-all-source-installer.tar.bz2
#		tar -jxf gt5.0.3-all-source-installer.tar.bz2
#		mv gt5.0.3-all-source-installer/source-trees/gatekeeper/source globus_gatekeeper-5.7
#		cp -p gt5.0.3-all-source-installer/source-trees/core/source/GLOBUS_LICENSE globus_gatekeeper-5.7
#		tar -zcf globus_gatekeeper-5.7.tar.gz globus_gatekeeper-5.7
Source:		%{_name}-%{version}.tar.gz
#		Source1 is extracted from the globus toolkit installer:
#		wget -N http://www-unix.globus.org/ftppub/gt5/5.0/5.0.3/installers/src/gt5.0.3-all-source-installer.tar.bz2
#		tar -jxf gt5.0.3-all-source-installer.tar.bz2
#		mv gt5.0.3-all-source-installer/source-trees/gatekeeper/setup globus_gatekeeper_setup-2.2
#		cp -p gt5.0.3-all-source-installer/source-trees/core/source/GLOBUS_LICENSE globus_gatekeeper_setup-2.2
#		tar -zcf globus_gatekeeper_setup-2.2.tar.gz globus_gatekeeper_setup-2.2
Source1:	%{_name}_setup-%{setupversion}.tar.gz
Source2:	%{name}
Source3:	%{name}.README
#		README file
Source8:	GLOBUS-GRAM5

Source9:        %{name}.sysconfig
#		Fixes for FHS installation:
#		http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=6820
Patch0:		%{name}.patch
#		Fixes for FHS installation:
#		http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=6821
Patch1:		%{name}-setup.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:	%{name}-setup = %{setupversion}
Requires:	globus-common >= 11.5
Requires:	globus-common-setup >= 2
Requires:	globus-gatekeeper-setup >= 2
BuildRequires:	grid-packaging-tools
BuildRequires:	globus-gss-assist-devel%{?_isa} >= 3
BuildRequires:	globus-gssapi-gsi-devel%{?_isa} >= 4
BuildRequires:	globus-core%{?_isa} >= 4

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
Globus Gatekeeper
Globus Gatekeeper Setup

%prep
%setup -q -n %{_name}-%{version}
%setup -D -T -q -n %{_name}-%{version} -a 1
%patch0 -p1
cd %{_name}_setup-%{setupversion}
%patch1 -p1
cd -

%build
# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache

%{_datadir}/globus/globus-bootstrap.sh

%configure --with-flavor=%{flavor}

make %{?_smp_mflags}

# setup package
cd %{_name}_setup-%{setupversion}

# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache

%{_datadir}/globus/globus-bootstrap.sh

%configure --without-flavor

make %{?_smp_mflags}

cd -

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# setup package
cd %{_name}_setup-%{setupversion}
make install DESTDIR=$RPM_BUILD_ROOT
cd -

# Register setup
perl -MGrid::GPT::Setup <<EOF
my \$metadata = new Grid::GPT::Setup(package_name => "%{_name}_setup",
				     globusdir => "$RPM_BUILD_ROOT%{_prefix}");
\$metadata->finish();
EOF

# This script is intended to be sourced, not executed
chmod 644 $RPM_BUILD_ROOT%{_datadir}/globus/setup/setup-globus-gatekeeper.pl

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages

# Install start-up script
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -p %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}

# Install sysconfig defaults
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -p %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/globus-gatekeeper

# Install license file
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m 644 -p GLOBUS_LICENSE $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# Install README file
install -m 644 -p %{SOURCE8} \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/README

# Install post installation instructions
install -m 644 -p %{SOURCE3} \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/README.Fedora

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
    $GLOBUSPACKAGEDIR/%{_name}_setup/noflavor_pgm.filelist \
  | sed -e s!^!%{_prefix}! -e 's!.*/man/.*!%doc &*!' > package.filelist

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 = 1 ]; then
    /sbin/chkconfig --add %{name}
fi

%preun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/GLOBUS_LICENSE
%doc %{_docdir}/%{name}-%{version}/README
%dir %{_datadir}/globus/packages/%{_name}_setup
%{_datadir}/globus/packages/setup/%{_name}_setup
%{_initrddir}/%{name}
%doc %{_docdir}/%{name}-%{version}/README.Fedora

%changelog
* Sun Jul 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 5.7-5
- Add a sysconfig environment script.

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.7-4
- Add README file

* Tue Apr 19 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.7-3
- Add start-up script and README.Fedora file

* Mon Feb 28 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.7-2
- Fix typos in the setup patch

* Thu Feb 24 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.7-1
- Update to Globus Toolkit 5.0.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-2
- Simplify directory ownership

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-1
- Update to Globus Toolkit 5.0.1

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.3-1
- Update to Globus Toolkit 5.0.0

* Wed Jul 29 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0-1
- Autogenerated
