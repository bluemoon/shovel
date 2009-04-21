from setuptools import setup # this is new

setup(
	name='shovel',
	version='0.0.1-c2-dev',
	install_requires = ['PyYaml>=3.0'],
	scripts=['shovel'],
	packages=['Core','Plugins'],
)