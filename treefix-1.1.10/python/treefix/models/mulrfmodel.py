#
# Python module for duploss cost
#

# treefix libraries
from treefix.models import CostModel

# python libraries
import optparse

# rasmus libraries
from rasmus import treelib

# compbio libraries
from compbio import phylo

#=============================================================================

class MulRFModel(CostModel):
    """Computes Robinson-Foulds or MulRF costs"""

    def __init__(self, extra):
        """Initializes the model"""
        CostModel.__init__(self, extra)

        self.VERSION = "1.0.1"
        self.mincost = 0
        self.duplist = []
        parser = optparse.OptionParser(prog="MulRFModel")
        parser.add_option("-R", "--rfcost", dest="rfcost",
                          metavar="<robinson foulds cost>",
                          default=1.0, type="float",
                          help="robinson-foulds cost (default: 1.0)")
        self.parser = parser

        CostModel._parse_args(self, extra)

    def optimize_model(self, gtree, stree, gene2species):
        """Optimizes the model"""
        CostModel.optimize_model(self, gtree, stree, gene2species)
        
        #Checking for Duplications in the stree
        index = 0
        list = []
        for x in self.leaves():
            if x not in list:
                list.append(x)
            else
                if x in list & x not in self.duplist:
                    self.duplist.append(x)
        #end of duplication check
        #need to implement gtree transform
        
        if self.rfcost < 0:
            self.parser.error("-RF/--rfcost must be >= 0")

        # ensure gtree and stree are both rooted and binary
        if not (treelib.is_rooted(gtree) and treelib.is_binary(gtree)):
            raise Exception("gene tree must be rooted and binary")
        if not (treelib.is_rooted(stree) and treelib.is_binary(stree)):
            raise Exception("species tree must be rooted and binary")
        try:
            junk = phylo.reconcile(gtree, stree, gene2species)
        except:
            raise Exception("problem mapping gene tree to species tree")

    def recon_root(self, gtree, newCopy=True, returnCost=False):
        """Reroots the tree by minimizing the rf cost"""
        # assert valid inputs
        assert rootby in ["rf","mulrf"], "unknown rootby value '%s'" % rootby
        assert rfcost >= 0

        # make a consistent unrooted copy of gene tree
        if newCopy:
            gtree = gtree.copy()

        # TODO
        

    def compute_cost(self, gtree):
        """Returns the rf cost"""
        # TODO












        
#cherry yum diddly dip