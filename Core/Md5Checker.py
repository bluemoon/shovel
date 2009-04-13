import md5
def md5checker():
	 f1 = file(os.path.join(path_1, os.listdir(path_1)[0]) ,'rb')
	 md5.new(f1.read()).digest())