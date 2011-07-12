Name:           osg-discovery
Version:        1.0.6
Release:        1
Summary:        OSG Discovery Tools
Group:          System Environment
License:        Stanford (modified BSD with advert clause)
URL:            http://code.google.com/p/osg-discovery/

Source:        discovery-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-root
BuildRequires:  maven2
Requires:  java

%description
DSI module and POSIX preload libraries for Xrootd

%prep
%setup -q -n %{name}

%build
# To download source
# svn checkout https://osg-discovery.googlecode.com/svn/osg/xpathsearch/trunk/  osg-discovery --username doug.strain

mvn -Pdev package assembly:attached

%install


%changelog
* Mon Jul 12 2011 Doug Strain <dstrain@fnal.gov> 1.0.6
Initial creation of spec file
