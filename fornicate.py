import socket
import AES
import random
import Verify
import RSA

PORT = 12000
SERVER_IP = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    client.send(bytes(msg,FORMAT))

def getConCode():
    """Prompts the Agent to enter connection code and returns said code"""
    connCode = input("Enter Connection Code - ")
    return connCode

def getAnswer(question):
    print(question)
    answer = input("Enter Answer To secret Question - ")
    return answer

def computeSessionKey(n):
	"""Computes this node's session key"""
	sessionKey = random.randint(1, n-10)
	return sessionKey

try:
    # Write Code that allows the Client to send a "100 Hello" message to the Server.
    send('100 Hello')

    # Write Code that allows the Client to receive the server's public key and a nonce (e,n and nonce).
    key = client.recv(1024).decode(FORMAT)
    x,y,z = key.split()
    e = int(x)
    n = int(y)
    nonce = z

    # Write Code that allows the Client to compute the Symmetric Key.
    symmkey = computeSessionKey(n)

    # Write Code that allows the Client to encrypt the compted session key using the server's public key.
    e_sess= RSA.RSAencrypt(int(symmkey),e,n)

    # Write Code that allows the Client to send a "103 Session Key" message and the computed session Key to the Server.
    message = "103 session key "+str(e_sess)
    send(message)

    # Write Code to set up the Agent's Symmetric Key.
    AES.keyExp(symmkey)

    # Write Code that allows the Agent's to send the nonce (encrypted with the Agent's symmetric key) to the server.
    e_nonce = str(AES.encrypt(int(nonce)))
    print('')
    send(e_nonce)

    # Write Code that allows the Client to receive the server's "200 ok" message.
    message = client.recv(1024).decode(FORMAT)
    print(message)

    # Write Code that allows the Client to send its encrypted connection code.
    conncode = str(input("Enter your connection code: "))
    if Verify.check_conn_codes(conncode)!=-1:
        e_conn = AES.encryptMessage(AES.strToASCI(conncode))
        send(e_conn)
    else: 
        client.close()
    # Write Code that allows the Client to receive the server's encrypted secret question.
    ques = client.recv(1024).decode(FORMAT)
    question = AES.decryptMessage(ques)
    print(question)

    for q in Verify.questions:
        if question == q[0]:
            realques = q
            break
    
    # Write Code that allows the Client to send its encrypted answer to the server.
    ans = str(input("Enter your answer to the question: "))
    if ans==realques[1]:
        e_ans = AES.encryptMessage(AES.strToASCI(ans))
        send(e_ans)
    else: 
        client.close()

    # Write Code that allows the Client to receive the server's encrypted welcome message.
    wel = client.recv(1024).decode(FORMAT)
    d_wel = AES.decryptMessage(wel)
    print(d_wel)

    client.close()
except Exception:
    print("Disconnected from Server")
    client.close()
# AJK782975 - Agent A
# AJK786144 - Agent B