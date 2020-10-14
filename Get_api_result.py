from requests.packages.urllib3.exceptions import InsecureRequestWarning
from json.decoder import JSONDecodeError
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt,Confirm,Console
import requests
import json
import csv
import time
import readline
import sys


### Prompts user to select the Device Platform ###
Device_Platform =  Prompt.ask("[bold][blue] Please Enter Platform Name to connect",choices=['IOS-XE','IOS-XR','NX-OS'])


### Path of RESTCONF_API_MODULES_FOR_TABLE , This file contains modules value of API Module Table# 
restconf_api_module ='/home/shebin/NETDEVOPS/Net_automation_Project/RESTCONF/Get_Request_Script/'+Device_Platform+'-RESTCONF_API_MODULES_FOR_TABLE.csv'
print(restconf_api_module)

global user_module
global module_list


module_list=[]
console = Console()
modules_table =Table(title="API module Table",show_header=True,header_style='bold magenta')

modules_table.add_column('Modules',style='yellow bold',width=32)
modules_table.add_column('Vendors',style='blue bold',width=12)
modules_table.add_column("Description",style='purple bold',width=52)
modules_table.add_column("Platform",style='bold yellow',width=8)

with open(restconf_api_module,'r') as mr:
    module_read = csv.DictReader(mr) 
    for row in module_read:
        module_name = row['Modules']   
        vendor_name = row['Vendors'] 
        Desc        = row['Description'] 
        Platform    = row['Platform'] 
        modules_table.add_row(module_name,vendor_name,Desc,Platform) 
        module_list.append(module_name)
        continue 


### Custom Autocomplete Class for completing users input ###
class AutoComplete(object):  

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches 
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options if s and s.startswith(text)]
            else:  # no text entered #
                self.matches = self.options[:]

        # return match indexed by state
        try: 
            response =  self.matches[state]

            return response

        except IndexError:
            return None

        

completer = AutoComplete(module_list)
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')

console.print(modules_table)
console.print('\n')
console.print("Press [bold][red]<TAB> <TAB>[/bold][/red] to autocomplete words",style='yellow bold')
console.print('\n')
console.print("[bold][yellow]Select your API to request Data =[/bold][/yellow]")
user_module= Prompt.ask("[bold][yellow]Select your API to request Data =[/bold][/yellow]=")  
console.print('\n')
console.print("You entered the following module->"+user_module,style='bold purple')
time.sleep(0.5)


### This function will execute the request by user and will return Results ###
def Rest_Get():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    
    #Move to the Get_Request_Script Folder and Specify the path of get_module_csv file here# 
    get_module_csv = '/home/shebin/NETDEVOPS/Net_automation_Project/RESTCONF/Get_Request_Script/'+Device_Platform+'-get_module.csv'
    print(get_module_csv)
   
    
    if "IOS-XE" in Device_Platform:
        
        hostname = Prompt.ask("[bold][purple]Please Enter your End Device Hostname or IP-Address to connect->[/bold][/purple]",
            choices=['ios-xe-mgmt.cisco.com'],default='ios-xe-mgmt.cisco.com')
        
        port_number = Prompt.ask("[bold][yellow] Please Enter Port Number",choices=['9443','443'],default='9443')
        
    
    elif "IOS-XR" in Device_Platform:
        pass
    
    elif 'NX-OS':

        hostname = Prompt.ask("[bold][purple]Please Enter Hostname or IP-Address of End Device to connect->[/bold][/purple]",
            choices=['sbx-nxos-mgmt.cisco.com'],default='sbx-nxos-mgmt.cisco.com')
        
        port_number = Prompt.ask("[bold][yellow] Please Enter Port Number",choices=['443','80'],default='443')
    
    #hostname=hostname
    #port_number=port_number
                  
    
    try:
        print("inside Try")
        with open(get_module_csv,'r') as dr:

            csv_dict_read = csv.DictReader(dr)

            for row in csv_dict_read:
            
                if row['get_module']==str(user_module):
                    api = row['get_api']
                else:
                    continue


            if "IOS-XE" in Device_Platform:

                main_url = 'https://{}:{}'.format(hostname,port_number)  
                iosxe_url   = main_url + api
                headers     = {'Accept':'application/yang-data+json','Content-Type':'application/yang-data+json'}
                credentials = {'username':"developer",'password':"C1sco12345"}

                response = requests.get(url=iosxe_url,auth=(credentials['username'],credentials['password']),verify=False,headers=headers).json()
                final_result = json.dumps(response,indent=2,sort_keys=True)
                console.print('Please Wait for the Results....',style='bold green')
                console.print('='*40)
                time.sleep(1)
                console.print(final_result,style='bold blue')
            
            elif "IOS-XR" in Device_Platform:
                pass

            elif "NX-OS" in Device_Platform:
                print("inside nxos")
                print('rest_csv',restconf_api_module)

                nxos_url = 'https://{}'.format(hostname)+str(api) 
                print(nxos_url)
                headers={'Accept':'application/json','Content-Type':'application/json'}
                credentials = {'username':'admin','password':'Admin_1234!'}
                login_body = {"aaaUser":{"attributes":{"name":credentials['username'],"pwd":credentials['password']}}}
                login_url = 'https://{}/api/mo/aaaLogin.json'.format(hostname)
                print(login_url)

                ### Login into device and getting the token back ###
                login_response = requests.post(url=login_url,data=json.dumps(login_body),verify=False,timeout=10).json()
                print(login_response)
                token = login_response['imdata'][0]['aaaLogin']['attributes']['token']
                cookies = {}
                cookies['APIC-Cookie'] = token
                print(cookies)
               # login_response = requests.post(url=login_url,data=json.dumps(login_body),verify=False,timeout=10).json()
               # print(login_response)
               # token = login_response['imdata'][0]['aaaLogin']['attributes']['token']
               # cookies = {}
               # cookies['APIC-Cookie'] = token
               # print(cookies)

                ### Getting Data for the requested models by user ###

                response_data = requests.get(url=nxos_url,cookies=cookies,timeout=10,verify=False).json()
                final_result = json.dumps(response_data,indent=2,sort_keys=True)
                console.print('Please Wait for the Results....',style='bold green')
                console.print('='*40)
                time.sleep(1)
                console.print(response_data,style='bold yellow')

                    

    except requests.exceptions.ConnectionError as ec:
        console.print("See whether you have connectivity with the end device",ec,style='bold red')
    except requests.exceptions.HTTPError as eh:
        console.print("Bad Request specify correct Requests",eh,style='bold red')
        console.print("Check  whether you correctly specified  http/https or else Check Authentication parameters",style='bold yellow')
        console.print(eh.response.text,style='bold green')
    except requests.exceptions.InvalidURL as eiu:
        console.print('URL specified is not a valid one',eiu,style='bold red')
    except requests.exceptions.URLRequired as eur:
        console.print("Please specify a URL for request",eur,style='bold red')
    except requests.exceptions.InvalidSchema as esc:
        console.print("Please use either 'HTTP' or 'HTTPS'",esc,style='bold red')
    except requests.exceptions.ContentDecodingError as edc:
        console.print('Please specify correct Encodings',edc,style='bold red')
    except requests.exceptions.RequestException as erq:
        console.print("Sorry not able to rectify the issue,Please ",erq,style='bold red')
    except KeyboardInterrupt as ki:
        console.print("Sorry cannot Execute further..Your Execution stopped due to keyboard interupt",ki,style='bold red')
    except ValueError:
        console.print('No content available for this request',style='bold red')
        console.print("Device not able to return anything,since no configuration found on the device for requested API",style='bold red')
    except NameError:
        console.print("The API you entered not listed in our database",style='bold red')
    except Exception:
        console.print("Sorry some other issues occured..Please look into it")
    


        
    finally:
        console.print('='*40)
        console.print("Execution completed...",style='bold yellow')
        console.print('\n')
        time.sleep(1)
        console.print("Exiting the Programme....",style='green')
    
    

Rest_Get()
