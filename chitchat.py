#!/usr/bin/python


import readline, sys
import threading
import time

class Chat(threading.Thread):
	def __init__(self, fname, username):
		threading.Thread.__init__(self)
		self.fname=fname
		fh=open(fname, 'r')
		fh.seek(0,2)

		self.username = username

		self.pos = fh.tell()
		self.stop = False

	def run(self):
		while True:
			if self.stop:
				return
			fh = open(self.fname, 'r')
			fh.seek(self.pos)
			
			line = fh.read()
			if line:
				username, message=line.split(":", 1)
				self.printMessage(username, message)
				self.pos = fh.tell()
				fh.close()
			else:
				fh.close()
				time.sleep(0.5)
		print 'EOF'

	def watch(self):
		while True:
			if self.stop:
				return
			line = self.fh.readline()
			if not line:
				time.sleep(0.5)
				continue
			yield line

	def printMessage(self, username, message):
		sys.stdout.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')
		color=32
		if username == self.username:
			color=37
		print '\033[1;%dm%s\033[0m: %s' % (color, username, message)
		sys.stdout.write(readline.get_line_buffer())
		sys.stdout.flush()

print "Welcome to ChitChat"
print "\n"
username = None
#username = 'test'
while not username:
	username = raw_input('Please enter a name: ')

chat = Chat('chat.log', username)
chat.start()

print 'You may now chat'
print '________________'

def log(line):
	fh = open('chat.log', 'a')
	fh.write(line)
	fh.close()

log('System:%s has entered the chat...' % username) 

while True:
	try:
		#line = raw_input('[1;37m%s[0m: ' % username)
		line = raw_input()
		sys.stdout.write('\x1b[1A\r' + ' '*len(line) + '\r')
		if line:
			log('%s:%s' % (username, line))
	except KeyboardInterrupt, EOFError:
		chat.stop=True
		print "byebye!"
		sys.exit(0)
	except Exception:
		chat.stop=True
