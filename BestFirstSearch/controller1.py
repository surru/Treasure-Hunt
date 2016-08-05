# Saurabh Khoria
# 2013CSB1029

# singleAgentSearch function takes board as an input
# returns three lists as described in README file
# In board, following convention is followed
#         1 -> musketeer
#         2 -> soldier
#         0 -> empty location
#         3 -> Soldier With Diamond (Goal State)

# Breadth First Search

import Queue as Q

class node:
	'''
		This is the class for the node which represents a particular position on the board
		where   x is the x -cordinate
				y is the y -cordinate
				p is pointing to the parent of this node
				f is the f(n) which is equal to h(n) for greedy best first search
				h(n) is the heuristic function which is equal manhettan distance and it is admissible heuristic function
	'''
	def __init__(self,xc,yc,p,fx,fy):
		self.x=xc
		self.y=yc
		self.p=p 				# This is a pointer to the parent of this node
		self.f=abs(fx-xc)+abs(fy-yc)	

	def __cmp__(self,other):
		if self.f>=other.f:
			return 1
		else:
			return -1

def expand(en,fl,es,mat,fx,fy):
	'''
		This function expands the given node en and adds the children of en into the frontier list fl if they are not present 
		in the frontier list fl or the explored nodes set es.
	'''
	m=len(mat)
	n=len(mat[0])

	x=en.x
	y=en.y

	y-=1
	
	if y>=0 and not any(a.x==x and a.y==y for a in fl.queue) and not any(a.x==x and a.y==y for a in es) and (mat[x][y]==2 or mat[x][y]==3):
		fl.put(node(x,y,en,fx,fy))
	x+=1
	y+=1
	
	if x<m and y<n and not any(a.x==x and a.y==y for a in fl.queue) and not any(a.x==x and a.y==y for a in es) and (mat[x][y]==2 or mat[x][y]==3):
		fl.put(node(x,y,en,fx,fy))
	y+=1
	x-=1
	
	if y<n and x>=0 and not any(a.x==x and a.y==y for a in fl.queue) and not any(a.x==x and a.y==y for a in es) and (mat[x][y]==2 or mat[x][y]==3):
		fl.put(node(x,y,en,fx,fy))
	y-=1
	x-=1
	
	if y>=0 and x>=0 and not any(a.x==x and a.y==y for a in fl.queue) and not any(a.x==x and a.y==y for a in es) and (mat[x][y]==2 or mat[x][y]==3):
		fl.put(node(x,y,en,fx,fy))

	return fl


def singleAgentSearch(board):
	'''
		This function implements the Best First Search
	'''
	mat=board
	m=len(mat)
	n=len(mat[0])
	
	muske=[]

	for x in range(0,m):
		for y in range(0,n):
			if mat[x][y]==3:
				fx=x
				fy=y

	for x in range(0,m):
		for y in range(0,n):
			if mat[x][y]==1:
				muske.append(node(x,y,None,fx,fy))

	num=len(muske)      # num is the number of musketers
	
	EN=[]
	SQ=[]
	SP=[]
	for i in range(0,num):

		musk=muske[i]
		es=[]
		fl=Q.PriorityQueue()
		fl.put(musk)
		sq=[]
		s=[]
		while(1):
			if(fl.empty()):
				break
			en=fl.get()
			es.append(en)
			if mat[en.x][en.y]==3:
				break
			fl=expand(en,fl,es,mat,fx,fy)
			s=fl.queue
			t=[]
			for i in range(len(s)):
				t.append([s[i].x,s[i].y])
			 
			sq.append(t)
		s=fl.queue
		
		t=[]
		for i in range(len(s)):
			t.append([s[i].x,s[i].y])
		 
		sq.append(t)
		est=[]
		for i in range(0,len(es)):
			est.append([es[i].x,es[i].y])
		

		
		path=[]
		par=en.p
		path.append([en.x,en.y])
		while(par):
			path.append([par.x,par.y])
			par=par.p

		path.reverse()

		if mat[en.x][en.y]==3:
			EN.append(est)
			SQ.append(sq)
			SP.append(path)


	# Returning the shortest path which is shortest among all the available musketers

	number=len(EN)
	mini=0
	if number>=2:
		if len(SP[0])<=len(SP[1]):
			mini=0
		else:
			mini=1

	if number==3:
		if len(SP[2])<=len(SP[mini]):
			mini=2

	if number==0:
		exploredNodes=[]
		searchQueue=[]
		shortestPath=[]
	else:
		exploredNodes = EN[mini]
		searchQueue  = SQ[mini]
		shortestPath = SP[mini]

	return (exploredNodes,searchQueue,shortestPath)


