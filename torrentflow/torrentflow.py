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

    def __init__(self, key, prefix):
        """
        Constructor.

        @arg key: Key sequence.
        @type key: str
        @arg prefix: Initialisation sequence.
        @type prefix: str
        """
        self.mod = len(self.order)
        self.offset = 0
        self.offset = self.findFlow(key)
        self.offset = self.findFlow(prefix)
    #__init__

    def findFlow(self, fragment):
        """
        Calculate the flow position after sequencing {fragment}.

        @arg fragment: A DNA fragment.
        @type fragment: str

        @returns: The flow position.
        @rtype: int
        """
        position = self.offset

        for nucleotide in fragment:
            while self.order[position % self.mod] != nucleotide:
                position += 1

        return position % self.mod
    #findFlow

    def findFlowCode(self, flow):
        """
        Find a flow code that lets the sequencer end in flow {flow}.

        @arg flow: Target flow.
        @type flow: int

        @returns: A flow code.
        @rtype str
        """
        offset = self.offset + flow
        flowcode = self.order[offset % self.mod]

        for position in range(offset - 1, self.offset - 1, -1):
            if self.order[position % self.mod] == flowcode[-1]:
                flowcode += self.order[(position + 1) % self.mod]

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

def generate(amount, handle, key, prefix):
    """
    Generate a list of flowcodes and write them to a file.

    @arg amount: Number of flowcodes to be generated.
    @type amount: int
    @arg handle: Open writeable file handle.
    @type handle: stream
    @arg key: Key sequence.
    @type key: str
    @arg prefix: Initialisation sequence.
    @type prefix: str
    """
    maxFc = len(FlowCode.order)

    if amount > maxFc:
        raise ValueError("Amount of flow codes too large (max=%i)." % maxFc)

    for flowcode in FlowCode(key, prefix).makeFlowCodes(amount):
        handle.write("%s\n" % flowcode)
#generate

def plot(handle, key, prefix):
    """
    Visualise the flows of a list of fagments.

    @arg fragmentList: List of fragemnts.
    @type fragmentList: list(str)
    @arg handle: Open readable file handle.
    @type handle: stream
    @arg key: Key sequence.
    @type key: str
    @arg prefix: Initialisation sequence.
    @type prefix: str
    """
    fragments = map(lambda x: x.strip(), handle.readlines())
    histogram = FlowCode(key, prefix).makeHistogram(fragments)

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

    init_parser = argparse.ArgumentParser(add_help=False)
    init_parser.add_argument("-k", dest="key", type=str, default=FlowCode.key,
        help="key sequence (%(type)s default=\"%(default)s\")")
    init_parser.add_argument("-i", dest="prefix", type=str, default="",
        help="initialisation sequence (%(type)s default=\"%(default)s\")")

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=usage[0], epilog=usage[1])
    parser.add_argument("-v", action="version", version=version(parser.prog))
    subparsers = parser.add_subparsers(dest="subcommand")

    parser_generate = subparsers.add_parser("gen", parents=[init_parser],
        description=docSplit(generate))
    parser_generate.add_argument("-a", dest="amount", type=int,
        default=len(FlowCode.order),
        help="amount of flowcodes (%(type)s default=%(default)s)")
    parser_generate.add_argument("OUTPUT", type=argparse.FileType('w'),
        help="output file")

    parser_plot = subparsers.add_parser("plot", parents=[input_parser,
        init_parser], description=docSplit(plot))

    args = parser.parse_args()

    if args.subcommand == "gen":
        try:
            generate(args.amount, args.OUTPUT, args.key, args.prefix)
        except ValueError, err:
            parser.error(err)
    #if

    if args.subcommand == "plot":
        plot(args.INPUT, args.key, args.prefix)
#main

if __name__ == '__main__':
    main()
