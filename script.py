import sys, getopt
import re
import requests
from bs4 import BeautifulSoup

pages   = set()
videos  = 0

def get_links(url, page_url):
  global pages
  pattern = re.compile("^(/)")
  html    = requests.get(f"{url}{page_url}")
  soup    = BeautifulSoup(html.content, "html.parser")
  for link in soup.find_all("a", href=pattern):
    if "href" in link.attrs:
      if link.attrs["href"] not in pages:
        new_page = link.attrs["href"]
        print(new_page)
        pages.add(new_page)
        get_links(url, new_page)

def get_video_links(url):
  #create response object
  r = requests.get(url)
  #create beautiful-soup object
  soup = BeautifulSoup(r.content,'html.parser')
  #find all links on web-page
  links = soup.findAll('a')
  #filter the link ending with .mp4
  video_links = [archive_url + link['href'] for link in links if link['href'].endswith('mp4')]
 
  return video_links

def download_video_series(video_links):
 
  for link in video_links:
    
   # iterate through all links in video_links
    # and download them one by one
    #obtain filename by splitting url and getting last string
    file_name = link.split('/')[-1]  
 
    print ("Downloading file:%s"%file_name)
 
    #create response object
    r = requests.get(link, stream = True)
 
    #download started
    with open(file_name, 'wb') as f:
      for chunk in r.iter_content(chunk_size = 1024*1024):
        if chunk:
          f.write(chunk)
 
    print ("%s downloaded!\n"%file_name)
 
  print ("All videos downloaded!")
  return

def main(argv):
  url     = ''
  numbers = 5
  global videos
  try:
    opts, args = getopt.getopt(argv,"u:v:",["url=","videos="])
  except getopt.GetoptError:
    print('script.py --url <url> --videos <numbers>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('script.py --url <url> --videos <numbers>')
      sys.exit()
    elif opt in ("-u", "--url"):
      url = arg
    elif opt in ("-v", "--videos"):
      numbers = arg
  get_links(url, "")
  for page in pages:
    if videos < int(numbers):
      video_links = get_video_links(url + page)
      print( page, " : ", video_links)
      videos += len(video_links)
      download_video_series(video_links)

if __name__ == "__main__":
  main(sys.argv[1:])