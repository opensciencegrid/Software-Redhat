Name:           osg-se-bestman
Summary:        OSG BeStMan Storage Element package for RPM distribution
Version:        3.0.0
Release:        3
License:        GPL
Group:          System Environment/Daemons
URL:            https://twiki.grid.iu.edu/twiki/bin/view/Storage/WebHome
BuildArch:      noarch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# from VDT
Requires: java-1.6.0-sun-compat
Requires: bestman2-server
Requires: dcache-srmclient
Requires: grid-certificates
Requires: edg-mkgridmap
Requires: fetch-crl
Requires: gratia-probe-gridftp-transfer
Requires: gums
Requires: gums-client
# from EPEL
Requires: globus-gridftp-server-progs

%description
%{summary}


%install

%clean
rm -rf $RPM_BUILD_ROOT

%files


%changelog
* Thu Aug 11 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-3
- Require virtual dep grid-certificates, not actual package osg-ca-certs.

* Wed Jul 20 2011 Alex Sim <asim@lbl.gov>
- Created an initial osg-se-bestman RPM
