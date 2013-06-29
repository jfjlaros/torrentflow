#!/usr/bin/env python

#
# TODO: Design a set of barcodes that keep the flow in sync.
#

import argparse
import collections
from matplotlib import pyplot

from . import docSplit, version, usage

class FlowCode(object):
    """
    """

    order = "TACGTACGTCTGAGCATCGATCGATGTACAGC"
    key = "TCAG"

    def __init__(self):
        """
        Constructor.
        """
        self.floworder = self.order
        keyflow = self.findFlow(self.key)
        self.floworder = self.order[keyflow:] + self.order[:keyflow]
    #__init__

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
            while self.floworder[position % len(self.floworder)] != nucleotide:
                position += 1

        return position % len(self.floworder)
    #findFlow

    def findFlowCode(self, flow):
        """
        Find a flow code that lets the sequencer end in flow {flow}.

        @arg flow: Target flow.
        @type flow: int

        @returns: A flow code.
        @rtype str
        """
        flowcode = self.floworder[flow]

        for position in range(flow - 1, -1, -1):
            if self.floworder[position] == flowcode[-1]:
                flowcode += self.floworder[position + 1]

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
        @type amount: int

        @returns: List of flowcodes.
        @rtype: list(str)
        """
        flowcodes = map(lambda x: self.findFlowCode(x), range(amount))
        newlength = max(map(lambda x: len(x), flowcodes))

        return map(lambda x: self.expandFlowCode(x, newlength), flowcodes)
    #makeFlowCodes

    def makeHistogram(self, fragments):
        """
        Make a histogram of all the flows after sequencing {fragements}.

        @arg fragments: List of fragments.
        @type fragments: list(str)

        @returns: Counts of all flows.
        @rtype: dict(int)
        """
        histogram = collections.defaultdict(int)

        for fragment in fragments:
            histogram[self.findFlow(fragment)] += 1

        return histogram
    #makeHistogram
#FlowCode

def generate(amount, handle):
    """
    Generate a list of flowcodes and write them to a file.

    @arg amount: Number of flowcodes to be generated.
    @type amount: int
    @arg handle: Open writeable file handle.
    @type handle: stream
    """
    for flowcode in FlowCode().makeFlowCodes(amount):
        handle.write("%s\n" % flowcode)
#generate

def plot(handle):
    """
    Visualise the flows of a list of fagments.

    @arg fragmentList: List of fragemnts.
    @type fragmentList: list(str)
    @arg handle: Open readable file handle.
    @type handle: stream
    """
    fragments = map(lambda x: x.strip(), handle.readlines())
    histogram = FlowCode().makeHistogram(fragments)

    pyplot.bar(histogram.keys(), histogram.values())
    pyplot.xlim(-1, len(FlowCode.order) + 1)
    pyplot.ylim(0, len(fragments) + 1)
    pyplot.xlabel("flow number")
    pyplot.ylabel("amount")
    pyplot.show()
#plot

def main():
    """
    Main entry point.
    """
    input_parser = argparse.ArgumentParser(add_help=False)
    input_parser.add_argument("INPUT", type=argparse.FileType('r'),
        help="input file")

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=usage[0], epilog=usage[1])
    parser.add_argument("-v", action="version", version=version(parser.prog))
    subparsers = parser.add_subparsers(dest="subcommand")

    parser_generate = subparsers.add_parser("gen",
        description=docSplit(generate))
    parser_generate.add_argument("-a", dest="amount", type=int,
        default=len(FlowCode.order), help="amount of flowcodes")
    parser_generate.add_argument("OUTPUT", type=argparse.FileType('w'),
        help="output file")

    parser_plot = subparsers.add_parser("plot", parents=[input_parser],
        description=docSplit(plot))

    args = parser.parse_args()

    if args.subcommand == "gen":
        generate(args.amount, args.OUTPUT)

    if args.subcommand == "plot":
        plot(args.INPUT)
#main

if __name__ == '__main__':
    main()
