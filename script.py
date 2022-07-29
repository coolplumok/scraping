import sys, getopt

def main(argv):
   url = ''
   numbers = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'script.py -url <url> -videos <numbers>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'script.py -url <url> -videos <numbers>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         url = arg
      elif opt in ("-o", "--ofile"):
         numbers = arg
   print 'URL is "', url
   print 'Numbers of videos is "', numbers

if __name__ == "__main__":
   main(sys.argv[1:])