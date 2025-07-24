Summary: Scitokens mapfile for OSG
Name: osg-scitokens-mapfile
Version: 14
Release: 2%{?dist}
License: ASL 2.0
Source0: https://github.com/opensciencegrid/topology/archive/data-%{version}.tar.gz
Source1: https://vdt.cs.wisc.edu/upstream/osg-scitokens-mapfile/pydeps/icalendar-4.0.7-py2.py3-none-any.whl
Source2: https://vdt.cs.wisc.edu/upstream/osg-scitokens-mapfile/pydeps/xmltodict-0.12.0-py2.py3-none-any.whl
BuildRequires: python3
BuildRequires: python3-pip
%if 0%{?el7}
BuildRequires: python36-ldap3
BuildRequires: python36-pytz
BuildRequires: python36-dateutil
BuildRequires: python36-PyYAML
BuildRequires: python36-six
%else
BuildRequires: python3-ldap3
BuildRequires: python3-pip-wheel
BuildRequires: python3-pytz
BuildRequires: python3-dateutil
BuildRequires: python3-pyyaml
BuildRequires: python3-six
%endif

%global debug_package %{nil}
%global __python /usr/bin/python3


%description
Contains file for mapping scitokens issuers to Unix users for OSG.


%prep
%setup -q -n topology-data-%{version}


%build
for whl in %{SOURCE1} %{SOURCE2}; do
    pip3 install --no-deps "$whl" --prefix $PWD
done
PYTHONPATH=$PYTHONPATH:$(echo "$PWD"/lib/python3*/site-packages)
export PYTHONPATH
./bin/get-scitokens-mapfile --regex --outfile osg-scitokens-mapfile.conf


%install
mkdir -p %{buildroot}/usr/share/condor-ce/mapfiles.d/
mv osg-scitokens-mapfile.conf %{buildroot}/usr/share/condor-ce/mapfiles.d/


%files
/usr/share/condor-ce/mapfiles.d/osg-scitokens-mapfile.conf


%changelog
* Thu Jul 24 2025 Matt Westphall <westphall@wisc.edu> 15-1
- Update to data-15 tag (SOFTWARE-6190)

* Fri Jan 17 2025 Matt Westphall <westphall@wisc.edu> 14-1
- Update to data-14 tag (SOFTWARE-6058)

* Wed Mar 20 2024 Matt Westphall <westphall@wisc.edu> 13-1
- Update to data-13 tag (SOFTWARE-5844)

* Thu Mar 09 2023 Mátyás Selmeci <matyas@cs.wisc.edu> 12-1
- Update to data-12 tag (SOFTWARE-5520)

* Wed Nov 23 2022 Mátyás Selmeci <matyas@cs.wisc.edu> 11-1
- Update to data-11 tag (SOFTWARE-5359)

* Tue Nov 22 2022 Mátyás Selmeci <matyas@cs.wisc.edu> 9-1
- Update to data-9 tag (SOFTWARE-5359)

* Wed Apr 06 2022 Mátyás Selmeci <matyas@cs.wisc.edu> 8-1
- Update to data-8 tag (SOFTWARE-5108, SOFTWARE-5110)

* Tue Mar 29 2022 Mátyás Selmeci <matyas@cs.wisc.edu> 7-1
- Update to data-7 tag (SOFTWARE-5102)

* Wed Feb 23 2022 Brian Lin <blin@cs.wisc.edu> 6-1
- Update to data-6 tag (SOFTWARE-5049)

* Wed Jan 26 2022 Brian Lin <blin@cs.wisc.edu> 5-1
- Update to data-5 tag (SOFTWARE-4969)

* Thu Dec 16 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 4-1
- Update to data-4 tag (SOFTWARE-4854)
- Add ldap3 build requirement

* Wed Apr 28 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 3-1
- Update to data-3 tag (SOFTWARE-4572)

* Wed Apr 21 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 2-1
- Update to data-2 tag
- Use regex format and add .conf extension (SOFTWARE-4572)

* Thu Feb 11 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 1-1
- First version (SOFTWARE-4453)

