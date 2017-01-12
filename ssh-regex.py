import re

commands = {
	# only hostname
	'ssh hostname'                             : 'hostname',
	'ssh host.name.example.com'                : 'host.name.example.com',

	# only hostname with username
	'ssh root@foo.example.com'                 : 'foo.example.com',

	# with options
	'ssh -v hostname'                          : 'hostname',
	'ssh -vv hostname'                         : 'hostname',
	'ssh -l foo hostname'                      : 'hostname',
	'ssh -l bar test@hostname'                 : 'hostname',
	'ssh -l root bar123.ex-ample.com'          : 'bar123.ex-ample.com',
	'ssh -v -i asdaff.pem -l root 10.10.10.10' : '10.10.10.10',
	'ssh -vv -p 8888 10.123.213.1'             : '10.123.213.1',
	'ssh -vv -p 8888 -1 10.123.213.1'          : '10.123.213.1',

	# options after hostname
	'ssh -p 8888 -v 10.123.213.1 -l root'      : '10.123.213.1',

	# short options an option with param with no space
	'ssh -vv -p8888 -1 10.123.213.1 -l root'   : '10.123.213.1',

	# 2 options with param without space
	'ssh -p8888 -lroot -v 10.123.213.1'        : '10.123.213.1',

	# hostname with path
	'ssh -v 10.123.213.1/foo/1'                : '10.123.213.1',
}

username     = '[^@]*@'
empty_option = '-[1246AaCfGgKkMNnqsTtVvXxYy]+\s'
param_option = '-[bcDEeFIiLlmOopQRSWw]+\s*\S+\s'
hostname     = '(?P<host>[^\s/]+)\s?'

reg_str = '^ssh\s+(%s|((%s)*(%s)*)*)%s' % (username, empty_option, param_option, hostname)

print "\n-----------\n%s\n-----------\n" % reg_str

reg = re.compile(reg_str)

testSummarySuccess = True
for command in commands:
	res = re.match(reg, command)

	hostname = '<not found>'
	if res:
		hostname = res.group('host')

	testSuccess = (commands[command] == hostname)
	testSummarySuccess &= testSuccess
	testResult = 'ok' if testSuccess else 'failed'

	print '[%s] Check "%s" -> %s' % (testResult, command, hostname)

print "\nTest %s" % ('passed' if testSummarySuccess else 'failed')