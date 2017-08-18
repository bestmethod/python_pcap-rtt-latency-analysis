# python_pcap-rtt-latency-analysis
## Version: 0.9b
### Version notes: works, does paramter parse and handles tshark errors. Only does reading and counting, so should be safe no matter what.
### Disclaimer: I take no responsibility for this software breaking anything, causing issues to systems, financial, or other loss, or for it destroying the planet. It comes with no guarantee and support.
Python script to produce rtt (packet round trip) latency analysis from pcap files

Pre-requisites:
* tshark package (on ubuntu: $ sudo apt install tshark)
* python3 package (on ubuntu: $ sudo apt install python3)

Usage:
```
Usage: rttcheck2.py [-h] [-d pcapDirectory] [-f pcapFile] [-p printFormat]
	-h | --help                                 	This help screen                                                        
	-d pcapDir | --pcap-dir=pcapDir             	Directory containing a list of pcap file to be analyzed                 
	-f pcapFile | --pcap-file=pcapFile          	A single pcap file that should be analyzed.                             
	.                                           	If pcap-dir is also provided, this file is added to the end of the list.
	-p printFormat | --print-format=printFormat 	Format used for printing. Currently available: tabbed|length            
```

Example 1:
```
$ python3 rttcheck2.py -d tcpdump_pcap_list/ -p tabbed
Filename: tcpdump_pcap_list/file1.pcap
Max_rtt_msec:39.821000000000005 Count_rtt:61486 Avg_rtt_msec:5.649642536511778
RTT_hist:
>0msec >1msec >2msec >4msec >8msec 16msec >32msec >64msec >128msec >256msec >512msec >1024msec
 61486  36174  32547  26964  18497   6030     243       0        0        0        0         0
==================================================
Filename: tcpdump_pcap_list/file2.pcap
Max_rtt_msec:40.493 Count_rtt:62467 Avg_rtt_msec:5.730288280211252
RTT_hist:
>0msec >1msec >2msec >4msec >8msec 16msec >32msec >64msec >128msec >256msec >512msec >1024msec
 62467  39910  37461  31515  19009   4783     157       0        0        0        0         0
==================================================
```

Example 2:
```
$ python3 rttcheck2.py -f file2.pcap -p length
Filename: file2.pcap
Max_rtt_msec:39.821000000000005 Count_rtt:61486 Avg_rtt_msec:5.649642536511778
RTT_hist:
 >msec	Count
0	61486
1	36174
2	32547
4	26964
8	18497
16	6030
32	243
==================================================
```
