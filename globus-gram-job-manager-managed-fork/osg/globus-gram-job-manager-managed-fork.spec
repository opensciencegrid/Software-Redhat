%{!?perl_vendorlib: %global perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)}

Name:           globus-gram-job-manager-managed-fork
Version:        2.0.0
Release:        1%{?dist}
Summary:        Globus Toolkit - Fork Job Manager Setup

Group:          Applications/Internet
BuildArch:      noarch
License:        ASL 2.0
URL:            http://www.globus.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source:		Globus-ManagedFork-Setup.tar.gz
Requires:       globus-gram-job-manager-scripts
Requires:       globus-gass-cache-program >= 2
Requires:       globus-common-setup >= 2
Requires:       globus-gram-job-manager >= 10.59
#BuildRequires:  grid-packaging-tools
#BuildRequires:  globus-core

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world.   This package augments the Globus job
manager typically found on the gatekeeper to allow the control and monitoring
of job manager "fork" jobs that can run on the gatekeeper.  This helps to 
prevent high job load from occuring on the gatekeeper that can paralyze a site.

%prep
%setup -q -n Globus-ManagedFork-Setup

%build
#No build necessary for this package

%install

#Documentation
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m 644 notes.html $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM/JobManager/
install -m 644 globus/lib/perl/Globus/GRAM/JobManager/managedfork.pm $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM/JobManager/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/globus
install -m 644 globus/share/globus_gram_job_manager/managedfork.rvf $RPM_BUILD_ROOT%{_datadir}/globus


%files
%{_datadir}/globus/managedfork.rvf
%{perl_vendorlib}/Globus/GRAM/JobManager/managedfork.pm
%{_docdir}/%{name}-%{version}/notes.html



