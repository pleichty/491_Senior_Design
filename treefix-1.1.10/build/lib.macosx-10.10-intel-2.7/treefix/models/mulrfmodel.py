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

#debug
import StringIO
#=============================================================================

class MulRFModel(CostModel):
    """Computes Robinson-Foulds or MulRF costs"""

    def __init__(self, extra):
        """Initializes the model"""
        CostModel.__init__(self, extra)

        self.VERSION = "1.0.1"
        self.mincost = 0
        self.printed = False
    def optimize_model(self, gtree, stree, gene2species):
        """Optimizes the model"""
        CostModel.optimize_model(self, gtree, stree, gene2species)
        
        # ensure gtree and stree are both rooted and binary
        if not (treelib.is_rooted(gtree) and treelib.is_binary(gtree)):
            raise Exception("gene tree must be rooted and binary")
        if not (treelib.is_rooted(stree) and treelib.is_binary(stree)):
            raise Exception("species tree must be rooted and binary")
        try:
            junk = phylo.reconcile(gtree, stree, gene2species)
        except:
            raise Exception("problem mapping gene tree to species tree")
    
        treeout = StringIO.StringIO()
        if not self.printed:
            import pprint
            treelib.draw_tree(gtree, out=treeout, minlen=5, maxlen=5)
            print "gene tree:\n"
            print(treeout.getvalue())
            
            treelib.draw_tree(self.stree, out=treeout, minlen=5, maxlen=5)
            print "spec tree:\n"
            print(treeout.getvalue())
            pprint.pprint(junk)

            self.printed = True

    
    def compute_cost(self, gtree):
        """Returns the rf cost"""
        recon = phylo.reconcile(gtree, self.stree, self.gene2species)
        
        #rf_cost = recon.size
        #for every node in recon:
        #   for every othernode in recon.dropLeft(index.nodeIn(recon)):
        #       if there exists an inverse for this key-value pair, subtract 2  
        #       from recon cost.
        
        rf_cost = 0
        recon_relevant = recon.copy()
        for node_key, node_value in recon.items():
            if not node_key.name is node_value.name:
                rf_cost += 1
         
        # for node_key, node_value in recon.items():
        #     recon_relevant.pop(node_key, node_value)
        #     for othernode_key, othernode_value in recon_relevant.items():
        #         if (node_key.name is othernode_value.name) and (node_value.name is othernode_key.name):
        #             rf_cost -= 2
        
        return rf_cost
     
#cherry yum diddly dip