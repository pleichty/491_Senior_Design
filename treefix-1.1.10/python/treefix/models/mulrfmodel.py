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
        self.count = 0
        self.log = open('matched.txt', 'w')
        
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
            #Recon plus find duplications in gene tree, for each gene tree leaf we map it to a stree leaf, we also keep track of duplications in the gene tree 
            leaves = gtree.leaves()
            for node in leaves:
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
                    #remove node from the parent's children list, create a new parent and append it the the old parent's children list 
                    node.parent.children.remove(node)
                    parent = treelib.TreeNode(name = streeCopy.new_name())
                    node.parent.children.append(parent)
                
                    count = 0 
                    #add a copy of the node to the new parent for each copy in the gene tree
                    append = parent.children.append
                    while count < len(find_dup[node]):
                        count = count + 1
                        append(node)
         
        def printLca(tree, lca):

            for node in lca:
                if  len(node.leaves()) > 1 and (node is not tree.root):
                    print >> self.log, node
                    print >> self.log, lca[node]
        
        #LCA method 
        def lca(node, lca_dict):
            """Creates a dictionary of (node, lca) pairs from given tree"""
            if node.is_leaf():
                lca_dict[node] = []
                lca_dict[node].append(node)
            
            else:
                lca_dict[node] = []
                append = lca_dict[node].append
                for child in node.children:
                    lca(child, lca_dict)
                    for x in lca_dict[child]:
                        append(x)

        stree_lca_dict = {}
        gtree_lca_dict = {}
        
        recon_dup(streeCopy, gtree, recon, find_dup)
        duplicate_nodes(streeCopy, find_dup)
        lca(gtree.root, gtree_lca_dict)
        lca(streeCopy.root, stree_lca_dict)
                        
        # used to determine the number of leaves in the lca in order to correctly calculate the cost
        #streeLeaveCount = 0
        #for node in stree_lca_dict:
            #if len(stree_lca_dict[node]) == 1:
                #streeLeaveCount = streeLeaveCount + 1;
         
        cost = len(stree_lca_dict) + (len(gtree_lca_dict) - len(gtree.leaves()) - 1 )
        
        #print >> self.log, self.count
        #print >> self.log, "STree"
        #treelib.draw_tree(streeCopy, out=self.log, minlen=5, maxlen=5)  
        #print >> self.log, "GTree"
        #treelib.draw_tree(gtree, out=self.log, minlen=5, maxlen=5)  
        
        
        for sNode in stree_lca_dict:
            #check leaf or root
            if len(stree_lca_dict[sNode]) > 1 and sNode != streeCopy.root:
                for gNode in gtree_lca_dict:
                    if len(stree_lca_dict[sNode]) == len(gtree_lca_dict[gNode]) and gNode != gtree.root:
                    
                        #Used to evaluate if the lca matches exactly.
                        stree_lca = []
                        for x in stree_lca_dict[sNode]:
                            stree_lca.append(x)
                    
                        match = True
                    
                        for node in gtree_lca_dict[gNode]:
                            if recon[node] not in stree_lca:
                                match = False
                                break
                            else:
                                stree_lca.remove(recon[node])
                    
                        if match:
                            #print >> self.log, stree_lca_dict[sNode]
                            cost = cost - 2
            #if node is a leaf or the root we subtract one, because we dont count the them 
            else:
                cost  = cost - 1
       
        
        #print >> self.log, "STree Lca"
        #printLca(streeCopy, stree_lca_dict)
        #print >> self.log, "GTree Lca"
        #printLca(gtree, gtree_lca_dict)
        #print >> self.log, cost
        #print >> self.log, ""         
        #self.count = self.count + 1
        #print cost 
        #raw_input("Press Enter to continue...")
        return cost
     

#cherry yum diddly dip