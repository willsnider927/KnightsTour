from collections import defaultdict
import math

#construct a open (closed==0), closed (closed==1), corner closed (closed==2), or stretched (closed==3) using Warnsdorff's Heuristic
class KnightsTour:
    def __init__(self, m, n, startSquares, endSquares, closed):
        __slots__ = ['n','m','size','endSquares','moves','closed','graph']
        self.n = n
        self.m = m
        self.size = n*m
        self.startSquares = startSquares
        if self.startSquares == []:
            self.startSquares = [i for i in range(self.size)]
        self.endSquares = endSquares
        self.closed = closed
        if self.closed == 3:
            self.maxIter = self.size*10
        else:
            self.maxIter = self.size*2
        self.moves = {(-1,-2),(1,-2),(-2,1),(-2,-1),(2,1),(2,-1),(1,2),(-1,2)} #all moves
        self.graph = self.buildGraph()
        self.path = self.FindTour()
        if self.closed == 2:
            self.path.insert(0,0)

    def legalMoves(self, x, y): # x,y = current, m*n = size
        for (moveX, moveY) in self.moves:
            nextX = x+moveX
            nextY = y+moveY
            if (nextX >= 0 and nextX < self.m and nextY >= 0 and nextY < self.n): #see if move is valid
                square = nextX + nextY*self.m #convert (x,y) into a numbered board 0-n*m-1
                yield square

    def buildGraph(self): #dictionary with sets as key
        graph = defaultdict(set)
        for y in range(self.n):
            for x in range(self.m):
                for i in self.legalMoves(x,y): #add legal moves as edges
                    square = x + y*self.m
                    graph[square].add(i)
        return graph

    def findLonelySquares(self, currSquare, path): #application of Warnsdorff's Heuristic https://en.wikipedia.org/wiki/Knight%27s_tour
        pathSet = set(path) 
        moves = defaultdict(int)
        for i in self.graph[currSquare]:
            if i not in pathSet:
                moves[i] = len(self.graph[i]-pathSet)
        if self.size > 64: #second order tiebreaking caused issue in small tours for some reason
            moveslist = sorted(moves, key=lambda square: (moves[square], sum([len(self.graph[i] - pathSet) for i in self.graph[square]-pathSet]))) #second order tie breaking
        else:
            moveslist = sorted(moves, key=moves.get)
        #everything below here is only required for building the stretched catalog of bases.
        if self.closed == 3: #pruning of the move tree so as to prevent wrong moves early in the case of stretched tour 
            if self.n == 5 or (self.n==8 and self.m==8): #specific cases where structured tour wasn't generated, had to force the moves to make it structured
                if currSquare == (self.m -2) and self.m*3 -1 not in pathSet:
                    moveslist = [self.m*3 -1]
                    return moveslist
                if currSquare == (self.m*3 -1) and self.m -2 not in pathSet:
                    moveslist = [self.m -2]
                    return moveslist
                if currSquare == (self.m*(self.n -2)) and self.m*(self.n -1) +2 not in pathSet:
                    moveslist = [self.m*(self.n -1) +2]
                    return moveslist
                if currSquare == (self.m*(self.n -1) +2) and self.m*(self.n -2) not in pathSet:
                    moveslist = [self.m*(self.n -2)]
                    return moveslist
            if len(path) != self.size-2:
                try:
                    moveslist.remove(self.endSquares[0]) #should only be one value if looking for stretched tour
                except:
                    pass
            if len(path) < self.size//2: #remove moves two levels from final square if half the board hasn't been searched
                endGraph = self.graph[self.endSquares[0]]
                for i in endGraph:
                    try:
                        moveslist.remove(i)
                    except:
                         pass
        return moveslist

    def _hamiltonianPath(self, path, count, currSquare): #recursive helper function
        if self.iter > self.maxIter:
            return None
        if (count == self.size): #if the path has been found
            if not self.endSquares: #open
                return path + [currSquare]
            if currSquare not in self.endSquares: #specific end point(s)
                return None
            return path + [currSquare]
        moves = self.findLonelySquares(currSquare, path)  
        for i in moves: #follow path with least following branches first
            self.iter = self.iter+1
            result = self._hamiltonianPath(path+[currSquare], count + 1, i) 
            if (result is not None):
                return result
        return None #no moves now or in the recursion

    def FindTour(self): 
        if self.closed ==1 or self.closed == 2: #corner or closed
            ranking = list()
            for i in range(self.size): #rank the start squares from closest to center out, the heuristic searches "outwards", this method has more success for closed tours
                x = i % self.m
                y = i//self.m
                disMap = math.sqrt(abs(self.m/2 - x)**2 + abs(self.n/2 - y)**2)
                ranking.append(disMap)
            order = sorted([i for i in range(self.size)], key=lambda square: ranking[square])
            if self.closed == 2: # if corner closed, the corner will have a 0 in that corner to make future manipulation of the path easier
                self.size = self.size -1 
                self.graph.pop(0)
                for i in range(1, self.size):
                    self.graph[i] = self.graph[i] - {0}
            for i in order:
                self.endSquares = self.graph[i]
                self.iter = 0
                found = self._hamiltonianPath([], 1, i)
                if found:
                    return found
            return None
        else:
            for i in self.startSquares:
                self.iter = 0
                found = self._hamiltonianPath([], 1, i)#start recursion with the empty path, move 1, start square i
                if found is not None:
                    return found
            return None

def printSolution(path,n,m): #print function
        size = n*m
        numDigits = int(math.log10(size)) +1
        if path:
            board = [None] *len(path)
            for i,v in enumerate(path):
                board[v] = i
            for i in range(n):
                print('-'.join(['' for i in range((numDigits+3)*m)]))
                for j in range(m):
                    step = board[j + i*m]
                    if step == 0:
                        numStepDigs = 1
                    else:
                        numStepDigs = int(math.log10(step))+1
                    pre = ' '*(numDigits-numStepDigs+1)
                    print(pre,step,end = '|')
                print()
            print('-'.join(['' for i in range((numDigits+3)*m)]))
        else:
            print(n,m)
            print("error tour not found, try different bounds")
    
    