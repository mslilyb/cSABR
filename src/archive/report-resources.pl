use strict;
use warnings 'FATAL' => 'all';

die "usage: $0 <bakeoff log file>\n" unless @ARGV == 1;

print "Program\tUser\tSystem\tElapsed\tMemory\n";
my ($prog, $utime, $stime, $etime, $mem);
while (<>) {
	if    (/Command being timed.+ (\S+)"$/) {$prog = $1}
	elsif (/User time.+ (\S+)$/) {$utime = $1}
	elsif (/System time.+ (\S+)$/) {$stime = $1}
	elsif (/Elapsed.+ (\S+)$/) {$etime = $1}
	elsif (/Maximum resident.+ (\S+)$/) {$mem = $1}
	elsif (/^\s+Exit status:/) {print "$prog\t$utime\t$stime\t$etime\t$mem\n"}
}
