import KnightTours
import HeuristicApproach
import mycheck
import time
import pygame


if __name__ == '__main__':
    print("\nConstructing Bases...\n")
    catalog = KnightTours.buildCatalog()
    print("Optimal Knights Tour Algorithm Guide:\n")
    print("1. Selecting n at the first prompt will close the program, y will continue\n")
    print("2. First and second inputs will be sorted and n will be set to the smallest\n")
    print("3. Types and their bounds: (all lowercase)")
    print("   a) closed: (1) n*m is even, and (2) n>=5 or (n==3 and m>=10)")
    print("   b) open: (1) n==3 and (m==4 or m>=7), or (2) n>=4 and m>=5")
    print("   c) corner: (1) n*m is odd, and (2) n>=5 or (n==3 and m>=9)\n")
    print("4. All boards will be printed with each square labeled as which step it was when it got there starting from 0.")
    print("   Exception is in the case of a corner closed, the missing corner will be labeled 0 and the tour starts at 1.\n")
    while (input("Find a Knights tour? [y/n]\n") == 'y'):
        try:
            try:
                n = int(input("Give the first side length\n"))
                m = int(input("Give the second side length\n"))
            except:
                raise Exception("invalid, must be integer value\n")
            if n > m:
                n, m = m,n
            type = input("enter the type of tour, eg. closed, open, corner\n")
            if type == "closed":
                if ((n*m)%2 == 0 and (n>=5 or (n==3 and m>=10))):
                    tic = time.perf_counter()
                    path = KnightTours.Knight(n,m,type,1,catalog)
                    toc = time.perf_counter()
                    HeuristicApproach.printSolution(path,n,m)
                else:
                    raise Exception("Board with desired dimensions and type does not exist.\n")
            elif type == "corner":
                if ((n*m)%2 == 1 and (n>=5 or (n==3 and m>=9))):
                    tic = time.perf_counter()
                    path = KnightTours.Knight(n,m,type,1,catalog)
                    toc = time.perf_counter()
                    HeuristicApproach.printSolution(path,n,m)
                else:
                    raise Exception("Board with desired dimensions and type does not exist.\n")
            elif type == "open":
                if ((n==3 and (m==4 or m>=7)) or (n>=4 and m>=5)):
                    tic = time.perf_counter()
                    path = KnightTours.Knight(n,m,type,1,catalog)
                    toc = time.perf_counter()
                    HeuristicApproach.printSolution(path,n,m)
                else:
                    raise Exception("Board with desired dimensions and type does not exist.\n")
            else:
                raise Exception("Invalid input.\n")
            print("Board solved in %f seconds\n" %(toc-tic))
            if m > 20:
                print("make sure to readjust the window\n")
            if (n >30 or m >30):
                print("Board too big for visualiser")
            elif (input("Display knight path animation? (y/n)\n") == 'y'):
                print("A window has opened in the background showing the path of the knight!")
                print("Don't try to exit from the path window.")
                mycheck.pathshow(n,m,path)
        except Exception as e:
            print(e)


