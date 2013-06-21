#!/usr/bin/env python

import argparse
import collections
from matplotlib import pyplot

from barcode.barcode import BarCode
#from fastools import fastools

#from . import docSplit, version, usage
usage = ["", ""]

class FlowCode(object):
    order = "TACGTACGTCTGAGCATCGATCGATGTACAGC"
    key = "TCAG"

    def findFlow(self, fragment):
        """
        Calculate the flow position after sequencing {fragment}.

        @arg fragment: A DNA fragment.
        @type fragment: str

        @returns: The flow position.
        @rtype: int
        """
        position = 0

        for nucleotide in fragment:
            while self.order[position % len(self.order)] != nucleotide:
                position += 1

        return position
    #findFlow

    def findFlowCode(self, flow):
        """
        Find a flow code that lets the sequencer end in flow {flow}.

        @arg flow: Target flow.
        @type flow: int

        @returns: A flow code.
        @rtype str
        """
        flowcode = self.order[flow]

        for position in range(flow - 1, -1, -1):
            if self.order[position] == flowcode[-1]:
                flowcode += self.order[position + 1]

        return flowcode[::-1]
    #findFlowCode

    def expandFlowCode(self, flowcode, length):
        """
        Expand a flowcode by extending the last nucleotide into a stetch.

        @arg flowcode: A flowcode.
        @type flowcode: str
        @arg length: Target length of {flowcode}.
        @type length: int

        @returns: A flow code.
        @rtype str
        """
        return flowcode + (flowcode[-1] * (length - len(flowcode)))
    #expandFlowCode

    def makeFlowCodes(self, amount):
        """
        Make {amount} amount of flowcodes.

        @arg amount: Number of flowcodes to be generated.
        @amount: int

        @returns: List of flowcodes.
        @rtype: list(str)
        """
        bc = map(lambda x: self.findFlowCode(x), range(amount))
        newlength = max(map(lambda x: len(x), bc))

        return map(lambda x: self.expandFlowCode(x, newlength), bc)
    #makeFlowCodes
#FlowCode

def makeHistogram(fragments):
    """
    """
    histogram = collections.defaultdict(int)
    FC = FlowCode()

    for fragment in fragments:
        histogram[FC.findFlow(fragment)] += 1

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

    FC = FlowCode()
    #torrentflow(args.length)
    bc = FC.makeFlowCodes(args.length)
    print '\n'.join(bc)
    testflow(bc)
#main

if __name__ == '__main__':
    main()
