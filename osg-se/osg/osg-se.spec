Name:           OSG-SE
Version:        1.0
Release:        1
Summary:        OSG Storage Element package for RPM distribution
Group:          System Environment/Daemons
License:        GPL
URL:            https://twiki.grid.iu.edu/twiki/bin/view/Storage/WebHome
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
Open Science Grid Storage Element pacakge for RPM distribution

Requires: java-1.6.0-sun-compat
Requires: bestman2-client
Requires: bestman2-libs
Requires: bestman2-server
Requires: gratia-probe
Requires: dcache-srmclient
Requires: osg-ca-certs
Requires: edg-mkgridmap
Requires: fetch-crl
Requires: globus-gridftp-server
Requires: gums

#%prep

#%setup -q -n %{name}

#%build

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files

%changelog
* Wed Jul 20 12:38:22 PDT 2011 Alex Sim <asim@lbl.gov>
- Created an initial osg-se RPM
