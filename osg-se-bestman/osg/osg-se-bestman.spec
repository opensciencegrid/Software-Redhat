Name:           osg-se-bestman
Summary:        OSG BeStMan Storage Element package for RPM distribution
Version:        3.0.0
Release:        1
License:        GPL
Group:          System Environment/Daemons
URL:            https://twiki.grid.iu.edu/twiki/bin/view/Storage/WebHome
BuildArch:      noarch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# from VDT
Requires: java-1.6.0-sun-compat
Requires: bestman2-client
Requires: bestman2-libs
Requires: bestman2-server
Requires: dcache-srmclient
Requires: osg-ca-certs
Requires: edg-mkgridmap
Requires: fetch-crl
# from EPEL
Requires: globus-gridftp-server-progs
# These are not there yet
#Requires: gratia-probe
#Requires: gums

%description
%{summary}


%install

%clean
rm -rf $RPM_BUILD_ROOT

%files


%changelog
* Wed Jul 20 2011 Alex Sim <asim@lbl.gov>
- Created an initial osg-se-bestman RPM
