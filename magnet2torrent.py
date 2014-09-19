#!/usr/bin/python
#coding:utf-8
#author:Richard Liu
#email:richardxxx0x@gmail.com

import sys
import re
import random
import string
import datetime
import os.path
import requests
from optparse import OptionParser
import bencode

"""
  exit status
  0 ==> ok;
  1 ==> the url is not magnet format;
  2 ==> torrent file not on the server or you are offline or you need proxy;
  3 ==> local torrent not found
"""

class Magnet2Torrent(object):
  def __init__(self, magnet_url=""):
    self.magnet_url = magnet_url
    self.confirm = ['y','ye','yes']
  """
  Get magnet hash and output the torrent url
  """
  def get_hash(self):
    magnet_hash = re.search(r"urn:btih:(.*)&dn=", self.magnet_url)
    if magnet_hash:
      torrent_url = "http://torrage.com/torrent/"+magnet_hash.group(1)+".torrent"
      print "\nTorrent url is ===> %s" % (torrent_url)
    else:
      print "Your input url is not magnet format.Please check it."
      sys.exit(1)
    download = raw_input("\nDo you want to download this torrent?(y/n):")
    if download in self.confirm:
      self.download_torrent(torrent_url)
    else:
      sys.exit(0)
      
  """
  Download torrent from torrage.com
  
  Todo: 对content-type 进行判断，如果是 application/x-bittorrent ，ok，others no ok.
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
      print "\nFailed:The torrent you are looking for can not be found on the system or you need proxy or you are offline\n"
      sys.exit(2)
      
class RenameTorrent(object):
  def __init__(self, torrent_file=""):
    self.torrent_file = torrent_file
    self.save_type = ['1','2','3','4']
  
  def print_options(self):
    print "\n\tWhich type of torrent do you want to save? \n\
           1. Random name \n\
           2. Pinyin name \n\
           3. Poem name \n\n\
           anything else to exit \n\
           "

  def torrent_info(self):
    if not os.path.exists(self.torrent_file):
      print "file not found in current directory"
      sys.exit(3)
    with file(self.torrent_file) as f:
      raw_data = f.read()
      torrent_dic = bencode.bdecode(raw_data)
      # print torrent_dic['info']['name']
    self.print_options()
    save_type = raw_input('\t')
    if save_type == '1':
      self.random_name(torrent_dic)
    elif save_type == '2':
      pass
      # self.pinyin_name(torrent_dic)
    elif save_type == '3':
      # self.poem_name(torrent_dic)
      pass
    else:
      sys.exit(0)
    
  def random_name(self, torrent_dic):
    torrent_dic_new = torrent_dic
    file_name = self.torrent_file.split('.')[0]+'_random_name.torrent'
    try:
      length =  len(torrent_dic_new['info']['files'])
      for i in range(0,length):
        s=string.lowercase+string.digits
        content_type = torrent_dic_new['info']['files'][i]["path"][0].split('.')[-1]
        content_name = ''.join(random.sample(s,32))
        torrent_dic_new['info']['files'][i]["path"][0] = content_name + '.' + content_type
    except:
      n = len(torrent_dic_new['info']['name'].split('.'))
      content_type = '.'+torrent_dic_new['info']['name'].split('.')[-1] if n==2 else ''
    print "Before process,the content name is %s" % torrent_dic['info']['name']
    torrent_dic_new['info']['name'] = datetime.datetime.now().strftime("%y%m%d_%H%M%S")  + content_type
    print "After process,the content name is %s" % torrent_dic_new['info']['name']
    torrent_content_new = bencode.bencode(torrent_dic_new)
    with open(file_name,'wb') as f:
      f.write(torrent_content_new)
    
  # def pinyin_name(self, torrent_dic):
  # def poem_name(self, torrent_dic):
      
if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("-u", "--url", dest="url",
                    help="convert magnet link to torrent, like magnet:?xt=urn:btih:xxxx")
  parser.add_option("-f", "--file", dest="file",
                    help="print torrent info")
  
  (options, args) = parser.parse_args()

  if options.url:
    magnet2torrent = Magnet2Torrent(options.url)
    magnet2torrent.get_hash()
  
  elif options.file:
    torrentinfo = RenameTorrent(options.file)
    torrentinfo.torrent_info()
    
  else:
    parser.error("use -h or --help for help information")