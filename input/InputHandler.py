import sys
from time import sleep
import os
import urllib
#setup the path, i.e add the 3rd party stuff I need
current_path= os.getcwd()
sys.path.append(os.path.join(current_path,'simplejson-1.9.2/simplejson'))
sys.path.append(os.path.join(current_path,'python-transmission/python-transmission'))
import bot_config
import traceback

from transmissionClient import TransmissionClient


class InputHandler:

    def handleInput(self,receivedMsg):
        client = TransmissionClient()
        command = receivedMsg.lower()
        output = ""
        if command == 'overview':
            results = client.sessionStats()
            arguments = results['arguments']
            
            uploadSpeed = arguments['uploadSpeed']
            uploadSpeed = float(uploadSpeed)/1000
            uploadSpeed = str(uploadSpeed) + " kb/s"
            
            downloadSpeed = arguments['downloadSpeed']
            downloadSpeed = float(downloadSpeed)/1000
            downloadSpeed = str(downloadSpeed) + " kb/s"
            
            activeTorrents = str(arguments['activeTorrentCount'])
            pausedTorrents = str(arguments['pausedTorrentCount'])
            totalTorrents = str(arguments['torrentCount'])
            
            output = "Download Speed: "+downloadSpeed+"\n"
            output = output + "Upload Speed: "+uploadSpeed+"\n"
            output = output + "Number of Active Torrents: " + activeTorrents+"\n"
            output = output + "Number of Paused Torrents: " + pausedTorrents+"\n"
            output = output + "Total Number of Torrents: " + totalTorrents
            
        if command == 'all torrents':
            torrents = self.getTorrentList(client)
            if len(torrents) == 0:
                output = "No torrents in the system"
            for torrent in torrents:
                output = output+self.calculateTorrentMsg(torrent)
                
                
        if command.startswith("get torrent"):
            torrentName = command.split(":")[1].lower()
            torrents = self.getTorrentList(client)
            for torrent in torrents:
                name = torrent['name']
                if name.lower() == torrentName:
                    output = self.calculateTorrentMsg(torrent)
                    break
            if output == "":
               output = "Torrent not found"
               
        if command.startswith("download torrent"):
            command=command.replace(':','#',1)
            url = command.split("#")[1]
            filename = self.saveFile(url)
            results = client.torrentAdd(filename)
            success = results['result']
            output = "Addition of torrent was a "+success

        if command.startswith("delete torrent"):
            torrentName = command.split(":")[1].lower()
            torrents = self.getTorrentList(client)
            id = -1
            for torrent in torrents:
                name = torrent['name']
                if name.lower() == torrentName:
                    id = torrent['id']
                    break
            if id == -1:
                output = "Torrent not found"
            else:
                results = client.torrentRemove(id)
                success = results['result']
                output = "Deletion of torrent was a "+success

        if command.startswith("help"):
            output = "Commands \n"
            output = output+"overview --> Overview of torrent client current state \n"
            output = output+"all torrents --> Info on all torrents currently being downloaded or seeded \n"
            output = output+"get torrent:<torrent name> --> Info on the specified torrent \n"
            output = output+"download torrent:<url of torrent file> --> Downloads the specified torrent file and starts downloading it \n"
            output = output+"delete torrent:<torrent name> --> Removes the torrent, but does not delete the data \n"
            sessionStats = client.sessionGet()
            output = output + "\n Transmission Version: " + sessionStats['arguments']['version']
                       
        return output
                
    def getTorrentList(self,client):
        results  = client.torrentGet(fields=['name','id','totalSize','downloadedEver','rateDownload','rateUpload','files'])
        torrents = results['arguments']['torrents']
        return torrents

    def calculateTorrentMsg(self,torrent):
        name = torrent['name']
        totalSize = float(torrent['totalSize'])/1048576
        totalSize = round(totalSize,3)
        #downloaded = float(torrent['downloadedEver'])/1048576
        #downloaded = round(downloaded,3)
        #going to calculate current downloaded amount based on the files array.  The above method seems to be off when
        #the client has been stopped and restarted
        files = torrent['files']
        
        sum = 0
        for file in files:
            sum = sum+file['bytesCompleted']
        downloaded = float(sum) / 1048576
        downloaded = round(downloaded,3)
        downloadRate = float(torrent['rateDownload'])/1000
        downloadRate = round(downloadRate,3)
        uploadRate = float(torrent['rateUpload'])/1000
        uploadRate = round(uploadRate,3)
        percent = (downloaded/totalSize)*100
        percent = round(percent,3)
              

        torrentMsg = "Name: "+name+"\n"
        torrentMsg = torrentMsg + "Total Size: "+str(totalSize)+" MB \n"
        torrentMsg = torrentMsg + "Downloaded So Far: "+str(downloaded) +" MB \n"
        torrentMsg = torrentMsg + "Percent Completed: "+ str(percent)+" %\n"
        torrentMsg = torrentMsg + "Download Rate: " + str(downloadRate) + " kb/s \n"
        torrentMsg = torrentMsg + "Upload Rate: " + str(uploadRate) + " kb/s \n"
             

        remaining = totalSize-downloaded
        remaining = remaining * 1024 
        if remaining > 0:
            if downloadRate > 0:
                #time in seconds
                time = remaining/downloadRate
                time = uptime(time)
                torrentMsg = torrentMsg +"Time Remaining "+ time +"\n"
            else:
                torrentMsg = torrentMsg +"Time Remaining ? \n"
        else:
            torrentMsg = torrentMsg +"Download complete \n"
        output = torrentMsg+"-----\n"
        return output
    
    def saveFile(self,link):
        try:
            webFile = urllib.urlopen(link)
            localFile = open(link.split('/')[-1], 'wb')
            localFile.write(webFile.read())
            webFile.close()
            localFile.close()
            path = os.getcwd()+os.sep+localFile.name
            return path
        except Exception:
            type,value,tb = sys.exc_info()
            traceback.print_exception(type,value,tb)
            traceback.print_tb(tb)
            
#uptime function from: http://thesmithfam.org/blog/2005/11/19/python-uptime-script/
def uptime(total_seconds):
     # Helper vars:
     MINUTE  = 60
     HOUR    = MINUTE * 60
     DAY     = HOUR * 24
     # Get the days, hours, etc:
     days    = int( total_seconds / DAY )
     hours   = int( ( total_seconds % DAY ) / HOUR )
     minutes = int( ( total_seconds % HOUR ) / MINUTE )
     seconds = int( total_seconds % MINUTE )
     # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
     string = ""
     if days> 0:
         string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
     if len(string)> 0 or hours> 0:
         string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
     if len(string)> 0 or minutes> 0:
         string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
     string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
     return string;