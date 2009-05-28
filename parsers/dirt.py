## File: Lexer.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)


## System imports
import re
import os

## Local imports
from Lib.Plex import *

from Core.Exceptions import SchemaNotFound


class Schema(object):
    def schemaFromDirt(self, schema):
        ## split up the schema so its parseable
        schSplit = schema.split(':')
        if schSplit[0] == 'strict':
            self.schemaStrict = True
        self.schemaName = schSplit[1]
        return self.schemaName
        ## self.schemaLoad(self.schemaName)

    def schemaLoad(self, schema):
        if os.path.exists("Schema/" + schema):
            sch = open("Schema/" + schema,"r")
            while 1:
                line = sch.readline()
                if not line:
                    break
            return schema
        else:
            raise SchemaNotFound

class ProceduralParser(object):
    def __init__(self):
        self.noFurther   = False
        self.commands    = []
        self.useFeatures = []

    def parseBlock(self, text, level):
        import os
        cleanText = text[1:-2]
        #print '%d:%s' % (Level,CleanText)
        if Level == 0:
            if os.uname()[0] == cleanText:
                self.noFurther = False
                print '%d:%s' % (level, cleanText)
            else:
                self.noFurther = True
        
        elif level == 1 and not self.noFurther:
            print '%d:%s' % (level, cleanText)
            self.commands.append(cleanText)
            print self.commands
      
        elif level == 2 and not self.noFurther:
            print '%d:%s' % (level, cleanText)
            #Configurator.PutPackage(self,Package,Yaml)

    def parseUseFeatureBlock(self, text, level):
        if not self.noFurther:
            self.useFeatures.append(Text[:-2].split('[')[1])
            print Text[:-2].split('[')[0]

    def parseFeatureBlock(self,Text,Level):
        if not self.noFurther:
            print "  " + Text

class Lexi(object):
  def __init__(self):
    self.LexQueue = []
    self.Current = []
    self.ProParse = ProceduralParser()
  
  def loadLexer(self,File):
    self.fHandle = open(File,"r")
    self.Lexer = DirtLexer(self.fHandle)

  def runSchema(self,sch):
    sch = Schema()
    sch.schemaFromDirt(sch)

  def newLineReset(self):
    self.LexQueue = []

  def next(self):
    self.value, self.text = self.Lexer.read()
    self.nexted = True

  def expect(self,What):
    self.next()
    if self.Text == What:
      return True
    else:
      return False

  def runLexer(self):
    self.level      = 0
    self.flExpected = False

    while 1:
        self.brackOpen = False
        self.nexted = False
        self.next()
         
        ## here we keep track of the indent level
        if self.value == 'INDENT':
            self.level = self.level + 1
            
        if self.value == 'DEDENT':
            self.level = self.level - 1
            
        ## if we match the schema block    
        if self.value == 'schema':
            print '[%s] %s' % (self.value,self.text[4:])
            self.runSchema(self.text[4:])
            
        if self.Value == 'block':
            self.ProParse.parseBlock(self.text,self.level)
            
        if self.Value == 'use_fblock':
            self.ProParse.parseUseFeatureBlock(self.Text,self.Level)
            
        if self.Value == 'fblock':
            self.ProParse.parseFeatureBlock(self.Text,self.Level)

        if self.Value is None:
            break
      
        if not self.nexted:
            self.next()

      #self.LexQueue.append(self.Text)
      
                
class DirtLexer(Scanner):
  def __init__(self,File):
    Scanner.__init__(self,self.Lexicon,File)
    self.NestingLevel        =  0
    self.IndentationStack    = [0]
    self.BracketNestingLevel =  0      
    self.begin('indent')
    
  def OpenBracketAction(self, Text):
    self.BracketNestingLevel = self.BracketNestingLevel + 1
    return Text
    
  def CloseBracketAction(self, Text):
    self.BracketNestingLevel = self.BracketNestingLevel - 1
    return Text
    
  def CurrentLevel(self):
    return self.IndentationStack[-1]
    
  def NewlineAction(self, Text):
    if self.BracketNestingLevel == 0:
      self.begin('indent')
      return 'newline'
      
  def IndentationAction(self, Text):
    CurrentLevel = self.CurrentLevel()
    NewLevel = len(Text)
    if NewLevel > CurrentLevel:
      self.IndentTo(NewLevel)
    elif NewLevel < CurrentLevel:
      self.DedentTo(NewLevel)
    self.begin('')
    
  def IndentTo(self, newLevel):
    self.IndentationStack.append(newLevel)
    self.produce('INDENT', '')

  def DedentTo(self, newLevel):
    while newLevel < self.CurrentLevel():
      self.IndentationStack.pop()
      self.produce('DEDENT', '')
  
            
        
  def eof(self):
    self.DedentTo(0)
    
  Letter   = Range("AZaz") | Any("_")
  Digit    = Range("09")
  HexDigit = Range("09AFaf")
  Name     = Letter + Rep(Letter | Digit)
  Number   = Rep1(Digit) | (Str("0x") + Rep1(HexDigit))
  Indentation = Rep(Str(" ")) | Rep(Str("\t"))

  SqString = (
      Str("'") + 
      Rep(AnyBut("\\\n'") | (Str("\\") + AnyChar)) + 
      Str("'"))
  DqString = (
      Str('"') + 
      Rep(AnyBut('\\\n"') | (Str("\\") + AnyChar)) + 
      Str('"'))
  NonDq = AnyBut('"') | (Str('\\') + AnyChar)
  TqString = (
      Str('"""') +
      Rep(
      NonDq |
      (Str('"') + NonDq) |
      (Str('""') + NonDq)) + Str('"""'))
    
  StringLiteral = SqString | DqString | TqString
  Punctuation = Any(":,;<>+*/|&=.%`~^-!@")
  Period = Str(".")
  Colon = Str(":")
  OpenBracket  = Any("{([<")
  CloseBracket = Any("})]>")
  bBracketOpen  = Str("{")
  bBracketClose = Str("}") 
  bFunction = (OpenBracket + Rep(Name|Punctuation|Number) + CloseBracket)
  iFunction = ( Any("!") + Name + AnyBut(" \n"))
  Function = (Any("@") + Name + ((OpenBracket + AnyChar + CloseBracket)| AnyChar))
  Diphthong = Str("==", "!=", "<=", "<<", ">>", "**")
  Spaces = Rep1(Any(" \t"))
  Comment = Str("#") + Rep(AnyBut("\n"))
  EscapedNewline = Str("\\\n")
  LineTerm = Str("\n") | Eof
  Schema = (Str("---") + Opt(Str("^")) + Name + Str(":") + (Name|Number))
  Block = (OpenBracket + Rep(Punctuation|Name) + CloseBracket + Str(":"))
  FeatureBlock = (Rep(Punctuation|Name) + Str(":") + Rep(AnyBut('\n')) )
  wUseFeatureBlock = (Name + OpenBracket + Rep(Punctuation|Name) + CloseBracket + Str(":"))
  
  Function = (Str("@") + Name + Opt(Rep(OpenBracket)+ AnyChar|Punctuation  + Rep(CloseBracket)))
  ListBlock = (Str("-") + Opt(Any(" \t")) + Rep(Name|Number|Period))

  Lexicon = Lexicon([
        (Name,                  'name'),
        (Number,                'number'),
        (StringLiteral,         'string'),
        (Punctuation,           'punct'),
        (Schema,                'schema'),
        (Block,                 'block'),
        (wUseFeatureBlock,      'use_fblock'),
        (FeatureBlock,          'fblock'),
        (OpenBracket,           OpenBracketAction),
        (CloseBracket,          CloseBracketAction),
        (LineTerm,              NewlineAction),
        (Comment,               IGNORE),
        (Spaces,                IGNORE),
        (EscapedNewline,        IGNORE),
        State('indent', [
              (Indentation + Opt(Comment) + LineTerm, IGNORE),
              (Indentation, IndentationAction),
        ]),
     ])
