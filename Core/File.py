import os
def rmDirectoryRecursive(Path):
	for I in os.listdir(Path):
		FullPath = Path + "/" + I
		if os.path.isdir(FullPath):
			rmDirectoryRecursive(FullPath)
		else:
			os.remove(FullPath)
	os.rmdir(Path)