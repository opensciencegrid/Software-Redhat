# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
%define man_dir %{_mandir}
%define bigtop_jsvc_version 0.3.0
%define bigtop_jsvc_release 1.1%{?dist}
%define bigtop_jsvc_base_version 1.0.10

%if  %{?suse_version:1}0
%define bin_jsvc /usr/lib/bigtop-utils
%define doc_jsvc %{_docdir}/%{name}
%else
%define bin_jsvc %{_libexecdir}/bigtop-utils
%define doc_jsvc %{_docdir}/%{name}-%{bigtop_jsvc_version}
%endif

Name: bigtop-jsvc
Version: %{bigtop_jsvc_version}
Release: %{bigtop_jsvc_release}
Summary: Application to launch java daemon
URL: http://commons.apache.org/daemon/
Group: Development/Libraries
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
License: ASL 2.0
Source0: commons-daemon-%{bigtop_jsvc_base_version}.tar.gz
Source1: do-component-build
Source2: install_jsvc.sh
BuildRequires: ant, autoconf, automake, gcc
BuildRequires: java7-devel
BuildRequires: jpackage-utils
Provides: jsvc

%description 
jsvc executes classfile that implements a Daemon interface.

%prep
%setup -n commons-daemon-%{bigtop_jsvc_base_version}-src

%clean
rm -rf $RPM_BUILD_ROOT

%build
bash %{SOURCE1}

%install
%__rm -rf $RPM_BUILD_ROOT
sh %{SOURCE2} \
          --build-dir=.                         \
          --bin-dir=$RPM_BUILD_ROOT/%{bin_jsvc} \
          --doc-dir=$RPM_BUILD_ROOT/%{doc_jsvc} \
          --man-dir=$RPM_BUILD_ROOT/%{man_dir}  \
          --prefix=$RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{bin_jsvc}
%doc %{doc_jsvc}


%changelog
* Mon May 20 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 0.3.0-1.1
- Rebuild with Java 7


