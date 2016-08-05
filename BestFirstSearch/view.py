#
#     Functions for rendering the graphics are taken and modified from :
#		"Invent your Own Computer Games with Python, 2nd Edition"
#       Author : Al Sweigart
#


'''
	View.py holds the graphical support for the three musketeers board game. It uses pygame library for supporting all
	graphics and sounds. This library helps to abstract the game logic (implemented separately in controller.py)  
	from the graphics. 
	
	Students are required to implent the single-agent search code (BFA/DFA/AStar) in 
	'controller1.py' and the output of the same can be visualized.

    To visualize the output, type 'python view.py' from the command line after the successful implementation of 
    single agent search algorithms. 
'''


import pygame,sys
import os
from pygame.locals import *
import controller
try:
	import controller1
except ImportError:
	raise ImportError


#making the controller object to call single agent search function 
controllerObj = controller.controller()

CELLSIZE = 35                  # size of each square of game board 
WINDOWWIDTH = 860              # size of game window : width
WINDOWHEIGHT = 640             # size of game window : height
FPS = 300

#              R   G   B        # colors used in GUI 
BLACK     = (  0,  0,  0)
WHITE     = (255,255,255)
LIGHTSKY  = (239,239,239)
TURQUOISE = (207,226,243)
DARKBLUE  = ( 57,106,211)
LIGHTBLUE = (170,180,220)
GREEN     = (  0,204,  0)
BUTTONCOLOR = (51,122,183)
BUTTONHOVER = (40,96,144)

BGCOLOR = LIGHTSKY
CELLCOLOR = TURQUOISE
TEXTCOLOR = WHITE
BORDERCOLOR = DARKBLUE

# font sizes used in game
BASICFONTSIZE = 20
BASICFONTSIZESMALL = 13

XMARGIN = 60  # left margin of game board from game window 
YMARGIN = 50  # top margin of game board from game window  

_image_library = {} # dictionary to store images


class Button:
	'''Button class to draw the buttons on the top of the board and provide the highlight on mouse hover functionality

	   Attributes:
	   		hovered (bool) : To keep track of mouse on hover event	
	'''
	hovered = False

	def __init__(self,bType,pos,size):
		'''This method makes the button class object. 

			Arguments:
				bText (str): Text to be displayed on button
				pos (tuple of int) : Position of the button in the form (x,y) where x and y are coordinates assuming 	
							  top-left corner as the origin
				size (tuple of int) : Size in the form of tuple (width,height)	where width and height are as required		  	
		'''
		self.rect = pygame.draw.rect(DISPLAYWINDOW,BUTTONCOLOR,(pos[0],pos[1],180,30))
		self.pos = pos
		self.size = size
		self.text = BASICFONT.render(bType,True,WHITE)
		self.textRect = self.text.get_rect()
		self.textRect.topleft = (pos[0]+15,pos[1]+1)
	
	def draw(self):                      
		'''This function draw a rectangle to be used as a button. It gets the background color by calling get_color
		method which returns button color depending on mouse hover event.
		'''
		self.rect = pygame.draw.rect(DISPLAYWINDOW,self.get_color(),(self.pos[0],self.pos[1],self.size[0],self.size[1]))
		DISPLAYWINDOW.blit(self.text,self.textRect)		

	def get_color(self):
		'''This function returns the button color depending on the mouse on hover event.

			Returns:
				BUTTONHOVER color if mouse pointer is on the button,
				default BUTTONCOLOR otherwise.
		'''
		if self.hovered:
			return BUTTONHOVER
		else:
			return BUTTONCOLOR

def main():
	''' The is the main function for playing the game. It handles all the game events, make the moves entered,
	    call the relevant functions to render graphics.  
	'''

	global FPSCLOCK,DISPLAYWINDOW,BASICFONT,BASICFONTSMALL
	pygame.init()     								
	
	FPSCLOCK = pygame.time.Clock()
	DISPLAYWINDOW = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))   						# rendering the pygame window as per defined size
	
	pygame.display.set_caption('Single Agent Search - The Three Musketeers Board Game')     	# title for pygame window
	BASICFONT = pygame.font.Font('../fonts/Comic_Sans_MS.ttf',BASICFONTSIZE)         		# font for rendering the text
	BASICFONTSMALL = pygame.font.Font('../fonts/Comic_Sans_MS.ttf',BASICFONTSIZESMALL)   	# small sized font

	# creating the button class objects 
	buttons = [Button('Trace path',(650,20),(140,30)),Button('Prev',(650,90),(70,30)),Button('Next',(730,90),(75,30))]

	mainBoard = getStartingBoard()							# get the starting state of board in the form of a 2-d list
	drawBoard(mainBoard)            						# render the board according to the list obtained in mainboard

	# get the lists containing visited nodes, nodes to be visited after each iteration, and actual sequence of moves
	(visitedNodes,neighborNodes,moves) = controllerObj.makeMove(mainBoard)
	
	clickCount = -1;   										# variable for handling the next and prev button requests

	while True:         									# main game loop
		
		checkForQuit()     									# check if any game is quit or not
		for button in buttons:   							# renders the button objects on the screen
			if button.rect.collidepoint(pygame.mouse.get_pos()):
				button.hovered = True
			else:
				button.hovered = False
			button.draw()
		
		
		for event in pygame.event.get():        				# get events occuring on pygame window
			if event.type == MOUSEBUTTONUP:     				# get the mouse click event

				if buttons[0].rect.collidepoint(event.pos):  	# check if clicked on trace path button
					tracePath(mainBoard,moves)

				if buttons[1].rect.collidepoint(event.pos):  	# check if clicked on prev button for highlighting nodes
					clickCount = max(-1,clickCount-1)        
					higlightNodes(mainBoard,visitedNodes,neighborNodes,moves,clickCount)
						

				if buttons[2].rect.collidepoint(event.pos):  	# check if clicked on next button for highlighting nodes
					clickCount = min(len(neighborNodes)-1,clickCount+1)
					higlightNodes(mainBoard,visitedNodes,neighborNodes,moves,clickCount)
					
		if event.type == QUIT: 
			pygame.quit()
			sys.exit()

		pygame.display.update()      
		FPSCLOCK.tick(FPS)

def terminate():
	''' This function terminates the pygame program and returns to the command line from where it was started'''
	pygame.quit()
	os._exit(1)

def checkForQuit():
	''' This function checks for any of the quit events and calls the terminate function'''
	for event in pygame.event.get(QUIT):	# get all the QUIT events
		terminate()							# terminate if any QUIT events are present
	for event in pygame.event.get(KEYUP):	# get all the KEYUP events
		if event.key == K_ESCAPE:			
			terminate()						# terminate if the KEYUP event was for the Esc key
		pygame.event.post(event)			# put the other KEYUP event objects back

def getLeftTopOfCell(cellx,celly):
	''' This function computes the pixel coordinates of top-left corner of a selected cell of game board.
		cellx,celly = (0,0) for the top-left cell of game board
		cellx,celly = (1,0) for the cell just below cell at (0,0)

		Args:
		  cellx (int) : x-index of selected cell of game board i.e. distance from top 
		  celly (int) : y-index of selected cell of game board i.e distance from left
		
		Returns:
		  pixel coordinates of the top-left corner of selected cell. 

	'''
	left = XMARGIN + (cellx*CELLSIZE) + (cellx-1)
	top = YMARGIN + (celly*CELLSIZE) + (celly-1)
	return (top,left)	

def makeText(text,color,top,left):
	''' renders the text on screen at given position

		Args:
		  text (str) : Text string to be rendered on screen
		  color (tuple) : Value in (R,G,B) format of color in which the text is to be drawn.  
	      top (int) : top pixel co-ordinate (distance from left side of pygame window) of the text.
	      left (int) : left pixel co-ordinate (distance from top side of pygame window) of the text.

	    Returns:
	    	It displays the text on screen and returns nothing.  
	'''
	textSurf = BASICFONT.render(text,True,color)        # defines the text to be drawn
	textRect = textSurf.get_rect()                      # gets the rectange bounding the defined text
	textRect.topleft = (top,left)                       # sets the top-left coordinates of bounded rectangle
	DISPLAYWINDOW.blit(textSurf,textRect)               # renders the text on pygame window

def makeTextSmall(text,color,top,left):
	''' renders the text with smaller font on screen at given position 

		Args:
		  text (str) : Text string to be rendered on screen
		  color (tuple) : Value in (R,G,B) format of color in which the text is to be drawn.  
	      top (int) : top pixel co-ordinate (distance from left side of pygame window) of the text.
	      left (int) : left pixel co-ordinate (distance from top side of pygame window) of the text.

	    Returns:
	    	It displays the text on screen and returns nothing.  
	'''
	textSurf = BASICFONTSMALL.render(text,True,color)
	textRect = textSurf.get_rect()
	textRect.topleft = (top,left)
	DISPLAYWINDOW.blit(textSurf,textRect)
	
def drawCell(cellx,celly,number,highlightType):
	''' This function draws a cell at board indices cellx and celly,also highlights the cell 
	    if it is the clicked cell.

	    Args:
          cellx (int): x-index of board cell (0 for top-left, 1 for below it and so on)
          celly (int): y-index of board cell (0 for top-left, 1 for the cell to its right and so on)
          number(int): tells the player type - 1 for musketeer, 2 for soldier, 0 otherwise
          highlightType (int) : tells the highlight type -  1 for visited nodes, 2 for yet to visit nodes i.e. nodes in queue and 0 otherwise

        Returns:
          This function doesn't return anything, it draws the square on game board with appropriate player on it.

	'''
	if (cellx < 0 or celly < 0):
		print "IndexError: list index cannot be negative"	
		terminate()
		return

	left,top = getLeftTopOfCell(cellx,celly)  						# get the top-left coordinated of sqaure to be drawn
	if highlightType ==0:                      									
		pygame.draw.rect(DISPLAYWINDOW,CELLCOLOR,(left,top,CELLSIZE,CELLSIZE))      
	elif highlightType == 1:                   
		pygame.draw.rect(DISPLAYWINDOW,GREEN,(left,top,CELLSIZE,CELLSIZE)) 
	elif highlightType == 2:                   
		pygame.draw.rect(DISPLAYWINDOW,BUTTONCOLOR,(left,top,CELLSIZE,CELLSIZE))	

	if number == 1:                          						# renders the musketeer image
		imageSurf = get_image('../images/musketeers.png')
	elif number == 2:                       						# renders the soldier image
		imageSurf = get_image('../images/soldier.png') 
	elif number == 3:                          						# renders the diamond image
		imageSurf = get_image('../images/diamond.png')
	elif number == 0:                           					# case the square is empty
		return

    
	imageSurf = pygame.transform.scale(imageSurf,(30,30))	 		# scaling down the image to fit it onto square
	imageRect = imageSurf.get_rect()                         		# get the bounding rectangle for image rendered
	imageRect.center = left + int(CELLSIZE/2),top+int(CELLSIZE/2)    # set the position of image at the center of square
	DISPLAYWINDOW.blit(imageSurf,imageRect)               			# renders the image onto the pygame window

def drawBoard(board):
	''' This function draws the entire pygame window. It describes what component is to be drawn and at which position.

		Args:
		  board (list of lists) : list of lists having the board state (2-d lists of int type)
		  
		Returns:
		  This function doesn't return anything.

	'''
	BOARDWIDTH = len(board[0])
	BOARDHEIGHT = len(board)
	DISPLAYWINDOW.fill((238, 238, 238))  # background color

	# renders each sqaure with its corresponding player image
	for cellx in range(len(board)):
		for celly in range(len(board[cellx])):
			drawCell(cellx,celly,board[cellx][celly],0)

	# writes the game board index i.e. 1,2,3,.... on the top of board
	for i in range(len(board[0])):
		makeTextSmall(str(i+1),DARKBLUE,YMARGIN + (i*CELLSIZE) + i-3 + int(CELLSIZE/2),XMARGIN-22)

	# writes the game board index i.e. a,b,c,d,..... on the left of Board	
	for i in range(len(board)):
		makeTextSmall(chr(ord('a')+i),DARKBLUE,YMARGIN-20,XMARGIN + (i*CELLSIZE) + i-10 + int(CELLSIZE/2))
			

	# draw green rectangle as legend to indicate for the visited node	
	makeText('Highlight Nodes',DARKBLUE,650,60)	
	pygame.draw.rect(DISPLAYWINDOW,GREEN,(650,150,30,30))	
	makeText('Visited Node',DARKBLUE,690,150)

	# draw blue rectangle as legend to indicate for the nodes to be visited	
	pygame.draw.rect(DISPLAYWINDOW,BUTTONCOLOR,(650,200,30,30))	
	makeText('To be explored ',DARKBLUE,690,200)

	makeText("#nodes visited",DARKBLUE,650,250)
	makeText("#nodes in Queue",DARKBLUE,650,320)

	
	left,top = getLeftTopOfCell(0,0)
	width = BOARDWIDTH*CELLSIZE
	height = BOARDHEIGHT*CELLSIZE
	pygame.draw.rect(DISPLAYWINDOW,BORDERCOLOR,(left-5,top-5,width+23,height+23),4)   # draws the boundary around the game board
	
def getStartingBoard():
	''' This function reads the 'input.txt' file and returns the list of lists as a board with starting configuration as
	    0 for soldier, 1 for musketeer, 2 for blank space and 3 for diamond.

	    Args:
	    	None

	    Returns:
	    	board (list of lists) : list of lists having the board state (2-d lists of int type)
	'''
	board = []
	inp = open('input.txt','r')
	board = [[int(n) for n in line.split()] for line in inp]    # splitting each line of file on the basis of spaces
	inp.close()
	return board

def tracePath(board,moves):
	''' This function draws the line tracing the path from a musketeer to diamond. 

		Args:
			board (list of lists) : list of lists having the board state (2-d lists of int type)
			moves (list of lists) : contains lists of type [x1,y1],[x2,y2],....,[xn,yn] i.e. the path from musketeer to diamond
	
		Returns:
			This function doesn't return anything.	
	'''
	for i in range(len(moves)-1):          # gets the consecutives coordinates in moves list and draw a line connecting the two
		start_pos = moves[i]
		end_pos = moves[i+1]
		top1,left1 = getLeftTopOfCell(start_pos[0],start_pos[1])
		top2,left2 = getLeftTopOfCell(end_pos[0],end_pos[1])
		coord1 = (top1 + CELLSIZE/2,left1+CELLSIZE/2)       # coordinates of center of first square
		coord2 = (top2 + CELLSIZE/2,left2+CELLSIZE/2)       # coordinates of center of second square
		pygame.draw.line(DISPLAYWINDOW,BLACK,coord1,coord2,2)

def higlightNodes(board,visitedNodes,neighborNodes,moves,clickCount):
	''' This function highlight the nodes as visited or to be explored.

		Args:
			board (list of lists) : list of lists having the board state (2-d lists of int type)
			visitedNodes (list of type:[x1,y1]) : Contains list of nodes visited
			neighborNodes (list of lists) : Contains list of lists (BFS/DFS queue) at each iteration of the algorithm
			moves (list of type : [x1,y1]) : Contains the path from one of the musketeers to the diamond
			clickCount (int) : stores the number of clicks on next/prev button.

		Returns:
			This function doesn't return anything. It highlights the visited nodes in green color and nodes yet to 
			be visited in blue color.

	''' 

	drawBoard(board)
	if clickCount > -1:    

		pygame.draw.rect(DISPLAYWINDOW,BUTTONCOLOR,(700,280,70,30))      # rectangular box to display the count of visited nodes
		makeText(str(clickCount+1),WHITE,730,280)

		pygame.draw.rect(DISPLAYWINDOW,BUTTONCOLOR,(700,350,70,30))     # rectangular box to display the count of nodes to be explored
		makeText(str(len(neighborNodes[clickCount])),WHITE,730,350)

	
		clickCount = min(clickCount,len(visitedNodes)-1) # restricting the clickcount variable value to equal to number of lists in visitedNodes
		
		for i in range(clickCount+1):   # highlights the visited nodes as green
			x = visitedNodes[i][0]
			y = visitedNodes[i][1]
			drawCell(x,y,board[x][y],1)
			
		for i in range(len(neighborNodes[clickCount])): # highlight the nodes to be explored as blue
			p = neighborNodes[clickCount][i][0]
			q = neighborNodes[clickCount][i][1]
			drawCell(p,q,board[p][q],2)

		
		if clickCount == len(visitedNodes)-1:      # display the number of steps to reach the diamond
			makeText("#steps to diamond",DARKBLUE,650,390)
			pygame.draw.rect(DISPLAYWINDOW,BUTTONCOLOR,(700,420,70,30))
			makeText(str(len(moves)-1),WHITE,730,420)			

def get_image(path):
	''' This function stores the image once loaded locally so that they are not loaded again and again.

		Args:
			path (str) : path (with name) to the image to be loaded

		Returns:
			image surface after being loaded using pygame.image.load module
	'''
	global _image_library
	image = _image_library.get(path)
	if image == None:
		canonicalized_path = path.replace('/',os.sep).replace('\\',os.sep)
		image = pygame.image.load(canonicalized_path)
		_image_library[path] = image
	return image

if __name__ == '__main__':
        try:
        	main()
        except:
                print('Invalid List Format')
                terminate()
