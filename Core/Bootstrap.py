class Bootstrap(object):
	"""docstring for Bootstrap"""
	def __init__(self, arg):
		super(Bootstrap, self).__init__()
		self.arg = arg
	def Build(self,Directory,Output):
		import tarfile, re
		pyFileExp = re.compile(".*\.py$")
		zipType = "bz2"
		if zipType not in zip_types:
			zipType = zip_types[0]
		tar = tarfile.open('%s.tar.%s' % (Output, zipType), "w:%s" % zipType)
		tarFiles=[]
		DirectoryList = os.listdir(Directory)
		files = [os.path.join(Directory, S) for S in DirectoryList if pyFileExp.match(S)]
		for x in files:
			tarinfo = tar.gettarinfo(x, x)
			tarinfo.uid = tarinfo.gid=1000
			tarinfo.uname = tarinfo.gname = "bozo"
			(code, size, cnt) = sfilter(x)
			tarinfo.size = size
			tar.addfile(tarinfo, code)
		tar.close()
		prefix = ''
		if Build.bld:
			prefix = Build.bld.env['PREFIX'] or ''
		'''
		reg = re.compile('^INSTALL=(.*)', re.M)
		code1 = reg.sub(r'INSTALL=%r' % prefix, code1)
		#change the tarfile extension in the waf script
		reg = re.compile('bz2', re.M)
		code1 = reg.sub(zipType, code1)

		f = open('%s.tar.%s' % (mw, zipType), 'rb')
		cnt = f.read()
		f.close()

		# the REVISION value is the md5 sum of the binary blob (facilitate audits)
		m = md5()
		m.update(cnt)
		REVISION = m.hexdigest()
		reg = re.compile('^REVISION=(.*)', re.M)
		code1 = reg.sub(r'REVISION="%s"' % REVISION, code1)

		def find_unused(kd, ch):
			for i in xrange(35, 125):
				for j in xrange(35, 125):
					if i==j: continue
					if i == 39 or j == 39: continue
					if i == 92 or j == 92: continue
					s = chr(i) + chr(j)
					if -1 == kd.find(s):
						return (kd.replace(ch, s), s)
			raise

		# The reverse order prevent collisions
		(cnt, C2) = find_unused(cnt, '\r')
		(cnt, C1) = find_unused(cnt, '\n')
		f = open('waf', 'wb')
		f.write(code1.replace("C1='x'", "C1='%s'" % C1).replace("C2='x'", "C2='%s'" % C2))
		f.write('#==>\n')
		f.write('#')
		f.write(cnt)
		f.write('\n')
		f.write('#<==\n')
		f.close()

		if sys.platform == 'win32' or Options.options.make_batch:
			f = open('waf.bat', 'wb')
			f.write('@python -x %~dp0waf %* & exit /b\n')
			f.close()

		if sys.platform != 'win32':
			os.chmod('waf', 0755)
		os.unlink('%s.tar.%s' % (mw, zipType 
		'''