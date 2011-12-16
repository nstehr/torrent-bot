#!/usr/bin/env python

##  need more specifications on rpc protocol implemented by transmission-daemon?
##  consider reading http://trac.transmissionbt.com/browser/trunk/doc/rpc-spec.txt
##

__author__    = "lesion (lesion@autistici.org)"
__version__   = "$Revision: 0.1 $"
__date__      = "$Date: 2008/09/10 $"
__license__   = "GPL2"

"""
transmissionClient.py
"""

from simplejson import dumps, loads
from urllib import urlopen
import sys
import httplib


class TransmissionClientFailure(Exception): pass

class TransmissionClient(object):
  
  rpcUrl = None
  sessionId = None
  def __init__( self, rpcUrl='http://localhost:9091/transmission/rpc' ):
    """ try to do a stupid call to transmission via rpc """

    try:
      self.rpcUrl = rpcUrl
      #Nathan Stehr: June 4, 2009: 
      #the new version of transmission uses a session key, so make a dummy
      #request and get the session id from the headers 
      self._getSessionID()

    except Exception, e:
      raise TransmissionClientFailure, \
            "Make sure your transmission-daemon is running  %s" % e


  def _getSessionID(self):
       conn = httplib.HTTPConnection("localhost:9091")
       conn.request("GET", "/transmission/rpc?")
       response = conn.getresponse()
       self.sessionId = response.getheader('x-transmission-session-id')
  
  def _rpc( self, method, params=[] ):
    """ generic rpc call to transmission """

    postdata = dumps({ 'method': method, 
                       'arguments': params, 
                       })
    
    try:
        conn = httplib.HTTPConnection("localhost:9091")
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","x-transmission-session-id":self.sessionId}
        conn.request("POST", "/transmission/rpc", postdata,headers)
        response = conn.getresponse()
        status = response.status
        if status==409:
            self._getSessionID()
            self._rpc(method,params)
        data = response.read()
        conn.close()
        return loads(data)
    except Exception, e:
      raise TransmissionClientFailure, \
            "Make sure your transmission-daemon is running  %s" % e

    return response



  def sessionStats( self ):
    return self._rpc( 'session-stats' )


  def torrentGet( self, torrentIds='', fields=[ 'id', 'name']):
    if torrentIds == '':
        return self._rpc( 'torrent-get', {'fields': fields } )
    else:
        return self._rpc( 'torrent-get', { 'ids': torrentIds, 'fields': fields } ) 

  def torrentAdd( self, torrentFile, downloadDir='.' ):
    return self._rpc( 'torrent-add', { 'filename': torrentFile, 
                                      'download-dir': downloadDir } )


  def torrentRemove( self, torrents=None ):
    return self._rpc( 'torrent-remove', { 'ids': torrents } )


  def sessionSet( self, key, value ):
    return self._rpc( 'session-set', { key: value } )

  
  def sessionGet( self ):
    return self._rpc( 'session-get' )




