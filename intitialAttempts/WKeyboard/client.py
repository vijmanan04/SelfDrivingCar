import socket
import drive


host = "000.000.0.000" #ip of computer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #set instance of socket
s.connect((host, xxxx)) #connect to computer using port xxx

msg = s.recv(1024) #recieve data in bits of 1024
print(msg.decode("utf-8")) #print data and decode as utf-8

if __name__ == "__main__":
    drive.main()  #run main function in drive
