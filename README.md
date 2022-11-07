# UTA_CSE_5344_001_PROJECT

## Authors:
Preetham Karanth Kota</br>
pxk6418@mavs.uta.edu</br>
1002076418</br>

## System Requirements:
_***Linux OS:***</br>
Developed and tested the software on Ubunut 22.04 LTS. Any linux distribution should do just fine with
Python 3.10_

## Contents of the PROJECT:

### Features Involve as follows:
1. Will be able to run the server with the given port number default port number would be 8080
2. Will be able to see the said file contents on any web browser which could handle multiple request
3. The server would return Error Codes "200", "400" & "404" error codes for the web client
4. The server would return Error codes "200", "400" & "404" error codes for the client based on terminal displayed on webpage
5. When used via client via terminal the code would also print the RTT

**How to Use:**</br>
1. Open any Linux terminal and run the command "python3 server_side_code.py" or " <port_num>python3 server_side_code.py <port_num>" to get the server running </br>
2. Then type "http://localhost:<port_num>/<file_at_server.txt>" (Eg: http://localhost:8080/text.txt) You could use to get the corresponding results</br>
3. Open any Linux terminal and run the command "python3 client_side_code.py" or " <port_num>python3 9client_side_code.py <port_num>" to get the client running</br>
4. As mentioned in [3] this will get client running at terminal.Once entered please ENTER the method (Eg: GET) and the file name (Eg: text.txt)</br>
5. After entering the method to be used and the file name the server would return the said files with accesss codes which will be displayed in the webbrowser </br>
6. It will also print the RTT at client end at the terminal after the steps [5] </br>


