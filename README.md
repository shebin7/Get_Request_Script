[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/shebin7/Get_Request_Script)


## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)         
* [Libraries](#libraries)
* [Setup](#setup)
* [Other Informations](#other-informations)

## General info
This project is based on REST API to request information from Network Device,it will list all the available API modules,
User can select the module and can send request to the end device which will return the response in JSON format,
An autocomplete feature is also added to make the request module easily accessible. 
Below snap shows you results from  IOS-XE and NX-OS Platforms.


* IOS-XE
![alt text](https://github.com/shebin7/Get_Request_Script/blob/master/API_REQUESTS_IOS-XE.gif)


* NX-OS
![alt text](https://github.com/shebin7/Get_Request_Script/blob/master/API_REQUESTS_NX-OS.gif)


	
## Technologies
Project is created with:
* Python 3.6.9

Network Device from Cisco Sandbox
* [Cisco IOS-XE Sandbox](https://developer.cisco.com/site/sandbox/)
* [Cicso NX-OS Sandbox](https://developer.cisco.com/site/sandbox/)
* [Ciso IOS-XR Sandbox](https://developer.cisco.com/site/sandbox/)


## Libraries
 * [Rich](https://rich.readthedocs.io/en/latest/)

 * [Requests](https://requests.readthedocs.io/en/master/)

 * [readline](https://docs.python.org/3/library/readline.html)

	
## Setup
To run this project, clone this to your local Folder using 'git clone'

```
$ git clone https://github.com/shebin7/Get_Request_Script
```
Then run it from IDE or from Terminal 
```
$ python3 Get_api_result.py
```

# Other Informations
This project does not support IOS-XR modules for now since it is not tested , also more NX-OS and IOS-XE modules will be added in future.