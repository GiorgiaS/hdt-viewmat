# https://treelib.readthedocs.io/en/latest/
# https://treelib.readthedocs.io/en/latest/genindex.html

from treelib import Tree, Node

class Trees(Tree):

    def __init__(self):
        super().__init__()

    def CreateDataTree(self):
        self.create_node('DataRoot', 'dataroot', parent = None) # It is for Wu&Palmer Similarity:
        self.create_node('All', 'all', parent='dataroot')
        # Physical sub-nodes
        self.create_node('Physical', 'physical', parent='all')
        ## Personal sub-nodes
        self.create_node('Personal', 'personal', parent='physical')
        ### Body shape sub-nodes
        self.create_node('Body Shape', 'bodyshape', parent='personal')
        self.create_node('Height', 'height', parent='bodyshape')
        self.create_node('Weight', 'weight', parent='bodyshape')
        ### Identity sub-nodes
        self.create_node('Identity', 'identity', parent='personal')
        self.create_node('Gender', 'gender', parent='identity')
        self.create_node('Race', 'race', parent='identity')
        ## System sub-nodes
        self.create_node('Systems', 'systems', parent='physical')
        ### Cardiovascular sub-nodes
        self.create_node('Cardiovascular', 'cardiovascular', parent='systems')
        self.create_node('BPM', 'bpm', parent='cardiovascular')
        self.create_node('ECG', 'ecg', parent='cardiovascular')
        self.create_node('CardioReport', 'cardioreport', parent='cardiovascular')
        ### Respiratory sub-nodes
        self.create_node('Respiratory', 'respiratory', parent='systems')
        self.create_node('Spirometry', 'spirometry', parent='respiratory')
        self.create_node('X-Ray', 'x-ray', parent='respiratory')
        self.create_node('PulmonaryReport', 'pulmonaryreport', parent='respiratory')
        # print(self)
        # self.show()

        return self

    def createPurposeTree(self):
        self.create_node('PurposeRoot', 'purposeroot', parent=None) # It is for Wu&Palmer Similarity:
        self.create_node('All', 'all', parent='purposeroot')
        # Medical sub-nodes
        self.create_node('Medical', 'medical', parent='all')
        self.create_node('Treatment', 'treatment', parent='medical')
        self.create_node('Monitoring', 'monitoring', parent='medical')
        self.create_node('Check', 'check', parent='medical')
        # Statistic sub-nodes
        self.create_node('Statistic', 'statistic', parent='all')
        self.create_node('Marketing Preferences', 'marketingpreferences', parent='statistic')
        ## Research sub-nodes
        self.create_node('Research', 'research', parent='all')
        self.create_node('Private', 'private', parent='research')
        self.create_node('Accademic', 'accademic', parent='research')
        # Marketing sub-nodes
        self.create_node('Marketing', 'marketing', parent='all')
        self.create_node('Suggestions', 'suggestions', parent='marketing')
        self.create_node('Offers', 'offers', parent='marketing')

        # print(self)
        # self.show()

        return self

    def getAncestor(self, tree, pp, pol):
        if tree.is_ancestor(pol, pp):
            # print('Trees::getAncestor - pol is the ancestor:', pol)
            return pol
        else: # if pp and pol are siblings
            if tree[pol] in tree.siblings(pp):
                # print('Trees::getAncestor - sibling nodes with ancestor:', tree.parent(pp))
                return tree.parent(pp)
            else:
                for parent in tree.rsearch(pp):
                    if tree.is_ancestor(parent, pol):
                        # print('Trees::getAncestor - lower ancestor:', parent)
                        return parent

    # getRootDistance() returns the number of nodes between the node and the root
    def getRootDistance(self, tree: Tree, node):
        # print(tree)
        if type(node) == Node:
            nodeId = node._identifier
        else:
            nodeId = node
        # print('Trees::getRootDistance - node ID:', node._identifier)
        nodes = tree.level(nodeId) - 1 
        # print('Trees::getRootDistance - nodes between the node and the root:', nodes)

        return nodes


