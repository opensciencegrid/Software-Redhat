 
%define bigtop_tomcat_version 0.7.0+cdh5.13.0+0 
%define bigtop_tomcat_patched_version 6.0.53-cdh5.13.0 
%define bigtop_tomcat_base_version 6.0.53 
%define bigtop_tomcat_release 1.cdh5.13.0.p0.34%{?dist} 
%define cdh_customer_patch p0 
%define cdh_parcel_custom_version 0.7.0+cdh5.13.0+0-1.cdh5.13.0.p0.34%{?dist}
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
%define lib_tomcat %{_usr}/lib/%{name}

%if  %{?suse_version:1}0
  %define doc_tomcat %{_docdir}/%{name}
%else
  %define doc_tomcat %{_docdir}/%{name}-%{version}
%endif

Name: bigtop-tomcat
Version: %{bigtop_tomcat_version}
Release: %{bigtop_tomcat_release}
Summary: Apache Tomcat
URL: http://tomcat.apache.org/
Group: Development/Libraries
BuildArch: noarch
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
License: ASL 2.0
Source0: bigtop-tomcat-%{bigtop_tomcat_patched_version}.tar.gz
Source1: do-component-build
Source2: install_tomcat.sh
Requires: bigtop-utils >= 0.7

BuildRequires: ant
%if 0%{?rhel} >= 7
BuildRequires: maven >= 3.0.0
%else
BuildRequires: maven3
%endif

%description 
Apache Tomcat is an open source software implementation of the
Java Servlet and JavaServer Pages technologies.

%prep
%setup -n bigtop-tomcat-%{bigtop_tomcat_patched_version}

%build
export COMPONENT_HASH=c5f90582119ab994c6e6711f5578370ca6cef0b7
env FULL_VERSION=%{bigtop_tomcat_patched_version} bash %{SOURCE1}

%install
bash %{SOURCE2} \
    --build-dir=build/bigtop-tomcat-%{bigtop_tomcat_patched_version} \
    --doc-dir=%{doc_tomcat} \
    --prefix=$RPM_BUILD_ROOT

%files 
%attr(0755,root,root) %{lib_tomcat}
%doc %{doc_tomcat}

%changelog

