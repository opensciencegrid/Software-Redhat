# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.


# Copyright 2008 Red Hat, Inc
# written by Seth Vidal <skvidal@fedoraproject.org>

# Updated and adopted for OSG by Brian Bockelman <bbockelm@cse.unl.edu>
# Updated 11/28/2011 for OSG by Neha Sharma <neha@fnal.gov>
#FIXME:
# When two requirements of a pkg being removed mutually require each other
# there's no way to have one know about the other and have this know to remove both
# ex: foo is being removed. it requires bar. bar requires baz. baz requires bar. 
#     nothing other than foo and baz require bar. 

"""
This plugin allows packages to clean up dependencies they pulled in which are
not in use by any other package if they are part of a OSG repository.
"""

from yum import config
from yum.plugins import PluginYumExit, TYPE_CORE
from yum.constants import *

requires_api_version = '2.4'
plugin_type = (TYPE_CORE,)

_requires_cache = {}
ignore_list = ['glibc', 'bash', 'libgcc']

exclude_bin = False
remove_always = False


def _requires_this_package(rpmdb, pkg):
    if pkg in _requires_cache:
        return _requires_cache[pkg]
        
    requirers = {}
    for prov in pkg.provides:
        for req_pkg in rpmdb.getRequires(prov[0], prov[1], prov[2]):
            if req_pkg == pkg:
                continue
            requirers[req_pkg.pkgtup] = 1
    # do filelists, too :(
    for prov in pkg.filelist + pkg.dirlist + pkg.ghostlist:
        for req_pkg in rpmdb.getRequires(prov):
            if req_pkg == pkg:
                continue
            requirers[req_pkg.pkgtup] = 1

    _requires_cache[pkg] = requirers.keys()
    return requirers.keys()

def _consider_leaf(pkg, possible_leaves):
    # funny, this doesn't look like a leaf to me...
    for leave, pkgs in possible_leaves.items():
        for tmppkg in pkgs:
             if pkg.name in [i[0] for i in tmppkg.provides]:
                 return True
    return False

def postresolve_hook(conduit):
    
    global exclude_bin, remove_always
    opts, commands = conduit.getCmdLine()
    if opts and hasattr(opts,'exclude_bin'):
        if exclude_bin or opts.exclude_bin:
            exclude_bin = True
            
    if (opts and opts.remove_osg) or remove_always:
        # get all the items in 
        tsInfo  = conduit.getTsInfo()
        rpmdb = conduit.getRpmDB()
        oldlen = 0
        allrepos = conduit.getRepos().repos
        possible_osg = 0
        for repo_name in allrepos:
            repo = conduit.getRepos().getRepo(repo_name)
            if repo.consider_as_osg:
                possible_osg += 1
        enabled_repos = conduit.getRepos().listEnabled()
        possible_leaves = {}
        for repo in enabled_repos:
            if repo.consider_as_osg:
                possible_leaves[repo] = conduit.getPackages(repo)

        if possible_osg and not possible_leaves:
            raise PluginYumExit('You asked to remove OSG components, but have no enabled OSG repos.  Try adding --enablerepo=osg to your command line.')

        while oldlen != len(tsInfo):
            oldlen = len(tsInfo)
            for txmbr in tsInfo.getMembersWithState(output_states=[TS_ERASE]):
                if conduit._base.allowedMultipleInstalls(txmbr.po): 
                    # these make everything dodgy, skip it
                    continue
                for req in txmbr.po.requires:
                    if req[0].startswith('rpmlib('):
                        continue
                    for pkg in rpmdb.getProvides(req[0], req[1], req[2]):
                        if pkg.pkgtup in [ txmbr.po.pkgtup for txmbr in tsInfo.getMembersWithState(output_states=[TS_ERASE]) ]:
                            continue # skip ones already marked for remove, kinda pointless
                        if pkg.name in ignore_list: # there are some pkgs which are NEVER going to be leafremovals
                            continue

                        # Skip manually installed packages.
                        #if pkg.yumdb_info.get('reason') == 'user':
                        #    continue

                        non_removed_requires = []
                        for req_pkgtup in _requires_this_package(rpmdb,pkg):
                            pkgtups = [ txmbr.po.pkgtup for txmbr in tsInfo.getMembersWithState(output_states=[TS_ERASE]) ]
                            if req_pkgtup not in pkgtups:
                                non_removed_requires.append(req_pkgtup)
                        if exclude_bin: # if this pkg is a binary of some kind, skip it
                            is_bin=False
                            for file_name in pkg.filelist:
                                if file_name.find('bin') != -1:
                                    is_bin = True
                            if is_bin:
                                continue
    
                        if not non_removed_requires:
                            if hasattr(conduit, 'registerPackageName'):
                                conduit.registerPackageName("yum-plugin-remove-osg")
                            if possible_osg:
                                myrepo = _consider_leaf(pkg, possible_leaves)
                                if myrepo:
                                    conduit.info(2, 'removing %s. It is not required by anything else and from OSG.' % pkg)
                                    conduit._base.remove(pkg)
                                else:
                                    conduit.info(2, 'not removing %s because it is not from an OSG repo' % pkg)
                             
			    #Commenting since we need to remove only OSG repo packages                            
			    #else:
                            #    conduit.info(2, 'removing %s. It is not required by anything else.' % pkg)
                            #    conduit._base.remove(pkg)

def config_hook(conduit):
    global exclude_bin, remove_always
    exclude_bin  = conduit.confBool('main', 'exclude_bin', default=False)
    remove_always = conduit.confBool('main', 'remove_always', default=False)

    config.RepoConf.consider_as_osg = config.BoolOption(False)

    parser = conduit.getOptParser()
    if parser:
        if hasattr(parser, 'plugin_option_group'):
            parser = parser.plugin_option_group

        parser.add_option("", "--osg-exclude-bin", dest="exclude_bin",
                action="store_true", default=False, 
                help="do not remove OSG packages which contain executable binaries")
        parser.add_option('', '--osg', dest='remove_osg', 
                action='store_true', default=False, 
                help="remove dependencies no longer needed by any other packages")


