#!/usr/bin/perl
# ═══════════════════════════════════════════════════════
# SERVER LOG ANALYZER
# Parses Apache/Nginx-style log entries, extracts
# statistics, identifies patterns, and generates
# a comprehensive security and performance report
# ═══════════════════════════════════════════════════════

use strict;
use warnings;

# ─── Simulated log data (Apache Combined Log Format) ───
my @log_entries = (
    '192.168.1.10 - admin [10/Jan/2025:08:15:22 +0000] "GET /index.html HTTP/1.1" 200 4523 "-" "Mozilla/5.0"',
    '192.168.1.10 - admin [10/Jan/2025:08:15:25 +0000] "GET /css/style.css HTTP/1.1" 200 1205 "/index.html" "Mozilla/5.0"',
    '10.0.0.5 - - [10/Jan/2025:08:16:01 +0000] "GET /api/users HTTP/1.1" 200 8432 "-" "Python-urllib/3.9"',
    '172.16.0.22 - - [10/Jan/2025:08:16:15 +0000] "POST /api/login HTTP/1.1" 401 245 "-" "curl/7.68"',
    '172.16.0.22 - - [10/Jan/2025:08:16:18 +0000] "POST /api/login HTTP/1.1" 401 245 "-" "curl/7.68"',
    '172.16.0.22 - - [10/Jan/2025:08:16:20 +0000] "POST /api/login HTTP/1.1" 401 245 "-" "curl/7.68"',
    '172.16.0.22 - - [10/Jan/2025:08:16:22 +0000] "POST /api/login HTTP/1.1" 200 1024 "-" "curl/7.68"',
    '192.168.1.10 - admin [10/Jan/2025:08:17:00 +0000] "GET /dashboard HTTP/1.1" 200 12045 "/index.html" "Mozilla/5.0"',
    '10.0.0.5 - - [10/Jan/2025:08:17:30 +0000] "GET /api/products HTTP/1.1" 200 24501 "-" "Python-urllib/3.9"',
    '192.168.1.50 - - [10/Jan/2025:08:18:00 +0000] "GET /admin/config HTTP/1.1" 403 512 "-" "Mozilla/5.0"',
    '192.168.1.50 - - [10/Jan/2025:08:18:05 +0000] "GET /admin/users HTTP/1.1" 403 512 "-" "Mozilla/5.0"',
    '10.0.0.5 - - [10/Jan/2025:08:18:30 +0000] "DELETE /api/users/5 HTTP/1.1" 204 0 "-" "Python-urllib/3.9"',
    '192.168.1.10 - admin [10/Jan/2025:08:19:00 +0000] "GET /reports HTTP/1.1" 200 8901 "/dashboard" "Mozilla/5.0"',
    '10.0.0.100 - - [10/Jan/2025:08:19:15 +0000] "GET /favicon.ico HTTP/1.1" 404 289 "-" "Mozilla/5.0"',
    '10.0.0.100 - - [10/Jan/2025:08:19:20 +0000] "GET /robots.txt HTTP/1.1" 404 289 "-" "Googlebot/2.1"',
    '192.168.1.10 - admin [10/Jan/2025:08:20:00 +0000] "PUT /api/settings HTTP/1.1" 200 512 "/dashboard" "Mozilla/5.0"',
    '172.16.0.22 - - [10/Jan/2025:08:20:30 +0000] "GET /api/users HTTP/1.1" 200 8432 "-" "curl/7.68"',
    '10.0.0.5 - - [10/Jan/2025:08:21:00 +0000] "GET /api/orders HTTP/1.1" 500 1024 "-" "Python-urllib/3.9"',
    '10.0.0.5 - - [10/Jan/2025:08:21:05 +0000] "GET /api/orders HTTP/1.1" 500 1024 "-" "Python-urllib/3.9"',
    '192.168.1.10 - admin [10/Jan/2025:08:22:00 +0000] "POST /api/reports/generate HTTP/1.1" 200 45023 "/reports" "Mozilla/5.0"',
    '10.0.0.200 - - [10/Jan/2025:08:22:30 +0000] "GET / HTTP/1.0" 301 0 "-" "Wget/1.21"',
    '10.0.0.200 - - [10/Jan/2025:08:22:31 +0000] "GET /index.html HTTP/1.1" 200 4523 "-" "Wget/1.21"',
    '192.168.1.50 - - [10/Jan/2025:08:23:00 +0000] "GET /../../../etc/passwd HTTP/1.1" 400 0 "-" "Mozilla/5.0"',
    '192.168.1.50 - - [10/Jan/2025:08:23:02 +0000] "GET /admin/shell.php HTTP/1.1" 404 289 "-" "Mozilla/5.0"',
    '192.168.1.10 - admin [10/Jan/2025:08:24:00 +0000] "GET /logout HTTP/1.1" 302 0 "/dashboard" "Mozilla/5.0"',
);

# ─── Parse log entries ───
my %ip_requests;
my %status_codes;
my %url_hits;
my %methods;
my %user_agents;
my %hourly;
my $total_bytes = 0;
my $total_requests = 0;
my @failed_logins;
my @suspicious;

my $log_pattern = qr/^(\S+) \S+ (\S+) \[([^\]]+)\] "(\S+) (\S+) \S+" (\d+) (\d+)/;

for my $entry (@log_entries) {
    if ($entry =~ $log_pattern) {
        my ($ip, $user, $timestamp, $method, $url, $status, $bytes) =
           ($1, $2, $3, $4, $5, $6, $7);

        $total_requests++;
        $total_bytes += $bytes;
        $ip_requests{$ip}++;
        $status_codes{$status}++;
        $url_hits{$url}++;
        $methods{$method}++;

        # Extract hour
        if ($timestamp =~ /(\d{2}):\d{2}:\d{2}/) {
            $hourly{$1}++;
        }

        # Extract user agent
        if ($entry =~ /"([^"]+)"$/) {
            $user_agents{$1}++;
        }

        # Track failed logins
        if ($url =~ /login/i && $status eq '401') {
            push @failed_logins, { ip => $ip, time => $timestamp };
        }

        # Track suspicious requests
        if ($url =~ /(\.\.|shell|passwd|admin)/i && $status =~ /^[45]/) {
            push @suspicious, { ip => $ip, url => $url, status => $status, time => $timestamp };
        }
    }
}

# ═══════════════════════════════════════════════════════
# REPORT OUTPUT
# ═══════════════════════════════════════════════════════

print "=" x 62, "\n";
print "         SERVER LOG ANALYSIS REPORT\n";
print "=" x 62, "\n\n";

# ─── Overview ───
print "-" x 62, "\n";
print "  TRAFFIC OVERVIEW\n";
print "-" x 62, "\n";
printf "  Total Requests:     %d\n", $total_requests;
printf "  Total Data Served:  %.2f KB\n", $total_bytes / 1024;
printf "  Avg Response Size:  %.0f bytes\n", $total_bytes / ($total_requests || 1);
printf "  Unique IPs:         %d\n", scalar keys %ip_requests;
printf "  Unique URLs:        %d\n", scalar keys %url_hits;
print "\n";

# ─── Status Code Distribution ───
print "-" x 62, "\n";
print "  HTTP STATUS CODE DISTRIBUTION\n";
print "-" x 62, "\n";
for my $code (sort keys %status_codes) {
    my $count = $status_codes{$code};
    my $pct = ($count / $total_requests) * 100;
    my $bar = "#" x int($pct / 2);
    my $label = $code eq '200' ? 'OK' :
                $code eq '204' ? 'No Content' :
                $code eq '301' ? 'Redirect' :
                $code eq '302' ? 'Found' :
                $code eq '400' ? 'Bad Request' :
                $code eq '401' ? 'Unauthorized' :
                $code eq '403' ? 'Forbidden' :
                $code eq '404' ? 'Not Found' :
                $code eq '500' ? 'Server Error' : 'Other';
    printf "  %s %-14s %3d (%5.1f%%) %s\n", $code, $label, $count, $pct, $bar;
}
print "\n";

# ─── Top IPs ───
print "-" x 62, "\n";
print "  TOP IP ADDRESSES BY REQUEST COUNT\n";
print "-" x 62, "\n";
my $rank = 1;
for my $ip (sort { $ip_requests{$b} <=> $ip_requests{$a} } keys %ip_requests) {
    my $count = $ip_requests{$ip};
    my $bar = "#" x $count;
    printf "  %d. %-18s %3d requests  %s\n", $rank++, $ip, $count, $bar;
}
print "\n";

# ─── HTTP Methods ───
print "-" x 62, "\n";
print "  HTTP METHOD BREAKDOWN\n";
print "-" x 62, "\n";
for my $method (sort { $methods{$b} <=> $methods{$a} } keys %methods) {
    my $count = $methods{$method};
    my $pct = ($count / $total_requests) * 100;
    printf "  %-8s %3d requests (%5.1f%%)\n", $method, $count, $pct;
}
print "\n";

# ─── Most Requested URLs ───
print "-" x 62, "\n";
print "  MOST REQUESTED URLS\n";
print "-" x 62, "\n";
$rank = 1;
for my $url (sort { $url_hits{$b} <=> $url_hits{$a} } keys %url_hits) {
    last if $rank > 10;
    printf "  %2d. %-35s %d hits\n", $rank++, $url, $url_hits{$url};
}
print "\n";

# ─── User Agents ───
print "-" x 62, "\n";
print "  CLIENT USER AGENTS\n";
print "-" x 62, "\n";
for my $ua (sort { $user_agents{$b} <=> $user_agents{$a} } keys %user_agents) {
    printf "  %-35s %d requests\n", $ua, $user_agents{$ua};
}
print "\n";

# ─── Security Analysis ───
print "-" x 62, "\n";
print "  SECURITY ANALYSIS\n";
print "-" x 62, "\n\n";

print "  Failed Login Attempts:\n";
if (@failed_logins) {
    my %login_by_ip;
    for my $fl (@failed_logins) {
        $login_by_ip{$fl->{ip}}++;
    }
    for my $ip (sort keys %login_by_ip) {
        my $count = $login_by_ip{$ip};
        my $alert = $count >= 3 ? " ** BRUTE FORCE ALERT **" : "";
        printf "    %-18s %d failed attempts%s\n", $ip, $count, $alert;
    }
} else {
    print "    No failed login attempts detected.\n";
}
print "\n";

print "  Suspicious Requests:\n";
if (@suspicious) {
    for my $s (@suspicious) {
        printf "    [%s] %-18s -> %-30s (HTTP %s)\n",
            $s->{time}, $s->{ip}, $s->{url}, $s->{status};
    }
} else {
    print "    No suspicious activity detected.\n";
}
print "\n";

# ─── Error Rate Analysis ───
my $errors_4xx = 0;
my $errors_5xx = 0;
for my $code (keys %status_codes) {
    $errors_4xx += $status_codes{$code} if $code =~ /^4/;
    $errors_5xx += $status_codes{$code} if $code =~ /^5/;
}

print "-" x 62, "\n";
print "  ERROR RATE ANALYSIS\n";
print "-" x 62, "\n";
printf "  Client Errors (4xx):  %d (%.1f%%)\n", $errors_4xx, ($errors_4xx / $total_requests) * 100;
printf "  Server Errors (5xx):  %d (%.1f%%)\n", $errors_5xx, ($errors_5xx / $total_requests) * 100;
printf "  Success Rate:         %.1f%%\n",
    (($total_requests - $errors_4xx - $errors_5xx) / $total_requests) * 100;

my $health = ($errors_5xx / $total_requests) * 100;
if ($health < 1) {
    print "  Server Health:        EXCELLENT\n";
} elsif ($health < 5) {
    print "  Server Health:        GOOD\n";
} elsif ($health < 10) {
    print "  Server Health:        WARNING\n";
} else {
    print "  Server Health:        CRITICAL\n";
}
print "\n";

print "=" x 62, "\n";
print "  Log Analysis Complete - $total_requests entries processed\n";
print "=" x 62, "\n";
