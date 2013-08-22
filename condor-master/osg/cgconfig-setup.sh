#!/bin/bash

usage () {
  echo "$(basename "$0") {--add|--remove}"
  echo "Add or remove htcondor cgroup configuration to cgroup config file."
  exit
}

add () {
  perl -pi -e '
    BEGIN {undef $/}

    s/\n?^### BEGIN HTCONDOR CONFIG ###.*^### END HTCONDOR CONFIG ###\n?$//ms;

    s/$/
### BEGIN HTCONDOR CONFIG ###
group htcondor {
        cpu {}
        cpuacct {}
        memory {}
        freezer {}
        blkio {}
}
### END HTCONDOR CONFIG ###
/;' /etc/cgconfig.conf
}

remove () {
  perl -pi -e '
    BEGIN {undef $/}

    s/\n?^### BEGIN HTCONDOR CONFIG ###.*^### END HTCONDOR CONFIG ###\n?$//ms;
' /etc/cgconfig.conf
}

case $1 in
     --add ) add ;;
  --remove ) remove ;;
         * ) usage ;;
esac

