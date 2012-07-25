
Name:		globus-gram-job-manager-managedfork
Version:	0.2
Release:	1%{?dist}
Summary:	OSG extensions to Globus Toolkit - Condor-integrated Fork Job Manager

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.opensciencegrid.org/
Source:		jobmanager-managedfork

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:	globus-gram-job-manager-condor
Requires(preun): initscripts

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
jobmanager-managedfork, an OSG-contributed job-manager that runs fork jobs in
Condor's local universe

%prep

%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/grid-services/available
install -m 644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/grid-services/available/jobmanager-managedfork

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-managedfork > /dev/null 2>&1 || :
    globus-gatekeeper-admin -e jobmanager-managedfork -n jobmanager-fork > /dev/null 2>&1 || :
    globus-gatekeeper-admin -e jobmanager-managedfork -n jobmanager > /dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ]; then
    globus-gatekeeper-admin -d jobmanager-managedfork > /dev/null 2>&1 || :

    if [ -f /etc/grid-services/available/jobmanager-fork-poll ]; then
        globus-gatekeeper-admin -e jobmanager-fork-poll -n jobmanager
        globus-gatekeeper-admin -e jobmanager-fork-poll -n jobmanager-fork
    else
        globus-gatekeeper-admin -d jobmanager-fork > /dev/null 2>&1 || :
        globus-gatekeeper-admin -d jobmanager > /dev/null 2>&1 || :
    fi

    /sbin/service globus-gatekeeper condrestart > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%{_sysconfdir}/grid-services/available/jobmanager-managedfork

%changelog
* Wed Aug 24 2012 Alain Roy <roy@cs.wisc.edu> - 0.2-1
- Make default jobmanager when installed (match OSG 1.2 behavior)

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.1-1
- Initial packaging of jobmanager-managedfork.

