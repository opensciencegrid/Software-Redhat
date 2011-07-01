
Name:      osg-wn-client
Summary:   OSG Worker-Node Client
Version:   2.0.0
Release:   1
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

%description
%{summary}

Requires: /usr/bin/curl
Requires: /usr/bin/dccp
Requires: edg-gridftp-client
Requires: fetch-crl
Requires: glite-fts-client
Requires: lcg-utils
Requires: lfc-client
Requires: myproxy
Requires: /usr/bin/ldapsearch
Requires: srm-fnal
Requires: bestman2-client
Requires: /usr/bin/uberftp
Requires: /usr/bin/wget

%changelog
* Fri Jul 1 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.0-1
- Created an initial osg-wn-client RPM.
- Not all deps actually exist: just giving us a target to strive for.

