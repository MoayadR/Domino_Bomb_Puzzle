import tkinter as Tk
import pathlib
from pyswip import Prolog , Atom

def displayResults(resList , rows , columns):
    slave = Tk.Tk()
    window_width = columns * 133
    window_height = rows * 80
    slave.geometry("%dx%d" % (window_width, window_height))
    slave.title("Domino Results")
    for i in range(rows):
        for j in range(columns):
            if(resList[i][j] == 'bomb'):
                L = Tk.Label(slave,text=resList[i][j],bg='red' , width= 15 )
            elif(resList[i][j] == 'domino'):
                L = Tk.Label(slave,text=resList[i][j],bg='green',width= 15 )
            else:
                L = Tk.Label(slave,text=resList[i][j],bg='grey',width= 15 )
            L.grid(row=i,column=j , sticky=Tk.W + Tk.E,  padx=10, pady=10)

def atoms_to_strings(answer):
    if isinstance(answer, dict):
        result = {}
        for k in answer.keys():
            result[k] = atoms_to_strings(answer[k])
    elif isinstance(answer, list):
        result = [atoms_to_strings(val) for val in answer]
    elif isinstance(answer, Atom):
        result = answer.value
    elif isinstance(answer, int) or isinstance(answer, str):
        result = answer
    else:
        print("Unsupported result from Prolog: " + str(type(answer)) + str(answer))
    return result 

def solveBoard(board, rows , columns , slave):
    prolog = Prolog()
    cwd = str(pathlib.Path(__file__).parent.resolve())
    cwd = cwd.replace('\\' , '/')
    prolog.consult(cwd+"/PlacingDominosLogic.pl")
    L = list(prolog.query("initSearch("+str(rows)+", "+str(columns)+" ," +str(board)+ ",Solution )"))
    L = atoms_to_strings(L)
    slave.destroy()
    for i in range(len(L)):
        displayResults(L[i].get('Solution') , rows , columns)

    
def on_click(i , j  , board , slave , rows , columns , e):
    board[i][j] = "bomb"
    slave.destroy()
    defineBoard(rows , columns , board)

def defineBoard(rows , columns , board):
    slave = Tk.Tk()
    window_width = columns * 133
    window_height = rows * 80
    slave.geometry("%dx%d" % (window_width, window_height))
    slave.title("Domino")
    for i in range(rows):
        for j in range(columns):
            if(board[i][j] == 'bomb'):
                L = Tk.Label(slave,text=board[i][j],bg='red' , width= 15 )
            else:
                L = Tk.Label(slave,text=board[i][j],bg='grey',width= 15 )
            L.grid(row=i,column=j , sticky=Tk.W + Tk.E,  padx=10, pady=10)
            L.bind('<Button-1>',lambda e,i=i,j=j: on_click(i,j ,board ,slave, rows , columns ,e))
    
    B = Tk.Button(slave, text ="Solve" , command= lambda : solveBoard(board, rows , columns , slave), width=10)
    B.grid(row = rows +1, column = columns // 2)
   

def startGame(e1, e2 ):
    rows = int(e1.get())
    columns = int(e2.get())
    board = [ ['x']*columns for _ in range(rows) ]
    defineBoard(rows , columns , board)

def mainGameLoop():
    master = Tk.Tk()
    master.geometry('250x200')
    master.title("Domino")
    Tk.Label(master, text='Rows').grid(row=0)
    Tk.Label(master, text='Columns').grid(row=1)
    e1 = Tk.Entry(master)
    e2 = Tk.Entry(master)
    e1.grid(row=0, column=1, padx=10, pady=5)
    e2.grid(row=1, column=1, padx=10, pady=10)

    B = Tk.Button(master, text ="Start" , command= lambda : startGame( e1,e2,), width=10)
    B.grid(row = 2, column=1)
    Tk.mainloop()



mainGameLoop()
