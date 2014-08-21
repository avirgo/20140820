# Allow users belonging wheel group to use sudo
augeas { 'sudoneeraj':
    context => '/files/etc/sudoers', # target file is /etc/sudoers
    changes => [
        # allow wheel users to use sudo
        'set spec[user = "neeraj"]/user neeraj',
        'set spec[user = "neeraj"]/host_group/host ALL',
        'set spec[user = "neeraj"]/host_group/command[1] "/bin/su - dctm"',
        'set spec[user = "neeraj"]/host_group/command[2] "/bin/su - cmsprod"',
        'set spec[user = "neeraj"]/host_group/command[3] "/bin/su - root"',
    ]
}

augeas { 'limitsdctm':
    context => '/files/security/limits.conf',
    changes => [
        'set spec[domain = "dctm"]/domain[1] dctm',
        'set spec[domain = "dctm"]/domain[1]/type soft',
        'set spec[domain = "dctm"]/domain[1]/item nproc',
        'set spec[domain = "dctm"]/domain[1]/value 131072',
        'set spec[domain = "dctm"]/domain[2] dctm',
        'set spec[domain = "dctm"]/domain[2]/type hard',
        'set spec[domain = "dctm"]/domain[2]/item nproc',
        'set spec[domain = "dctm"]/domain[2]/value 131072',
        'set spec[domain = "dctm"]/domain[3] dctm',
        'set spec[domain = "dctm"]/domain[3]/type soft',
        'set spec[domain = "dctm"]/domain[3]/item nofile',
        'set spec[domain = "dctm"]/domain[3]/value 131072',
        'set spec[domain = "dctm"]/domain[4] dctm',
        'set spec[domain = "dctm"]/domain[4]/type hard',
        'set spec[domain = "dctm"]/domain[4]/item nofile',
        'set spec[domain = "dctm"]/domain[4]/value 131072',
    ]
}
