
# eval {
#     my $result = 1 / 0; 
#     print "Result: $result\n";
# };
# if ($@) {
#     print "Error Caught: $@\n";
# }

# use autodie;

# eval {
#     open my $fh, '<', 'badfile.txt';
#     close $fh
# };
# if ($@) {
#     print "Error Caught: $@\n";
# }

# use Try::Tiny;


# try {
#     my $n=1/0;
# }
# catch {
#     print "Exception Caught: $_";
# }
# finally {
#     print "Exception or not, this code was written by Abishek";
# };

use strict;
use warnings;
use Carp;

sub bad_function {
    my ($value) = @_;
    if (!$value) {
        confess "Error from bad_function: value is undefined";
    }
}

sub good_function {
     my ($value) = 10;
    if (!$value) {
        confess "Error from good_function: value is undefined";
    }
}

eval {
    bad_function();
    good_function();
};

if ($@) {
    print "Error Caught in main: $@\n";
}