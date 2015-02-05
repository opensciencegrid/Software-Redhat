package Globus::GRAM::JobManager::condor_accounting_groups;
use strict;
use warnings;

use base qw(Exporter);
our @EXPORT_OK = qw(obtain_condor_group);
our $VERSION = 1.00;

our $UID_FILENAME     = "/etc/osg/uid_table.txt";
our $EXTATTR_FILENAME = "/etc/osg/extattr_table.txt";

my @ea;
my @Environment;
my $Job_Manager;
my %UID_Table;
my %Extattr_Table;

sub obtain_condor_group {
    @Environment = @{(shift)};
    $Job_Manager = shift;

    _populate_uid_table();
    my $group = _match_uid_to_condor_group($>);
    return $group if $group;

    _populate_extended_attribute_table();

    $group = _match_extended_attribute_to_condor_group();
    return $group; 
}

sub _populate_uid_table {
    if (open my $uidfile, '<', $UID_FILENAME) {
        while (<$uidfile>) {
            chomp;
            next if /^\#/;  # remove comments
            next if !/\w+/; # remove blank lines
            s/\#.*$//;         # remove comments
            my ($uid, $group) = split(/\s+/, $_);

            $UID_Table{$uid} = $group;
        }
        close $uidfile;
    } else {
        $Job_Manager->log("unable to open $UID_FILENAME: $!");
    }
}

sub _match_uid_to_condor_group {
    my ($uid) = @_;

    # check numeric UID first, then username
    my $name = getpwuid($uid);
    return $UID_Table{$uid} || $UID_Table{$name};
} 

sub _populate_extended_attribute_table {
    if (open my $eafile, '<', $EXTATTR_FILENAME) {
        while (<$eafile>) {
            chomp;
            next if /^\#/;  # remove comments
            next if !/\w+/; # remove blank lines
            s/\#.*$//;         # remove comments

            my @fields = split(/\s+/, $_);
            my $groupname = pop(@fields);
            my $ea_name = join " ", @fields;
	    push @ea, $ea_name;
            $Extattr_Table{$ea_name} = $groupname;
        }
        close $eafile;
    } else {
        $Job_Manager->log("unable to open $EXTATTR_FILENAME: $!");
    }
}

sub _match_extended_attribute_to_condor_group() {
    my $proxy_filename;

    map {
        if ($_->[0] eq 'X509_USER_PROXY') {$proxy_filename = $_->[1];}
    } @Environment;

    $proxy_filename ||= $ENV{X509_USER_PROXY};

    my @attributes;
    if ($proxy_filename) {
        my $safe_proxy_filename = quotemeta $proxy_filename;
        @attributes = split "\n",
            `voms-proxy-info -all -file $safe_proxy_filename | grep -E "attribute|subject"`;
    }

    foreach my $regexp (@ea) {
        foreach my $attribute (@attributes) {
            if (eval{$attribute =~ $regexp}) {
                my $group = $Extattr_Table{$regexp};
                $Job_Manager->log("match found: regexp: $regexp,\tgroup: $group\n");
                return $group;
            }
            $Job_Manager->log("regexp match error in condor_accounting_groups: @_") if @_;
        }
    }
}

1;
