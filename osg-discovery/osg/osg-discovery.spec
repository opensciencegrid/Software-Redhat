Name:           osg-discovery
Version:        1.0.7
Release:        1
Summary:        OSG Discovery Tools
Group:          System Environment
License:        Stanford (modified BSD with advert clause)
URL:            http://code.google.com/p/osg-discovery/

Source:        osg-discovery.tar.gz

BuildRoot:      %{_tmppath}/%{name}-root
#BuildRequires:  maven2
Requires:  java

%description
DSI module and POSIX preload libraries for Xrootd

%prep
%setup -q -n %{name}

%build
# To download source
# svn checkout https://osg-discovery.googlecode.com/svn/osg/xpathsearch/trunk/  osg-discovery --username doug.strain
pushd osg
pushd discovery
mvn -Pdev package assembly:attached
popd
popd
tar xzvf osg/discovery/target/discovery-*.tar.gz
mv discovery-1.0-r* discovery-built

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}

pushd discovery-built
for i in `ls bin`; do
	install -m 0755 bin/$i $RPM_BUILD_ROOT%{_bindir}
done
for i in `ls lib`; do
	install -m 0644 lib/$i $RPM_BUILD_ROOT%{_javadir}/%{name}
done
install -m 0644 conf/xpathsearch.properties $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -m 0644 conf/xpathsearch.rc $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
popd

mkdir -p $RPM_BUILD_ROOT/var/run/%{name}
mkdir -p $RPM_BUILD_ROOT/var/log/%{name}

%files
%{_bindir}/*
%{_javadir}/%{name}/*
%{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/xpathsearch.rc
%{_sysconfdir}/%{name}/xpathsearch.properties
/var/run/%{name}
/var/log/%{name}


%changelog
* Mon Jul 12 2011 Doug Strain <dstrain@fnal.gov> 1.0.6
Initial creation of spec file
