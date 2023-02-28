import socket
import random
import threading
import time

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip_address="127.0.0.1"
port=8000

server.bind((ip_address,port))
server.listen()

clients=[]
nicknames=[]

print("[STARTED] server started successfully...")


questions={
    "\nWho developed Python Programming Language?\na) Wick van Rossum\nb) Rasmus Lerdorf\nc) Guido van Rossum\nd) Niene Stom":"c",
    "\nWhich type of Programming does Python support?\na) object-oriented programming\nb) structured programming\nc) functional programming\nd) all of the mentioned":"d",
    "\nIs Python case sensitive when dealing with identifiers?\na) no\nb) yes\nc) machine dependent\nd) none of the mentioned":"b",
    "\nWhich of the following is the correct extension of the Python file?\na) .python\nb) .pl\nc) .py\nd) .p":"c",
    "\nIs Python code compiled or interpreted?\na) Python code is both compiled and interpreted\nb) Python code is neither compiled nor interpreted\nc) Python code is only compiled\nd) Python code is only interpreted":"a",
    "\nAll keywords in Python are in _________\na) Capitalized\nb) lower case\nc) UPPER CASE\nd) None of the mentioned":"d",
    "\nWhat will be the value of the following Python expression? 4 + 3 % 5\na) 7\nb) 2\nc) 4\nd) 1":"a",
    "\nWhich of the following is used to define a block of code in Python language?\na) Indentation\nb) Key\nc) Brackets\nd) All of the mentioned":"a",
    "\nWhich keyword is used for function in Python language?\na) Function\nb) def\nc) Fun\nd) Define":"b",
    "\nWhich of the following character is used to give single-line comments in Python?\na) //\nb) #\nc) !\nd) /*":"b",
}

def get_random_question_answer(conn,nickname):

    # generating a random question and sending it
    # getting the list of all keys in question dict
    list_of_questions=list(questions.keys())

    # generating a random number
    random_index=random.randint(0,len(questions)-1)

    # generating a random question and sending it
    random_question=list_of_questions[random_index]
    conn.send(random_question.encode("utf-8"))

    # storing the actual answer
    actual_answer=questions[random_question]

    # returning variables
    return actual_answer,random_question

def client_thread(conn,nickname):
    player_score=0
    intro="\nWelcome to this quiz game!\nYou will receive a question. The answer to that question should be one of a ,b ,c ,d\nGood Luck..!"
    conn.send(intro.encode("utf-8"))
    time.sleep(3)
    conn.send("\nLoading your First Question🔃. Be Ready!".encode("utf-8"))
    time.sleep(4)
    actual_answer,random_question=get_random_question_answer(conn,nickname)

    while True:
        try:
            message=conn.recv(2048).decode("utf-8")
            if message:
                if message.lower()==actual_answer:
                    player_score+=1
                    conn.send(f"Correct answer\nYour score : {player_score}".encode("utf-8"))
                    time.sleep(3)
                    conn.send("Loading next Question🔃".encode("utf-8"))
                    time.sleep(3)
                else:
                    conn.send("Oops! Wrong answer...attempt carefully ☹️".encode("utf-8"))
                    time.sleep(3)
                    conn.send("Loading next Question🔃".encode("utf-8"))
                    time.sleep(3)

                remove_question(random_question)
                actual_answer,random_question=get_random_question_answer(conn,nickname)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue
    
def remove_question(already_asked_ques):
    del questions[already_asked_ques]


def remove(conn):
    if conn in clients:
        clients.remove(conn)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)


while True:
    conn,addr=server.accept()
    clients.append(addr[0])
    conn.send("nickname".encode("utf-8"))
    nickname=conn.recv(2048).decode("utf-8")
    nicknames.append(nickname)

    print(f"{nickname} joined")

    threading.Thread(target=client_thread,args=(conn,nickname)).start()