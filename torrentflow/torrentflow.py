#!/usr/bin/env python

import argparse
import collections
from matplotlib import pyplot

from barcode.barcode import BarCode

#from . import docSplit, version, usage
usage = ["", ""]

def makeHistogram(length):
    """
    """
    order = "TACGTACGTCTGAGCATCGATCGATGTACAGC"
    histogram = collections.defaultdict(int)

    for barcode in BarCode().allBarcodes(length):
        i = 0
        j = 0

        while j < len(barcode):
            while j < len(barcode) and order[i % len(order)] == barcode[j]:
                j += 1
            i += 1
        #while

        histogram[i] += 1
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

    print torrentflow(args.length)
    print "total: %i" % 4 ** args.length
#main

if __name__ == '__main__':
    main()
