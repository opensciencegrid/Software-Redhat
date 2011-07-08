%define clean_buildroot             [[ -n "%buildroot" && "%buildroot" != / ]] && rm -rf %buildroot

# defined and true
%define is_true()                   %{expand:%%{?%{1}}%%{?!%{1}:0}}
%define is_false()                  ! %{expand:%%{?%{1}}%%{?!%{1}:0}}

Summary: Profiles your system
Name: vdt-system-profiler
Version: 0.0.1
Release: 1%{?dist}
License: Apache License, 2.0
Group: Applications/Grid
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Packager: VDT <vdt-support@opensciencegrid.org>
AutoReq: yes
AutoProv: yes
BuildArch: noarch

%define extract_dir %{name}-%{version}

%description
vdt system profiler profiles your system



%prep
# %%setup quick reference:
#   -a N        Unpack source N after cd
#   -b N        Unpack source N before cd
#   -c          Create and cd to dir before unpacking
#   -D          Do not delete dir before unpacking
#   -n DIR      Name of extract dir (instead of NAME-VERSION)
#   -T          Do not autounpack Source0

# Templates:
# 1. No Build Glue:
#       %%setup -c -n %extract_dir
# 2. Build Glue in Source 1:
#       %%setup -T -b 1 -c -n %extract_dir
#       %%setup -D -n %extract_dir
%setup -c -n %extract_dir




%build
exit 0






%install
%clean_buildroot
mkdir -p %buildroot
mv * %buildroot



%clean
%if %is_false NOCLEAN
%clean_buildroot
%endif




%define _unpackaged_files_terminate_build 1
%files
/usr/bin/vdt-system-profiler



%changelog
* Thu Jun 09 2011 matyas@cs.wisc.edu - 0.0.1-1
- Initial spec file


# vim:ft=spec

