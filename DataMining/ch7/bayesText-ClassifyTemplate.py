import os, codecs, math

class BayesText:

    def __init__(self, trainingdir, stopwordlist):
        """This class implements a naive Bayes approach to text
        classification
        trainingdir is the training data. Each subdirectory of
        trainingdir is titled with the name of the classification
        category -- those subdirectories in turn contain the text
        files for that category.
        The stopwordlist is a list of words (one per line) will be
        removed before any counting takes place.
        """
        self.vocabulary = {}
        self.prob = {}
        self.totals = {}
        self.stopwords = {}
        f = open(stopwordlist)
        for line in f:
            self.stopwords[line.strip()] = 1
        f.close()
        categories = os.listdir(trainingdir)
        #filter out files that are not directories
        self.categories = [filename for filename in categories
                           if os.path.isdir(trainingdir + filename)]
        print("Counting ...")
        for category in self.categories:
            print('    ' + category)
            (self.prob[category],
             self.totals[category]) = self.train(trainingdir, category)
        # I am going to eliminate any word in the vocabulary
        # that doesn't occur at least 3 times
        toDelete = []
        for word in self.vocabulary:
            if self.vocabulary[word] < 3:
                # mark word for deletion
                # can't delete now because you can't delete
                # from a list you are currently iterating over
                toDelete.append(word)
        # now delete
        for word in toDelete:
            del self.vocabulary[word]
        # now compute probabilities
        vocabLength = len(self.vocabulary)
        print("Computing probabilities:")
        for category in self.categories:
            print('    ' + category)
            denominator = self.totals[category] + vocabLength
            for word in self.vocabulary:
                if word in self.prob[category]:
                    count = self.prob[category][word]
                else:
                    count = 1
                self.prob[category][word] = (count + 1) / denominator
        print ("DONE TRAINING\n\n")
                    

    def train(self, trainingdir, category):
        """counts word occurrences for a particular category"""
        currentdir = trainingdir + category
        files = os.listdir(currentdir)
        counts = {}
        total = 0
        for file in files:
            #print(currentdir + '/' + file)
            f = codecs.open(currentdir + '/' + file, 'r', 'iso8859-1')
            for line in f:
                tokens = line.split()
                for token in tokens:
                    # get rid of punctuation and lowercase token
                    token = token.strip('\'".,?:-')
                    token = token.lower()
                    if token != '' and not token in self.stopwords:
                        self.vocabulary.setdefault(token, 0)
                        self.vocabulary[token] += 1
                        counts.setdefault(token, 0)
                        counts[token] += 1
                        total += 1
            f.close()
        return(counts, total)
                    
                    
    def classify(self, filename):
        results = {}
        wordList=[]
        f = codecs.open(filename,'r','iso8859-1')
        for line in f:
            tokens=line.split()
            for token in tokens:
                # get rid of punctuation and lowercase token
                token = token.strip('\'".,?:-')
                token = token.lower()
                if token != '' and not token in self.stopwords:
                    wordList.append(token)
            for category in self.categories:
                if category not in results:
                    results[category]=0
                else:
                    for word in wordList:
                        if word in self.prob[category]:
                            i = self.prob[category][word]
                            if i>0 :
                                results[category]+=math.log(i)
        maxval=0
        coreval=0
        for i in results.keys():
            if results[i]>maxval:
                maxval=results[i]
                coreval=i
        return coreval






              
# change these to match your directory structure
trainingDir = "/Users/mohamedkane/Desktop/selfDev/DataMining/ch7/20news-bydate/20news-bydate-train/"
# (just create an empty file to use as a stoplist file.)
stoplistfile = "/Users/mohamedkane/Desktop/selfDev/DataMining/ch7/20news-bydate/stoplist.txt"

bT = BayesText(trainingDir, stoplistfile)
print("Running Test ...")
result = bT.classify("/Users/mohamedkane/Desktop/selfDev/DataMining/ch7/20news-bydate/20news-bydate-test/rec.motorcycles/104673")
print(result)
result = bT.classify("/Users/mohamedkane/Desktop/selfDev/DataMining/ch7/20news-bydate/20news-bydate-test/sci.med/59246")
print(result)
result = bT.classify("/Users/mohamedkane/Desktop/selfDev/DataMining/ch7/20news-bydate/20news-bydate-test/soc.religion.christian/21424")
print(result)

