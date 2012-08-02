Name:		netlogger
Version:	4.2.0
Release:	3%{?dist}
Summary:	Netlogger toolkit

Group:		Productivity/File utilities
License:	LBNL.  See http://netlogger.lbl.gov/software/netlogger-license
URL:		http://netlogger.lbl.gov/
# Retrieved on Mon Aug 22 2011
# svn export https://bosshog.lbl.gov/repos/netlogger/trunk/python netlogger_trunk
# cd netlogger_trunk
# python setup.py sdist
Source0:        netlogger-trunk.tar.gz

Patch0:         remove_setuptools.patch
Patch1:         gridftp_auth.patch

BuildArch:      noarch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  python

%description
%{summary}

%prep
%setup -n netlogger-trunk
%patch0 -p0
%patch1 -p0

%build

cat > setup.cfg << EOF
[install]
optimize=1
EOF

python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root,-)

%changelog
* Thu Aug 2 2012 Neha Sharma <neha@fnal.gov> - 4.2.0-3
- Fixed patch for gridftp_auth parser module
* Wed Mar 21 2012 Neha Sharma <neha@fnal.gov> - 4.2.0-2
- Patch for gridftp_auth parser module
* Mon Aug 22 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 4.2.0-1
- Initial creation of netlogger RPM.
