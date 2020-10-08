from requests.packages.urllib3.exceptions import InsecureRequestWarning
from json.decoder import JSONDecodeError
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import requests
import json
import csv
import time
import readline




restconf_api_module = '/home/shebin/NETDEVOPS/Net_automation_Project/RESTCONF/Get_Request_Script/RESTCONF_API_MODULES_FOR_TABLE.csv'

global user_module
global module_list


module_list=[]
console = Console()
module_table =Table(title="API module Table",show_header=True,header_style='bold magenta',show_footer=True)

module_table.add_column('Modules',style='yellow bold',width=32)
module_table.add_column('Vendors',style='blue bold',width=12)
module_table.add_column("Description",style='purple bold',width=52)
module_table.add_column("Platform",style='bold yellow',width=8)

with open(restconf_api_module,'r') as mr:
    module_read = csv.DictReader(mr) 
    for row in module_read:
        module_name = row['Modules']   
        vendor_name = row['Vendors'] 
        Desc        = row['Description'] 
        Platform    = row['Platform'] 
        module_table.add_row(module_name,vendor_name,Desc,Platform) 
        #module_list.append(module_name) 




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

module_table.add_row('get_ospf','Cisco',"Gets configuration of OSPF")
module_table.add_row('get_interfaces','IETF/Open','Gets all interfaces details')
console.print(module_table)
console.print('\n')
console.print("Press [bold][red]<TAB>[/bold][/red] to autocomplete words",style='yellow bold')
console.print('\n')
user_module= input("Please Enter the API module you want to retrieve =>")
console.print('\n')
console.print("You entered the following module->"+user_module,style='bold purple')
time.sleep(0.5)


### This function will execute the request by user and will return Results ###
def Rest_Get():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    get_module_csv = '/home/shebin/NETDEVOPS/Net_automation_Project/RESTCONF/Get_Request_Script/get_module.csv'

    main_url = 'https://ios-xe-mgmt-latest.cisco.com:9443/restconf/'

    headers={'Accept':'application/yang-data+json','Content-Type':'application/yang-data+json'}

    
    try:
        with open(get_module_csv,'r') as dr:

            csv_dict_read = csv.DictReader(dr)

            for row in csv_dict_read:
            
                if row['get_module']==str(user_module):
                    api = row['get_api']
                else:
                    continue

                url = main_url + api
                    
        response = requests.get(url=url,auth=("developer","C1sco12345"),verify=False,headers=headers).json()
        final_result = json.dumps(response,indent=2,sort_keys=True)
        console.print('Please Wait for the Results....',style='bold green')
        console.print('='*40)
        time.sleep(1)
        console.print(final_result,style='bold blue')
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