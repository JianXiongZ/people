#!/usr/bin/expect
for {set i 21} {$i < 86} {incr i} {
	spawn telnet 192.168.1.$i 
	send "reboot -f\r"
	expect eof
	puts "reboot 192.168.1.$i ok"
}

