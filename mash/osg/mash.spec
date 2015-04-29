%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           mash
Version:        0.5.22
Release:        3%{?dist}
Summary:        Koji buildsystem to yum repository converter
Group:          Development/Tools
License:        GPLv2
URL:            http://fedorahosted.org/releases/m/a/mash/
Source0:        http://fedorahosted.org/releases/m/a/mash/%{name}-%{version}.tar.gz
Patch0:         multilib-python.patch
Patch1:         multilib-lcmaps.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       yum, createrepo, koji
Conflicts:	pungi < 1.0.0
BuildRequires:  python-devel
BuildArch:      noarch

%description
mash is a tool that queries a koji buildsystem for the latest RPMs for
any particular tag, and creates repositories of those RPMs, including
any multlib RPMs that are necessary.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT/%{_bindir}/mash.py $RPM_BUILD_ROOT/%{_bindir}/mash
mkdir -p $RPM_BUILD_ROOT/var/cache/mash
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%config(noreplace) %{_sysconfdir}/mash
%{python_sitelib}/mash*
%{_bindir}/*
%{_datadir}/mash
/var/cache/mash

%changelog
* Thu Sep 27 2012 Matyas Selmeci <matyas@cs.wisc.edu> 0.5.22-3
- Add patch to mark lcmaps plugins as multilib

* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> 0.5.22-2
- Add patch to add python*/site-packages dirs as multilib if they have .so files

* Mon Feb 27 2011 Bill Nottingham <notting@redhat.com> 0.5.22-1
- Add perl-libs whitelist
- fix arm dependency checks (<dennis@ausil.us>)
- fix key ordering

* Tue Feb 10 2011 Bill Nottingham <notting@redhat.com> 0.5.21-1
- update configs for F15 (<dennis@ausil.us>)
- add a knob for frobbing which ppc arch is preferred (<jwboyer@gmail.com>)
- fix gdk-pixbuf loader path (#649339)

* Tue Sep 28 2010 Bill Nottingham <notting@redhat.com> 0.5.20-1
- solve multilib against parent repos if configured (#633136)
- fix traceback when only binary RPMS exist (modified from #636697, <tguthmann@iseek.com.au>)
- disable sigchecking on deltas in source, not via patch (#512454)
- mark LSB-providing packages as multilib (#585858)
- fix libmunge to catch more cases (#637172, <mschwendt@gmail.com>)
- add krb5 plugin dir to multilib list (#632611)
- add libstdc++-static as a multilib whitelist (#630581)
- add dri as a multilib dir
- arm arch compatiblitiy <dennis@ausil.us>

* Fri Jul 30 2010 Bill Nottingham <notting@redhat.com> 0.5.19-1
- retarget branched.mash at f14

* Mon Jul 26 2010 Bill Nottingham <notting@redhat.com> 0.5.18-1
- add F14 key (<jkeating@redhat.com>)

* Fri Jun 25 2010 Bill Nottingham <notting@redhat.com> 0.5.17-1
- fix copying of prior deltarpms, broken in 0.5.16 (#598584)

* Wed Apr 21 2010 Bill Nottingham <notting@redhat.com> 0.5.16-1
- fix use of prior repodata (<jkeating@redhat.com>)

* Fri Apr 16 2010 Bill Nottingham <notting@redhat.com> 0.5.15-1
- branched compose configuration tweaks
- speed up composes a teeny bit

* Tue Feb 23 2010 Bill Nottingham <notting@redhat.com> 0.5.14-1
- further changes for NFR (<jkeating@redhat.com>)

* Fri Feb 19 2010 Bill Nottingham <notting@redhat.com> 0.5.13-1
- assorted fixes for no-frozen-rawhide
- make package hash directories all lowercase

* Wed Feb 17 2010 Bill Nottingham <notting@redhat.com> 0.5.12-1
- adjust for branched trees and no-frozen-rawhide (<jkeating@redhat.com>)
- allow for source repos to be optional (<jgregusk@redhat.com>)
- allow for pulling all builds, not just latest (<kanarip@fedoraunity.org>)
- enable hashed packages for rawhide

* Fri Dec 18 2009 Bill Nottingham <notting@redhat.com> 0.5.11-1
- allow package directories to be hashed by the package name
  (adapted from <skvidal@fedoraproject.org>)

* Mon Nov 16 2009 Bill Nottingham <notting@redhat.com> 0.5.10-1
- fix up distro_tags and content_tags
- bump rawhide version
- there is no ppc in Fedora rawhide anymore (<jkeating@redhat.com>)

* Mon Oct  5 2009 Bill Nottingham <notting@redhat.com> 0.5.9-1
- set dist_tags & content_tags when making metadata; update rawhide config
  (<jkeating@redhat.com>)
- allow glibc-static as a devel package
- allow making ancient yum-arch metadata

* Mon Jun 29 2009 Bill Nottingham <notting@redhat.com> 0.5.8-1
- noarch packages can have debuginfo too (#508746)
- remove wine-arts from multilib whitelist (not needed, doesn't exist)

* Tue Jun 23 2009 Bill Nottingham <notting@redhat.com> 0.5.7-1
- when using previous runs for deltas, only look in the appropriate arch dirs
- wine multilib fixes

* Mon Jun 22 2009 Bill Nottingham <notting@redhat.com> 0.5.6-1
- more gtk2 multilib (#507165)
- minor transaction speedups
- handle new yum arch-setting API. (<skvidal@fedoraproject.org>)

* Fri May  8 2009 Bill Nottingham <notting@redhat.com> 0.5.5-1
- fix setting delta_dirs in config file
- canonicalize -o option if passed as a relative path

* Wed May  6 2009 Bill Nottingham <notting@redhat.com> 0.5.4-1
- allow configuring createrepo hash type
- remove old config files

* Mon Apr 27 2009 Bill Nottingham <notting@redhat.com> 0.5.3-1
- when copying in old deltas, make sure the signatures match current packages
- don't delta source and debuginfo packages

* Fri Apr 17 2009 Bill Nottingham <notting@redhat.com> 0.5.2-1
- set a max size for deltarpm-able packages (#496242)

* Thu Apr 16 2009 Bill Nottingham <notting@redhat.com> 0.5.1-1
- delta fixes
- handle qt/kde plugins better (#495947)

* Wed Apr 15 2009 Bill Nottingham <notting@redhat.com> 0.5.0-1
- Add support for generating deltas with createrepo
- add F11 key to config (<jkeating@redhat.com>)
- various multlib updates (#485242, etc.)

* Thu Jan  8 2009 Bill Nottingham <notting@redhat.com> 0.4.9-1
- error out if strict_keys is set and we can't download the signed package

* Thu Dec 18 2008 Bill Nottingham <notting@redhat.com> 0.4.8-1
- Fix debuginfo exclusion
- Fix --skip-stat with old createrepo
- Use update_from, if it's available

* Wed Dec 17 2008 Bill Nottingham <notting@redhat.com> 0.4.7-1
- Fix noarch handling

* Wed Dec 17 2008 Bill Nottingham <notting@redhat.com> 0.4.6-1
- Fix -p/--previous for certain repository layouts

* Tue Dec 16 2008 Bill Nottingham <notting@redhat.com> 0.4.5-1
- fix caching bug with respect to epochs
- work with both python createrepo API and commandline createrepo

* Tue Dec 16 2008 Bill Nottingham <notting@redhat.com> 0.4.4-1
- Mark gstreamer plugins as multilib (#252173)
- Some more multilib devel blacklisting, including php. (#342851)
- Add a --previous option, for copying createrepo data

* Wed Oct 15 2008 Bill Nottingham <notting@redhat.com> 0.4.2-1
- Enable unique repoadata file names (<jkeating@redhat.com>)
- Add a kernel multilib policy for sparc (<dennis@ausil.us>)
- Fix base multilib policy, and packages with no key (<dennis@ausil.us>)

* Mon Sep 15 2008 Bill Nottingham <notting@redhat.com> 0.4.1-1
- Adjust for new keys

* Tue Jul 22 2008 Bill Nottingham <notting@redhat.com> 0.4.0-1
- add simple timestamping for profiling usage
- add support for caching non-local koji repositories

* Fri May 16 2008 Bill Nottingham <notting@redhat.com> 0.3.7-1
- add F9 updates configuration

* Tue Apr 29 2008 Bill Nottingham <notting@redhat.com> 0.3.6-1
- adjust qt path to catch scim-bridge-qt

* Mon Apr 14 2008 Bill Nottingham <notting@redhat.com> 0.3.5-1
- add pulseaudio-utils as well

* Fri Apr 11 2008 Bill Nottingham <notting@redhat.com> 0.3.4-1
- add alsa plugins to multilib list (#338211)

* Tue Apr  1 2008 Bill Nottingham <notting@redhat.com> 0.3.3-1
- add gtk modules to multilib list (#439949)

* Fri Feb 22 2008 Bill Nottingham <notting@redhat.com> 0.3.2-1
- fix typo that broke handling of unsigned packages
- fix yum api usage (#433555, <peter@pramberger.at>)
- fix noarch w/o src.rpm logic (#433551, <peter@pramberger.at>)
- Add a 'use_repoview' option that allows us to toggle repoview generation. (<lmacken@redhat.com>)
- Tell createrepo to be quiet (<lmacken@redhat.com>)
- Don't re-generate repoview after multilib solving. (<lmacken@redhat.com>)
- Fix our "failsafe" shutil.copyfile call (<lmacken@redhat.com>)

* Thu Jan 17 2008 Bill Nottingham <notting@redhat.com> 0.3.0-1
- use createrepo's python API
- allow running without local koji storage

* Mon Nov 19 2007 Bill Nottingham <notting@redhat.com> 0.2.10-1
- handle non Packages/ repositories better (#350391)

* Fri Nov  9 2007 Bill Nottingham <notting@redhat.com> 0.2.9-1
- handle noarch excludearch for packages without source
  rpms (<rob.myers@gtri.gatech.edu>)
- use yum's pkgSack, not yumLocalPackage

* Tue Sep 25 2007 Bill Nottingham <notting@redhat.com> 0.2.8-1
- libflashsupport (#305541)

* Fri Sep 21 2007 Bill Nottingham <notting@redhat.com> 0.2.7-1
- disable repoview for now

* Thu Sep 20 2007 Bill Nottingham <notting@redhat.com> 0.2.6-1
- repoview cleanups/fixes
- fix gtkimmodules typo (#295371, <petersen@redhat.com>)

* Tue Sep 18 2007 Bill Nottingham <notting@redhat.com> 0.2.5-1
- handle valgrind for multilib differently (#294761)

* Mon Sep 17 2007 Bill Nottingham <notting@redhat.com> 0.2.4-1
- repoview support (<jkeating@redhat.com>)

* Thu Sep  6 2007 Bill Nottingham <notting@redhat.com> 0.2.3-1
- blacklist java-1.7.0-icedtea-devel (#271761)

* Tue Sep  4 2007 Bill Nottingham <notting@redhat.com> 0.2.2-1
- add nspluginwrapper to multilib whitelist (#275021)
- fix kernel-devel (#247321)

* Tue Aug 28 2007 Bill Nottingham <notting@redhat.com> 0.2.0-1
- updates to work with pungi 1.0.0, conflict with older pungi
- fix some multilib compose issues (<drago01@gmail.com>)

* Mon Jul 23 2007 Bill Nottingham <notting@redhat.com> 0.1.19-1
- fix spam-o-matic to use python mailer

* Thu Jun 21 2007 Bill Nottingham <notting@redhat.com> 0.1.18-1
- pull in cyrus-sasl plugins (#245176)

* Thu Jun  7 2007 Bill Nottingham <notting@redhat.com> 0.1.17-1
- exclude debuginfo from repodata where appropriate
- add spam-o-matic

* Thu May 31 2007 Bill Nottingham <notting@redhat.com> 0.1.16-1
- fix arch handling

* Thu May 31 2007 Bill Nottingham <notting@redhat.com> 0.1.15-1
- propagate errors better
- handle signatures in koji correctly

* Wed May 30 2007 Bill Nottingham <notting@redhat.com> 0.1.14-1
- add a use_sqlite config option for determining whether to use createrepo -d

* Wed May 30 2007 Bill Nottingham <notting@redhat.com> 0.1.13-1
- hopefully fix the db locking issues
- make source rpm path configurable
- add updates config files

* Tue May 29 2007 Bill Nottingham <notting@redhat.com> 0.1.12-1
- use /tmp where appropriate
- hacks to use less memory

* Sat May 26 2007 Bill Nottingham <notting@redhat.com> 0.1.11-1
- run more operations in parallel

* Thu May 24 2007 Bill Nottingham <notting@redhat.com> 0.1.10-1
- fix kernel handling
- tweak rawhide config

* Wed May 23 2007 Bill Nottingham <notting@redhat.com> 0.1.9-1
- add wine, wine-arts to multilib whitelist (#241059)

* Fri May 18 2007 Bill Nottingham <notting@redhat.com> 0.1.8-1
- spec cleanups

* Thu May 17 2007 Bill Nottingham <notting@redhat.com> 0.1.7-1
- initial build
