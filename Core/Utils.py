import sys, os
import termios, fcntl, struct, sys

ColorList = {
'USE' : True,
'BOLD'  :'\x1b[01;1m',
'RED'   :'\x1b[01;91m',
'GREEN' :'\x1b[32m',
'YELLOW':'\x1b[33m',
'PINK'  :'\x1b[35m',
'BLUE'  :'\x1b[01;34m',
'CYAN'  :'\x1b[36m',
'NORMAL':'\x1b[0m',
'cursor_on'  :'\x1b[?25h',
'cursor_off' :'\x1b[?25l',
}

def PPrint(String, Label,Color=None,LabelColor=None):
	PadChar         = ' '
	EndPadLen       = 2
	LabelMessageLen = 0
	
	s = struct.pack("HHHH", 0, 0, 0, 0)
	fd_stdout = sys.stdout.fileno()
	x = fcntl.ioctl(fd_stdout, termios.TIOCGWINSZ, s)
	Pack = struct.unpack("HHHH", x)
	RowLen = Pack[1]
	
	TotalLen = RowLen
	if Label:
		LabelMessageLen = len(Label.splitlines()[0]) + 2
	
	StringLen = len(String.splitlines()[0])
	Padding = PadChar * (TotalLen - (StringLen + LabelMessageLen + EndPadLen))
	EndPad  = PadChar * EndPadLen
	
	Overflow = (StringLen/TotalLen)
	if Overflow:
		Counter = 0
		while Counter < Overflow:
			sys.stdout.write("%s%s%s\n" %
			(ColorList[Color.upper()], String[(Counter*TotalLen):((Counter+1)*TotalLen)], ColorList['NORMAL']))
			Counter += 1
			if Counter == Overflow:
				Padding = PadChar * (TotalLen - ((Counter*TotalLen) -((Counter+1)*TotalLen)))
				sys.stdout.write("%s%s%s%s[%s%s%s]\n" %
				(ColorList[Color.upper()], String[(Counter*TotalLen):((Counter+1)*TotalLen)], ColorList['NORMAL'], Padding, ColorList[LabelColor.upper()], Label, ColorList['NORMAL']))
			
	if Color:
		sys.stdout.write("%s%s%s%s[%s%s%s]%s\n" %
		(ColorList[Color.upper()], String, ColorList['NORMAL'], Padding, ColorList[LabelColor.upper()], Label, ColorList['NORMAL'],EndPad))
	else:
		sys.stdout.write("%s%s[%s%s%s]%s\n" %
		(String, Padding, ColorList[LabelColor.upper()], Label, ColorList['NORMAL'],EndPad))