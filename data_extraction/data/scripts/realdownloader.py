import os
import re
import json
import time
import hashlib
import random
from bs4 import BeautifulSoup
from urllib.request import urlopen

IMAGEDIR='images'
PROFILES='real'

iurlrx = re.compile('.* background-image: url\(([^\)]+)\)')

remap = {'I am' : 'gender',
         'Age' : 'age',
         'City' : 'location',
         'Marital status' : 'status',
         'Username' : 'username',
         'Ethnicity' : 'ethnicity',
         'Occupation' : 'occupation',
         'About me' : 'description',
         'My match\'s age' : 'match_age',
         'Children' : 'children',
         'Sexual Orientation' : 'orientation',
         'Religion' : 'religion',
         'Do you smoke' : 'smoking',
         'Do you drink' : 'drinking',
         'Here for' : 'intent'}

def save_image(url):
    """ Take a URL, generate a unique filename, save 
        the image to said file and return the filename."""
    ext = url.split('.')[-1]
    filename = IMAGEDIR+os.sep+hashlib.md5(url.encode('utf-8')).hexdigest()+'.'+ext
    if os.path.exists(filename):
        return filename
    try:
        content = urlopen(url).read()
        # print('dskldk;sakd;a', len(content))
        f = open(filename,'wb') 
        # print("AFTER OPEEN")
        f.write(content)
        f.close()
        # print(f"Save image from {url}")
    except Exception as e:
      print('*********************************', url, filename)
      print(e)
      return None
    return filename 


def scrape_profile(inhandle, outfile):
  """Scrape an input scamdiggers page for the profile content
  of the scammer. """
  #Read file
  html = inhandle.read()
  soup = BeautifulSoup(html, 'html.parser')

  pfnode = soup.find('div', {'class':'profile-BASE_CMP_UserViewWidget'})
  avnode = soup.find(id='avatar_console_image')

  #Pull the provided profile data out.
  rows = pfnode.findAll('tr')
  labels = {}
  for row in rows:
    lab = row.find('td',{'class':'ow_label'})
    val = row.find('td',{'class':'ow_value'})
    if lab:
      labels[lab.get_text()] = val.get_text().strip()

  profile = {}

  #Populate our own profile structure.
  for lab in remap:
    if lab in labels:
      profile[remap[lab]] = labels[lab]
    else:
      profile[remap[lab]] = "-"
  
  #Tweak for consistency.
  profile['gender'] = profile['gender'].lower()
  
  #Extract avatar image
  img = iurlrx.match(avnode.attrs['style']).group(1)
  profile['images'] = [save_image(img)]

  #Save output
  json.dump(profile, open(outfile,'w+'))



def enumerate_profiles(inhandle):
  """ Extract all the profile page links from
  this index page. """
  html = inhandle.read()
  soup = BeautifulSoup(html, 'html.parser')
  
  urls = [ node.find('a')['href'] for node in soup.findAll('div',  {'class':'ow_user_list_data'})]
  return urls


def scrape():
  """ Harvest profiles from every third page from the site. """
  urls = []
  urlstr="http://datingnmore.com/site/users/latest?page={}" 

  print("Begin URL harvesting.")

  #For every third page (sample size calculated to finish overnight). 
  # for i in range(1,2000,2):
  # for i in range(1, 750, 2):
  # for i in range(750, 1500, 2):
  # for i in range(2, 751, 2):
  # for i in range(751, 1502, 2):
  # for i in range(1, 1000):
  for i in range(2500):
    url = urlstr.format(i)
    jitter = random.choice([0,1])
    try:
      urlhandle = urlopen(url)
      print(f"Open iurl {url}")
      # urls += enumerate_profiles(urlhandle)


      for url in enumerate_profiles(urlhandle):
        uid = url[33:]
        outfile=PROFILES+os.sep+uid+'.json'
        if os.path.exists(outfile):
            continue
        jitter = random.choice([0, 0, 0, 0, 1])
        try:
          urlhandle = urlopen(url)
          print(f"Open iurl {url} page: {i}")
          scrape_profile(urlhandle, outfile)
          time.sleep(jitter)
        except Exception as e:
          print("Exception when handling {} 456".format(url))
          print(e)
      

      # time.sleep(1+jitter)
    except Exception as e:
      print("Exception when handling {} 123".format(url))
      print(e)
      break

  print("Harvesting complete. {} URLs to scrape.".format(len(urls)))
      
  # for url, page in urls:
  # for i in range(len(urls)):
  #   url = urls[i]
  #   page = i
  #   uid = url[33:]
  #   outfile=PROFILES+os.sep+uid+'.json'
  #   if os.path.exists(outfile):
  #       continue
  #   jitter = random.choice([0, 0, 0, 0, 1])
  #   try:
  #     urlhandle = urlopen(url)
  #     print(f"Open iurl {url} page: {page}")
  #     scrape_profile(urlhandle, outfile)
  #     # time.sleep(jitter)
  #   except Exception as e:
  #     print("Exception when handling {} 456".format(url))
  #     print(e)
 
  print("Scraping complete.")


scrape()

