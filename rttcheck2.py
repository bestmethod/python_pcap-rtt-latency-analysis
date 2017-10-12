import sys
import os
import subprocess
import getopt

def printusage(argv0):
  print('Usage: %s [-h] [-d pcapDirectory] [-f pcapFile] [-p printFormat]' %argv0)
  data='-h | --help\tThis help screen\n-d pcapDir | --pcap-dir=pcapDir\tDirectory containing a list of pcap file to be analyzed\n-f pcapFile | --pcap-file=pcapFile\tA single pcap file that should be analyzed.\n.\tIf pcap-dir is also provided, this file is added to the end of the list.\n-p printFormat | --print-format=printFormat\tFormat used for printing. Currently available: tabbed|length'
  rows = [ line.strip().split('\t') for line in data.split('\n') ]
  cols = zip(*rows)
  col_widths = [ max(len(value) for value in col) for col in cols ]
  format = ' '.join(['\t%%-%ds' % width for width in col_widths ])
  for row in rows:
      print(format % tuple(row))


def main(argv):
  fmt = "tabbed"
  nFileList = []
  try:
      opts, args = getopt.getopt(argv[1:],"hd:f:p:",["help","pcap-dir=","pcap-file=","print-format="])
  except getopt.GetoptError as e:
      print('Getopt Error: %s' %str(e))
      printusage(argv[0])
      return 2
  for opt, arg in opts:
      if opt in ('-h','--help'):
          printusage(argv[0])
          return 0
      elif opt in ("-d", "--pcap-dir"):
          for fn in os.listdir(arg): nFileList.append(os.path.join(arg,fn))
      elif opt in ("-f", "--pcap-file"):
          nFileList.append(arg)
      elif opt in ("-p", "--print-format"):
          if not arg in ['tabbed','length']:
              print('Error: print format must be one of: tabbed | length')
              printusage(argv[0])
              return 3
          fmt=arg
      else:
          print('Argument not recognised')

  if len(nFileList) == 0:
    print('No directories/files specified. Use either -d or -f (or both). Use --help to see full help')

  comm="tshark -r %s -2 -R \"tcp.analysis.ack_rtt\" -e tcp.analysis.ack_rtt -T fields"

  for fn in nFileList:
    print("Filename: %s" %fn)
    nTot=float(0)
    nCount=0
    nCountMs = {}
    nMax = float(0)
    proc = subprocess.Popen(comm%(fn), shell=True, stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline().strip()
        if str(line) == "b''" or str(line) == "":
            proc.communicate()
            if proc.returncode > 0:
                print("ERROR: Something went wrong with tshark (error should be above)")
                return 6
            break
        try:
            rtt = float(line)
        except:
            print("Error processing line: %s" %line)
        nTot = nTot + rtt
        nCount = nCount + 1
        if nMax < rtt: nMax = rtt
        for i in [0,1,2,4,8,16,32,64,128,256,512,1024]:
            if (rtt*1000) > i:
                try:
                    nCountMs[i] = nCountMs[i] + 1
                except KeyError:
                    nCountMs[i] = 1
    print("Max_rtt_msec:%s Count_rtt:%s Avg_rtt_msec:%s" %(str(nMax*1000),str(nCount),str(nTot/nCount*1000)))
    print("RTT_hist:")
    if fmt == "tabbed":
        data=">0msec >1msec >2msec >4msec >8msec 16msec >32msec >64msec >128msec >256msec >512msec >1024msec\n"
        for i in [0,1,2,4,8,16,32,64,128,256,512,1024]:
            try:
                if i == 0:
                    data="%s%s" %(data,str(nCountMs[i]))
                else:
                    data="%s %s" %(data,str(nCountMs[i]))
            except KeyError:
                data="%s 0" %data
        rows = [ line.strip().split(' ') for line in data.split('\n') ]
        cols = zip(*rows)
        col_widths = [ max(len(value) for value in col) for col in cols ]
        format = ' '.join(['%%%ds' % width for width in col_widths ])
        for row in rows:
            print(format % tuple(row))
    else:
        print(" >msec\tCount")
        for i in [0,1,2,4,8,16,32,64,128,256,512,1024]:
            try:
                print("%s\t%s" %(str(i),str(nCountMs[i])))
            except KeyError:
                pass
    print("==================================================")
  return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

