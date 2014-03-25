Name:      osg-wn-client
Summary:   OSG Worker-Node Client
Version:   3.0.0
Release:   20%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Java included because users expect it to be available
Requires: jpackage-utils
Requires: java7-devel 

Requires: /usr/bin/curl
Requires: /usr/bin/dccp
Requires: dcap-tunnel-gsi
Requires: edg-gridftp-client
Requires: glite-fts-client
Requires: lcg-util
Requires: lfc-client
Requires: lfc-python
Requires: myproxy
Requires: /usr/bin/ldapsearch
Requires: dcache-srmclient
Requires: bestman2-client
Requires: /usr/bin/uberftp
Requires: /usr/bin/wget
Requires: grid-certificates
%if 0%{?rhel} < 6
Requires: fetch-crl3
%else
Requires: fetch-crl
%endif
Requires: osg-system-profiler
Requires: vo-client
Requires: osg-version
Requires: globus-gass-copy-progs

%description
%{summary}

%package glexec
Summary: OSG Worker-Node client meta-package for glexec
Group: Grid
Requires: %{name} = %{version}-%{release}
Requires: glexec
Requires: glexec-wrapper-scripts
Requires: gratia-probe-glexec
Requires: mkgltempdir

%description glexec
%{summary}

%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/osg/wn-client/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/osg/wn-client/setup.sh << EOF
#!/bin/sh

# You no longer need to source \$OSG_GRID/setup.sh
# However, this file has been left for backward compatibility purposes.

EOF

cat > $RPM_BUILD_ROOT%{_sysconfdir}/osg/wn-client/setup.csh << EOF
#!/bin/csh

# You no longer need to source \$OSG_GRID/setup.csh
# However, this file has been left for backward compatibility purposes.

EOF

mkdir -p $RPM_BUILD_ROOT%{_prefix}/etc/
cat > $RPM_BUILD_ROOT%{_prefix}/etc/globus-user-env.sh << EOF
#!/bin/sh

# This file is expected by gLite jobs because GLOBUS_LOCATION 
# defaults to /usr, and they're looking for 
# $GLOBUS_LOCATION/etc/globus-user-env.sh. It doesn't need to have
# anything, it just needs to be there. 

EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %{_sysconfdir}/osg/wn-client
%config(noreplace) %{_sysconfdir}/osg/wn-client/setup.sh
%config(noreplace) %{_sysconfdir}/osg/wn-client/setup.csh
%config(noreplace) %{_prefix}/etc/globus-user-env.sh

%files glexec

%changelog
* Tue Mar 25 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-20
- Update lcg-utils requirement to lcg-util (SOFTWARE-1373)

* Wed Apr 03 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-19.osg
- Update to require java7-devel and jpackage-utils

* Fri Feb 22 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-18.osg
- Update rhel5 to require fetch-crl3 instead of fetch-crl.

* Fri Jan 03 2013 Dave Dykstra <dwd@fnal.gov> - 3.0.0-17.osg
- Added mkgltempdir as osg-wn-client-glexec requirement

* Wed Jul 25 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.0-16.osg
- Add explicit dependency on globus-gass-copy-progs (for globus-url-copy)

* Thu Mar 08 2012 Dave Dykstra <dwd@fnal.gov> - 3.0.0-15.osg
- Rebuild after merging to trunk

* Mon Feb 27 2012 Dave Dykstra <dwd@fnal.gov> - 3.0.0-14.osg
- Added glexec-wrapper-scripts requirement on glexec

* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-13
- Added dependency on osg-version

* Mon Oct 24 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-12
- Added dependency on on lfc-python (Needed by ATLAS)
- Added /usr/etc/globus-user-env.sh, which is needed by 
  gLite jobs.

* Tue Oct 11 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-11
- Added setup.csh to match setup.sh, just in case someone
  needs it.

* Mon Aug 22 2011 Dave Dykstra <dwd@fnal.gov> - 3.0.0-10
- Remove lcmaps-plugins-glexec-tracking from osg-wn-client-glexec
  Requires because it has been moved down to glexec instead

* Mon Aug 22 2011 Dave Dykstra <dwd@fnal.gov> - 3.0.0-9
- Remove redundant Requires from osg-wn-client-glexec which were
  already Required by lcmaps (which is Required by glexec).
- Added gratia-probe-glexec as Required by osg-wn-client-glexec

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

