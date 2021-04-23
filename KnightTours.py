import HeuristicApproach
from collections import defaultdict
import time

#any time "path" or a variation of path is referenced,
#the indexes are the move # and the values are which square number.
#the numbering of the board follows the pattern below:
# 0,1,2
# 3,4,5
# 6,7,8

#build catalog of all possibly needed stretched bases, 
#every board besides the top left corner will be stretched.
#luckily, the heuristic approach creates the correct board for all but a few cases
#the last integer in the key represents what side of the start sqaure we want to end on
# 0 = right below, 1 = to its right
def buildCatalog():
    #stretched will be called for every board except the first corner, cataloging these cases are useful as they often repeat in large boards
    cat = defaultdict(list)
    for i in [0,1]:
        for n in range(4,11):
            for m in range(4,11):
                if (n*m)%2 != 1:
                    if i:
                        end = 1
                    else:
                        end = m
                    path = HeuristicApproach.KnightsTour(m,n,[0],[end],3).path 
                    if path is None:
                        path = HeuristicApproach.KnightsTour(m,n,[end],[0],3).path #try in reverse
                    if path is None:
                        path = HeuristicApproach.KnightsTour(m,n,[n*m-1],[n*m -end-1],3).path #try rotated 180 degrees
                        if path:
                            path = [n*m -1-i for i in path]
                    if path is None:
                        path = HeuristicApproach.KnightsTour(m,n,[n*m -end-1],[n*m-1],3).path #try 180 degrees and reverse
                        if path:
                            path = [n*m -1-i for i in path]
                    cat["stretch%d,%d,%d" %(n,m,i)] = path
    path107 = HeuristicApproach.KnightsTour(7,10,[6],[5],3).path #10,7,1 provided further issues
    cat["stretch10,7,1"] =  [6 - i%7 + (i//7)*7 for i in path107] #can be mirrored along 'n' axis

    path109 = [9 - i%10 + (i//10)*10 for i in cat["stretch9,10,1"]] #10,9,0 also had issues. start by mirroring across 'n' axis
    path109 = [(i//10) + (9- i%10)*9 for i in path109] #rotate -90degrees (x->y, y->max(x)-x)
    cat["stretch10,9,0"] = path109

    cat["stretch3,4,0"] = [0,6,8,1,7,9,2,11,5,3,10,4]

    cat["double4,5,1"] = [0,7,4,13,16,5,2,9,18,11] #Needed for open 4xm's
    cat["double4,5,0"] = [1,8,19,12,15,6,3,14,17,10]
    return cat


#generate a closed, open, corner closed, or stretched knights tour from an arbritarily sized boared in linear time
def Knight(n,m, required, side,catalog):
    if n <= 10 and m <= 10: #can be found from the heuristic search
        if required == "open":
            return HeuristicApproach.KnightsTour(m,n,[],[],0).path 
        if required == "closed":
            return HeuristicApproach.KnightsTour(m,n,[],[],1).path
        if required == "stretched":
            path = catalog["stretch%d,%d,%d" %(n,m,side)]
            if (path[0] != 0):
                path = path[::-1] #reversing a list
            return path
        if required == "corner":
            return HeuristicApproach.KnightsTour(m,n,[],[],2).path


    elif n == 3 and m>10: #can be built from (3,k) and series of 3,4 stretched tours
        #path from 0 to 2
        pathToTop = catalog["stretch3,4,0"][0:catalog["stretch3,4,0"].index(2)+1] #seperate the 3x4 stretched tour into multiple segments
        #path from 11 to 4
        pathFromBottom = catalog["stretch3,4,0"][catalog["stretch3,4,0"].index(2)+1:12]
        #path from 2 to 0
        pathTo0 = pathToTop[::-1]
        #path from 4 to 11
        pathTo4 = pathFromBottom[::-1]

        if required == "open":
            k = ((m-7)%4) + 7 #7,8,9,10
            closed = HeuristicApproach.KnightsTour(k,3,[],[],0).path 
        else:
            k = ((m-9)%4) + 9 #9,10,11,12
            if k%2 ==1:
                closed = HeuristicApproach.KnightsTour(k,3,[],[],2).path #corner
            else:
                closed = HeuristicApproach.KnightsTour(k,3,[],[],1).path #closed
        if closed.index(k-2) < closed.index((k*n)-1): #ensure the index needed to jump from board to board is first
            closed = closed[::-1]
            if required == "corner": #ensure zero at square 0 in case of corner
                closed.remove(0)
                closed.insert(0,0)
        path = [i%k + (i//k)*m for i in closed[0:closed.index(n*k-1)+1]]
        for i in range((m-k)//4): #add as many 3,4's as needed
            if i%2==0: #which path followed alternates based on which 3x4 board it is
                pathToTopShifted = [j%4 + (j//4)*m + k +4*i for j in pathToTop]
                path = path + pathToTopShifted
            else:
                path = path + [j%4 + (j//4)*m +k +4*i for j in pathTo4]
        for i in reversed(range((m-k)//4)): #add the path backwards
            if i%2==0: #path back also alternates
                pathFromBottomShifted = [j%4 + (j//4)*m + k +4*i for j in pathFromBottom]
                path = path + pathFromBottomShifted
            else:
                path = path+ [j%4 + (j//4)*m +k + 4*i  for j in pathTo0]
        path = path + [i%k + (i//k)*m for i in closed[closed.index(n*k-1)+1:]] #add end of 3,k tour
        return path


    elif n==4 and m>10: #special case for open knights tours
        #split the double 4x5 tour into 4 components.
        path1to3 = catalog["double4,5,0"][0:7]
        path5to9 = catalog["double4,5,1"][5:8]
        path14to10 = catalog["double4,5,0"][7:]
        path18to16 = catalog["double4,5,1"][8:] + catalog["double4,5,1"][0:5]

        k = (m-6)%5 +6 #6,7,8,9,10
        pathK = [k-1-(i%k)+(i//k)*k for i in catalog["stretch4,%d,1" %k]] #mirror across 'n' axis
        
        #follow both ends of the tour simultaneously
        path1 = [i%5 + k + (i//5)*m for i in catalog["double4,5,1"][6:8]]
        path2 = [i%5 + k + (i//5)*m for i in path1to3]
        for i in range(1,(m-k)//5 -1): #iterate through each 4x5 board
            if i%2 == 1: #one gets path1to3, one gets 5to9
                path1 = path1 + [j%5 + (j//5)*m +k +5*i for j in path1to3]
                path2 = path2 + [j%5 + (j//5)*m +k +5*i for j in path5to9]
            else:
                path1 = path1 + [j%5 + (j//5)*m +k +5*i for j in path5to9]
                path2 = path2 + [j%5 + (j//5)*m +k +5*i for j in path1to3]
        if path1[len(path1)-1]//(m-5) == 1: #add the last double board 
            path1 = path1 + [i%5 + (i//5)*m + m-5 for i in catalog["double4,5,1"][5:] + catalog["double4,5,1"][0:5]]
            path2 = path2 + [i%5 + (i//5)*m + m-5 for i in catalog["double4,5,0"]]
        else:
            path1 = path1 + [i%5 + (i//5)*m + m-5 for i in catalog["double4,5,0"]]
            path2 = path2 + [i%5 + (i//5)*m + m-5 for i in catalog["double4,5,1"][5:] + catalog["double4,5,1"][0:5]]
        for i in reversed(range(1,(m-k)//5 -1)): #traverse the path back for both
            if i%2:
                path1 = path1 + [j%5 + (j//5)*m +k +5*i for j in path14to10]
                path2 = path2 + [j%5 + (j//5)*m +k +5*i for j in path18to16]
            else:
                path1 = path1 + [j%5 + (j//5)*m +k +5*i for j in path18to16]
                path2 = path2 + [j%5 + (j//5)*m +k +5*i for j in path14to10]
        path1End = catalog["double4,5,1"][8:] + catalog["double4,5,1"][0:6] #add the end of each path
        path1 = path1 + [i%5 +k + (i//5)*m for i in path1End]
        path2 = path2 + [i%5 +k + (i//5)*m for i in path14to10]
        path1 = path1[::-1] #reverse path1
        path = path2 + [i%k + (i//k)*m for i in pathK] + path1 #combine the paths
        return path


    elif 4 <= n and n <= 10 and m >10: #can be built from bases found in case 1 and spliting into two sections
        m1 = (m//4)*2 +(m%2) #m1 is guaranteed odd and m2 even, guarantees we can create a stretched in second partitioning
        m2 = m - m1
        path1 = Knight(n,m1,required,side,catalog)
        if(path1.index(m1-2) > path1.index((m1*3)-1)):
            path1 == path1[::-1]
            if required == "corner":
                path1.remove(0)
                path1.insert(0,0)
        path2 = Knight(n,m2,"stretched",0,catalog)
        if path2[0] == 0:
            path2 = path2[::-1]
        path2 = [i%m2 + (i//m2)*m +m1 for i in path2]
        #stiches together the segments from each tour we need
        path = [i%m1 + (i//m1)*m for i in path1[0:path1.index(m1-2)+1]] + path2 + [i%m1 + (i//m1)*m for i in path1[path1.index(m1-2)+1:]]
        return path


    elif n>10 and m >10: #can be segmented into 4 different boards
        m1,n1 = (m//4)*2 +(m%2), (n//4)*2 +(n%2) #partionioning guarantees the same as previous case, only one board will be odd
        m2, n2 = m-m1, n-n1
        path1 = Knight(n1,m1,required,side,catalog)
        path2 = Knight(n1,m2,"stretched",0,catalog)
        path3 = Knight(n2,m1,"stretched",1,catalog)
        path4 = Knight(n2,m2,"stretched",0,catalog)
        if path2[0] == 0:
            path2 = path2[::-1]
        if path4[0] == 0:
            path4 = path4[::-1]
        
        #stictch boards 1 and 2 togehter first 
        if(path1.index(m1-2) > path1.index((m1*3)-1)):
            path1 = path1[::-1]
            if required == "corner":
                path1.remove(0)
                path1.insert(0,0)
        path2 = [i%m2 + (i//m2)*m +m1 for i in path2]
        path1_2 = [i%m1 + (i//m1)*m for i in path1[0:path1.index(m1-2)+1]] + path2 + [i%m1 + (i//m1)*m for i in path1[path1.index(m1-2)+1:m1*n1]]

        #stitch 3 and 4 together
        if(path3.index(m1-2) > path3.index((m1*3)-1)):
            path3 = path3[::-1]
        path4 = [i%m2 + (i//m2)*m + m1 for i in path4]
        path3_4 =  [i%m1 + (i//m1)*m for i in path3[0:path3.index(m1-2)+1]] + path4 + [i%m1 + (i//m1)*m for i in path3[path3.index(m1-2)+1:m1*n2]]
        path3_4 = [i + n1*m for i in path3_4] #adjust 3_4 squares for being the lower half

        #ensures all the paths are ordered correctly
        if path3_4[0] != n1*m: 
            path3_4 = path3_4[::-1]
        if path1_2.index((n1-1)*m +2) > path1_2.index((n1-2)*m):
            path1_2 = path1_2[::-1]
            if required == "corner":
                path1_2.remove(0)
                path1_2.insert(0,0)
        path = path1_2[0:path1_2.index((n1-1)*m +2) +1] + path3_4 + path1_2[path1_2.index((n1-1)*m +2) +1:n1*m] #stitch 1_2 and 3_4 together
        return path


