#!/usr/bin/env python
##############################################################################
## File: Lexer.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################


#### System Imports ##########################################################
import exceptions
import re
import os
#### Local Imports ###########################################################
from Core.Plex import *
class SchemaNotFound(Exception):
  pass
class Schema(object):
  def schemaFromDirt(self,Schema):
    schSplit = Schema.split(':')
    if schSplit[0] == 'strict':
      self.SchemaStrict = True
    self.SchemaName = schSplit[1]
    self.schemaLoad(self.SchemaName)

  def schemaLoad(self,Schema):
    if os.path.exists("Schema/" + Schema):
      Schema = open("Schema/" + Schema,"r")
      while 1:
        Line = Schema.readline()
        if not Line:
          break
    else:
      raise SchemaNotFound

class ProceduralParser(object):
  def __init__(self):
    self.noFurther   = False
    self.commands    = []
    self.useFeatures = []

  def ParseBlock(self,Text,Level):
    import os
    CleanText = Text[1:-2]
    #print '%d:%s' % (Level,CleanText)
    if Level == 0:
      if os.uname()[0] == CleanText:
        self.noFurther = False
        print '%d:%s' % (Level,CleanText)
      else:
        self.noFurther = True
    elif Level == 1 and not self.noFurther:
      print '%d:%s' % (Level,CleanText)
      self.commands.append(CleanText)
    elif Level == 2 and not self.noFurther:
      print '%d:%s' % (Level,CleanText)
      #Configurator.PutPackage(self,Package,Yaml)

  def ParseUseFeatureBlock(self,Text,Level):
    if not self.noFurther:
      self.useFeatures.append(Text[:-2].split('[')[1])
      print Text[:-2].split('[')[0]

  def ParseFeatureBlock(self,Text,Level):
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

  def runSchema(self,Sch):
    S = Schema()
    S.schemaFromDirt(Sch)

  def newLineReset(self):
    self.LexQueue = []

  def next(self):
    self.Value, self.Text = self.Lexer.read()
    self.nexted = True

  def expect(self,What):
    self.next()
    if self.Text == What:
      return True
    else:
      return False

  def runLexer(self):
    self.Value      = True
    self.Level      = 0
    self.flExpected = False

    while 1:
      self.BrackOpen = False
      self.nexted = False
      self.next()
      #print '[%s] %s' % (self.Value,self.Text) 
      if self.Value == 'INDENT':
        self.Level = self.Level + 1
      if self.Value == 'DEDENT':
        self.Level = self.Level - 1
      if self.Value == 'schema':
        print '[%s] %s' % (self.Value,self.Text[4:])
        self.runSchema(self.Text[4:])
      if self.Value == 'block':
        self.ProParse.ParseBlock(self.Text,self.Level)
      if self.Value == 'use_fblock':
        self.ProParse.ParseUseFeatureBlock(self.Text,self.Level)
      if self.Value == 'fblock':
        self.ProParse.ParseFeatureBlock(self.Text,self.Level)

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
