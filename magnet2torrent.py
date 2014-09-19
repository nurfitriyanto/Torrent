#!/usr/bin/python
#coding:utf-8
#author:Richard Liu
#email:richardxxx0x@gmail.com

import sys
import re
import os.path
import requests

"""
  exit status
  0 ==> ok;
  1 ==> the url is not magnet format;
  2 ==> torrent file not on the server;
"""
confirm = ['y','ye','yes']
class Magnet2Torrent(object):
  def __init__(self, magnet_url=""):
    self.magnet_url = magnet_url
    
  """
  Get magnet hash and output the torrent url
  """
  def get_hash(self):
    magnet_hash = re.search(r"urn:btih:(.*)&dn=", self.magnet_url)
    if magnet_hash:
      torrent_url = "http://torrage.com/torrent/"+magnet_hash.group(1)+".torrent"
      print "Torrent url is ===> %s" % (torrent_url)
    else:
      print "Your input url is not magnet format.Please check it."
      sys.exit(1)
    download = raw_input("If you want to download this torrent?(y/n):")
    if download in confirm:
      self.download_torrent(torrent_url)
    else:
      sys.exit(0)
      
  """
  Download torrent from torrage.com
  """
  def download_torrent(self, torrent_url):
    local_filename = torrent_url.split('/')[-1]
    try:
      r = requests.get(torrent_url)
      f = open(local_filename, 'wb')
      for chunk in r.iter_content(chunk_size=512 * 1024):
          if chunk: # filter out keep-alive new chunks
              f.write(chunk)
      f.close()
      print "Torrent downloaded."
    except:
      print "The torrent you are looking for can not be found on the system"
      sys.exit(2)

def main():
  magnet_url = sys.argv[1]
  magnet2torrent = Magnet2Torrent(magnet_url)
  magnet2torrent.get_hash()
  
if __name__ == "__main__":
  main()
