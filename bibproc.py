#!/usr/bin/env python

### A quick hack to process the bibtex exported from refworks,
### replacing the refkeys by a new key based on first author, year
### and a running number (1--)

import sys
from textutil import text_to_id

import re

articles_lines = []
current = []

#pick keyword, value
re_kv = re.compile('([^=]+)=\{([^\}]+)\},.*')

# process input, collect entries
# readlines doesn't work on mac, due to DOS line breaks... split by \r
for line in sys.stdin.read().split('\r'):
    l = line.strip()
    if len(l) == 0:
        continue
    if line.startswith('@'):
        articles_lines.append(current)
        current = [l]
    else:
        if len(l)>0:
            current.append(l)

# process entries into key-value pairs
current = {}
failed = 0
refkeys = [] # keep track on refkeys used so far

for a in articles_lines:
    if len(a) == 0:
        continue
    line1 = a[0]
    etype = line1.split('{')[0] # @article or @something
    for l in a[1:]: # key={value}
        m = re_kv.match(l)
        if m and len(m.groups()) == 2:
            current[m.groups()[0]] = m.groups()[1]
    # pick name and year
    try:
        name = current['author']
        year = current['year']
        if len(name.split(' '))>1:
            try:
                name = name.split(' and')[0].split(' ')[-1]
            except:
                name = name.split(' ')[1].lower()
        else:
            name = name.lower()
        # pick a refkey
        idx = 1
        while True:
            refkey = text_to_id("%s_%s_%d" % (name, year, idx))
            if refkey in refkeys:
                idx += 1
            else:
                refkeys.append(refkey)
                break
        # print the article
        print "%s{%s,"%(etype, refkey)
        for key, val in current.items():
            print "    %s={%s},"%(key, val)
        print "}\n\n"
    except:
        sys.stderr.write("bad entry: %s\n"%str(a))
        failed += 1
        continue


