#!/usr/bin/env python

import argparse
import collections
from matplotlib import pyplot

from barcode.barcode import BarCode
from fastools import fastools

#from . import docSplit, version, usage
usage = ["", ""]

def makeHistogram(length):
    """
    """
    order = "TACGTACGTCTGAGCATCGATCGATGTACAGC"
    histogram = collections.defaultdict(int)

    for barcode in BarCode().allBarcodes(length):
        j = 0

        for i in fastools.collapse(barcode, 1)[0]:
            while order[j % len(order)] != i:
                j += 1
            j += 1
        #for

        histogram[j] += 1
    #for

    return histogram
#makeHistogram

def torrentflow(length):
    """
    """
    for i in range(1, length + 1):
        h = makeHistogram(i)

        x = pyplot.plot(h.keys(), h.values(), "o-", label=str(i))
    #for

    pyplot.legend(numpoints=1)
    pyplot.show()
#torrentflow

def main():
    """
    Main entry point.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=usage[0], epilog=usage[1])
    parser.add_argument("-l", dest="length", type=int, default=4,
        help="barcode lendth")

    args = parser.parse_args()

    torrentflow(args.length)
    #print "total: %i" % 4 ** args.length
#main

if __name__ == '__main__':
    main()
