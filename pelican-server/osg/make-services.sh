#!/bin/bash

for service in "$@"; do

    if [[ $service = osdf-* ]]; then
        base_service=${service#osdf-}

        cat > ${service}.yaml <<EOF
Xrootd:
  ManagerHost: redirector.osgstorage.org
  SummaryMonitoringHost: xrd-report.osgstorage.org
  DetailedMonitoringHost: xrd-mon.osgstorage.org
Federation:
  DiscoveryUrl: osg-htc.org
  TopologyNamespaceURL: https://topology.opensciencegrid.org/stashcache/namespaces.json
EOF

    elif [[ $service = pelican-* ]]; then
        base_service=${service#pelican-}

        cat > ${service}.yaml <<EOF
Federation:
  DiscoveryUrl:
EOF
    fi

    cat > ${service}.service <<EOF
[Unit]
Description = Pelican service %N
After = network.target nss-lookup.target

[Service]
ExecStart = /usr/bin/pelican --config /etc/pelican/%N.yaml ${base_service} serve

[Install]
WantedBy = multi-user.target
EOF

    if [[ $service = *-origin ]]; then
        cat > ${service}-multiuser.service <<EOF
[Unit]
Description = Pelican service %N with multiuser support
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
