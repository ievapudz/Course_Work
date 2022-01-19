#!/usr/bin/perl

use strict;
use warnings;

# This is a script that is used to create
# separate (proportion) files to create embeddings. 

my $portion_size = 30000;

$/ = "\n>";
while(<>) {
    /^>?([^\n]*)\n([^>]*)/; 
    my( $header, $sequence ) = ( $1, $2 ); 
    my @split_header = split( '_', $header );
    if( $split_header[0] == $id ) {
        print $split_header[0], "\n";
    }
}
exit;
