Name:           pegasus
Version:        3.0.3
Release:        1
Summary:        Pegasus Workload Management System
Group:          Applications/System
License:        ASL 2.0
URL:            http://pegasus.isi.edu/index.php

Source:        pegasus-source-%{release}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-root
BuildArch:      noarch
BuildRequires:  ant java
Requires:  java

%define sourcedir %{name}-source-%{release}

%description
The Pegasus project encompasses a set of technologies that help workflow-based applications execute in a number of different environments including desktops, campus clusters, grids, and now clouds. Scientific workflows allow users to easily express multi-step computations, for example retrieve data from a database, reformat the data, and run an analysis. Once an application is formalized as a workflow the Pegasus Workflow Management Service can map it onto available compute resources and execute the steps in appropriate order. Pegasus can handle 1 to 1 million computational tasks.

%prep
%setup -q -n %{sourcedir}

%build

pushd %{sourcedir}
ant dist dist-worker
popd

%install

%clean
ant clean

%files


%changelog
* Mon Jul 20 2011 Doug Strain <dstrain@fnal.gov> 3.0.3-1
Initial creation of spec file
