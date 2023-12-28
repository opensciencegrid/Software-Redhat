#!/bin/bash

for service in "$@"; do

    if [[ $service = osdf-* ]]; then
        base_service=${service#osdf-}

        cat > ${service}.yaml <<END
Debug: false
Logging:
  Level: "Error"
Federation:
  DiscoveryUrl: osg-htc.org
  TopologyNamespaceURL: https://topology.opensciencegrid.org/stashcache/namespaces.json
Server:
  TLSCertificate: /etc/grid-security/xrd/xrdcert.pem
  TLSKey: /etc/grid-security/xrd/xrdkey.pem
  TLSCACertificateDirectory: /etc/grid-security/certificates
#  Hostname: f.q.d.n
Xrootd:
  Sitename: TOPOLOGY_RESOURCE_NAME
  ManagerHost: redirector.osgstorage.org
  SummaryMonitoringHost: xrd-report.osgstorage.org
  DetailedMonitoringHost: xrd-mon.osgstorage.org
  Mount: "/mnt/osdf"
END
        if [[ $base_service == origin ]]; then
            cat >> ${service}.yaml <<END
  Port: 1094
Origin:
  NamespacePrefix: "/MY_NAMESPACE"
  Multiuser: false
  EnableUI: false
END
        elif [[ $base_service == cache ]]; then
            cat >> ${service}.yaml <<END
  Port: 8443
Cache:
  Port: 8443
END

        fi

    elif [[ $service = pelican-* ]]; then
        base_service=${service#pelican-}

        cat > ${service}.yaml <<EOF
Debug: false
Logging:
  Level: "Error"
Federation:
  DiscoveryUrl:
#Server:
#  Hostname: f.q.d.n
Xrootd:
  Mount: "/mnt/pelican"
  Port: 8443
EOF
        if [[ $base_service == origin ]]; then
            cat >> ${service}.yaml <<END
Origin:
  NamespacePrefix: "/MY_NAMESPACE"
  Multiuser: false
  EnableUI: true
END
        elif [[ $base_service == cache ]]; then
            cat >> ${service}.yaml <<END
Cache:
  Port: 8443
END
        fi
    fi

    cat > ${service}.service <<EOF
[Unit]
Description = Pelican service ${service}
After = network.target nss-lookup.target

[Service]
ExecStart = /usr/bin/pelican --config /etc/pelican/${service}.yaml ${base_service} serve

[Install]
WantedBy = multi-user.target
EOF

    if [[ $service = *-origin ]]; then
        cat > ${service}-multiuser.service <<EOF
[Unit]
Description = Pelican service ${service} with multiuser support
After = network.target nss-lookup.target

[Service]
ExecStart = /usr/bin/pelican --config /etc/pelican/${service}.yaml ${base_service} serve
CapabilityBoundingSet = CAP_SETUID CAP_SETGID CAP_DAC_OVERRIDE
Capabilities = CAP_SETGID+p CAP_SETUID+p

[Install]
WantedBy = multi-user.target
EOF
    fi

done
