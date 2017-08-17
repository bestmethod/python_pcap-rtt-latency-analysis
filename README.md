# python_pcap-rtt-latency-analysis
Python script to produce rtt (packet round trip) latency analysis from pcap files

Pre-requisites:
* tshark package (on ubuntu: $ sudo apt install tshark)
* python3 package (on ubuntu: $ sudo apt install python3)

Usage:
```
$ python3 rttcheck2.py directory_with_pcap_files/ tabbed|length
```
Tabbled and length are formating parameters only, see examples below.

Example 1:
```
$ python3 rttcheck2.py tcpdump_pcap_list/ tabbed
Filename: file1.pcap
Max_rtt_msec:39.821000000000005 Count_rtt:61486 Avg_rtt_msec:5.649642536511778
RTT_hist:
>0msec >1msec >2msec >4msec >8msec 16msec >32msec >64msec >128msec >256msec >512msec >1024msec
 61486  36174  32547  26964  18497   6030     243       0        0        0        0         0
==================================================
Filename: file2.pcap
Max_rtt_msec:40.493 Count_rtt:62467 Avg_rtt_msec:5.730288280211252
RTT_hist:
>0msec >1msec >2msec >4msec >8msec 16msec >32msec >64msec >128msec >256msec >512msec >1024msec
 62467  39910  37461  31515  19009   4783     157       0        0        0        0         0
==================================================
```

Example 2:
```
$ python3 rttcheck2.py tcpdump_pcap_list/ length
Filename: clf1002_clf1010.pcap
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
Filename: clf1003_clf1010.pcap
Max_rtt_msec:40.493 Count_rtt:62467 Avg_rtt_msec:5.730288280211252
RTT_hist:
 >msec	Count
0	62467
1	39910
2	37461
4	31515
8	19009
16	4783
32	157
==================================================
```
