import numpy as np
import tkinter as tk
from tkinter import font
from tkinter import Toplevel
import time

class Backend:
    
    def __init__(self,seed=None):
        file = open("words.txt","r")
        self.words = [_ for _ in file]
        self.shuffle(seed)
        self.gen_board()
        self.gen_roles()
        
    def newgame(self):
        self.gen_board()
        self.gen_roles()
        
    def shuffle(self,seed=None):
        if type(seed)==int and seed>=0 and seed<=4294967295:
            pass
        elif seed==None:
            # move to GUI
            while True:
                try:
                    seed = int(input('Input a random positive number: '))
                except:
                    print('INPUT ERROR: input not a whole number')
                    continue
                if seed>=0 and seed<=4294967295:
                    break
                else:
                    print('INPUT ERROR: number must be within range [0,4294967295]')
        else:
            # move to GUI
            print('Invalid seed provided.')
            while True:
                try:
                    seed = int(input('Input a random positive number: '))
                except:
                    print('INPUT ERROR: input not a whole number')
                    continue
                if seed>=0 and seed<=4294967295:
                    break
                else:
                    print('INPUT ERROR: number must be within range [0,4294967295]')
        np.random.seed(seed)
        self.shuffled = True

    def gen_board(self):
        self.board = np.random.choice(self.words,size=(5,5),replace=False)

    def gen_roles(self):
        if np.random.random()>0.5:
            nr,nb = 8,9
        else:
            nr,nb = 9,8
        roles = np.array(['#f0dcc1']*25).reshape(self.board.shape)
        for _ in range(nr):
            while True:
                i = round(np.random.random()*24)
                if roles[round((i-i%5)/5),i%5] == '#f0dcc1':
                    roles[round((i-i%5)/5),i%5] = 'red'
                    break
        for _ in range(nb):
            while True:
                i = round(np.random.random()*24)
                if roles[round((i-i%5)/5),i%5] == '#f0dcc1':
                    roles[round((i-i%5)/5),i%5] = 'blue'
                    break
        while True:
            i = round(np.random.random()*24)
            if roles[round((i-i%5)/5),i%5] == '#f0dcc1':
                roles[round((i-i%5)/5),i%5] = 'black'
                break
        self.roles = roles

class Frontend:
    
    def __init__(self,back):
        self.table = tk.Tk()
        self.key = Toplevel()
        self.cardfont = font.Font(self.table,family='Helvetica',size=36,weight='bold')
        self.scorefont = font.Font(self.table,family='Helvetica',size=24,weight='bold')
        self.r_rem = np.where(back.roles.flatten()=='red')[0].shape[0]
        self.b_rem = np.where(back.roles.flatten()=='blue')[0].shape[0]
        self.scoreboard()
        for i in range(back.board.shape[0]):
            for j in range(back.board.shape[1]):
                word = back.board[i,j]
                # button labels (for destroying later)
                tk.Button(self.table,
                          text=word,command=lambda i=i,j=j:self.guess(i,j,back),
                          height=1,width=8,border=5,
                          bg='#f0dcc1',fg='black',activebackground='#c9b9a3',
                          relief='raised',cursor='target',
                          font=self.cardfont,justify='center',anchor='n'
                          ).grid(row=i+1,column=j)
        for i in range(back.board.shape[0]):
            for j in range(back.board.shape[1]):
                tk.Label(self.key,
                         height=2,width=4,border=3,
                         bg=back.roles[i,j],
                         relief='ridge',cursor='target'
                         ).grid(row=i+1,column=j)
    
    def guess(self,i,j,back):
        # destroy button?
        word = back.board[i,j]
        color = back.roles[i,j]
        # show assassin
        tk.Button(self.table,
                 text=word,state='disabled',
                 height=1,width=8,border=5,
                 bg=color,fg='white',
                 relief='sunken',cursor='target',
                 font=self.cardfont,justify='center',anchor='n'
                 ).grid(row=i+1,column=j)
        time.sleep(1)
        self.logic(color)
    
    def logic(self,color):
        if color == 'red':
            self.r_rem -= 1
        elif color == 'blue':
            self.b_rem -= 1
        self.scoreboard()
        if color == 'black':
            self.gameover('ASSASSINATED!')
        elif self.r_rem==0:
            self.gameover('RED WINS!')
        elif self.b_rem==0:
            self.gameover('BLUE WINS!')
        
    def scoreboard(self):
        tk.Label(self.table,
                 text=str(self.r_rem),
                 height=1,width=12,border=5,
                 bg='red',fg='white',
                 relief='solid',cursor='target',
                 font=self.scorefont,justify='center',anchor='n'
                 ).grid(row=0,column=1)
        tk.Label(self.table,
                 text='REMAINING',
                 height=1,width=12,border=5,
                 bg='black',fg='white',
                 relief='solid',cursor='target',
                 font=self.scorefont,justify='center',anchor='n'
                 ).grid(row=0,column=2)
        tk.Label(self.table,
                 text=str(self.b_rem),
                 height=1,width=12,border=5,
                 bg='blue',fg='white',
                 relief='solid',cursor='target',
                 font=self.scorefont,justify='center',anchor='n'
                 ).grid(row=0,column=3)
    
    def gameover(self,message):
        # move to GUI
        print()
        print(message)
        new = input('Type \'n\' for a new game. ')
        self.table.destroy()
        if new=='n':
            back.newgame()
            front = Frontend(back)
            front.table.mainloop()
        else:
            print('Goodbye.')
            
def main():
    global back
    global front
    back = Backend()
    front = Frontend(back)
    front.table.mainloop()

if __name__ == '__main__':
    main()