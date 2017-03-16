#!/usr/bin/expect

set timeout 3
set host [lindex $argv 0]
set hostname [lindex $argv 1]
set username "uname"
set password "s3cr3+"
set command1 "sys"
set command2 "acl number 1234"
set command3 "rule 10 permit source 1.2.3.4 0.0.0.255"
set command4 "quit"
set command5 "snmp-agent community read snmpcommunity acl 1234"
set command6 "return"
set command7 "save all"
set OUTPUT "dummy text"
eval spawn telnet $host
expect {
"Connected" {puts "Connected"}
"Connection closed by foreign host"  {set OUTPUT "Telnet busy, try again later"; puts "### OUTPUT for $hostname@$host: $OUTPUT ###"; exit}
"No route to host" {set OUTPUT "Destination host unreachable"; puts "### OUTPUT for $hostname@$host: $OUTPUT ###"; exit}
timeout {set OUTPUT "connection timeout"; puts "### OUTPUT for $hostname@$host: $OUTPUT ###"; exit}
}
expect {
"sername:" {send "$username\r"}
timeout {set OUTPUT "unexpected device maybe";  puts "### OUTPUT for $hostname@$host: $OUTPUT ###"; exit}
}
expect {
"assword:" {send "$password\r"}
timeout {set OUTPUT "unexpected device maybe";  puts "### OUTPUT for $hostname@$host: $OUTPUT ###"; exit}
}
expect {
">" {send "$command1\r"}
timeout {set OUTPUT "check login credentials"; puts "### OUTPUT for $hostname@$host: $OUTPUT ###"; exit}
}
expect "\]"
send "$command2\r"
expect "\]"
send "$command3\r"
expect "\]"
send "$command4\r"
expect "\]"
send "$command5\r"
expect "\]"
send "$command6\r"
expect ">"
send "$command7\r"
expect "n\]:"
send "y\r"
expect ">"
set OUTPUT "Done."
send "quit\r"
expect eof
puts "### OUTPUT for $hostname@$host: $OUTPUT ###"
