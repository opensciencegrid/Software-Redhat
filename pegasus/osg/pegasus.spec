Name:           pegasus
Version:        3.0.3
Release:        2%{?dist}
Summary:        Pegasus Workload Management System
Group:          Applications/System
License:        ASL 2.0
URL:            http://pegasus.isi.edu/index.php

Source:        pegasus-source-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-root
BuildRequires:  ant ant-optional ant-apache-regexp java gcc groff python-devel jpackage-utils-compat-el5 gcc-c++
Requires:  java >= 1.6, python >= 2.4, condor >= 7.4

%define sourcedir %{name}-source-%{version}
%define installroot %{_datadir}/%{name}-%{version}


%description
The Pegasus project encompasses a set of technologies that help workflow-based applications execute in a number of different environments including desktops, campus clusters, grids, and now clouds. Scientific workflows allow users to easily express multi-step computations, for example retrieve data from a database, reformat the data, and run an analysis. Once an application is formalized as a workflow the Pegasus Workflow Management Service can map it onto available compute resources and execute the steps in appropriate order. Pegasus can handle 1 to 1 million computational tasks.


#NOTE TO SELF:
# At some later point, we need to split this package up into 
# logical components, ie pegasus-libs
# However, the libraries are not yet in FHS locations, so I have delayed this.
#%package libs
#Summary: Pegasus Java libraries
#Group: System Environment/Libraries
#%description libs
#Java libraries for Pegasus

#%package worker
#Summary: Pegasus Worker Node
#Group: Applications/System
#%description worker
#Pegasus worker


%prep
%setup -q -n %{sourcedir}

%build

ant dist dist-worker
pushd dist dist-worker
tar xzf pegasus-binary-*.tar.gz
mv pegasus-%{version} ../pegasus-build
tar xzf pegasus-worker-*.tar.gz
mv pegasus-%{version} ../pegasus-worker
popd

# FIX COMMON.SH
mv pegasus-build/bin/common.sh pegasus-build/bin/pegasus-common.sh
INSTALLROOT=`echo %{installroot} |  sed 's/\//\\\\\//g'`
PERLROOT=`echo %{installroot}/lib/perl |  sed 's/\//\\\\\//g'`
sed -i "s/common\.sh/pegasus-common.sh/" pegasus-build/bin/*
sed -i "s/PEGASUS_HOME=\".*/PEGASUS_HOME=$INSTALLROOT/" pegasus-build/bin/pegasus-common.sh
sed -i "s/pegasus_home = .*/pegasus_home = \"$INSTALLROOT\"/" pegasus-build/bin/common.py
sed -i "s/dirname(.0), .common.pm./\'$PERLROOT\', \'common.pm\'/" pegasus-build/bin/*
sed -i "s/ENV{\'PEGASUS_HOME\'} = .*/ENV{\'PEGASUS_HOME\'} = \'$PERLROOT\'/" pegasus-build/bin/*

for file in pegasus-bug-report pegasus-remove pegasus-run pegasus-status pegasus-submit-dag
do
	sed -i "s/BEGIN {/BEGIN { push(@INC,\"$PERLROOT\");/" pegasus-build/bin/$file
done

%install

#Deprecated and should be removed to avoid dependency issues
rm pegasus-build/libexec/pegasus-delegationd

mv pegasus-build/bin/common.pm pegasus-build/lib/perl
mkdir -p $RPM_BUILD_ROOT/%{installroot}
mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}

install -m 644 pegasus-build/README $RPM_BUILD_ROOT%{_docdir}/%{name}
install -m 644 pegasus-build/LICENSE $RPM_BUILD_ROOT%{_docdir}/%{name}
install -m 644 pegasus-build/RELEASE_NOTES $RPM_BUILD_ROOT%{_docdir}/%{name}
install -m 644 pegasus-build/stamp $RPM_BUILD_ROOT%{_docdir}/%{name}
install -m 644 pegasus-build/GTPL $RPM_BUILD_ROOT%{_docdir}/%{name}


cp -aR pegasus-build/man/man1 $RPM_BUILD_ROOT%{_mandir}

install -m 644 pegasus-build/doc/advanced-properties.pdf $RPM_BUILD_ROOT%{_docdir}/%{name}
install -m 644 pegasus-build/doc/basic-properties.pdf $RPM_BUILD_ROOT%{_docdir}/%{name}
cp -aR pegasus-build/doc/docbook $RPM_BUILD_ROOT%{_docdir}/%{name}/
cp -aR pegasus-build/doc/schemas $RPM_BUILD_ROOT%{_docdir}/%{name}/
cp -aR pegasus-build/bin/* $RPM_BUILD_ROOT%{_bindir}/


# OK, lets switch these to install statements + FHS one at a time
# Anything below here is total crap and should be fixed
cp -aR pegasus-build/contrib $RPM_BUILD_ROOT%{installroot}
cp -aR pegasus-build/etc $RPM_BUILD_ROOT%{installroot}
cp -aR pegasus-build/examples $RPM_BUILD_ROOT%{installroot}
cp -aR pegasus-build/libexec $RPM_BUILD_ROOT%{installroot}
cp -aR pegasus-build/lib $RPM_BUILD_ROOT%{installroot}
cp -aR pegasus-build/sql $RPM_BUILD_ROOT%{installroot}
cp -aR pegasus-build/test $RPM_BUILD_ROOT%{installroot}


# Fix symlinks
pushd $RPM_BUILD_ROOT%{installroot}
ln -s ../../bin $RPM_BUILD_ROOT%{installroot}/bin
popd

%clean
ant clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{installroot}
%{_bindir}/*
%{_docdir}/%{name}
%{_mandir}/man1/*

#%files worker
#%defattr(-,root,root,-)
#
#%files libs
#%defattr(-,root,root,-)
#%{installroot}/lib



%changelog
* Fri Jul 22 2011 Doug Strain <dstrain@fnal.gov> 3.0.3-2
- Fixing common.pm
- Adding g++ to dependencies

* Wed Jul 20 2011 Doug Strain <dstrain@fnal.gov> 3.0.3-1
- Initial creation of spec file
- Installs into /usr/share/pegasus-3.0.3
- Binaries into /usr/bin



