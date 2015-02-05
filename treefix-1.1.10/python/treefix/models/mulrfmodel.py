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
        self.g = open('gtree.tree', 'w')
        
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
    
    def compute_cost(self, gtree):
        """Returns the duplication-loss cost"""
        #recon = phylo.reconcile(gtree, self.stree, self.gene2species)            
        
        recon = {}
        find_dup = {}
        streeCopy = self.stree.copy()
        
        def recon_dup(stree, gtree, recon, dup):
            #Recon plus find duplications in gene tree
            for node in gtree.leaves():
                sNode = stree.nodes[self.gene2species(node.name)]
                recon[node] = sNode
                if not sNode in dup:
                    dup[sNode] = []
                dup[sNode].append(node)
                
        def duplicate_nodes(tree, find_dup):
            #make modifications to the streeCopy to acount for duplications
            
            leaves = tree.leaves()
            for node in leaves:
                if node in find_dup and len(find_dup[node]) > 1:
                    node.parent.children.remove(node)
                    parent = treelib.TreeNode(name = streeCopy.new_name())
                    node.parent.children.append(parent)
                
                    count = 0 
                    while count < len(find_dup[node]):
                        count = count + 1
                        parent.children.append(node.copy(parent = parent))

        #LCA method 
        def lca(node, lca_dict):
            """Creates a dictionary of (node, lca) pairs from given tree"""
            if node.is_leaf():
                lca_dict[node] = []
                lca_dict[node].append(node)
            
            else:
                lca_dict[node] = []
                for child in node.children:
                    lca(child, lca_dict)
                    for x in lca_dict[child]:
                        lca_dict[node].append(x)
        
        #recon_dup(streeCopy, gtree, recon, find_dup)
        recon_dup(self.stree, gtree, recon, find_dup)
        #duplicate_nodes(streeCopy, find_dup)
                
                
        stree_lca_dict = {}
        gtree_lca_dict = {}
        
        #Using self.stree
        if False:
            recon_dup(self.stree, gtree, recon, find_dup)
            lca(self.stree.root, stree_lca_dict)
            lca(gtree.root, gtree_lca_dict)
            cost = (len(stree_lca_dict) - len(self.stree.leaves()) - 1) * 2
            
            
        
        #Using streeCopy
        if True:
            recon_dup(streeCopy, gtree, recon, find_dup)
            duplicate_nodes(streeCopy, find_dup)
            lca(streeCopy.root, stree_lca_dict)
            lca(gtree.root, gtree_lca_dict)
            cost = (len(stree_lca_dict) - len(streeCopy.leaves()) - 1) * 2
          
        # cost equals number of internal nodes from each tree
        cost = (len(stree_lca_dict) - len(streeCopy.leaves()) - 1 ) + (len(gtree_lca_dict) - len(gtree.leaves()) - 1 ) 
        
        # Removes root and leave node from list, we can save alot of compute time by leaving them in the list and checking to make sure we 
        # dont query them
        #del stree_lca_dict[self.stree.root]
        #for node in self.stree.leaves():
        #   del stree_lca_dict[node]
        
        for sNode in stree_lca_dict:
            # if is root or leaf continue: ??
            for gNode in gtree_lca_dict:
                
                #Used to evaluate if the lca matches exactly.
                stree_lca = []
                for x in stree_lca_dict[sNode]:
                    stree_lca.append(x)
                    
                match = True
                if len( stree_lca) == len(gtree_lca_dict[gNode]) and len( stree_lca) > 1 and gNode != gtree.root and sNode != streeCopy.root:
                    for node in gtree_lca_dict[gNode]:
                        if recon[node] not in stree_lca:
                            match = False
                            break
                        else:
                            stree_lca.remove(recon[node])
                    
                    if match:
                        cost = cost - 2

        
        #raw_input("Press Enter to continue...") 
        treelib.draw_tree(gtree, out=self.g, minlen=5, maxlen=5)    
        print >> self.g, cost 
        #print cost
        return cost
     
#cherry yum diddly dip