import socket
import threading
import time
from tkinter import *


def loading_animation():
    animation = "|/-\\"
    idx = 0
    while idx<=20:
        print("Connecting with the server...",animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)

# nickname=input("Enter your name to join the quiz : ")
# time.sleep(1)
# loading_animation()
# time.sleep(2)



client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address="127.0.0.1"
port=8000

client.connect((ip_address,port))
print("Connected..")

class GUI:

    def write(self):
        while True:
            time.sleep(10)
            msg=input("\nEnter your answer: \n\n")
            client.send(msg.encode("utf-8"))

    def recv(self,nickname):
            while True:
                try:
                    msg=client.recv(2048).decode("utf-8")
                    if msg=="nickname":
                        client.send(nickname.encode("utf-8"))
                    else:
                        print(msg)
                except:
                    print("an error occured!")
                    client.close()

    def goAhead(self,nickname):
        self.login.destroy()
        self.nickname=nickname
        threading.Thread(target=self.recv,args=(nickname)).start()
        threading.Thread(target=self.write).start()
    

    def __init__(self):

        self.PRIMARY_FG='white'
        self.PRIMARY_BG="#141414"
        self.HEADING_FONT="regular 20"
        self.WIDTH=400
        self.HEIGHT=400

        self.window=Tk()
        self.window.maxsize(width=self.WIDTH,height=self.HEIGHT)
        self.window.minsize(width=self.WIDTH,height=self.HEIGHT)
        self.window.iconbitmap("login.ico")
        self.window.withdraw()

        self.login=Toplevel()
        self.login.iconbitmap("login.ico")
        self.login.title("Login")
        self.login.maxsize(width=self.WIDTH,height=self.HEIGHT)
        self.login.minsize(width=self.WIDTH,height=self.HEIGHT)
        self.login.configure(width=self.WIDTH,height=self.HEIGHT,bg=self.PRIMARY_BG)

        self.heading=Label(self.login,text="Login To Continue",fg=self.PRIMARY_FG,bg=self.PRIMARY_BG,font=self.HEADING_FONT)
        self.heading.place(x=100,y=20)
        self.info_msg=Label(self.login,text="Enter single alphabet",fg=self.PRIMARY_FG,bg=self.PRIMARY_BG)
        self.info_msg.place(x=130,y=60)

        self.nickname_label=Label(self.login,text="Nickname",fg=self.PRIMARY_FG,bg=self.PRIMARY_BG,font="regular 20")
        self.nickname_label.place(x=140,y=100)
        self.nickname_entry=Entry(self.login,fg=self.PRIMARY_BG,bg=self.PRIMARY_FG,font="regular 15",width=self.WIDTH)
        self.nickname_entry.place(y=140)

        self.loginBtn=Button(self.login,text="Login",font="regular 10",width=10,command=lambda:self.goAhead(str(self.nickname_entry.get())))
        self.loginBtn.place(x=155,y=200)

        self.window.mainloop()
        



root=GUI()

# def recv():
#     while True:
#         try:
#             msg=client.recv(2048).decode("utf-8")
#             if msg=="nickname":
#                 client.send(nickname.encode("utf-8"))
#             else:
#                 print(msg)
#         except:
#             print("an error occured!")
#             client.close()

def write():
    while True:
        time.sleep(10)
        msg=input("\nEnter your answer: \n\n")
        client.send(msg.encode("utf-8"))



# recv_thread=threading.Thread(target=recv)
# recv_thread.start()

# write_thread=threading.Thread(target=write)
# write_thread.start()