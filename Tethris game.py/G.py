import pygame
import random
 
pygame.font.init()

#Shape ORIENTATIONS

S = [ ['.....',
       '.....',
       '..00.',
       '.00..',
       '.....'],
      ['.....',
       '..0..',
       '..00.',
       '...0.',
       '.....']]
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
I=[['..0..',
    '..0..',
    '..0..',
    '..0..',
    '.....'],
   ['.....',
    '0000.',
    '.....',
    '.....',
    '.....']]
O=[['.....',
    '.....',
    '.00..',
    '.00..',
    '.....']]
J=[['.....',
    '.0...',
    '.000.',
    '.....',
    '.....'],
   ['.....',
    '..00.',
    '..0..',
    '..0..',
    '.....'],
   ['.....',
    '.....',
    '.000.',
    '...0.',
    '.....'],
   ['.....',
    '..0..',
    '..0..',
    '.00..',
    '.....']]

L=[['.....',
    '...0.',
    '.000.',
    '.....',
    '.....'],
   ['.....',
    '..0..',
    '..0..',
    '..00.',
    '.....'],
   ['.....',
    '.....',
    '.000.'
    '.0...',
    '.....'],
   ['.....',
    '.00..',
    '..0..',
    '..0..'
    '.....']]
T =[['.....',
     '..0..',
     '.000.',
     '.....',
     '.....'],
    ['.....',
     '..0..',
     '..00.',
     '..0..',
     '.....'],
    ['.....',
     '.....',
     '.0000.',
     '..0..',
     '.....'],
    ['.....',
     '..0..',
     '.00..',
     '..0..',
     '.....']]
#GLOBAL VARIABLES 
shapes = [S ,Z ,I ,O ,J ,L, T]
shape_colors = [(0 ,255 , 0),  (255,0,0),(0,255,255),(255,255,0),(255,165,0),(0,0,255),(128,0,128)]
block_size = 30

w_height =700
w_width =800
score =0
play_width=300
play_height=600

block_size=30
top_left_x = (w_width - play_width)//2
top_left_y = w_height-play_height

                                                      
#CLASS DEFINITION
class Piece:
    x=10
    y=20
    shape = 0
    color=()
    rotation =0
#constructor
    def __init__ (self , column ,row ,shape):
           self.x=column
           self.y =row
           self.shape =shape
           self.color = shape_colors[shapes.index(shape)]
           self.rotation =0


#Function Definition
    
def draw_text_middle(text,size,color,surface):

    #Assign the font
    
    font = pygame.font.SysFont('comicsans' ,size ,bold=True)

    #render the font of the text
    label = font.render(text , 1 ,color)

    #display
    surface.blit(label,(top_left_x + play_width/2 - (label.get_width()/2),top_left_y + play_height/2 - label.get_height()/2))

def check_lost(positions):
    for pos in positions:
        x,y=pos
        if y<1:
            return True
    return False

def get_shape():
    newPiece = Piece(5,0,random.choice(shapes))
    return newPiece

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation %len(piece.shape)]
    i=0
    for line in format:
        row = list(line)
        j=0
        for column in row:
            if column =='0':
                positions.append((piece.x +j,piece.y +i))
            j+=1
        i+=1
    k=0
    for pos in positions:
        positions[k]=(pos[0] -2,pos[1]-4)
        k+=1
    return positions

def valid_space( piece ,grid):
    accepted_positions = [[(j,i)for j in range(10) if grid[i][j]==(0,0,0)]for i in range (20)]
    accepted_positions = [ j for sub in accepted_positions for j in sub ]
    formatted = convert_shape_format(piece)
    
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True
def update_score(surface):
    text="Score : " +str(score)
    font=pygame.font.SysFont('comicsans',40)
    label=font.render(text,1,(255,255,255))
    
    sx= top_left_x + play_width + 40
    sy= top_left_y + play_height/2 - 100
    
    surface.blit(label,(sx+10,sy+150))
    
def draw_next_shape (piece,surface):
    font=pygame.font.SysFont('comicsans',30)
    label=font.render('Next Shape',1,(255,255,255))
    
    sx=top_left_x+play_width+50
    sy=top_left_y+play_height/2-100
    format=piece.shape[piece.rotation%len(piece.shape)]

    i=0
    for line in format:
        row=list(line)
        j=0
        for column in row:
            if column=='0':
                pygame.draw.rect(surface,piece.color,(sx+j*30,sy+i*30,30,30),0)
            j+=1
        i+=1
    surface.blit(label,(sx+10,sy-30))
    update_score(surface)

    
def draw_grid(surface,row,col):
    sx=top_left_x
    sy=top_left_y
    for i in range(row):
        pygame.draw.line(surface,(128,128,128),(sx,sy+i*30),(sx+play_width,sy+i*30))
        for j in range(col):
                 pygame.draw.line(surface,(128,128,128),(sx+j*30,sy),(sx+j*30,sy+play_height))
def draw_window(surface):
     surface.fill((0,0,0))
     font=pygame.font.SysFont('comicsans',60)
     label=font.render('TETRIS',1,(255,255,255))
     surface.blit(label,(top_left_x + play_width/2 - (label.get_width()/2),30))

     for i in range(len(grid)):
         for j in range(len(grid[i])):
                       pygame.draw.rect(surface,grid[i][j],(top_left_x+j*30,top_left_y+i*30,block_size,block_size),0)
     draw_grid(surface,20,10)
     pygame.draw.rect(surface,(255,0,0),(top_left_x,top_left_y,play_width,play_height),5)            

def play():
     global grid
     global score
     score=0
     locked_positions = {}
     grid = create_grid(locked_positions)
     
     change_piece =  False
     run = True
     current_piece = get_shape()
     next_piece = get_shape()
     clock = pygame.time.Clock()
     fall_time=0
    
     while run:
           fall_speed = 0.27
           grid = create_grid(locked_positions)
           fall_time += clock.get_rawtime()
           clock.tick()
           if fall_time/1000 >= fall_speed:
              fall_time =0
              current_piece.y += 1

              if not(valid_space(current_piece ,grid)) and current_piece.y >0:
                   current_piece.y -= 1
                   change_piece =True
           for event in pygame.event.get(): 
                   if event.type == pygame.QUIT:
                         run =False
                         pygame.display.quit()
                         quit()
                   if event.type ==pygame.KEYDOWN:
                       if event.key == pygame.K_LEFT:
                            current_piece.x -= 1
                            if not valid_space(current_piece,grid):
                                current_piece.x += 1
                                
                       elif event.key == pygame.K_RIGHT:
                           current_piece.x += 1
                           if not valid_space(current_piece,grid):
                                current_piece.x-=1
                       elif event.key==pygame.K_DOWN:       
                          current_piece.y+=1
                          if not valid_space(current_piece,grid):
                              current_piece.y-=1
                       elif event.key==pygame.K_UP:
                          current_piece.rotation=current_piece.rotation+1%len(current_piece.shape)
                          if not valid_space(current_piece, grid):
                              current_piece.rotation = current_piece.rotation -1%len(current_piece.shape)

           shape_pos=convert_shape_format(current_piece)
           for i in range(len(shape_pos)):
                   x,y=shape_pos[i]
                   if y > -1:
                        grid[y][x]=current_piece.color
           if change_piece:
              for pos in shape_pos:
                    p=(pos[0],pos[1])
                    locked_positions[p]=current_piece.color
              current_piece=next_piece
              next_piece=get_shape()
              change_piece=False
              clear_rows(grid ,locked_positions)
           draw_window(window)
           draw_next_shape(next_piece,window)
           pygame.display.update()

           if check_lost(locked_positions):
                 run =False
     window.fill((0,0,0))
     draw_text_middle("You Lost",80,(255,255,255),window)
     pygame.display.update()
     pygame.time.delay(2000)
     
def clear_rows(grid ,locked):
    global score
    inc =0
    for i in range(len(grid)-1,-1,-1):
        row =grid[i]
        if(0,0,0) not in row:
            inc+=1
            ind=i
            for j in range(len(row)):
                   try:
                       del locked[(j,i)]
                   except:
                       continue
    if inc>0:
          temp=sorted(list(locked),key=lambda x:x[1])
          for key in temp[::-1]:
                x,y=key
                if y<ind:
                    newKey=(x,y+inc)
                    locked[newKey] =locked.pop(key)
                 
          score+=10


def create_grid(locked_positions={}):

    grid = [[ (0,0,0) for x in range(10)] for y in range(20) ] 

    for i in range(len(grid)): #rows = 20

        for j in range(len(grid[i])): #columns = 10

            if (j,i) in locked_positions:

                c = locked_positions[(j,i)]

                grid[i][j] = c

    return grid       
                        
def game():
    run =True
    
    while run:
        window.fill((0,0,0))
        
        draw_text_middle("Press any key to begin!" ,60,(255,255,255),window)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                play()
                
            if event.type == pygame.QUIT:
                run = False
                
    pygame.quit()

 #driver code     
window = pygame.display.set_mode((800,700))
pygame.display.set_caption("Tetris")
game()
