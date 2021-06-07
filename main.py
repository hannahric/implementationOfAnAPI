import requests
import json
from requests import exceptions
from magentoAgent import MagentoAgent
from lexwareAgent import LexwareAgent
import sys
from sync import Syncer



#add trigger for this script
#manual execution
#cronjob (execute in interval or on specific time/date)
#webhooks or db trigger (magento or lexware can trigger execution on event)


def main(args):
    #i have to make sure, that this script only runs once on the current machine (pid file)
    #use args

    try: 
        #setup connections
        ma = MagentoAgent()
        ma.check_connection()

        le = LexwareAgent()

        #create syncer object and call the sync function to sync lexware and magento 
        Syncer(ma, le).sync()

    #CTRL+c to quit application
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print('Exception'+ str(e))
    finally:
        #cleanup stuff here 
        #e.g. kill ma
        pass
    
      
#check if files comes via commandline/ is called via commandline
if __name__ == '__main__':
    #run entry point with cli arguments
    main(sys.argv[1:])



response = requests.get('http://217.160.195.66')
#should return: <Response [200]> for success
print(response.status_code)  
#return raw bytes of the data payload 
#response.content()
#return string representation of the data payload
#response.text()
#returns JSON format
#print(response.json()) 



