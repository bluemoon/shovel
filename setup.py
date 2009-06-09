from setuptools import setup # this is new

setup(
  name='shovel',
  version='0.0.1',
  install_requires = ['PyYaml>=3.0'],
  scripts=['shovel'],
  packages=['core','plugins','lib','parsers','schema'],
  author = "Alex Toney",
  author_email = "toneyalex@gmail.com",
  license = "GPLv2",
  test_suite = 'nose.collector'
)
