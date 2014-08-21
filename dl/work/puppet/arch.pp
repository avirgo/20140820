file { '/root/architecture.txt' :
ensure => file,
content => $::architecture ? {
'i386' => "This machine has a 32-bit architecture.\n",
'x86_64' => "This machine has a 64-bit architecture.\n",
}
}
