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
#### Local Imports ###########################################################
from Core.Plex import *
class Lexi(object):
    def __init__(self):
        pass
    def loadLexer(self,File):
        self.fHandle = open(File,"r")
        self.Lexer = DirtLexer(self.fHandle)
    def runLexer(self):
        while 1:
            Value, Text = self.Lexer.read()
            if Text and Text <> Value:
                print "%s(%s)" % (Value, repr(Text))
            else:
                print repr(Value)
            if Value is None:
                break
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
    def DeclareSchema(self,Text):
        SchemaRe = re.compile("[a-zA-Z0-9\^\:]")
        Schema = SchemaRe.findall(Text)
        if Schema:
            print True
        else:
            print False
            
        
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
    Schema = (Str("---") + Opt(Str("^")) + Name + Str(":") + (Name|Number) + LineTerm)
    Block = (Rep(Name|Number) + Str(":") + Opt(Any(" \t")) + LineTerm)
    FeatureBlock = (Rep(Name|Number|Period|OpenBracket|CloseBracket) + Str(":"))
    Function = (Str("@") + Name + Opt(Rep(OpenBracket)+ AnyChar|Punctuation  + Rep(CloseBracket)))
    ListBlock = (Str("-") + Opt(Any(" \t")) + Rep(Name|Number|Period))

    Lexicon = Lexicon([
    	(Name,                  'name'),
    	(Number,                'number'),
    	(StringLiteral,         'string'),
        (Punctuation,           'punct'),
    	(OpenBracket,           OpenBracketAction),
    	(CloseBracket,          CloseBracketAction),
        (Schema,                DeclareSchema),
        #(Function,              'Function'),
        #(Block,                 'Block'),
        #(FeatureBlock,          'FeatureBlock'),
    	(LineTerm,              NewlineAction),
        (Comment,               IGNORE),
    	(Spaces,                IGNORE),
    	(EscapedNewline,        IGNORE),
    	State('indent', [
              (Indentation + Opt(Comment) + LineTerm, IGNORE),
              (Indentation, IndentationAction),
    	]),
     ])
