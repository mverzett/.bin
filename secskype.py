#! /bin/env python

from Skype4Py import Skype
global gHandler
global gHeader
gHandler = None
gHeader = None

class Handler(object):
	def __init__(self):
		self.contact = None
		self.skype = Skype()
		self.skype.OnMessageStatus = Handler.OnMessageStatus
		print('***************************************')
		print 'Connecting to Skype..'
		self.skype.Attach()
		self.contacts = dict(
			(user.FullName, user.Handle) \
			for user in self.skype.Friends
			)
		self.handles = set(self.contacts.values())
		self.contact = None
		self.prev = None
	
	@staticmethod
	def OnMessageStatus(Message, Status):
		if Status == 'RECEIVED':
			print('\n %s >> Me : %s' % (Message.FromHandle, Message.Body))
			gHandler.prev = Message.FromHandle
			if gHeader:
				print gHeader,
		if Status == 'READ':
			return
			print "READ"
			print(Message.FromDisplayName + ': ' + Message.Body)
		if Status == 'SENT':
			return
	
	def parse_cmd(self, cmd):
		if not cmd:
			return
		allowed = {'.contacts', '.chat', '.exit', '.help', '.r', '.reply'}
		if cmd.startswith('.'):
			args = cmd.split()[1:]
			cmd = cmd.split()[0]
			if cmd not in allowed:
				print('This command is not allowed!\n'
					'Allowed commands: %s' % ','.join(allowed))
			if cmd == '.contacts':
				for i in self.contacts.iteritems():
					print('%s     :      %s' % i)
			if cmd == '.help':
				print 'allowed commands:' % ','.join(allowed)
			if cmd == '.chat':
				if not len(args):
					print 'you should provide one target!'
					return
				target = ' '.join(args)
				if target in self.contacts:
					self.contact = self.contacts[target]
				elif target in self.handles:
					self.contact = target
				else:
					print 'I do not have %s as a contact!' % target
			if cmd == '.r' or cmd == '.reply':
				if self.prev is None:
					print 'No-one to reply!'
				self.skype.SendMessage(self.prev, ' '.join(args))
		else:
			self.skype.SendMessage(self.contact, cmd)

gHandler = Handler()
cmd = ''
while not cmd == '.exit':
	gHeader = 'Me >> %s : ' % gHandler.contact
	cmd = raw_input(gHeader)
	gHandler.parse_cmd(cmd)
