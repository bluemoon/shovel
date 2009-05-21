import unittest
import Core.Lexer

from Core.Exceptions import SchemaNotFound

class TestCoreLexer(unittest.TestCase):
    def setUp(self):
        self.sch = Core.Lexer.Schema()
        
    def test_1_Schema_schemaFromDirt(self):
        ret = self.sch.schemaFromDirt('strict:mosaic')
        assert ret == 'mosaic'
        
    def test_2_fail_Schema_schemaLoad(self):
        ##schema = self.sch.schemaFromDirt('strict:mosaic')
        self.assertRaises(SchemaNotFound, self.sch.schemaLoad, 'test')
    
    def test_3_Schema_schemaLoad(self):    
        ret = self.sch.schemaFromDirt('strict:mosaic')
        asrt = self.sch.schemaLoad(ret)
        
        assert asrt
        
class TestCoreProceduralParser(unittest.TestCase):
    def setUp(self):
        self.par = Core.Lexer.ProceduralParser()