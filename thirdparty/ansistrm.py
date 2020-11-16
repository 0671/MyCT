#coding:utf-8
import logging
import os
import re

if  os.name =='nt':
	import ctypes

class ColorizingStreamHandler(logging.StreamHandler):
	# color_map 为ansi转义序列中色彩的代码
	color_map={
	'black':0,
	'red':1,
	'green':2,
	'yellow':3,
	'blue':4,
	'magenta':5,
	'cyan':6,
	'white':7
	}
	# level_map 为日志记录各级别的对应ansi转义序列(背景色,字体色,字体强度)
	level_map={
	logging.DEBUG:(None,'blue',False),
	logging.INFO:(None,'green',False),
	logging.WARNING:(None,'yellow',None),
	logging.ERROR:(None,'red',None),
	logging.CRITICAL:('red','While',None),
	}
	csi='\x1b[' # ansi转义序列的前缀
	reset='\x1b[0m' # 当ansi转义序列为\x1b[0m时，则输出使用默认格式

	disable_coloring=False # 禁止彩色输出，默认为否


    # @property将函数转换为属性
    # is_tty 当前流为终端且允许彩色输出，返回true
	@property 
	def is_tty(self):
		isatty=getattr(self.stream,'isatty',None)
		return isatty and isatty() and not self.disable_coloring
	
	# 在logging.__file__下，打开__init__.py，找到emit函数
	# 可以看出来，emit函数 将记录进行格式化，然后输出
	# 而首先，我们进行彩色输出的第一步，需要给记录添加上彩色ANSI转义序列
	# 然后需要进行 彩色输出
	# 也就是说：我们先需要修改emit函数，使其调用专门的彩色输出
	# 所以我们在这里进行重构
	def emit(self,record):
		try:
			message=self.format(record) #将记录进行格式化,后面我们会重构format方法，使得format可以根据需要给记录添加上彩色ANSI转义序列
			stream=self.stream
			if not self.is_tty: #如果不是终端，则做些简单处理就直接输出
				if message and message[0]=="\r":
					message=message[1:]
				stream.write(message)
			else:               #终端的话，调用专用彩色输出函数
				self.output_colorized(message)
			stream.write(getattr(self,'terminator','\n')) #写入流 尾随符
			self.flush() #将内容从缓存写入流中
		except (KeyboardInterrupt, SystemExit):
			raise
		except IOError:
			pass
		except:
			self.handleError(record)

	# 接下来，我们需要构造彩色输出函数
	if not os.name == "nt": # 如果不是windows系统，则unix终端一般原生支持ansi转义序列，故而输出函数只需要直接write即可
		def output_colorized(self,message):
			self.stream.write(message)
	else:
		ansi_escape=re.compile(r'\x1b\[((?:\d+)(?:;(?:\d+))*)m') #通过这个正则，可以找到输出内容中的转义序列部分和日志记录部分
		nt_color_map={
		0:0x00,
		1:0x04,
		2:0x02,
		3:0x06,
		4:0x01,
		5:0x05,
		6:0x03,
		7:0x07,
		} # 因为windows控制端的颜色代码和ansi转义序列的颜色代码并不是一一对应的，所以需要进行映射

		def output_colorized(self,message):
			message_parts=self.ansi_escape.split(message)
			write=self.stream.write
			handle=None
			file_descripto=getattr(self.stream,'fileno',None)
			if file_descripto is not None:
				file_descripto=file_descripto()
				if file_descripto in (1,2):
					handle=ctypes.windll.kernel32.GetStdHandle(-10-file_descripto)
			while message_parts:
				text=message_parts.pop(0)
				if text:
					write(text)
				if message_parts:
					ansi_escape_parms=message_parts.pop(0)
					if handle is not None:
						ansi_escape_parms=[int(p) for p in ansi_escape_parms.split(';')]
						color=0
						for p in ansi_escape_parms:
							if 40<=p<=47:
								color|=self.nt_color_map[p-40]*0x10
							elif 30<=p<=37:
								color|=self.nt_color_map[p-30]
							elif p==1:
								color|=0x08
							elif p==0:
								color=0x07
							else:
								pass
						ctypes.windll.kernel32.SetConsoleTextAttribute(handle,color)
	def colorize(self,message,record):
		if record.levelno in self.level_map and self.is_tty:
			bg,fg,bold=self.level_map[record.levelno]
			ansi_escape_parms=[]
			if bg in self.color_map:
				ansi_escape_parms.append(str(self.color_map[bg]+40))
			if fg in self.color_map:
				ansi_escape_parms.append(str(self.color_map [fg]+30))
			if  bold in self.color_map:
				ansi_escape_parms.append('1')
			if ansi_escape_parms and message:
				if message.lstrip()!=message:
					prefix=re.search(r'^\s+',message).group(0)
					message=message[len(prefix):]
				else:
					prefix=""
				message="%s%s"%(prefix,''.join((self.csi,';'.join(ansi_escape_parms),'m',message,self.reset)))
		return message
	def format(self,record):
		message=logging.StreamHandler.format(self,record)
		return self.colorize(message,record)