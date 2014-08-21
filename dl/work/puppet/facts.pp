$string = "Hi, I'm a ${::osfamily} system and I have been up for ${::uptime}
seconds."
notify { 'info':
message => $string,
}
file { '/root/message.txt':
ensure => file,
content => $string,
}
