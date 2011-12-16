import sys
import os

#setup the path, i.e add the 3rd party stuff I need
current_path= os.getcwd()
sys.path.append(os.path.join(current_path,'jml-1.0b3-full.jar'))

from net.sf.jml import MsnMessenger
from net.sf.jml import MsnUserStatus
from net.sf.jml.impl import MsnMessengerFactory
from net.sf.jml import MsnSwitchboard
from net.sf.jml.event import MsnAdapter
from net.sf.jml.message import MsnControlMessage
from net.sf.jml.message import MsnDatacastMessage
from net.sf.jml.message import MsnInstantMessage
from net.sf.jml import MsnContact
from net.sf.jml import Email
import urllib
from net.sf.jml import MsnFileTransfer
from input import InputHandler

class MSNEventHandler(MsnAdapter):
    #overridden call back functions
    def instantMessageReceived(self, switchboard,message,contact):
        receivedText = message.getContent()
        #set the switchboard, so that we can send messages
        self.switchboard = switchboard
        
        #defines how we should handle the commands received from the other end
        input_handler = InputHandler()
        output = input_handler.handleInput(receivedText)
         #send the msg to the buddy        
        msnMessage = MsnInstantMessage()
        msnMessage.setContent(output)
        self.sendMessage(msnMessage)
    
    #Apparently file transfer isn't working in the jml library....
    #file transfer is handled instead by passing the url in a message and then downloading in the bot code

    #def fileTransferRequestReceived(self,transfer):
    #    print "Transfer request received..."
    #    filename = transfer.getFile().getName()
    #    file = File('/Users/nate/dls'+filename)
    #    transfer.setFile(file)
    #    transfer.start()
        
    #def fileTransferFinished(self,transfer):
    #    print "File transfer done!!!"
        
    def loginCompleted(self,messenger):
        messenger.getOwner().setDisplayName(bot_config.screenname)
 
    def contactAddedMe(self,messenger,contact):
        messenger.addFriend(contact.getEmail(),contact.getFriendlyName())
        
     #non overridden functions
    def sendMessage(self,message):
        self.switchboard.sendMessage(message)
        
class MSNMessenger:
    def initMessenger(self,messenger):
        print "Initializing...."
        listener = MSNEventHandler()
        messenger.addMessageListener(listener)
        messenger.addFileTransferListener(listener)
        
        messenger.addContactListListener(listener)        
        
		
    def connect(self,email,password):
        
        messenger = MsnMessengerFactory.createMsnMessenger(email,password)
        messenger.getOwner().setInitStatus(MsnUserStatus.ONLINE)
        self.initMessenger(messenger)
        messenger.login()
        
        
class MSNConnector:
    def connect(self,username,password):
        messenger = MSNMessenger()
        messenger.connect(username,password)        
