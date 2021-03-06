import clustering as p3
import random as ra
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat
from numpy import linalg as LA


#-------------------------------------------------------------------------------
# Section 1.a
#-------------------------------------------------------------------------------
# Test the provided kMeans method on the toy data for K=[1,2,3,4] with
# several different random initializations. Provide plots of the solution
# for each K that minimizes the total distortion cost.

# Write your code here
# K = 4
X = p3.readData('toy_data.txt')
# (Mu,P,Var) = p3.init(X,K) 
# (Mu,P,Var,post) = p3.kMeans(X, K, Mu, P, Var)
# p3.plot2D(X,K,Mu,P,Var,post,"Plot")


#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Section 1.b
#-------------------------------------------------------------------------------
# Fill in the Estep, Mstep, and mixGauss methods.
# Test your Estep using K=3, after initializing using
# (Mu,P,Var) = p3.init(X,K,fixedmeans=True).  The returned log-likelihood
# should be -1331.67489.

# Write your code here: 
# (Mu,P,Var) = p3.init(X,3,fixedmeans=True)
# (post, LL) = p3.Estep(X,3,Mu,P,Var)
# print LL

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Section 1.c and 1.d
#-------------------------------------------------------------------------------
# 1) Test your implementation of EM on the toy data set by checking that the
#	   LogLikelihoods at each iteration are indeed monotonically increasing; and,
# 2) Compare your algorithm's Log-likelihood to the one provided in the project.
#
# Once convinced that your EM implementation is working, generate plot like you
# did for kMeans above.  Compare these plots to those achieved using kMeans and
# explain when, how, and why they differ.

# Each run of mixGauss shouldn't take more than a few seconds.

# Write your code here
# K = 3
# (Mu,P,Var) = p3.init(X,3,fixedmeans=True)
# (Mu,P,Var,post,LL) = p3.mixGauss(X,K,Mu,P,Var)
# print LL

# K = 4
# (Mu,P,Var) = p3.init(X,K) 
# (Mu,P,Var,post,LL) = p3.mixGauss(X,K,Mu,P,Var)
# print LL
# p3.plot2D(X,K,Mu,P,Var,post,"Plot")

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Section 1.e
#-------------------------------------------------------------------------------
# Fill in the BICmix method, then find the best K in [1,2,3,4] for the toy
# dataset.  Report the best K and the corresponding BIC score.

# Write your code here
# Kmax = p3.BICmix(X,[1,2,3,4])
# print Kmax


#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Section 2.d
#-------------------------------------------------------------------------------
# Fill in the Estep_part2, Mstep_part2, and mixGaus_part2 methods.
# Run the file matrixCompletionTest.py (with irrelevant sections commented out)
# to test the E step, M step, mixGauss, and fillMatrix functions you wrote in part 2.
# (Note that you may need to comment out the fillMatrix portion of 
# matrixCompletionTest.py if you run it at this point before writing you fillMatrix
# function.) The expected results can be found in the file
# matrixCompletionTest_Solutions.txt. You do not need to include your code for
# this debugging / validation.

# Tip: The terminal command used to write the script output to
# matrixCompletionTest_Solutions.txt was:

# python matrixCompletionTest.py >> matrixCompletionTest_Solutions.txt

# So you can use the same line to write your own output to a file with a 
# different name (e.g. 'validation.txt', if there is not already a file 
# with that name in the same folder).

# NOTE: I GOT THIS PART DONE AND IT VALIDATES PERFECTLY

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Section 2.e
#-------------------------------------------------------------------------------
# Run the mixture model with K = 12 on 'netflix_incomplete.txt', and verify that
# the log-likelihood increases monotonically. Also run the model with K = 1,
# and verify that the log-likelihood is -1521060.95399.

# Write your code here

# X = p3.readData('netflix_incomplete.txt')
# K = 12
# (Mu,P,Var) = p3.init(X,K)
# (Mu,P,Var,post,LL) = p3.mixGauss_part2(X,K,Mu,P,Var)
# print "================================================"
# print "Mu: ", Mu
# print "P: ", P
# print "Var: ", Var
# print "post: ", post
# print "LL: ", LL
# print "================================================"


#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Section 2.h
#-------------------------------------------------------------------------------
# Run fillMatrix on 'netflix_incomplete.txt' with K=12 and mixture model on
# 'netflix_complete.txt' and report the root mean squared error between the two
# matrices using rmse.

# Write your code here
X = p3.readData('netflix_incomplete.txt')
Xc = p3.readData('netflix_complete.txt')
K = 12
(Mu,P,Var) = p3.init(X,K)
(Mu,P,Var,post,LL) = p3.mixGauss_part2(X,K,Mu,P,Var)
Xpred = p3.fillMatrix(X,K,Mu,P,Var)
error = p3.rmse(Xpred,Xc)
print "================================================"
print "Mu: ", Mu
print "P: ", P
print "Var: ", Var
print "post: ", post
print "LL: ", LL
print "================================================"
print "completed matrix: ", Xpred
print "================================================"
print "rmse: ", error
print "================================================"

#-------------------------------------------------------------------------------
