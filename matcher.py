import json
from trees import Trees
from similarity import Similarity

class Matcher:

    def match(self, id, ppFilename):
        similarity = Similarity()

        # get policy and pp
        pol = self.getPol(id)
        pp = self.getPP(id, ppFilename)

        # Create Data and Purpose Trees
        # dataTree.CreateDataTree()
        dataTree = Trees().CreateDataTree()
        purposeTree = Trees().createPurposeTree()

        # Compute similarity
        ## Data similarity
        # print('Matcher::match - data pp:', pp['data'], 'pol:', pol['data'])
        dataSimilarity = round(similarity.similarityWP(dataTree, pp['data'], pol['data']), 2)
        # print('Matcher::match - data similarity:', dataSimilarity)

        ## Purpose similarity
        # print('Matcher::match - purpose pp:', pp['purpose'], 'pol:', pol['purpose'])
        purposeSimilarity = round(similarity.similarityWP(purposeTree, pp['purpose'], pol['purpose']), 2)
        # print('Matcher::match - purpose similarity:', purposeSimilarity)

        ## Third Party similarity
        tpSimilarity = round(similarity.similarityJac(pp['third_party'], pol['third_party']), 2)
        # print('Matcher::match - third party similarity:', tpSimilarity)

        ## Retention similarity
        retSimilarity = round(similarity.similarityEuc(pp['retention'], pol['retention']), 2)
        # print('Matcher::match - retention similarity:', retSimilarity)

        agreement = {
            'data': dataSimilarity,
            'purp': purposeSimilarity,
            'tp': tpSimilarity,
            'ret': retSimilarity
        }

        return agreement

    
    def getPol(self, id):
        with open('./Policy&PP/policy AL = 1.json') as policy_file:
            policies = json.load(policy_file)
            return policies[id]
        
    def getPP(self, id, filename):
        with open(filename) as pp_file:
            # print('Matcher::getPP - filename:', filename)
            preferences = json.load(pp_file)
        return preferences[id]
