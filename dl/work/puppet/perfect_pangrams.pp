$perfect_pangram = 'Bortz waqf glyphs vex muck djin.'
$pgdir = '/root/pangrams'
file { $pgdir:
ensure => directory,
}
file { "${pgdir}/perfect_pangrams":
ensure => directory,
}
file { "${pgdir}/perfect_pangrams/bortz.txt":
ensure => file,
content => "A perfect pangram: \n${perfect_pangram}",
}
