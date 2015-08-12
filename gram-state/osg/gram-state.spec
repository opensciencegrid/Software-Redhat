Name:      gram-state
Version:   1.1
Release:   1%{?dist}
Summary:   Show information about Globus GRAM jobs, based on their job state files

Group:     System Environment/Base
License:   Apache 2.0
URL:       https://twiki.grid.iu.edu/bin/view/Documentation/Release3/

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%description
%{summary}

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}/
install -m 755 gram-state $RPM_BUILD_ROOT/%{_bindir}/

install -d $RPM_BUILD_ROOT%{_mandir}/
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 gram-state.1 $RPM_BUILD_ROOT/%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

%{_bindir}/gram-state
%{_mandir}/man1/gram-state.1.gz


%changelog
* Sat Sep 22 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.1-1
- Implement PBS support.
- Update to latest GRAM directory structure.

* Wed Jun 6 2012 Alain Roy <roy@cs.wisc.edu> 1.0-1
- Updated to 1.0: minor capitalization fix, more debugging output

* Fri May 25 2012 Alain Roy <roy@cs.wisc.edu> 0.1-1
- Created initial RPM for gram-state 
