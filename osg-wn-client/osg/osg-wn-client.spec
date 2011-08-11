
Name:      osg-wn-client
Summary:   OSG Worker-Node Client
Version:   3.0.0
Release:   8
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: java-1.6.0-sun-compat
Requires: /usr/bin/curl
Requires: /usr/bin/dccp
Requires: dcap-tunnel-gsi
Requires: edg-gridftp-client
Requires: glite-fts-client
Requires: lcg-utils
Requires: lfc-client
Requires: myproxy
Requires: /usr/bin/ldapsearch
Requires: dcache-srmclient
Requires: bestman2-client
Requires: /usr/bin/uberftp
Requires: /usr/bin/wget
Requires: grid-certificates
Requires: fetch-crl
Requires: osg-system-profiler
Requires: vo-client

%description
%{summary}

%package glexec
Summary: OSG meta-package for glexec
Group: Grid
Requires: %{name} = %{version}-%{release}
Requires: glexec
Requires: lcmaps-plugins-glexec-tracking
Requires: lcmaps-plugins-basic
Requires: lcmaps-plugins-gums
Requires: lcmaps-plugins-saz
Requires: lcmaps-plugins-verify-proxy

%description glexec
%{summary}

%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/osg/wn-client/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/osg/wn-client/setup.sh << EOF
#!/bin/sh

# You no longer need to source $OSG_GRID/setup.sh
# However, this file has been left for backward compatibility purposes.

EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %{_sysconfdir}/osg/wn-client
%config(noreplace) %{_sysconfdir}/osg/wn-client/setup.sh

%files glexec

%changelog
* Thu Aug 11 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-8
- Require virtual dep grid-certificates, not actual package osg-ca-certs.

* Thu Aug 04 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0.0-7
- Added vo-client to dependencies

* Wed Aug 03 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-6
- Correct plugin names in the glexec meta-package.

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-5
Update to reflect current plugin names.

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-4
Add glexec sub-package.

* Thu Jul 14 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0.0-3
- Added dcap-tunnel-gsi to list of dependencies

* Fri Jul 08 2011 Derek Weitzel <dweitzel@cse.unl.edu> 3.0.0-2
- Added fetch-crl dependency

* Wed Jul  6 2011 Brian Bockelman <bbockelm@cse.unl.edu> 3.0.0-1
- Bump to correct version number.
- Add osg-ca-certs to the requires.
- Re-added the pegasus worker node client.

* Fri Jul  1 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.0-1
- Created an initial osg-wn-client RPM.
- Not all deps actually exist: just giving us a target to strive for.

