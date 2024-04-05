from trees import Trees

class Similarity:

    # Compute the similarity between policy and pp trees
    # pp and pol corresponds to the 'data' or 'purpose' field
    def similarityWP(self, tree, pp, pol):
        if not tree.contains(pp):
            # print('Similarity::similarity - pp not in the tree:', pp)
            return 0
        if not tree.contains(pol):
            # print('Similarity::similarity - pol not in tree:', pol)
            return 0

        # return 1 if:
        # - pp and pol are the ID of the same node
        # - pp is ancestor of pol => pp includes the requirements of pol
        if pp == pol or tree.is_ancestor(pp, pol):
            # print('Similarity::similarity - pp = pol or pp is ancestor of pol')
            return 1

        ancestor = tree.getAncestor(tree, pp, pol)

        # print('Similarity::similarity - Ancestor:', ancestor)
        distanceRA = tree.getRootDistance(tree, ancestor)
        # print('Similarity::similarity - distance between Root and Ancestor (', ancestor, '):', distanceRA)
        distanceAPp = tree.getRootDistance(tree, pp)
        # print('Similarity::similarity - distance between Root and PP data (', pp, '):', distanceAPp)
        distanceAPol = tree.getRootDistance(tree, pol)
        # print('Similarity::similarity - distance between Root and Pol data (', pol, '):', distanceAPol)

        # Wu & Palmer Similarity:
        if distanceAPol == distanceRA and ancestor!=pol:
            similarityWP = (2 * distanceRA)/(distanceAPp - distanceRA)
        else:
            if distanceAPp == distanceRA:
                similarityWP = (2 * distanceRA)/(distanceAPol - distanceRA)
            else:
                # if distanceAPp != distanceRA and distanceAPol != distanceRA:
                similarityWP = (2 * distanceRA)/(distanceAPp + distanceAPol)

        # print('Similarity::similarity - W&P similarity:', similarityWP)

        return similarityWP
    
    def similarityJac(self, pp, pol):
        intersect = []
        for pref in pp:
            if pref in pol:
                intersect.append(pref)
        # print('Similarity::similarityJac - pp and pol intersection:', intersect)

        similarityJac = len(intersect)/(len(pp)+len(pol)-len(intersect))
        return similarityJac
    
    def similarityEuc(self, pp, pol):
        similarityEuc = 1 - (abs(pp-pol)/max(pp,pol))

        return similarityEuc