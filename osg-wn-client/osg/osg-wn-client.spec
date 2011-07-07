
Name:      osg-wn-client
Summary:   OSG Worker-Node Client
Version:   3.0.0
Release:   1
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: /usr/bin/curl
Requires: /usr/bin/dccp
Requires: edg-gridftp-client
Requires: fetch-crl
Requires: glite-fts-client
Requires: lcg-utils
Requires: lfc-client
Requires: myproxy
Requires: /usr/bin/ldapsearch
Requires: SRM-Client-Fermi
Requires: bestman2-client
Requires: /usr/bin/uberftp
Requires: /usr/bin/wget
Requires: osg-ca-certs
Requires: pegasus

%description
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

%changelog
* Wed Jul  6 2011 Brian Bockelman <bbockelm@cse.unl.edu> 3.0.0-1
- Bump to correct version number.
- Add osg-ca-certs to the requires.
- Re-added the pegasus worker node client.

* Fri Jul  1 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.0-1
- Created an initial osg-wn-client RPM.
- Not all deps actually exist: just giving us a target to strive for.

