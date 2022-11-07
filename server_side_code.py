"""
* Author 1:
* 	Preetham Karanth Kota 
*	pxk6418@mavs.uta.edu
*	1002076418
"""
import os
import re
import sys
import socket 
import threading
from datetime import datetime
from socket import AF_INET, SOCK_STREAM

#Creating threading lock object to create threading lock
RCV_BUFFER_SIZE             = 1000 	    			#1000 Bytes
port                        = [8080,0]         		#Creating a port number for our communication
host_name                   = "localhost"     		#socket.gethostname() #host name required to bind the port and host 
CTRL                        = "\r\n"

def Send_all_files(client_socket):
    
	now = datetime.now() # current date and time
	data = "HTTP/1.1 200 OK"+CTRL
	data += "Server: Apache/2.2.14 (WSL/Ubuntu)"+CTRL
	data += "Date: "+ now.strftime("%m/%d/%Y, %H:%M:%S")+CTRL
	data += "Content-Type: text/html; charset=utf-8"+CTRL
	data += "Connection: Closed" + CTRL + "IP Address: localhost" + CTRL
	data += "Protocol: TCP"+CTRL
	data += "Socket Type: Connection" + CTRL
	data += "Socket Family: AF_INET "+CTRL  
	data += CTRL
	data += CTRL
	data += "<html><title>CSE 5344 Project 4</title><body> <h1>Welcome to CSE 5344 Project 4</h1>"+CTRL+CTRL
	list_of_files = os.listdir()
	if (len(list_of_files)!=0 ):
		#If there are files in current directory display it on the webpage
		#current_directory_path = os.getcwdb().decode()
		data += "<h2>List of Files present on the server Directory: Search for One of these Files</h2><br>"+CTRL+CTRL
		for file_name in list_of_files:
			data += "<li><a href='localhost:"+str(port[0])+"/"+file_name+"'>"+file_name+"</a></li><br>"+CTRL
		data += " </ul>"
  
	data += "</body></html>"
	print("[******** WEB RESPONSE ********]\n\n",data)
	print("[******** WEB RESP END ********]\n\n")
	client_socket.sendall(data.encode())
	client_socket.close()

def write_the_contents_of_the_file_to_web_page(file_name_requested,client_socket):
    		
    #File present Construct HTTP 200 OK message and send it to the browser and client	
	print("[*] The File ",file_name_requested," is Present!!\n\n")
	now = datetime.now() # current date and time
	data = "HTTP/1.1 200 OK"+CTRL
	data += "Server: Apache/2.2.14 (WSL/Ubuntu)"+CTRL
	data += "Date: "+ now.strftime("%m/%d/%Y, %H:%M:%S")+CTRL
	data += "Content-Type: text/html; charset=utf-8"+CTRL
	data += "Connection: Closed" + CTRL + "IP Address: localhost" + CTRL
	data += "Protocol: TCP"+CTRL
	data += "Socket Type: Connection" + CTRL
	data += "Socket Family: AF_INET "+CTRL  
	data += CTRL
	data += "<html><title>CSE 5344 Project 4</title><body> <h1>Welcome to CSE 5344 Project 4</h1>"+CTRL+CTRL
	file_pointer = open(file_name_requested, "r")
	data += "<h2>Contents of the File : "+file_name_requested+"</h2>"
	for line in file_pointer:
		data += "<p>"+line+"</p><br>"
	data += "</body></html>"
	print("[******** WEB RESPONSE ********]\n\n",data)
	print("[******** WEB RESP END ********]\n\n")
	client_socket.sendall(data.encode())
	client_socket.close()
 
def send_404_file_not_found_request(client_socket):
    #If the said/requested file is not present then send 404 error to the client
	now = datetime.now() # current date and time
	data = "HTTP/1.0 404 NOT FOUND"+CTRL
	data += "Server: Apache/2.2.14 (WSL/Ubuntu)"+CTRL
	data += "Date: "+ now.strftime("%m/%d/%Y, %H:%M:%S")+CTRL
	data += "Content-type:NOT FOUND; charset=utf-8"+CTRL
	data += "Connection: Closed" + CTRL + "IP Address: localhost" + CTRL
	data += "Protocol: TCP"+CTRL
	data += "Socket Type: Connection" + CTRL
	data += "Socket Family: AF_INET "+CTRL  
	data += CTRL
	data += "<html><title>CSE 5344 Project 4</title><body> <h1>404 ERROR FILE NOT FOUND!!!</h1>"+CTRL+CTRL
	data += "</body></html>"
 
	print("[******** WEB RESPONSE ********]\n\n",data)
	print("[******** WEB RESP END ********]\n\n")
	
	client_socket.sendall(data.encode())
	client_socket.close()

def send_400_bad_reques(client_socket):
    print("\n\n[*] Sending BAD request as not GET Method")
    now = datetime.now() # current date and time
    data = "HTTP/1.0 400 BAD REQUEST"+CTRL
    data += "Server: Apache/2.2.14 (WSL/Ubuntu)"+CTRL
    data += "Date: "+ now.strftime("%m/%d/%Y, %H:%M:%S")+CTRL
    data += "Content-type:NOT FOUND; charset=utf-8"+CTRL
    data += "Connection: Closed" + CTRL + "IP Address: localhost" + CTRL
    data += "Protocol: TCP"+CTRL
    data += "Socket Type: Connection" + CTRL
    data += "Socket Family: AF_INET "+CTRL  
    data += CTRL
    data += "<html><title>CSE 5344 Project 4</title><body> <h1>400 ERROR BAD REQUEST!!!</h1>"+CTRL+CTRL
    data += "</body></html>"
    print("[******** WEB RESPONSE ********]\n\n",data)
    print("[******** WEB RESP END ********]\n\n")
    client_socket.sendall(data.encode())
    client_socket.close()
    
     
def send_file_to_client(client_socket,http_pieces,file_info):
    
    #Check if we are getting proper GET request, if not GET method send 400 bad request
	pattern_get = re.search("GET\s",http_pieces[0])
	if (pattern_get == None ):
		send_400_bad_reques(client_socket)
		return

	pattern_file = re.search("\s.*.\sH",http_pieces[0])

  
	if (pattern_file):
     	
		#Get the file name i.e from the list remove extra space infront,'/' and behind hence the below logic
		file_name_requested = pattern_file[0][2:-1].strip()
			#Generally web browser below request to get the icon but printing this icon, hence avoiding the request
		if file_name_requested == "favicon.ico":	
			return

		print("[******** WEB REQUEST ********]\n\n", file_info)
		print("[******** WEB REQ END ********]\n\n")
  
		#If the requested file is present in the server side folder then send OK and display in the web Browser
		if os.path.isfile(file_name_requested):
			write_the_contents_of_the_file_to_web_page(file_name_requested,client_socket)
		else:
			root_dir = pattern_file[0][1:-1].strip()
			#If no file is provided then give the user list of files present
			if root_dir == "/":
				Send_all_files(client_socket)

			#the provided file name is not correct hence send 404 error message
			elif (root_dir != "favicon.ico" ):
				print("\n\n[*] Requested File not Present at the server hence sending the ERROR message\n\n")
				send_404_file_not_found_request(client_socket)

def create_server_listen():

	#Create a socket object
	socket_at_server = socket.socket(AF_INET, SOCK_STREAM)
 
	#Check if the argument has port number if not then use the port 8080
	if (len(sys.argv) >= 2):
		socket_at_server.bind((host_name,int(sys.argv[1])))
		port[0]= int(sys.argv[1])
		print("[*] Listening as: ",host_name," Port: ",port[0])
	else:
		socket_at_server.bind((host_name,port[0]))
		print("[*] Listening as: ",host_name," Port: ",port[0])
  
	socket_at_server.listen(100)
 
	#Accepting the connnection at server end
	while True:
		#Accepting the connnection at server end, Open the client socket at server end
		client_sock , client_address = socket_at_server.accept()
		file_info = client_sock.recv(RCV_BUFFER_SIZE).decode()

		#Split the http request with the delimiter /n
		http_pieces = file_info.split("\n")
  
		#Creating Thread to handle multiple requests
		thread1 = threading.Thread(target = send_file_to_client, args = (client_sock,http_pieces,file_info,))
		thread1.start()

if __name__ == "__main__":
	print("\n[**** STARTING WEB SERVER ****]\n")
	create_server_listen()
