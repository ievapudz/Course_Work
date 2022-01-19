#!/usr/bin/perl

use strict;
use warnings;

# This is a script that is used to modify FASTA headers before 
# generation of embeddings.

$/ = "\n>";
while(<>) {
    /^>?([^\n]*)\n([^>]*)/; 
    my( $header, $sequence ) = ( $1, $2 ); 
    my @split_header = split('_', $header);
    print ">$ENV{TAX_ID}|$split_header[1]|$ENV{TEMPERATURE_LABEL}\n" .
	  "$sequence\n";
}

exit;
