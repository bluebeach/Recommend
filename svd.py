#!/usr/bin/python
# encoding: utf-8
import math
import random

data = []    # all data
train = []  # train data
test = []   # test data


P = dict()    # user Matrix
Q = dict()    # item Matrix
bu = dict()   # user bias
bi = dict()   # item bias
mu = 0        # global bias

#-------------------------------load data------------------------------------
def ReadFile(data):
	f = open('/Users/chenjun/PycharmProjects/Recommend/ml-100k/u.data','r')
	line = f.readline()
	while line:
		line_split = line.split('\t')
		data.append( (int(line_split[0]),int(line_split[1]),int(line_split[2])) )
		line = f.readline()
	f.close()
	return
#------------------------------split data---------------------------------------
def SplitData(data,train,test,M,k,seed):
	random.seed(seed)
	for user,item,rui in data:
		if random.randint(0,M) == k:
			test.append((user,item,rui))
		else:
			train.append((user,item,rui))
	return


#-----------------------------training model-------------------------------------------
#train训练集中的用户评分记录 F隐类的格式  n迭代次数  Alpha学习速率  Lambda正则化参数
def LearningLFM(train,F,n,Alpha,Lambda,P,Q,bu,bi,mu):
    InitLFM(train,F,P,Q,bu,bi)
    for step in range(0,n):
        for u,i,rui in train:
            pui = Predict(u,i,P,Q,bu,bi,mu)
            eui = rui - pui
            bu[u] += Alpha * (eui - Lambda * bu[u])
            bi[i] += Alpha * (eui - Lambda * bi[i])
            for f in range(0,F):
                P[u][f] += Alpha * (Q[i][f]*eui - Lambda*P[u][f])
                Q[i][f] += Alpha * (P[u][f]*eui - Lambda*Q[i][f])
        Alpha *= 0.9
    return


#------------------------------init model parameter---------------------------------------------------
def InitLFM(train,F,P,Q,bu,bi):
	for u,i,rui in train:
		bu[u] = 0
		bi[i] = 0
		if u not in P:
			P[u] = [random.random() / math.sqrt(F) for x in range(0,F)]
		if i not in Q:
			Q[i] = [random.random() / math.sqrt(F) for x in range(0,F)]
	return


#------------------------------------make predict--------------------------------------------
def Predict(u,i,P,Q,bu,bi,mu):
	ret = mu + bu[u] + bi[i]
	ret += sum( P[u][f] * Q[i][f] for f in range(0,len(P[u])) )
	return ret


#-------------------------------------------------------------------------------------
def TestDataRmse(data,train,test,P,Q,bu,bi,mu):
	rmse = 0
	num = 0
	for u,i,rui in test:
		if ((u in P) and (i in Q)):
			rmse += (rui - Predict(u,i,P,Q,bu,bi,mu)) * (rui - Predict(u,i,P,Q,bu,bi,mu))
			num += 1
	rmse = math.sqrt(rmse / num)
	return rmse

#-----------------------------------------------------------------------------------
def AllDataRmse(data,P,Q,bu,bi,mu):
	rmse = 0
	for u,i,rui in data:
		rmse +=  (rui - Predict(u,i,P,Q,bu,bi,mu)) * (rui - Predict(u,i,P,Q,bu,bi,mu))
	rmse = math.sqrt(rmse / len(data))
	return rmse


#-------------------------------------------------------------------------------------------------------
#----------------------------------------begin---------------------------------------------------------

ReadFile(data)
SplitData(data,train,test,8,1,1)
print(' train => ', train)
print(' test => ', test)
LearningLFM(train,F = 10,n = 25,Alpha = 0.04,Lambda = 0.15,P = P,Q = Q,bu = bu,bi = bi,mu = mu)
print(TestDataRmse(data,train,test,P,Q,bu,bi,mu))
