import fileinput
for line in fileinput.input('/etc/abc', inplace=True):
        print line.rstrip().replace('qwer', 'newLine'),
