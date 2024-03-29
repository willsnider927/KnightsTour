Optimal Knights Tour Algorithm: 
Created by Will Snider and Tucker Travins for CU Boulder's ECEN2703 Discrete Mathamatics

Required Packages:
pygame is required for the visualizer, if not installed, mycheck.py will try to do so through pip.
It is preferred you install this package yourself however.

Usage:
Run driver.py, the rest will be explained by the program.

Implementation:
An implementation of finding Knights tours using Warnsdorff's Heuristic (http://warnsdorff.com/)
is found in HeuristicApproach.py, the approach is modified in certain cases to provide specific
tours that can be used in constructing larger tours, comments should make clear what modifications were made.

This heuristic approach is insuffiecient for very large boards, yet still helpful for finding smaller tours that
can later be used. In order to construct large n*m boards, an implementation of the Optimal Knights Tour Algorithm
(https://www.sciencedirect.com/science/article/pii/S0166218X04003488) is found in KnightTours.py

The Algorithm is able to construct closed, corner closed, open, and stretched tours of any n<=m, n*m board in O(n*m).
The paper discusses seperate functions for open and closed boards, however the closed function only needs one extra
case to allow it to do all of the boards and so that is how it is implemented in the program.

Definitions of all the types of boards are found in the pdf.
 
Two special cases exist, for 3*m boards, constructing the tours involves finding a 3*k structured board that 
satisfies the original requested board, where k = ((m-7) mod 4) + 7 for open boards, and k = ((m-9) mod 4) + 9 for 
other boards. This board is then stitched together along the top right structured corner with (m-k)/4 
3*4 stretched boards. For the case of 4*m open boards, a 4*k where k = ((m-6) mod 5) + 6 stuctured open tour is 
constructed and stiched together with (m-k)/5 double loop 4*5 boards. 

For n<=10 and m<=10 boards, the heuristic approach is used to find the board. For n<=10 and m>10 boards, the board
is split into one n*m1 board and one n*m2 board, where m2 is guaranteed to be even by the partitioning rule used.
n*m1 is the desired type and is stitched together with a stretched n*m2 board where each was generated by recursively
calling the function until the first case appears and a base can be selected. For n>10 and m>10 boards, the boards are 
split into 4, n1*m1, n1*m2, n2*m1, n2*m2 where n1*m1 is the only one that can be odd and is set to the desired board type,
the other even boards are stretched. The boards are all stitched together in the same way as the previous case. 

By the partitioning rule used in the last two cases, every board besides the top left will be stretched and will often 
repeat sizes, thus a catalog of all these stretched bases is generated at startup and can be referenced whenever needed 
in order to find the needed stretched tour.



