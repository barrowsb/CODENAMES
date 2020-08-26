import numpy as np
import tkinter as tk
from tkinter import font
from tkinter import Toplevel
# from PIL import ImageTk,Image

# ---------------------
# IMPROVEMENTS TO MAKE:
# ---------------------
# [X] display startup menus on empty table
# [X]    gen_table() --> init_table() + set_table()
# [X]    fix logic so I can do menus sequentially without hacking
# [X]    stop program when I [X]-out startup menu(s)
# [X]       or solve by placing menus directly on table
# [ ] make startup menus window wide enough to show full title
# [ ] move key from TopLevel to table
# [ ] keep empty word/new/reveal buttons and display menus on status bar
# [ ]    init_table(): populate table with empty buttons
# [ ] bind <Enter> key to shuffle [OK]
# [ ] show icon on startup menus and taskbar (Mac compatability)
#      ^(https://stackoverflow.com/questions/45668895/tkinter-tclerror-image-doesnt-exist/45669789#45669789)
# [ ] map an app version as an executable
#      ^(https://stackoverflow.com/questions/5458048/how-to-make-a-python-script-standalone-executable-to-run-without-any-dependency)

class Game:
    
    def __init__(self,seed=None):
        file = open("words.txt","r")
        self.words = [_ for _ in file]
        self.init_table()
        self.is_shuffled = False
        self.shuffle(seed)
        # ^ implicitly starts new game
    
    def init_table(self):
        self.table = tk.Tk()
        self.table.title('CODENAMES')
        self.cardfont = font.Font(self.table,family='Helvetica',size=28,weight='bold')
        self.scorefont = font.Font(self.table,family='Helvetica',size=24,weight='bold')
    
    def shuffle(self,seed=None):
        # self.img = ImageTk.PhotoImage(Image.open('img\icon2.png'))
        # self.panel = tk.Label(self.table,image=self.img)
        # self.panel.image = self.img
        # self.panel.pack(side="bottom",fill="both",expand="yes")
        l = tk.Label(self.table,text='Input a random positive number.')
        l.pack()
        e = tk.Entry(self.table)
        e.pack()
        b = tk.Button(self.table,text='Ok',command=lambda \
                      root=self.table,e=e,l=l:self.do_shuffle_logic(root,e,l))
        b.pack()
        # self.table.bind('<Return>',lambda root=self.table,e=e,l=l:self.do_shuffle_logic(root,e,l))
        self.table.mainloop()
    
    def do_shuffle_logic(self,root,e,l):
        seed = e.get()
        try:
            seed = int(seed)
        except:
            l['text'] = 'Try again. Input not a whole number.'
            return
        if seed>=0 and seed<=4294967295:
            np.random.seed(seed)
            self.is_shuffled = True
            self.clear_table()
            self.start_newgame()
        else:
            l['text'] = 'Try again. Number must be within range 0-4294967295.'
            return
    
    def start_newgame(self):
        try:
            self.clear_table()
        except:
            pass
        self.is_spymaster = None
        self.is_gameover = False
        self.gen_board()
        self.gen_roles()
        self.ask_spymaster()
        # implicitly sets tables
        self.play_game()
    
    def gen_board(self):
        self.board = np.random.choice(self.words,size=(5,5),replace=False)
    
    def gen_roles(self):
        if np.random.random()>0.5:
            nr,nb = 8,9
        else:
            nr,nb = 9,8
        roles = np.array(['#e1b984']*25).reshape(self.board.shape)
        for _ in range(nr):
            while True:
                i = round(np.random.random()*24)
                if roles[round((i-i%5)/5),i%5] == '#e1b984':
                    roles[round((i-i%5)/5),i%5] = 'red'
                    break
        for _ in range(nb):
            while True:
                i = round(np.random.random()*24)
                if roles[round((i-i%5)/5),i%5] == '#e1b984':
                    roles[round((i-i%5)/5),i%5] = 'blue'
                    break
        while True:
            i = round(np.random.random()*24)
            if roles[round((i-i%5)/5),i%5] == '#e1b984':
                roles[round((i-i%5)/5),i%5] = 'black'
                break
        self.roles = roles
    
    def ask_spymaster(self):
        l = tk.Label(self.table,text='Are you the spymaster?')
        l.pack()
        y = tk.Button(self.table,text='YES',command=lambda \
                      root=self.table,v=True: self.set_spymaster(root,v))
        y.pack()
        n = tk.Button(self.table,text='NO',command=lambda \
                      root=self.table,v=False: self.set_spymaster(root,v))
        n.pack()
        self.table.mainloop()
    
    def set_spymaster(self,root,v):
        self.is_spymaster = v
        self.clear_table()
        self.set_table()
    
    def set_table(self):
        # scoreboard and options
        self.newgame = tk.Button(self.table,
                                 text='New Game',command=self.start_newgame,
                                 height=1,width=12,border=5,
                                 bg='white',fg='black',activebackground='#C0C0C0',
                                 relief='raised',cursor='target',
                                 font=self.scorefont,justify='center',anchor='n')
        self.newgame.grid(row=0,column=0)
        self.reveal = tk.Button(self.table,
                                text='Reveal Board',command=self.reveal_board,
                                height=1,width=12,border=5,
                                bg='white',fg='black',activebackground='#C0C0C0',
                                relief='raised',cursor='target',
                                font=self.scorefont,justify='center',anchor='n')
        self.reveal.grid(row=0,column=4)
        self.status = tk.Label(self.table,
                               text='REMAINING',
                               height=1,width=12,border=5,
                               bg='#C0C0C0',fg='black',
                               relief='solid',cursor='target',
                               font=self.scorefont,justify='center',anchor='n')
        self.status.grid(row=0,column=2)
        self.r_rem = np.where(self.roles.flatten()=='red')[0].shape[0]
        self.r_score = tk.Label(self.table,
                                text=str(self.r_rem),
                                height=1,width=12,border=5,
                                bg='red',fg='white',
                                relief='solid',cursor='target',
                                font=self.scorefont,justify='center',anchor='n')
        self.r_score.grid(row=0,column=1)
        self.b_rem = np.where(self.roles.flatten()=='blue')[0].shape[0]
        self.b_score = tk.Label(self.table,
                                text=str(self.b_rem),
                                height=1,width=12,border=5,
                                bg='blue',fg='white',
                                relief='solid',cursor='target',
                                font=self.scorefont,justify='center',anchor='n')
        self.b_score.grid(row=0,column=3)
        # rest of board
        self.buttons = {}
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                word = self.board[i,j]
                B = tk.Button(self.table,
                              text=word,command=lambda i=i,j=j:self.check_guess(i,j),
                              height=1,width=10,border=5,
                              bg='#f0dcc1',fg='black',activebackground='#c9b9a3',
                              relief='raised',cursor='target',
                             font=self.cardfont,justify='center',anchor='n')
                B.grid(row=i+1,column=j)
                self.buttons[5*i+j] = B
        # roles for spymaster
        if self.is_spymaster:
            self.key = Toplevel()
            self.key.title('CODENAMES: Spymaster Key')
            self.labels = {}
            for i in range(self.board.shape[0]):
                for j in range(self.board.shape[1]):
                    self.labels[5*i+j] = tk.Label(self.key,
                                                  height=2,width=4,border=3,
                                                  bg=self.roles[i,j],
                                                  relief='ridge',cursor='target'
                                                  ).grid(row=i+1,column=j)        
    
    def check_guess(self,i,j):
        color = self.roles[i,j]
        self.buttons[5*i+j]['state'] = 'disabled'
        self.buttons[5*i+j]['bg'] = color
        self.buttons[5*i+j]['fg'] = 'white'
        self.buttons[5*i+j]['relief'] = 'sunken'
        self.do_guess_logic(color)
    
    def do_guess_logic(self,color):
        if color == 'red':
            self.r_rem -= 1
        elif color == 'blue':
            self.b_rem -= 1
        self.update_scoreboard()
        if color == 'black' and not self.is_gameover:
            self.show_gameover('ASSASSIN!')
        elif self.r_rem==0 and not self.is_gameover:
            self.show_gameover('RED WINS!')
        elif self.b_rem==0 and not self.is_gameover:
            self.show_gameover('BLUE WINS!')
    
    def update_scoreboard(self):
        self.r_score['text'] = str(self.r_rem)
        self.b_score['text'] = str(self.b_rem)
    
    def show_gameover(self,message):
        self.is_gameover = True
        self.status['text'] = message
        if message == 'ASSASSIN!':
            self.status['bg'] = 'black'
            self.status['fg'] = 'white'
        elif message == 'RED WINS!':
            self.status['bg'] = 'red'
            self.status['fg'] = 'white'
        elif message == 'BLUE WINS!':
            self.status['bg'] = 'blue'
            self.status['fg'] = 'white'
    
    def reveal_board(self):
        if not self.is_gameover:
            self.status['text'] = 'REVEALED'
            self.status['bg'] = '#C0C0C0'
            self.status['fg'] = 'black'
        self.is_gameover = True
        for _,B in self.buttons.items():
            B.invoke()
        self.reveal['bg'] = '#C0C0C0'
        self.reveal['state'] = 'disabled'
        self.reveal['relief'] = 'sunken'
    
    def clear_table(self):
        for widget in self.table.winfo_children():
            widget.destroy()
    
    def play_game(self):
        self.table.mainloop()

def main():
    global game
    game = Game()

if __name__ == '__main__':
    main()