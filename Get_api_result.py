from requests.packages.urllib3.exceptions import InsecureRequestWarning
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import requests
import json
import csv
import time
import readline


console = Console()
module_table =Table(title="API module Table")
module_table.add_column('Modules',style='yellow bold')
module_table.add_column('Vendors',style='blue bold')
module_table.add_column("Description",style='purple bold')


global user_module

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

        

completer = AutoComplete(["get_interfaces","get_eigrp","get_cdp","get_ospf"])
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')

module_table.add_row('get_ospf','Cisco',"Gets configuration of OSPF")
module_table.add_row('get_interfaces','IETF/Open','Gets all interfaces details')
console.print(module_table)
console.print('\n')
console.print("Press [bold][red]<TAB>[/bold][/red] to autocomplete words",style='yellow bold')
console.print('\n')
user_module= input("Please Enter the API module you want to retrieve =>")
console.print("You entered the following->"+user_module,style='bold green')


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
        console.print('='*40)
        console.print(final_result,style='bold blue')
    except NameError as nr:
        console.print("The API you entered not listed in our database",style='bold red')
    
    finally:
        console.print('='*40)
        console.print("Execution completed...",style='bold yellow')
        console.print('\n')
        time.sleep(1)
        console.print("Exiting the Programme....",style='green')
    
    

Rest_Get()