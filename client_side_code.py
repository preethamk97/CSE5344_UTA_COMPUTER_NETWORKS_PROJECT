"""
* Author 1:
* 	Preetham Karanth Kota 
*	pxk6418@mavs.uta.edu
*	1002076418
"""
import sys
import socket 
import webbrowser
from datetime import datetime

SEND_BUFFER_SIZE          = 1000;                #1000 Bytes
port                        = [8080,0]         		#Creating a port number for our communication
host_name                   = "localhost"     		#socket.gethostname() #host name required to bind the port and host 
CTRL                        = "\r\n"

def get_file_from_the_server():
	# Create a socket object
	socket_at_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	print("[*] Connecting to Server: ",host_name," Port: ",port[0])
	socket_at_client.connect(("localhost", port[0]))
 
	#Take in the file name and the method to be used
	request_type = input("[*] Enter the Request type (Eg: GET/POST): ")
	file_to_download = input("[*] Enter the File name(Eg: text.txt): ")
 
	#Prepare the HTTP request message 
	data = request_type+" /" + file_to_download + " HTTP/1.1"+CTRL
	data += "Host: "+host_name + ":"+str(port[0])+CTRL
	data += "Date: "+ datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+CTRL
	data += "Connection: keep-alive"+CTRL
	data += "User-Agent: WSL/UBUNTU Terminal"
	
	Operation = data.encode()

	#Calculate time before sending Request to Server
	time_now = datetime.now()
	print("[******** WEB REQUEST ********]\n\n",data)
	print("\n\n[******** WEB REQ END ********]\n\n")
 
	#Send Request to server
	socket_at_client.send(Operation)

	#Recieve request from the server
	file_info = socket_at_client.recv(SEND_BUFFER_SIZE).decode()
 
	#Print the recieved HTTP data
	print("[******** WEB RESPONSE ********]\n\n",file_info)
	print("\n[******** WEB RESP END********]\n\n")
 
	#Record the time when the rsp was recieved
	time_after_rcv = datetime.now()
 
	#Print the RTT for the request sent
	print("[*] Round Trip Time (RTT): ", (time_after_rcv-time_now))
	
	#Splitting the request based on the delimiter
	http_pieces = file_info.split(CTRL)

	#The data part of the request during success part would be present at the end of the req.
	required_part = 10
	file_pointer = open("file_from_server.html","w")
 
	#Write the body of the recieved rsp to html file
	while (required_part < len(http_pieces)):
		if (file_pointer):
			file_pointer.write(http_pieces[required_part])
		required_part += 1

	file_pointer.close()

	#Run the html file using web browser and display it
	webbrowser.open_new_tab("file_from_server.html")
	socket_at_client.close()

def send_request_to_server():
    
    #Check if the argument has port number if not then use the default port 8080
	if (len(sys.argv) >= 2):
		port[0]= int(sys.argv[1])
		print("[*] Communication details at CLIENT: ",host_name," Port: ",port[0])
	else:
		print("[*] Communication details at CLIENT: ",host_name," Port: ",port[0])
  
	get_file_from_the_server()


if __name__ == "__main__":
	print("\n[****] WEB CLIENT [****]\n")
	send_request_to_server()
