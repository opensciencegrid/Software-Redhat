Summary: Security utilities
Name: emi-trustmanager
Version: 3.0.3
Release: 9%{?dist}
License: EMI
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildArch: noarch
BuildRequires: ant
BuildRequires: bouncycastle
BuildRequires: log4j
%if 0%{?rhel} >= 7
BuildRequires: bouncycastle-pkix
Requires: java-headless >= 1:1.7.0
%else
BuildRequires: java7-devel
BuildRequires: jpackage-utils
Requires: java7
%endif
Requires: jpackage-utils
# ensure these are present, from jpackage-utils or missing-java-1.7.0-dirs
Requires: /usr/lib/java-1.7.0
Requires: /usr/share/java-1.7.0
BuildRoot: %{_builddir}/%{name}-root
AutoReqProv: yes
Source: emi-trustmanager-3.0.3-1.src.tar.gz
Patch0: incorrect_oid.patch
Patch1: build.xml.patch
Patch2: better_log.patch
Patch3: X509Name_cast.patch

Patch10: 0010-ASN1Object-ASN1Primitive-bc1.47.patch
Patch11: 0011-ASN1Encodable-ASN1Object-bc1.47.patch
Patch12: 0012-DEREncodable-ASN1Encodable-bc1.47.patch
Patch13: 0013-DERObjectIdentifier-ASN1ObjectIdentifier-bc1.47.patch
Patch14: 0014-DERObject-ASN1Primitive-bc1.47.patch
Patch15: 0015-getDERObject-toASN1Primitive-bc1.47.patch
Patch16: 0016-DERInteger-ASN1Integer-bc1.47.patch
Patch17: 0017-getDEREncoded-getEncoded-ASN1Encoding.DER-bc1.47.patch
Patch18: 0018-Add-bcpkix-.jar-to-build.xml-EL7.patch
Patch19: 0019-PEMReader-PEMParser-bc1.47.patch
Patch20: 0020-JDKKeyPairGenerator-KeyPairGenerator-bc1.47.patch
Patch21: 0021-getASN1Primitive-toASN1Primitive-bc1.47.patch
Patch22: 0022-GeneralSubtree-constructor-fix-bc1.47.patch
Patch23: 0023-IssuingDistributionPoint-constructor-fix-bc1.47.patch
Patch24: 0024-GeneralNames-constuctor-fix-bc1.47.patch
Patch25: 0025-DEROctetString-new-exception-bc1.47.patch
Patch26: 0026-CertificationRequestInfo.getSubject-signature-change.patch
Patch27: private_key_exception.patch

%description
The java authentication and proxy generation implementation that supports grid proxies.

%prep

%setup

%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0

%if 0%{?rhel} >= 7
# bouncycastle patches
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p0
%endif


%build
 
  
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 ant dist -Dprefix=$RPM_BUILD_ROOT -Dstage=/ -Dmodule.version=3.0.3-1-E -Dant.build.javac.target=1.7
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/share/java/trustmanager.jar
%dir /usr/share/doc/trustmanager/
/usr/share/doc/trustmanager/LICENSE
%dir /usr/share/doc/trustmanager/html/
/usr/share/doc/trustmanager/html/index.html
/usr/share/doc/trustmanager/html/overview-frame.html
/usr/share/doc/trustmanager/html/overview-tree.html
/usr/share/doc/trustmanager/html/allclasses-frame.html
/usr/share/doc/trustmanager/html/constant-values.html
/usr/share/doc/trustmanager/html/overview-summary.html
/usr/share/doc/trustmanager/html/package-list
/usr/share/doc/trustmanager/html/stylesheet.css
/usr/share/doc/trustmanager/html/serialized-form.html
/usr/share/doc/trustmanager/html/allclasses-noframe.html
%dir /usr/share/doc/trustmanager/html/org/
%dir /usr/share/doc/trustmanager/html/org/glite/
%dir /usr/share/doc/trustmanager/html/org/glite/security/
/usr/share/doc/trustmanager/html/org/glite/security/package-frame.html
%dir /usr/share/doc/trustmanager/html/org/glite/security/trustmanager/
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/Log4jConfigurator.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/OpensslCertPathValidator.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/package-frame.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/ProxyCertPathValidator.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/UpdatingKeyManager.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/ContextFactory.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/TimeoutSSLSocketFactory.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/CertPathValidatorState.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/package-tree.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/package-summary.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/package-use.html
%dir /usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/Log4jConfigurator.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/OpensslCertPathValidator.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/ProxyCertPathValidator.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/UpdatingKeyManager.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/ContextFactory.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/TimeoutSSLSocketFactory.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/CertPathValidatorState.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/CRLCertChecker.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/OpensslTrustmanagerFactory.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/ContextWrapper.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/OpensslTrustmanager.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/InstanceID.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/CRLFileTrustManager.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/class-use/SSLContextWrapper.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/CRLCertChecker.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/OpensslTrustmanagerFactory.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/ContextWrapper.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/OpensslTrustmanager.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/InstanceID.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/CRLFileTrustManager.html
/usr/share/doc/trustmanager/html/org/glite/security/trustmanager/SSLContextWrapper.html
%dir /usr/share/doc/trustmanager/html/org/glite/security/util/
/usr/share/doc/trustmanager/html/org/glite/security/util/CAFilenameSplitter.html
/usr/share/doc/trustmanager/html/org/glite/security/util/FileCRLChecker.html
/usr/share/doc/trustmanager/html/org/glite/security/util/package-frame.html
/usr/share/doc/trustmanager/html/org/glite/security/util/DNImpl.html
/usr/share/doc/trustmanager/html/org/glite/security/util/X500Principal.html
/usr/share/doc/trustmanager/html/org/glite/security/util/HostNameChecker.html
/usr/share/doc/trustmanager/html/org/glite/security/util/DNHandler.html
/usr/share/doc/trustmanager/html/org/glite/security/util/TrustDirHandler.html
/usr/share/doc/trustmanager/html/org/glite/security/util/DirectoryList.html
/usr/share/doc/trustmanager/html/org/glite/security/util/Password.html
/usr/share/doc/trustmanager/html/org/glite/security/util/DNImplRFC2253.html
/usr/share/doc/trustmanager/html/org/glite/security/util/package-tree.html
/usr/share/doc/trustmanager/html/org/glite/security/util/package-summary.html
/usr/share/doc/trustmanager/html/org/glite/security/util/CertificateNotFoundException.html
/usr/share/doc/trustmanager/html/org/glite/security/util/CertificateRevokedException.html
/usr/share/doc/trustmanager/html/org/glite/security/util/RevocationChecker.html
/usr/share/doc/trustmanager/html/org/glite/security/util/CaseInsensitiveProperties.html
/usr/share/doc/trustmanager/html/org/glite/security/util/package-use.html
%dir /usr/share/doc/trustmanager/html/org/glite/security/util/proxy/
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/ProxyCertInfoExtension.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/ProxyTracingExtension.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/package-frame.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/SAMLExtension.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/ProxyRestrictionData.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/ProxyCertificateGenerator.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/package-tree.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/package-summary.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/ProxyCertUtil.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/ProxyChainInfo.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/package-use.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/ProxyPolicy.html
%dir /usr/share/doc/trustmanager/html/org/glite/security/util/proxy/class-use/
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/class-use/ProxyCertInfoExtension.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/class-use/ProxyTracingExtension.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/class-use/SAMLExtension.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/class-use/ProxyRestrictionData.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/class-use/ProxyCertificateGenerator.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/class-use/ProxyCertUtil.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/class-use/ProxyChainInfo.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/class-use/ProxyPolicy.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/class-use/ProxyCertificateInfo.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/class-use/CertificateExtensionData.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/ProxyCertificateInfo.html
/usr/share/doc/trustmanager/html/org/glite/security/util/proxy/CertificateExtensionData.html
%dir /usr/share/doc/trustmanager/html/org/glite/security/util/class-use/
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/CAFilenameSplitter.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/FileCRLChecker.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/DNImpl.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/X500Principal.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/HostNameChecker.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/DNHandler.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/TrustDirHandler.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/DirectoryList.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/Password.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/DNImplRFC2253.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/CertificateNotFoundException.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/CertificateRevokedException.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/RevocationChecker.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/CaseInsensitiveProperties.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/DN.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/FileEndingIterator.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/FullTrustAnchor.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/TrustStorage.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/PrivateKeyReader.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/CertUtil.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/KeyStoreGenerator.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/IPAddressComparator.html
/usr/share/doc/trustmanager/html/org/glite/security/util/class-use/FileCertReader.html
/usr/share/doc/trustmanager/html/org/glite/security/util/DN.html
/usr/share/doc/trustmanager/html/org/glite/security/util/FileEndingIterator.html
/usr/share/doc/trustmanager/html/org/glite/security/util/FullTrustAnchor.html
/usr/share/doc/trustmanager/html/org/glite/security/util/TrustStorage.html
%dir /usr/share/doc/trustmanager/html/org/glite/security/util/namespace/
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/LegacyNamespaceFormat.html
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/NamespaceFormat.html
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/package-frame.html
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/package-tree.html
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/package-summary.html
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/DNChecker.html
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/NamespacePolicy.html
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/package-use.html
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/DNCheckerImpl.html
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/EUGridNamespaceFormat.html
%dir /usr/share/doc/trustmanager/html/org/glite/security/util/namespace/class-use/
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/class-use/LegacyNamespaceFormat.html
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/class-use/NamespaceFormat.html
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/class-use/DNChecker.html
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/class-use/NamespacePolicy.html
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/class-use/DNCheckerImpl.html
/usr/share/doc/trustmanager/html/org/glite/security/util/namespace/class-use/EUGridNamespaceFormat.html
/usr/share/doc/trustmanager/html/org/glite/security/util/PrivateKeyReader.html
/usr/share/doc/trustmanager/html/org/glite/security/util/CertUtil.html
/usr/share/doc/trustmanager/html/org/glite/security/util/KeyStoreGenerator.html
/usr/share/doc/trustmanager/html/org/glite/security/util/IPAddressComparator.html
/usr/share/doc/trustmanager/html/org/glite/security/util/FileCertReader.html
/usr/share/doc/trustmanager/html/org/glite/security/package-tree.html
/usr/share/doc/trustmanager/html/org/glite/security/package-summary.html
/usr/share/doc/trustmanager/html/org/glite/security/package-use.html
%dir /usr/share/doc/trustmanager/html/org/glite/security/class-use/
/usr/share/doc/trustmanager/html/org/glite/security/class-use/SecurityException.html
/usr/share/doc/trustmanager/html/org/glite/security/class-use/SecurityInfo.html
/usr/share/doc/trustmanager/html/org/glite/security/class-use/SecurityContext.html
/usr/share/doc/trustmanager/html/org/glite/security/class-use/SecurityInfoContainer.html
/usr/share/doc/trustmanager/html/org/glite/security/SecurityException.html
/usr/share/doc/trustmanager/html/org/glite/security/SecurityInfo.html
/usr/share/doc/trustmanager/html/org/glite/security/SecurityContext.html
/usr/share/doc/trustmanager/html/org/glite/security/SecurityInfoContainer.html
/usr/share/doc/trustmanager/html/deprecated-list.html
/usr/share/doc/trustmanager/html/help-doc.html
%dir /usr/share/doc/trustmanager/html/resources/
/usr/share/doc/trustmanager/html/resources/*.gif
/usr/share/doc/trustmanager/html/index-all.html

%changelog
* Tue Sep 15 2015 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.3-9
- Avoid exception when creating SSL socket on RHEL7.

* Mon Jul 20 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.0.3-8
- Bump to rebuild

* Tue Nov 11 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.0.3-7
- Build with bouncycastle 1.50 and patch API breakage

* Wed Oct 29 2014 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.3-6
- Fix issues with newer bcprov.

* Tue May 07 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.0.3-5
- Require missing java dir names instead of workaround package

* Mon Apr 01 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.0.3-4
- Build with OpenJDK7
 
* Mon Sep 17 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.3-3
- Fix for misspelled OID for pre-RFC proxies.

