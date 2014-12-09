if $::uptime_hours < 2 {
$myuptime = "Uptime is less than two hours.\n"
}
elsif $::uptime_hours < 5 {
$myuptime = "Uptime is less than five hours.\n"
}
else {
$myuptime = "Uptime is greater than four hours.\n"
}
file {'/root/conditionals.txt':
ensure => present,
content => $myuptime,
}
