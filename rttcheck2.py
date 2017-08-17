import sys
import os
import subprocess

comm="tshark -r %s%s%s -2 -R \"tcp.analysis.ack_rtt\" -e tcp.analysis.ack_rtt -T fields"

for fn in os.listdir(sys.argv[1]):
    print("Filename: %s" %fn)
    nTot=float(0)
    nCount=0
    nCountMs = {}
    nMax = float(0)
    proc = subprocess.Popen(comm%(sys.argv[1],"/",fn), shell=True, stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline().strip()
        if str(line) == "b''":
            break
        rtt = float(line)
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
    try:
        sys.argv[2]
    except:
        fmt="tabbed"
    else:
        if sys.argv[2] == "tabbed":
            fmt="tabbed"
        elif sys.argv[2] == "length":
            fmt="length"
        else:
            fmt="tabbed"
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
