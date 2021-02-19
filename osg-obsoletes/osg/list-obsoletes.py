#!/usr/bin/env python3

# usage: ./list-obsoletes.py elX

import os
import sys
import json


def apicall(_api, **kw):
    kwstr = repr(repr(kw))
    cmdline = "osg-koji call --kwargs=%s --json-output %s" % (kwstr, _api)
    return json.load(os.popen(cmdline))


def list_tag_rpms(tag):
    return apicall('listTaggedRPMS', latest=True, tag=tag)[0]


def isbin(rpm):
    return rpm['arch'] != 'src'


def list_tag_bin_rpms(tag):
    return list(filter(isbin, list_tag_rpms(tag)))


def obsoletes_line(rpm):
    evfmt = "{epoch}:{version}" if rpm['epoch'] else "{version}"
    fmt = "Obsoletes: {name} <= " + evfmt
    return fmt.format(**rpm)


def rpm_dent(rpm):
    return rpm['name'], rpm


def tag2dict(tag):
    return dict(map(rpm_dent, list_tag_bin_rpms(tag)))


def main(args):
    elX, = args
    tag1 = 'osg-3.5-%s-release' % elX
    tag2 = 'osg-3.6-%s-development' % elX

    rpms35 = tag2dict(tag1)
    rpms36 = tag2dict(tag2)

    rpms35_only = set(rpms35) - set(rpms36)

    for name in sorted(rpms35_only):
        print(obsoletes_line(rpms35[name]))


if __name__ == '__main__':
    main(sys.argv[1:])

