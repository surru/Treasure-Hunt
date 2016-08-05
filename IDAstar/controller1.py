#,Saurabh Khoria
# 2013CSB1029

# singleAgentSearch function takes board as an input
# returns three lists as described in README file
# In board, following convention is followed
#         1 -> musketeer
#         2 -> soldier
#         0 -> empty location
#         3 -> Soldier With Diamond (Goal State)

# IDA*

import Queue as Q

class node:
	'''
		This is the class for the node which represents a particular position on the board
		where   x is the x -cordinate
				y is the y -cordinate
				p is pointing to the parent of this node
				g is the cost of path from musketeer to this node
	'''
	def __init__(self,xc,yc,p=None,g=0):
		self.x=xc
		self.y=yc
		self.p=p		# This is a pointer to the parent of this node
		self.g=g

def expand(en,fl,es,mat,fx,fy,cutoff,nxtcutoff):
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
		h=abs(fx-x)+abs(fy-y)+en.g+1
		if h<=cutoff:
			fl.put(node(x,y,en,en.g+1))
		elif nxtcutoff==0:
			nxtcutoff=h
	x+=1
	y+=1
	
	if x<n and y<n and not any(a.x==x and a.y==y for a in fl.queue) and not any(a.x==x and a.y==y for a in es) and (mat[x][y]==2 or mat[x][y]==3):
		h=abs(fx-x)+abs(fy-y)+en.g+1
		if h<=cutoff:
			fl.put(node(x,y,en,en.g+1))
		elif nxtcutoff==0:
			nxtcutoff=h
	y+=1
	x-=1
	
	if y<m and x>=0 and not any(a.x==x and a.y==y for a in fl.queue) and not any(a.x==x and a.y==y for a in es) and (mat[x][y]==2 or mat[x][y]==3):
		h=abs(fx-x)+abs(fy-y)+en.g+1
		if h<=cutoff:
			fl.put(node(x,y,en,en.g+1))
		elif nxtcutoff==0:
			nxtcutoff=h
	y-=1
	x-=1
	
	if y>=0 and x>=0 and not any(a.x==x and a.y==y for a in fl.queue) and not any(a.x==x and a.y==y for a in es) and (mat[x][y]==2 or mat[x][y]==3):
		h=abs(fx-x)+abs(fy-y)+en.g+1
		if h<=cutoff:
			fl.put(node(x,y,en,en.g+1))
		elif nxtcutoff==0:
			nxtcutoff=h

	return (fl,nxtcutoff)


def singleAgentSearch(board):
	'''
		This function implements the IDA* Search
	'''
	mat=board
	m=len(mat)
	n=len(mat[0])

	for x in range(0,m):
		for y in range(0,n):
			if mat[x][y]==3:
				fx=x
				fy=y
	
	muske=[]
	for x in range(0,m):
		for y in range(0,n):
			if mat[x][y]==1:
				muske.append(node(x,y))

	num=len(muske)      # num is the number of musketers
	
	EN=[]
	SQ=[]
	SP=[]
	for i in range(0,num):

		musk=muske[i]
		est=None
		sq=None
		path=None
		cutoff=abs(fx-musk.x)+abs(fy-musk.y)
		sq2=[]
		flag=1
		while est==None and sq==None and path == None:
			nxtcutoff=0
			t=iterative_dfs(board,cutoff,musk,fx,fy,nxtcutoff)
			if t[0]!=None and t[1]!=None and t[2]!=None:
				est=t[0][:]
				sq=t[1][:]
				path=t[2][:]
			nxtcutoff=t[3]
			if nxtcutoff<=cutoff:
				flag=0
				break
			else:
				cutoff=nxtcutoff
			# if sq==sq2:
			# 	flag=1
			# 	break
		
		if flag==1 and mat[est[-1][0]][est[-1][1]]==3:
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

	# YOUR CODE HERE #
	return (exploredNodes,searchQueue,shortestPath)

def iterative_dfs(mat,cutoff,musk,fx,fy,nxtcutoff):
	es=[]
	fl=Q.PriorityQueue()
	fl.put(musk)
	sq=[]
	s=[]
	flag=0
	while(1):
		if(fl.empty()):
			break
		en=fl.get()
		es.append(en)
		if mat[en.x][en.y]==3:
			flag=1
			break
		(fl,nxtcutoff)=expand(en,fl,es,mat,fx,fy,cutoff,nxtcutoff)
		s=fl.queue
		t=[]
		for i in range(len(s)):
			t.append([s[i].x,s[i].y])
	 
		sq.append(t)

	if flag==0:
		return (None,None,None,nxtcutoff)
	else:
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
	
	return (est,sq,path,nxtcutoff)


