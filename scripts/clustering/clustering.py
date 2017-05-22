import random as ra
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat
from numpy import linalg as LA
from scipy.misc import logsumexp

#---------------------------------------------------------------------------------
# Utility Functions - There is no need to edit code in this section.
#---------------------------------------------------------------------------------

# Reads a data matrix from file.
# Output: X: data matrix.
def readData(file):
    X = []
    with open(file,"r") as f:
        for line in f:
            X.append(map(float,line.split(" ")))
    return np.array(X)
    

# plot 2D toy data
# input: X: n*d data matrix;
#        K: number of mixtures;
#        Mu: K*d matrix, each row corresponds to a mixture mean;
#        P: K*1 matrix, each entry corresponds to the weight for a mixture;
#        Var: K*1 matrix, each entry corresponds to the variance for a mixture;
#        Label: n*K matrix, each row corresponds to the soft counts for all mixtures for an example
#        title: a string represents the title for the plot
def plot2D(X,K,Mu,P,Var,Label,title):
    r=0.25
    color=["r","b","k","y","m","c"]
    n,d = np.shape(X)
    per= Label/(1.0*np.tile(np.reshape(np.sum(Label,axis=1),(n,1)),(1,K)))
    fig=plt.figure()
    plt.title(title)
    ax=plt.gcf().gca()
    ax.set_xlim((-20,20))
    ax.set_ylim((-20,20))
    for i in xrange(len(X)):
        angle=0
        for j in xrange(K):
            cir=pat.Arc((X[i,0],X[i,1]),r,r,0,angle,angle+per[i,j]*360,edgecolor=color[j])
            ax.add_patch(cir)
            angle+=per[i,j]*360
    for j in xrange(K):
        sigma = np.sqrt(Var[j])
        circle=plt.Circle((Mu[j,0],Mu[j,1]),sigma,color=color[j],fill=False)
        ax.add_artist(circle)
        text=plt.text(Mu[j,0],Mu[j,1],"mu=("+str("%.2f" %Mu[j,0])+","+str("%.2f" %Mu[j,1])+"),stdv="+str("%.2f" % np.sqrt(Var[j])))
        ax.add_artist(text)
    plt.axis('equal')
    plt.show()

#---------------------------------------------------------------------------------



#---------------------------------------------------------------------------------
# K-means methods - There is no need to edit code in this section.
#---------------------------------------------------------------------------------

# initialization for k means model for toy data
# input: X: n*d data matrix;
#        K: number of mixtures;
#        fixedmeans: is an optional variable which is
#        used to control whether Mu is generated from a deterministic way
#        or randomized way
# output: Mu: K*d matrix, each row corresponds to a mixture mean;
#         P: K*1 matrix, each entry corresponds to the weight for a mixture;
#         Var: K*1 matrix, each entry corresponds to the variance for a mixture;    
def init(X,K,fixedmeans=False):
    n, d = np.shape(X)
    P=np.ones((K,1))/float(K)

    if (fixedmeans):
        assert(d==2 and K==3)
        Mu = np.array([[4.33,-2.106],[3.75,2.651],[-1.765,2.648]])
    else:
        # select K random points as initial means
        rnd = np.random.rand(n,1)
        ind = sorted(range(n),key = lambda i: rnd[i])
        Mu = np.zeros((K,d))
        for i in range(K):
            Mu[i,:] = np.copy(X[ind[i],:])

    Var=np.mean( (X-np.tile(np.mean(X,axis=0),(n,1)))**2 )*np.ones((K,1))
    return (Mu,P,Var)


# K Means method
# input: X: n*d data matrix;
#        K: number of mixtures;
#        Mu: K*d matrix, each row corresponds to a mixture mean;
#        P: K*1 matrix, each entry corresponds to the weight for a mixture;
#        Var: K*1 matrix, each entry corresponds to the variance for a mixture;
# output: Mu: K*d matrix, each row corresponds to a mixture mean;
#         P: K*1 matrix, each entry corresponds to the weight for a mixture;
#         Var: K*1 matrix, each entry corresponds to the variance for a mixture;
#         post: n*K matrix, each row corresponds to the soft counts for all mixtures for an example
def kMeans(X, K, Mu, P, Var):
    prevCost=-1.0; curCost=0.0
    n=len(X)
    d=len(X[0])
    while abs(prevCost-curCost)>1e-4:
        post=np.zeros((n,K))
        prevCost=curCost
        #E step
        for i in xrange(n):
            post[i,np.argmin(np.sum(np.square(np.tile(X[i,],(K,1))-Mu),axis=1))]=1
        #M step
        n_hat=np.sum(post,axis=0)
        P=n_hat/float(n)
        curCost = 0
        for i in xrange(K):
            Mu[i,:]= np.dot(post[:,i],X)/float(n_hat[i])
            # summed squared distance of points in the cluster from the mean
            sse = np.dot(post[:,i],np.sum((X-np.tile(Mu[i,:],(n,1)))**2,axis=1))
            curCost += sse
            Var[i]=sse/float(d*n_hat[i])
        print curCost
    # return a mixture model retrofitted from the K-means solution
    return (Mu,P,Var,post) 
#---------------------------------------------------------------------------------



#---------------------------------------------------------------------------------
# PART 1 - EM algorithm for a Gaussian mixture model
#---------------------------------------------------------------------------------

# E step of EM algorithm
# input: X: n*d data matrix;
#        K: number of mixtures;
#        Mu: K*d matrix, each row corresponds to a mixture mean;
#        P: K*1 matrix, each entry corresponds to the weight for a mixture;
#        Var: K*1 matrix, each entry corresponds to the variance for a mixture;
# output:post: n*K matrix, each row corresponds to the soft counts for all mixtures for an example
#        LL: a Loglikelihood value
def Estep(X,K,Mu,P,Var):
    n,d = np.shape(X) # n data points of dimension d
    post = np.zeros((n,K)) # posterior probabilities to compute
    LL = 0.0    # the LogLikelihood
    count = 0
    for i in range(n):      #for each point we need to "soft" assign a cluster
        for k in range(K): 
            post[i,k] = 1/np.power(2*np.pi*Var[k],d/2)
            post[i,k] = post[i,k]*np.exp(-1/(2*Var[k])*np.power(LA.norm(X[i,:]-Mu[k,:]),2))*P[k]
        
        LL = LL + np.log(np.sum(post[i,:]))
        post[i,:] = post[i,:] / np.sum(post[i,:])

    return (post,LL)


# M step of EM algorithm
# input: X: n*d data matrix;
#        K: number of mixtures;
#        Mu: K*d matrix, each row corresponds to a mixture mean;
#        P: K*1 matrix, each entry corresponds to the weight for a mixture;
#        Var: K*1 matrix, each entry corresponds to the variance for a mixture;
#        post: n*K matrix, each row corresponds to the soft counts for all mixtures for an example
# output:Mu: updated Mu, K*d matrix, each row corresponds to a mixture mean;
#        P: updated P, K*1 matrix, each entry corresponds to the weight for a mixture;
#        Var: updated Var, K*1 matrix, each entry corresponds to the variance for a mixture;
def Mstep(X,K,Mu,P,Var,post):
    n,d = np.shape(X) # n data points of dimension d

    #Update Mu, P, Var
    expNumK = np.sum(post, axis=0)
    P = expNumK/(np.sum(expNumK))

    for k in range(K): 
        Mu[k,:] = np.dot(np.transpose(X),post[:,k])*1/(expNumK[k])
        Var[k] = 1/(d*expNumK[k]) * np.dot(np.power(LA.norm(np.subtract(X,Mu[k,:]),axis = 1),2),post[:,k])

    return (Mu,P,Var)


# Mixture of Guassians
# input: X: n*d data matrix;
#        K: number of mixtures;
#        Mu: K*d matrix, each row corresponds to a mixture mean;
#        P: K*1 matrix, each entry corresponds to the weight for a mixture;
#        Var: K*1 matrix, each entry corresponds to the variance for a mixture;
# output: Mu: updated Mu, K*d matrix, each row corresponds to a mixture mean;
#         P: updated P, K*1 matrix, each entry corresponds to the weight for a mixture;
#         Var: updated Var, K*1 matrix, each entry corresponds to the variance for a mixture;
#         post: updated post, n*K matrix, each row corresponds to the soft counts for all mixtures for an example
#         LL: Numpy array for Loglikelihood values
def mixGauss(X,K,Mu,P,Var):
    n,d = np.shape(X) # n data points of dimension d
    post = np.zeros((n,K)) # posterior probabilities
    maxIter = 500
    LL = np.zeros(maxIter)

    (post, OLL) = Estep(X,K,Mu,P,Var)
    OLL = OLL - np.abs(OLL*0.5)         #just to insure that it will enter the loop and OLL is initialized small enough
    NLL = OLL + np.abs(OLL*0.1)
    tempMu = Mu
    tempP = P
    tempVar = Var
    it = 0
    while (NLL-OLL > np.power(10.0,-6)*np.abs(NLL) and it < maxIter): 
        Mu = tempMu         #Just so that we store Mu only after it passes the convergence criteria (so we don't get one after convergence...)
        P = tempP
        Var = tempVar
        OLL = NLL
        (post,NLL) = Estep(X,K,Mu,P,Var)
        (tempMu,tempP,tempVar) = Mstep(X,K,Mu,P,Var,post)
        LL[it] = NLL
        it = it + 1 
    
    LL = LL[0:it-1]
    return (Mu,P,Var,post,LL)


# Bayesian Information Criterion (BIC) for selecting the number of mixture components
# input:  n*d data matrix X, a list of K's to try 
# output: the highest scoring choice of K
def BICmix(X,Kset):
    n,d = np.shape(X)
    #Write your code here
    K = 0
    maxBIC = 0
    for k in Kset: 
        p = k*d + k + k   #k*d for means, k for stdev, k for weights
        (Mu,P,Var) = init(X,k) 
        (Mu,P,Var,post,LL) = mixGauss(X,k,Mu,P,Var)

        LLsize = np.shape(LL)
        BIC = LL[LLsize[0]-1] - 0.5*p*np.log(n)
        if(k == Kset[0]):
            maxBIC = BIC

        if(BIC >= maxBIC):
            maxBIC = BIC
            K = k

    return K
#---------------------------------------------------------------------------------



#---------------------------------------------------------------------------------
# PART 2 - Mixture models for matrix completion
#---------------------------------------------------------------------------------

# RMSE criteria
# input: X: n*d data matrix;
#        Y: n*d data matrix;
# output: RMSE
def rmse(X,Y):
    return np.sqrt(np.mean((X-Y)**2))


# E step of EM algorithm with missing data
# input: X: n*d data matrix;
#        K: number of mixtures;
#        Mu: K*d matrix, each row corresponds to a mixture mean;
#        P: K*1 matrix, each entry corresponds to the weight for a mixture;
#        Var: K*1 matrix, each entry corresponds to the variance for a mixture;
# output:post: n*K matrix, each row corresponds to the soft counts for all mixtures for an example
#        LL: a Loglikelihood value
def Estep_part2(X,K,Mu,P,Var):
    n,d = np.shape(X) # n data points of dimension d
    post = np.zeros((n,K)) # posterior probabilities to compute
    LL = 0.0    # the LogLikelihood
    fu = np.zeros(K)
	#Write your code here
    for i in range(n):

        Cu = np.nonzero(X[i,:])
        XCu = X[i,Cu]

        for k in range(K):
            MuCu = Mu[k,Cu]
            lenCu = np.shape(Cu)
            NCu = -lenCu[1]/2.0*np.log(2*np.pi*Var[k])

            NCu = NCu - 1/(2*Var[k])*np.power(LA.norm(XCu-MuCu),2)

            # wait = input("PRESS ENTER TO CONTINUE.")

            # fu[k]  = np.log(P[k]) + np.log(NCu)
            fu[k]  = np.log(P[k]) + NCu
            
        post[i,:] = fu - logsumexp(fu)
        LL = LL + logsumexp(fu)

    return (np.exp(post),LL)

	
# M step of EM algorithm
# input: X: n*d data matrix;
#        K: number of mixtures;
#        Mu: K*d matrix, each row corresponds to a mixture mean;
#        P: K*1 matrix, each entry corresponds to the weight for a mixture;
#        Var: K*1 matrix, each entry corresponds to the variance for a mixture;
#        post: n*K matrix, each row corresponds to the soft counts for all mixtures for an example
# output:Mu: updated Mu, K*d matrix, each row corresponds to a mixture mean;
#        P: updated P, K*1 matrix, each entry corresponds to the weight for a mixture;
#        Var: updated Var, K*1 matrix, each entry corresponds to the variance for a mixture;
def Mstep_part2(X,K,Mu,P,Var,post, minVariance=0.25):
    n,d = np.shape(X) # n data points of dimension d
    
	#Write your code here
    expNumK = np.sum(post, axis=0)
    P = expNumK/(np.sum(expNumK))

    for k in range(K):
        for l in range(d):
            denom = np.sum(post[np.nonzero(X[:,l]),k])
            if(denom >= 1):
                Mu[k,l] = np.dot(post[:,k],X[:,l])/denom


    dist = np.zeros((n,K))
    card = np.zeros(n)
    for i in range(n):
        Cu = np.nonzero(X[i,:])
        card[i] = np.count_nonzero(X[i,:])
        XCu = X[i,Cu]
        for k in range(K):
            MuCu = Mu[k,Cu]
            dist[i,k] = np.power(LA.norm(MuCu-XCu),2)
    
    for k in range(K): 
        Var[k] = np.dot(post[:,k],dist[:,k])/np.dot(card, post[:,k])
        if(Var[k] < 0.25):
            Var[k] = 0.25

    return (Mu,P,Var)

	
# mixture of Guassians
# input: X: n*d data matrix;
#        K: number of mixtures;
#        Mu: K*d matrix, each row corresponds to a mixture mean;
#        P: K*1 matrix, each entry corresponds to the weight for a mixture;
#        Var: K*1 matrix, each entry corresponds to the variance for a mixture;
# output: Mu: updated Mu, K*d matrix, each row corresponds to a mixture mean;
#         P: updated P, K*1 matrix, each entry corresponds to the weight for a mixture;
#         Var: updated Var, K*1 matrix, each entry corresponds to the variance for a mixture;
#         post: updated post, n*K matrix, each row corresponds to the soft counts for all mixtures for an example
#         LL: Numpy array for Loglikelihood values
def mixGauss_part2(X,K,Mu,P,Var):
    n,d = np.shape(X) # n data points of dimension d
    post = np.zeros((n,K)) # posterior probs tbd
    
    #Write your code here
    #Use function Estep and Mstep as two subroutines
    maxIter = 500
    LL = np.zeros(maxIter)

    (post, OLL) = Estep_part2(X,K,Mu,P,Var)
    OLL = OLL - np.abs(OLL*0.5)         #just to insure that it will enter the loop and OLL is initialized small enough
    NLL = OLL + np.abs(OLL*0.1)
    tempMu = Mu
    tempP = P
    tempVar = Var
    it = 0
    while (NLL-OLL > np.power(10.0,-6)*np.abs(NLL) and it < maxIter): 
        Mu = tempMu         #Just so that we store Mu only after it passes the convergence criteria (so we don't get one after convergence...)
        P = tempP
        Var = tempVar
        OLL = NLL
        (post,NLL) = Estep_part2(X,K,Mu,P,Var)
        (tempMu,tempP,tempVar) = Mstep_part2(X,K,Mu,P,Var,post)
        LL[it] = NLL
        it = it + 1 
    
    LL = LL[0:it-1]
    
    return (Mu,P,Var,post,LL)


# fill incomplete Matrix
# input: X: n*d incomplete data matrix;
#        K: number of mixtures;
#        Mu: K*d matrix, each row corresponds to a mixture mean;
#        P: K*1 matrix, each entry corresponds to the weight for a mixture;
#        Var: K*1 matrix, each entry corresponds to the variance for a mixture;
# output: Xnew: n*d data matrix with unrevealed entries filled
def fillMatrix(X,K,Mu,P,Var):
    n,d = np.shape(X)
    Xnew = np.copy(X)

    (post, LL) = Estep_part2(X,K,Mu,P,Var)

    for i in xrange(n):
        for j in xrange(d):
            if(X[i,j] == 0):
                Xnew[i,j] = np.dot(Mu[:,j],post[i,:])
    
    return Xnew
#---------------------------------------------------------------------------------