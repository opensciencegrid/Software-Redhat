 
%define bigtop_utils_version 0.7.0+cdh5.13.0+0 
%define bigtop_utils_patched_version 0.7.0-cdh5.13.0 
%define bigtop_utils_base_version 0.7.0 
%define osg_patchlevel 1
%define bigtop_utils_release 1.cdh5.13.0.p0.34.%{osg_patchlevel}%{?dist} 
%define cdh_customer_patch p0 
%define cdh_parcel_custom_version 0.7.0+cdh5.13.0+0-1.cdh5.13.0.p0.34.%{osg_patchlevel}%{?dist}
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
%define bin_dir /usr/bin
%define plugins_dir /var/lib/bigtop

# Disabling the following scripts from running:
# symbol stripping - not relevant here.
# jar repacking - to save time.
# byte-compiling python code - not relevant here.
# brp-compress - not relevant here.
#              - This compresses man and info pages under
#                 ./usr/man/man* ./usr/man/*/man* ./usr/info \
#                 ./usr/share/man/man* ./usr/share/man/*/man* ./usr/share/info \
#                 ./usr/kerberos/man ./usr/X11R6/man/man* ./usr/lib/perl5/man/man* \
#                 ./usr/share/doc/*/man/man* ./usr/lib/*/man/man*
%define __os_install_post %{nil}

Name: bigtop-utils
Version: %{bigtop_utils_version}
Release: %{bigtop_utils_release}
Summary: Collection of useful tools for Bigtop

License:    ASL 2.0
URL:        http://bigtop.apache.org/
BuildArch:  noarch
Source0:    bigtop-detect-javahome
Source1:    LICENSE
Source2:    bigtop-utils.default
Source3:    bigtop-detect-javalibs
Source4:    bigtop-detect-classpath
Source5:    bigtop-monitor-service

Patch0:     bigtop-detect-javahome.patch

Requires:   bash
Requires:   openssl
Requires:   curl

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
install -p -m 644 %{SOURCE4} .
install -p -m 644 %{SOURCE5} .
%patch0 -p1

%build
export COMPONENT_HASH=c5f90582119ab994c6e6711f5578370ca6cef0b7


%install
install -d -p -m 755 $RPM_BUILD_ROOT%{plugins_dir}/
install -d -p -m 755 $RPM_BUILD_ROOT%{lib_dir}/
install -d -p -m 755 $RPM_BUILD_ROOT%{bin_dir}/
install -d -p -m 755 $RPM_BUILD_ROOT/etc/default
install -p -m 755 %{SOURCE0} $RPM_BUILD_ROOT%{lib_dir}/
ln -s -T ../lib/bigtop-utils/`basename %{SOURCE0}` $RPM_BUILD_ROOT%{bin_dir}/`basename %{SOURCE0}`
install -p -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{lib_dir}/
install -p -m 755 %{SOURCE4} $RPM_BUILD_ROOT%{lib_dir}/
install -p -m 755 %{SOURCE5} $RPM_BUILD_ROOT%{lib_dir}/
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/default/bigtop-utils

%files
%defattr(-,root,root,-)
%doc LICENSE
%config(noreplace) /etc/default/bigtop-utils

%{lib_dir}
%{bin_dir}/bigtop-detect-javahome
%{plugins_dir}

%changelog

* Wed Nov 08 2017 Carl Edquist <edquist@cs.wisc.edu> - 0.7.0+cdh5.13.0+0-1.cdh5.13.0.p0.34.1
- update to bigtop-utils 0.7+ (SOFTWARE-2980)

* Mon Jun 27 2016 Carl Edquist <edquist@cs.wisc.edu> 0.6.0+248-1.cdh4.7.1.p0.13.1
- prefer /etc/alternatives for JAVA_HOME, then JAVA7 (SOFTWARE-2304)

