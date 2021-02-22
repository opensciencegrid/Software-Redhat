Name:      osg-obsoletes
Summary:   Obsoletes packages from previous OSG Release series
Version:   3.6
Release:   0.3%{?dist}
License:   Apache 2.0
URL:       http://www.opensciencegrid.org


%if 0%{?rhel} == 7
# EL7 OBSOLETES
Obsoletes: atlas-xcache <= 1.5.2
Obsoletes: avro-doc <= 1.7.6+cdh5.13.0+135
Obsoletes: avro-libs <= 1.7.6+cdh5.13.0+135
Obsoletes: avro-tools <= 1.7.6+cdh5.13.0+135
Obsoletes: bigtop-jsvc <= 0.3.0
Obsoletes: bigtop-jsvc-debuginfo <= 0.3.0
Obsoletes: bigtop-utils <= 0.7.0+cdh5.13.0+0
Obsoletes: cctools <= 7.1.7
Obsoletes: cctools-debuginfo <= 7.1.7
Obsoletes: cctools-devel <= 7.1.7
Obsoletes: cms-xcache <= 1.5.2
Obsoletes: gfal2-debuginfo <= 2.18.1
Obsoletes: glideinwms-common-tools <= 3.6.5
Obsoletes: glideinwms-condor-common-config <= 3.6.5
Obsoletes: glideinwms-factory <= 3.6.5
Obsoletes: glideinwms-factory-condor <= 3.6.5
Obsoletes: glideinwms-glidecondor-tools <= 3.6.5
Obsoletes: glideinwms-libs <= 3.6.5
Obsoletes: glideinwms-minimal-condor <= 3.6.5
Obsoletes: glideinwms-usercollector <= 3.6.5
Obsoletes: glideinwms-userschedd <= 3.6.5
Obsoletes: glideinwms-vofrontend <= 3.6.5
Obsoletes: glideinwms-vofrontend-standalone <= 3.6.5
Obsoletes: glite-ce-cream-client-api-c <= 1.15.4
Obsoletes: glite-ce-cream-client-devel <= 1.15.4
Obsoletes: globus-gridftp-osg-extensions <= 0.4
Obsoletes: globus-gridftp-osg-extensions-debuginfo <= 0.4
Obsoletes: globus-gridftp-server-debuginfo <= 13.20
Obsoletes: gratia-probe-condor-events <= 1.20.14
Obsoletes: gratia-probe-dcache-storage <= 1.20.14
Obsoletes: gratia-probe-dcache-storagegroup <= 1.20.14
Obsoletes: gratia-probe-dcache-transfer <= 1.20.14
Obsoletes: gratia-probe-debuginfo <= 1.20.14
Obsoletes: gratia-probe-enstore-storage <= 1.20.14
Obsoletes: gratia-probe-enstore-tapedrive <= 1.20.14
Obsoletes: gratia-probe-enstore-transfer <= 1.20.14
Obsoletes: gratia-probe-glideinwms <= 1.20.14
Obsoletes: gratia-probe-gridftp-transfer <= 1.20.14
Obsoletes: gratia-probe-hadoop-storage <= 1.20.14
Obsoletes: gratia-probe-lsf <= 1.20.14
Obsoletes: gratia-probe-metric <= 1.20.14
Obsoletes: gratia-probe-onevm <= 1.20.14
Obsoletes: gratia-probe-pbs-lsf <= 1.20.14
Obsoletes: gratia-probe-services <= 1.20.14
Obsoletes: gratia-probe-sge <= 1.20.14
Obsoletes: gratia-probe-slurm <= 1.20.14
Obsoletes: gratia-probe-xrootd-storage <= 1.20.14
Obsoletes: gratia-probe-xrootd-transfer <= 1.20.14
Obsoletes: gridftp-dsi-posix <= 1:1.4
Obsoletes: gridftp-dsi-posix-debuginfo <= 1:1.4
Obsoletes: gridftp-hdfs <= 1.1.1
Obsoletes: gridftp-hdfs-debuginfo <= 1.1.1
Obsoletes: gsi-openssh-debuginfo <= 7.4p1
Obsoletes: hadoop <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-0.20-conf-pseudo <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-0.20-mapreduce <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-client <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-conf-pseudo <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-debuginfo <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-doc <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-hdfs <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-hdfs-datanode <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-hdfs-fuse <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-hdfs-journalnode <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-hdfs-namenode <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-hdfs-nfs3 <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-hdfs-secondarynamenode <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-hdfs-zkfc <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-httpfs <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-kms <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-kms-server <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-libhdfs <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-libhdfs-devel <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-mapreduce <= 2.6.0+cdh5.12.1+2540
Obsoletes: hadoop-yarn <= 2.6.0+cdh5.12.1+2540
Obsoletes: lcas-lcmaps-gt4-interface <= 0.3.1
Obsoletes: lcas-lcmaps-gt4-interface-debuginfo <= 0.3.1
Obsoletes: llrun <= 0.1.3
Obsoletes: llrun-debuginfo <= 0.1.3
Obsoletes: myproxy-debuginfo <= 6.2.6
Obsoletes: osg-ce-bosco <= 3.5
Obsoletes: osg-gridftp <= 3.5
Obsoletes: osg-gridftp-hdfs <= 3.5
Obsoletes: osg-gridftp-xrootd <= 3.5
Obsoletes: osg-gsi-openssh-addons <= 1.0.0
Obsoletes: osg-release-itb <= 3.5
Obsoletes: osg-se-hadoop <= 3.5
Obsoletes: osg-se-hadoop-client <= 3.5
Obsoletes: osg-se-hadoop-datanode <= 3.5
Obsoletes: osg-se-hadoop-gridftp <= 3.5
Obsoletes: osg-se-hadoop-namenode <= 3.5
Obsoletes: osg-se-hadoop-secondarynamenode <= 3.5
Obsoletes: osg-xrootd <= 3.5
Obsoletes: osg-xrootd-standalone <= 3.5
Obsoletes: rsv <= 3.19.8
Obsoletes: rsv-consumers <= 3.19.8
Obsoletes: rsv-core <= 3.19.8
Obsoletes: rsv-metrics <= 3.19.8
Obsoletes: scitokens-cpp-debuginfo <= 0.5.1
Obsoletes: stash-cache <= 1.5.2
Obsoletes: stash-origin <= 1.5.2
Obsoletes: uberftp-debuginfo <= 2.8
Obsoletes: vomsxrd <= 1:0.6.0
Obsoletes: vomsxrd-debuginfo <= 1:0.6.0
Obsoletes: vomsxrd-devel <= 1:0.6.0
Obsoletes: xcache <= 1.5.2
Obsoletes: xcache-consistency-check <= 1.5.2
Obsoletes: xcache-redirector <= 1.5.2
Obsoletes: xrootd-debuginfo <= 1:4.12.6
Obsoletes: xrootd-hdfs <= 2.1.8
Obsoletes: xrootd-hdfs-debuginfo <= 2.1.8
Obsoletes: xrootd-hdfs-devel <= 2.1.8
Obsoletes: xrootd-lcmaps <= 1.7.8
Obsoletes: xrootd-lcmaps-debuginfo <= 1.7.8
Obsoletes: xrootd-multiuser <= 0.4.3
Obsoletes: xrootd-multiuser-debuginfo <= 0.4.3
Obsoletes: xrootd-scitokens <= 1.2.2
Obsoletes: xrootd-scitokens-debuginfo <= 1.2.2
Obsoletes: zookeeper <= 3.4.5+cdh5.14.2+142
Obsoletes: zookeeper-debuginfo <= 3.4.5+cdh5.14.2+142
Obsoletes: zookeeper-native <= 3.4.5+cdh5.14.2+142
Obsoletes: zookeeper-server <= 3.4.5+cdh5.14.2+142
%endif

%if 0%{?rhel} == 8
# EL8 OBSOLETES
Obsoletes: lcmaps <= 1.6.6
Obsoletes: lcmaps-common-devel <= 1.6.6
Obsoletes: lcmaps-db-templates <= 1.6.6
Obsoletes: lcmaps-debuginfo <= 1.6.6
Obsoletes: lcmaps-debugsource <= 1.6.6
Obsoletes: lcmaps-devel <= 1.6.6
Obsoletes: lcmaps-plugins-basic <= 1.7.0
Obsoletes: lcmaps-plugins-basic-debuginfo <= 1.7.0
Obsoletes: lcmaps-plugins-basic-debugsource <= 1.7.0
Obsoletes: lcmaps-plugins-basic-ldap <= 1.7.0
Obsoletes: lcmaps-plugins-basic-ldap-debuginfo <= 1.7.0
Obsoletes: lcmaps-plugins-verify-proxy <= 1.5.11
Obsoletes: lcmaps-plugins-verify-proxy-debuginfo <= 1.5.11
Obsoletes: lcmaps-plugins-verify-proxy-debugsource <= 1.5.11
Obsoletes: lcmaps-plugins-voms <= 1.7.1
Obsoletes: lcmaps-plugins-voms-debuginfo <= 1.7.1
Obsoletes: lcmaps-plugins-voms-debugsource <= 1.7.1
Obsoletes: lcmaps-without-gsi <= 1.6.6
Obsoletes: lcmaps-without-gsi-debuginfo <= 1.6.6
Obsoletes: lcmaps-without-gsi-devel <= 1.6.6
Obsoletes: voms-clients-cpp-debuginfo <= 2.1.0
Obsoletes: voms-debuginfo <= 2.1.0
Obsoletes: voms-debugsource <= 2.1.0
Obsoletes: voms-server-debuginfo <= 2.1.0
%endif


%description
%{summary}

%install

%files

%changelog
* Fri Feb 19 2021 Carl Edquist <edquist@cs.wisc.edu> - 3.6-1
- Initial version (SOFTWARE-4316)

