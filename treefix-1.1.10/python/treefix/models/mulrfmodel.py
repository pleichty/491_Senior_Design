#
# Python module for robinson foulds cost
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
        
        # parser = optparse.OptionParser(prog="MulRFModel")
        # parser.add_option("-R", "--rfcost", dest="rfcost",
                          # metavar="<robinson foulds cost>",
                          # default=1.0, type="float",
                          # help="robinson-foulds cost (default: 1.0)")
        # self.parser = parser

        # CostModel._parse_args(self, extra)

    def optimize_model(self, gtree, stree, gene2species):
        """Optimizes the model"""
        CostModel.optimize_model(self, gtree, stree, gene2species)
               
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
        recon = phylo.reconcile(gtree, self.stree, self.gene2species)
        
        #rf_cost = recon.size
        #for every node in recon:
        #   for every othernode in recon.dropLeft(index.nodeIn(recon)):
        #       if there exists an inverse for this key-value pair, subtract 2  
        #       from recon cost.

        rf_cost = len(recon)
        recon_relevant = recon.copy()
        for node_key, node_value in recon.items():
            recon_relevant.pop(node_key, node_value)
            for othernode_key, othernode_value in recon_relevant.items():
                if (node_key is othernode_value) and (node_value is othernode_key):
                    rf_cost = rf_cost - 2
        
        return rf_cost












        
#cherry yum diddly dip