from queue import PriorityQueue
import math


"""
Example code for hierarchical clustering
"""

def getMedian(alist):
    """get median value of list alist"""
    tmp = list(alist)
    tmp.sort()
    alen = len(tmp)
    if (alen % 2) == 1:
        return tmp[alen // 2]
    else:
        return (tmp[alen // 2] + tmp[(alen // 2) - 1]) / 2
    

def normalizeColumn(column):
    """Normalize column using Modified Standard Score"""
    median = getMedian(column)
    asd = sum([abs(x - median) for x in column]) / len(column)
    result = [(x - median) / asd for x in column]
    return result

class hClusterer:
    """ this clusterer assumes that the first column of the data is a label
    not used in the clustering. The other columns contain numeric data"""
    
    def __init__(self, filename):
        file = open(filename)
        self.data = {}
        self.counter = 0
        self.queue = PriorityQueue()
        lines = file.readlines()
        file.close()
        header = lines[0].split(',')
        self.cols = len(header)
        self.data = [[] for i in range(len(header))]
        for line in lines[1:]:
            cells = line.split(',')
            toggle = 0
            for cell in range(self.cols):
                if toggle == 0:
                   self.data[cell].append(cells[cell])
                   toggle = 1
                else:
                    self.data[cell].append(float(cells[cell]))
        # now normalize number columns (that is, skip the first column)
        for i in range(1, self.cols):
                self.data[i] = normalizeColumn(self.data[i])

        ###
        ###  I have read in the data and normalized the 
        ###  columns. Now for each element i in the data, I am going to
        ###     1. compute the Euclidean Distance from element i to all the 
        ###        other elements.  This data will be placed in neighbors, which
        ###        is a Python dictionary. Let's say i = 1, and I am computing
        ###        the distance to the neighbor j and let's say j is 2. The
        ###        neighbors dictionary for i will look like
        ###        {2: ((1,2), 1.23),  3: ((1, 3), 2.3)... }
        ###
        ###     2. find the closest neighbor
        ###
        ###     3. place the element on a priority queue, called simply queue,
        ###        based on the distance to the nearest neighbor (and a counter
        ###        used to break ties.
        neighbors={}
        closest = {}
        closestDistance = {}
        for i in range(len(self.data[0])):
            neighbors[i]={}
            dis = float('inf')
            closeneigh=i
            for j in range(len(self.data[0])):
                if i!=j:
                    neighbors[i][j]=((i,j),self.distance(i,j))
                    if neighbors[i][j][1]<dis:
                        dis=neighbors[i][j][1]
                        closeneigh=j
            currentCluster = [self.data[0][i]]
            currentNeigh = self.data[0][j]
            neighList = [currentNeigh,dis,(i,j)]
            tupleForQueue= (dis,i,[currentCluster,neighList],neighbors[i])
            self.queue.append(tupleForQueue)   

    def merge(dic1,dic2):
        dic3 = {}
        assert len(dic1)>0
        assert len(dic2)>0
        for key in dic1.keys():
            if key in dic2:
                op1 = dic1[key][1]
                op2 = dic2[key][1]
                print dic1[key][0]
                print dic2[key][0]
                if op1<op2:
                    dic3[key]=(dic1[key][0],op1)
                else:
                    dic3[key]=(dic2[key][0],op2)
        return dic3 



    def distance(self, i, j):
        sumSquares = 0
        for k in range(1, self.cols):
            sumSquares += (self.data[k][i] - self.data[k][j])**2
        return math.sqrt(sumSquares)
            

    def cluster(self):
        # TODO
        currentIndex = len(self.queue)
        while len(self.queue)>1:
            currentIndex+=1
            clus1 = self.queue.get()
            clus2 = self.queue.get()
            print clus1
            print clus2
            dist1 = clus1[0]
            dist2 = clus2[0]
            ney1= clus1[1]
            ney2= clus2[1]
            if dist1<dist2:
                newDist=dist1
                closestInfo=clus1[2][1]
            else: 
                newDist=dist2
                closestInfo=clus2[2][1]
            list1=clus1[2]
            list2=clus2[2]
            clusName1=list1[0]
            clusName2=list2[0]
            newClus=clusName2+clusName1
            newDic=self.merge(clus1[2][2],clus2[2][2])
            self.queue.append(newDist,currentIndex,[newClus,closestInfo,newDic])
        return self.queue.get()

                         
def printDendrogram(T, sep=3):
    """Print dendrogram of a binary tree.  Each tree node is represented by a length-2 tuple.
    printDendrogram is written and provided by David Eppstein 2002. Accessed on 14 April 2014:
    http://code.activestate.com/recipes/139422-dendrogram-drawing/ """
    
    def isPair(T):
        return type(T) == tuple and len(T) == 2
    
    def maxHeight(T):
        if isPair(T):
            h = max(maxHeight(T[0]), maxHeight(T[1]))
        else:
            h = len(str(T))
        return h + sep
        
    activeLevels = {}

    def traverse(T, h, isFirst):
        if isPair(T):
            traverse(T[0], h-sep, 1)
            s = [' ']*(h-sep)
            s.append('|')
        else:
            s = list(str(T))
            s.append(' ')

        while len(s) < h:
            s.append('-')
        
        if (isFirst >= 0):
            s.append('+')
            if isFirst:
                activeLevels[h] = 1
            else:
                del activeLevels[h]
        
        A = list(activeLevels)
        A.sort()
        for L in A:
            if len(s) < L:
                while len(s) < L:
                    s.append(' ')
                s.append('|')

        print (''.join(s))    
        
        if isPair(T):
            traverse(T[1], h-sep, 0)

    traverse(T, maxHeight(T), -1)




filename = '//Users/raz/Dropbox/guide/pg2dm-python/ch8/dogs.csv'
#filename = '//Users/raz/Dropbox/guide/pg2dm-python/ch8/cerealTemp.csv'

hg = hClusterer(filename)
cluster = hg.cluster()
printDendrogram(cluster)

