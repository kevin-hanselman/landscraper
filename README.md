landscraper
===========
Bringing you scenic desktop wallpapers courtesy of Reddit and its users.

Prerequisites
-----------
* python 3.x

Usage
------
```
usage: landscraper.py [-h] [-V] [-d DIR] [-a RATIO] [-T TOL] [-w WIDTH]
                      [-f {top,hot,new,random}] [-D]
                      [-t {hour,day,week,month,year,all}] [-c NUM]

Bringing you scenic desktop wallpapers courtesy of Reddit and its users.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -d DIR, --dir DIR     output directory for images
  -a RATIO              aspect ratio as decimal (e.g. 1.6)
  -T TOL, --tol TOL     aspect ratio absolute tolerance (e.g. 0.2)
  -w WIDTH              minimum resolution width as integer (e.g. 1024)
  -f {top,hot,new,random}
                        filter results from Reddit
  -D, --no-download     don't actually download any files
  -t {hour,day,week,month,year,all}
                        filter results by time, only applies to 'top'
  -c NUM, --count NUM   the maximum number of results to gather
```