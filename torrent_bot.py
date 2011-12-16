



__author__    = "Nathan Stehr (nstehr@gmail.com)"
__version__   = "$Revision: 1.0 $"
__date__      = "$Date: 2009/03/23 $"
__license__   = "GPL2"


#Torrent bot is a jython script that connects to the transmission (http://www.transmissionbt.com/) 
#bit torrent client via RPC and lets users communicate with their transmission client 
#via commands sent over the MSN network

#Makes use of:
# 1) the simplejson(http://code.google.com/p/simplejson/)
# 2) slightly modified version of: transmission client 
# (http://lesion.noblogs.org/post/2008/09/12/python-binding-to-transmission-1.33-bittorrent-client-jsonrpc)
# 3) java messenger library (http://jml.blathersource.org/)

from time import sleep
import bot_config
from connectors.msn import MSNConnector
        
def start():
    connector = MSNConnector()
    connector.connect(bot_config.username,bot_config.password)
    print "Connected"    

def main():
    start()
    while 1:
        sleep(10)


if __name__ == "__main__":
    main()
