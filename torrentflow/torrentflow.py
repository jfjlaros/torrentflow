#!/usr/bin/env python

import argparse
import collections
from matplotlib import pyplot

from barcode.barcode import BarCode
#from fastools import fastools

#from . import docSplit, version, usage
usage = ["", ""]

order = "TACGTACGTCTGAGCATCGATCGATGTACAGC"
key = "TCAG"

def findFlow(fragment):
    """
    Calculate the flow position after sequencing {fragment}.

    @arg fragment: A DNA fragment.
    @type fragment: str

    @returns: The flow position.
    @rtype: int
    """
    position = 0

    for nucleotide in fragment:
        while order[position % len(order)] != nucleotide:
            position += 1

    return position
#findFlow

def makeHistogram(fragments):
    """
    """
    histogram = collections.defaultdict(int)

    for fragment in fragments:
        histogram[findFlow(fragment)] += 1

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
    pyplot.xlabel("flow number")
    pyplot.ylabel("amount")
    pyplot.show()
#torrentflow

def testflow(barCodeList):
    """
    """
    h = makeHistogram(barCodeList)

    pyplot.plot(h.keys(), h.values(), "o-")
    pyplot.xlabel("flow number")
    pyplot.ylabel("amount")
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

def expand(flowcode, length):
    """
    """
    return flowcode + (flowcode[-1] * (length - len(flowcode)))
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
        help="flowcode lendth")

    args = parser.parse_args()

    #torrentflow(args.length)
    bc = genList(args.length)
    print '\n'.join(bc)
    testflow(bc)
#main

if __name__ == '__main__':
    main()
