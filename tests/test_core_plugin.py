import unittest
import mox
import os
import fnmatch

import core.debug as debug
import core.plugin as plugin

def locate(pattern, root):
    for path, dirs, files in os.walk(root):
        for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
            yield filename

def pathDifference(directory1, directory2):
    ''' accepts list input as in ['usr','home'] and ['usr','home','stuff']
        where the second input directory2 is the longer one.
    '''
    counter = 0
    while 1:
        try:
            if directory1[counter] == directory2[counter]:
                pass
            else:
                return directory2[counter:]
                break
                
        except IndexError:
            return directory2[counter:]
            break
            
        counter = counter + 1    

def getPlist():
    import plugins
    ''' gets all of the plugins '''
    rPath =  plugins.__dict__['__path__'][0]
    for loadable in locate('*.py', rPath):
        pyElement = loadable.split('/')[-1:]
        ## i only want the end element
        if pyElement[0] != '__init__.py':
            cwd = os.getcwd()
            diff = pathDifference(cwd.split('/'), loadable.split('/'))
            diffList = ['shovel']
            ## so our list is only ['shovel'] currently
            for k in diff[1:-1]:                
                diffList.append(k)
                ## now append all of the elements in the path
                ## list should be something like ['shovel','path','path']
                diffList.append(diff[-1:][0].split('.')[0])
                ## now append the last bit, stripped of the .py
                ## should be somethg like ['shovel','path','path','file']
                useString = '.'.join(diffList)
                yield useString


class TestCorePlugin(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
    def tearDown(self):
        self.mox.UnsetStubs()

    def test_1_pathDifference(self):
        output = plugin.pathDifference(['home','bluemoon'],['home','bluemoon','desktop','stuff'])
        assert output == ['desktop','stuff']
        
    def test_2_pathDifference(self):
        output = plugin.pathDifference(['home','bluemoon','desktop','stuff'], ['home','bluemoon'])
        assert output == []
    
    def test_3_plugin(self):
        p = plugin.plugin()
        p.config = self.mox.CreateMockAnything()
        #self.mox.StubOutWithMock(p.config, 'putFeature')]
        for each in getPlist():
            p.config.putFeature(each).InAnyOrder()

        self.mox.ReplayAll()
        #p.config.ReplayAll()
        p.getAll()

        self.mox.VerifyAll()

