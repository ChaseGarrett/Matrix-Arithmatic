#Chase Cummins
#December 1st, 2017
debug = False

import math
global n, p, i, j, solutionvector, max, maxrow, temp, a1, a2, a3, x1, x2, x3

p = 0
i = 0
j = 0
pivot = 0
count = 0

#Input Matrices uses the number of rows and columns in our square matrix.
#It then asks the user for the inputs for the cooresponding values
def inputmatrices(A,n):
    #Here we loop throught the rows
    for i in range(n):
        #We then loop through the columns of each row
        for j in range(n+1):
            #And we prompt the user to enter a value for each row,
            #repeating this line for each element in the matrix
            A[i][j] = int(input("Enter the number in row " + str(i+1) + ", column "+ str(j+1) + ":  "))
            
#Swap rows takes our row vector 'rows' and swaps rows m and n
def swapRows(rows,m,n):
    temp = rows[m]
    rows[m]=rows[n]
    rows[n] = temp 
              
#Back Sub takes our final matrix and solves for a fial solution vector
def backSub(a,n, rows):
    #Makes count global since it has to be used outside of this function later
    global count
    #Creates a list of n 0's, e.g. if n is 4, this line will create a list of [0,0,0,0]
    x = [0 for i in range(n)]
    #Sets r to be the final value in our row vector, the index for our full matrix
    #It solves for our last value in the solution vector and increments count by 1, since we divided
    r = rows[n-1]
    x[n-1] = float(a[r][n])/a[r][n-1]
    count += 1
    #Loops through the remaining rows, and sets r equal to the ith index of our row vector
    for i in range (n-1,-1,-1):
      z = 0
      r = rows[i]
      #Loops through the remaining values in our selected row, then calculates
      #our solution vector, and adds 4 to count. One for addition, multiplication,
      #subtration, and division. It then returns our solution vector
      for j in range(i+1,n):
         z = z  + float(a[r][j])*x[j]
         x[i] = float(a[r][n] - z)/a[r][i]
         count += 4
    return x

#FindS uses our full matrix and its size, n, to find the maxes of each row.
#Then it puts them all into the 'S' vector.
def findS(matrix,n,s):
    #Loops through the rows
    for i in range (0,n):
        max = 0
        #Loops through the values in each of our rows searching for a max.
        #If there is a value greater than max, it is replaced. If not, it keeps max the same
        for j in range (0, n):
            if max < math.fabs(matrix[i][j]):
                max = math.fabs(matrix[i][j])
                s[i] = max
    return s

#Gaussian loops through a row and compares the row vector, our pivot row location,
#the matrix size, n, and our current pass, p.
def gaussian(a,p,n,rows,pivot):
    global count
    #Loops through the values in our current passes row
    for i in range(p+1,n):
        #Sets r equal to the ith value in our row vector, creates a scaler specific
        #to the current row, m, increments count by 1, then sets the values in the
        #lower triangle equal to 0
        r = rows[i]                         
        m=-a[r][p]/a[pivot][p]
        count += 1
        a[r][p] = 0
        #Loops through the values/columns in our current row, performs some arithmetic,
        #then we add 2 to count because of the multiplication and addition.
        for j in range(p+1,n+1):            
          a[r][j] = float(a[r][j] + m * a[pivot][j])
          count += 2
              
#Partial uses our matrix, the matrix size, the row vector and the current pivot row
def partial(a,n,rowVector, pivotRow):
    global count
    #Loops through the passes of our matrix.
    for p in range(0,n-1):                       
        max = 0
        #Loops through the rows of our matrix.
        for i in range(p,n):
            #Tests if a value is greater than our max; if is is, we set max equal
            #to that value and set the maxrow at the row we are currently looking at.
            #If it isn't greater than max, we set maxrow equal to our pass number
            if abs(a[i][p]) > max:
                max = abs(a[i][p])
                maxrow = i                      
            else:
                maxrow = p
        #Tests if the row in which the maximum value is located is greater than
        #that of our pass, we will swap the rows and change the pivot to our max.
        #If this isn't the case, we will change the pivot row equal to p.
        if maxrow > p:                          
            swapRows(rowVector,p,maxrow)
            pivotRow = maxrow
        else:
            pivotRow = p
        #Performs gaussian on the matrix at the end of each pass
        gaussian(a,p,n,rowVector,pivotRow)

#Scaled uses our matrix, its size, our row vector, the pivot row, and the S vector
def scaled(a,n,rowVector,pivotRow,sVector):
    global count
    #Executes findS to find the s vector. This is the vector we will use
    #to decide when we swap rows in the algorithm.
    s = findS(a,n,sVector)    
    #Loops through our matrix by the way of passes
    for p in range(0,n-1):                      
        max = 0                                 
        #Loops though the rows of our matrix
        for i in range(p,n):
            #Sets row equal to the ith value in our row vector, calculates our scaler
            #adds 1 to count because of the division required for m.
            row = rowVector[i]
            m[i] = math.fabs(a[row][p])/s[row]
            count += 1
            #Tests if our ith value in m is greater than max. If it is, we set
            #max equal to that value and maxrow equal to our current row.
            if m[i] > max:
                max = m[i]
                maxrow = i
        #If the row our max value is on is greater than our pass number, we will swap
        #the rows in our row vector and change our pivot row to be the row our max is on.
        #If not, we set our pivot row to be our row vector's pth value
        if maxrow > p:                          
            swapRows(rowVector,p,maxrow)
            pivotRow = maxrow
        else:
            pivotRow = rowVector[p]       
        #We will execute gaussian using our matrix, pass number, matrix size, row vector,
        #and the location of the pivot row in our row matrix.
        gaussian(a,p,n,rowVector,pivotRow)

#Allows the user to select a method for solving the matrix they entered
selectedMethod = int(input("Select a method to solve the system of equations (1: Gaussian, 2: Partial Pivoting, 3: Scaled Partial Pivoting): "))

#Sets n to be the size of their matrix in integer
n = int(input("Enter the size of your square matrix (3+): "))
#Creates a matrix, called a, of size n+1 by n; e.g. if n is 3, it will create a 4x3 augmented matrix.
a = [[0 for x in range(n+1)] for y in range(n)]
#Creates a vector of 0's, called s, of size n
s = [0 for x in range(n)]
#Creates a vector of 0's, called m, of size n
m = [0 for x in range(n)]
#Creates a vector of i's, called partialRV, of size n. E.g. if n = 3, partialRV = [0,1,2]
partialRV = [i for i in range(n)]

#If debug is enabled, we will remove the need to input a matrix every time we execute the code.
if debug == True:
    a1 = [2,3,1,-4]
    a2 = [4,1,4,9]
    a3 = [3,4,6,0]
    a = [a1, a2, a3]
#If debug is disabled, we will prompt the user to enter a matrix at the beginning of the codes execution.
else:
    inputmatrices(a,n)
       
#Partial Pivoting Exercise
#a1 = [2,3,1,-4]
#a2 = [4,1,4,9]
#a3 = [3,4,6,0]
#a = [a1, a2, a3]

#Partial Pivoting matrix from Dr. Baker's code
#a1 = [0,3,1,1]
#a2 = [1,2,-2,7]
#a3 = [2,5,4,-1]
#a =[a1,a2,a3]

#If the user selects Gaussian, this code will run Gaussian, solve the matrix for a solution vector
#and it then prints the final matrix and the solution vector we calculated.
if selectedMethod == 1:  
    for p in range (0,n):
        gaussian(a,p,n,partialRV, partialRV[p])        
    
    solutionvector = backSub(a,n,partialRV)
        
    print("\n\nFinal Matrix:\n" + str(a[0]) + "\n" + str(a[1]) + "\n" + str(a[2]))
    print("\nSolution Vector: " + str(solutionvector) + ", with " + str(count) + " function evaluations.")
    
#If the user selects Partial Pivoting, this section of the code will run partial pivoting.
#It will then calculate the solution vector and print off the final matrix and that vector.
if selectedMethod == 2:
    partial(a,n,partialRV, pivot)
        
    solutionvector = backSub(a,n,partialRV)
    
    print("\n\nFinal Matrix:\n" + str(a[0][0:n+1]) + "\n" + str(a[1][0:n+1]) + "\n" + str(a[2][0:n+1]))
    print("\nSolution Vector: " + str(solutionvector) + ", with " + str(count) + " function evaluations.")
    
#If the user selects Scaled Partial Pivoting, this section of the code will run scaled partial pivoting.
#It will then calculate the solution vector and print off the final matrix and the solution vector.
if selectedMethod == 3:
    scaled(a,n,partialRV,pivot,s)
    
    solutionvector = backSub(a,n,partialRV)
    
    print("\n\nFinal Matrix:\n" + str(a[0][0:n+1]) + "\n" + str(a[1][0:n+1]) + "\n" + str(a[2][0:n+1]))
    print("\nSolution Vector: " + str(solutionvector) + ", with " + str(count) + " function evaluations.")
