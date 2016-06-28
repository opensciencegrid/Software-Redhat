 
%define bigtop_utils_version 0.6.0+248 
%define bigtop_utils_patched_version 0.6.0-cdh4.7.1 
%define bigtop_utils_base_version 0.6.0 
%define bigtop_utils_release 1.cdh4.7.1.p0.13.1%{?dist}
%define cdh_customer_patch p0 
%define cdh_parcel_custom_version 0.6.0+248-1.cdh4.7.1.p0.13.1%{?dist}
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

%define lib_dir /usr/lib/bigtop-utils

Name: bigtop-utils
Version: %{bigtop_utils_version}
Release: %{bigtop_utils_release}
Summary: Collection of useful tools for Bigtop

Group:      Applications/Engineering
License:    APL2
URL:        http://bigtop.apache.org/
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch
Source0:    bigtop-detect-javahome
Source1:    LICENSE
Source2:    bigtop-utils.default
Source3:    bigtop-detect-javalibs

Patch0:     bigtop-detect-javahome.patch

Requires:   bash

# "which" command is needed for a lot of projects.
# It is part of the package "util-linux" on suse and "which" everywhere else
%if  %{?suse_version:1}0
Requires:  util-linux
%else
Requires:       which
%endif

%description
This includes a collection of useful tools and files for Bigtop


%prep
%setup -q -T -c
install -p -m 644 %{SOURCE0} .
install -p -m 644 %{SOURCE1} .
install -p -m 644 %{SOURCE2} .
install -p -m 644 %{SOURCE3} .
%patch0 -p1

%build


%install
install -d -p -m 755 $RPM_BUILD_ROOT%{lib_dir}/
install -d -p -m 755 $RPM_BUILD_ROOT/etc/default
install -p -m 755 bigtop-detect-javahome $RPM_BUILD_ROOT%{lib_dir}/
install -p -m 755 bigtop-detect-javalibs $RPM_BUILD_ROOT%{lib_dir}/
install -p -m 644 bigtop-utils.default   $RPM_BUILD_ROOT/etc/default/bigtop-utils

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE
%config(noreplace) /etc/default/bigtop-utils

%{lib_dir}

%changelog

* Mon Jun 27 2016 Carl Edquist <edquist@cs.wisc.edu> 0.6.0+248-1.cdh4.7.1.p0.13.1
- prefer /etc/alternatives for JAVA_HOME, then JAVA7 (SOFTWARE-2304)

