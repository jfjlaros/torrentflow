#!/usr/bin/env python

import argparse
import collections
from matplotlib import pyplot

from barcode.barcode import BarCode
from fastools import fastools

#from . import docSplit, version, usage
usage = ["", ""]
order = "TACGTACGTCTGAGCATCGATCGATGTACAGC"

def makeHistogram(barcodeList):
    """
    """
    histogram = collections.defaultdict(int)

    for barcode in barcodeList:
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
        h = makeHistogram(list(BarCode().allBarcodes(i)))

        pyplot.plot(h.keys(), h.values(), "o-", label=str(i))
    #for

    pyplot.legend(numpoints=1)
    pyplot.show()
#torrentflow

def testflow(barCodeList):
    """
    """
    h = makeHistogram(barCodeList)

    pyplot.plot(h.keys(), h.values(), "o-")
    pyplot.show()
#testflow

def gen(pos):
    """
    """
    c = order[pos]
    w = c

    for i in range(pos - 1, -1, -1):
        if order[i] == c:
            w += order[i + 1]
            c = order[i + 1]
        #if

    return w[::-1]
#gen

def expand(barcode, length):
    """
    """
    return barcode + (barcode[-1] * (length - len(barcode)))
#expand

def genList(length):
    """
    """
    bc = map(lambda x: gen(x), range(length))
    newLength = max(map(lambda x: len(x), bc))

    return map(lambda x: expand(x, newLength), bc)
#genList

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

    #torrentflow(args.length)
    bc = genList(args.length)
    print '\n'.join(bc)
    #testflow(bc)
#main

if __name__ == '__main__':
    main()
