#############################################################################################################################################################

#README

#Throughout this script, i tried to realise all main functionality which should be able to be perfomed by my api.
#The most important part here is the authentication. Without any authentication mechanism, it would not be possible to access the resources of the magento REST API. 
#For the authentication i am using the bearer authentication method. By using this method, the token type i'm getting is
#an integration token. The default lifetime of this token is indefinite, until i decide to 
#revoke its manually. An admin token for example would last only for 4 hours and a customer token only for 1 hour. 
#Thus, the intergration token was perfect for my intent. But before i am able to work with my token, i have 
#to get my integration tokens. Magento generates here a consumer key, a consumer secret, an access token and an access token secret. 
#In my case i only require the access token, because of my decision using the bearer authentication method. 
#For generating my tokens, i use the backend of my magento shop. Under the point integrations, i am able to 
#display the integrations page. I am adding a new integration and name them. Under the API tab i can select, which resources my integration should be able to access.
#After my savings, i have to activate my newly-created integration. After the permission, i am retrieving my integration token. With my now received access token, 
#i am able to set up my request header, which requires the access token by using the bearer authentication method. 
#Secondary, another important role in this script are my stubs. Through my stubs, i am able to perform the main characteristics of my api. 
#This for example would be to get products, to upload products, to update and to delete products. Therefore i set up every request method by using my base url plus 
#the matching rest api endpoint. After this setup i can set up a few more functions, which let me play around with my api and let me retrieve  and work with its data. 

#During this script i resorted to a few resources:
#https://pythonhosted.org/magento/index.html
#https://github.com/Callino/python-magento2
#https://github.com/fulfilio/python-magento
#https://gist.github.com/nyov/5116258

##########################################################################################################################################################################          

import json
import os
import requests
from requests.auth import HTTPDigestAuth
import sys
from utils import handle_response 
from requests import exceptions
from requests import status_codes
from requests.api import head, request
from requests.models import Response
from requests_oauthlib import OAuth1

class MagentoAgent():
    url = 'http://217.160.195.66/index.php'
    api_path = '/rest/default/V1'
    #consumer_key = 'oujczu8j5yrz9mhmjb86z1eu8cl3on2d'
    #consumer_secret = '8615td8j5f5u7az4x0n03x8itpnz25kh'
    access_token = 'jxti0yt1kvyvaqajv8c6sxb9ixjbmxaw'
    #access_token_secret = 'b8bmasyon7eswgwl3uaxy0ejvz9xa29m'

    def __init__(self):
        self.check_connection()
        self.authenticate()

    def api_request(self, method, endpoint, headers=None, **kwargs):
        #working request:
        #curl -X GET "http://217.160.195.66/index.php/rest/default/V1/products?searchCriteria=" -H "Authorization:Bearer jxti0yt1kvyvaqajv8c6sxb9ixjbmxaw"
        _headers = {
            'Authorization':'Bearer ' + self.access_token,
            'Content-Type':'application/json',
            'Accept': 'application/json'
        }
        if headers:
            _headers.update(headers)

        return handle_response(requests.request(method, self.url + self.api_path + endpoint, headers=_headers, **kwargs))

    #by using **kwargs in my functions, it allows me to pass keyboarded variable length of arguments to my functions
    #really helpful, i you want to handle named arguments
    #**kwargs works actually exactly how *args, but instead of accepting positional arguments it accepts keyword(or named) arguments
    def api_get(self, url, **kwargs):
        return self.api_request('GET', url, **kwargs)
            
    def api_post(self, url, **kwargs):
        return self.api_request('POST', url, **kwargs)

    def api_put(self, url, **kwargs):
        return self.api_request('PUT', url, **kwargs)

    def api_delete(self, url, **kwargs):
        return self.api_request('DELETE', url, **kwargs)

    def check_connection(self):
        try:
            response = requests.get(self.url)

            #if response was successfull => no exception will be raised 
            response.raise_for_status()
        except Exception as e:
            print(f'An Error occured: {e}')
            sys.exit(1)
        else:
            print('Success!')

    #for authentication there are multiple options:
    #https://devdocs.magento.cm/guides/v2.4/get-started/authentication/gs-authentication-token.html
    #the easiest for my purpose is the integration token, since it has an unlimited lifetime and can be created in advance.
    #therefore i dont need this method for the current setup.
    #it is enough to pass the access_token as bearer token in every request
    def authenticate(self):
        return

        auth = OAuth1(
            client_key=self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret

        )
        headers = {'Content-Type':'application/json'}
        params = {'username':'','password':''}
        self.api_post('/integration/customer/token',params=params, headers=headers,auth=auth)


    def get_products(self):
        return self.api_get('/products?searchCriteria=')
      

    def get_product_byId(self):
        #fix
        return self.api_get('/product_list')

    def get_product_info(self, sku):
        #fix
        return self.api_get('product_info(sku)')

    def get_product_attribute(self, attribute_SetId, data=None):
        #fix
        #return requests.get(magento_url('//rest/default/V1/products/attribute-sets/{attributeSetId}/attributes'))
        return self.api_get('products/attribute-sets/' + attribute_SetId, json=data) 

    def upload_product(self, info):
        #success:
        ret = True
        #upload product from info
        return ret

    def delete_product(self, id):
        #success:
        ret = True
        #delete in magento + handle deletion failure
        return ret

    def put_productUpdate(self, product_sku, item_id, data=None):
        #return requests.put(magento_url('//rest/default/V1/products/{productSku}/stockItems/{itemId}'))
        return self.api_put('products/'+ product_sku, item_id, json=data)

    def get_stockItem(self,product_sku, data=None):
       #return (magento_url('//rest/default/V1/stockItems/{productSku}')
       return self.api_get('products/' + product_sku, json=data)
    #    body:

    #         {
    #         "stockItem": {
    #         "is_in_stock": true,
    #         "qty": 1
    #         }
    #         }

        #product already in magento?
        #check that over the sku

    def get_productInfo(self, product_sku, params=None):
        #return request.get(magento_url('//rest/default/V1/products/{sku}'))
        #remove or delete product 
        return self.api_get('products/' + product_sku, params=params)

    def delete_product(self, product_sku, params=None):
        #return requests.delete(magento_url('//rest/default/V1/product/{sku}'))
        return self.api_delete('products/'+ product_sku,params=params)

    def get_all_products(self,query):
        #response = testuser.search_product({'searchCriteria': ''})
        pass

    def create_product(self, data):
        # product_data = {
        #     'product':{
        #         'id': 0,
        #         'sku': 'string',
        #         'name': 'string',
        #         'attribut_set_id': 0,
        #         'price': 0,
        #         'status': 0,
        #         'visibility': 0,
        #         'type_id': 'string',
        #         'created_at': 'string',
        #         'updated_at': 'string',
        #         'weight':0
        #     }
        # }
        #response = testuser.create_product(product_data)
        pass

    #create custom field to store lexware (stock) meta data
    #necessary for the sync 
    #endpoint looks like: products/attribute-sets/{attributeSetId}/attributes

    def create_custom_attribute(self, data):
        #custom_attributes = {
        #   'attribute_code': 'string',
        #   'value': 'string'
        # }
        pass
    
    #get product
    def get_product(self, sku):
        #response = testuser.get_product('SKU')
        pass
    
    #delete product
    def delete_product(self, sku):
        #response = testuser.delete_product('SKU')
        pass

    #search product
    def search_product(self, searchCriteria):
        #response = testuser.search_product({'searchCriteria': ''})
        pass

    #get product attribute sets
    def get_product_attribute_sets(self, searchCriteria):
        #response = testuser.get_product_attribute_sets({'searchCriteria':''})
        pass 

##############################################################################################################################################################################
    #the follwoing is just a test sequence for myself
    #post/upload file 
    headers = {'content-type': 'application/json'}
    xmlfile = open('articlefile.xml', 'rb')

    r = requests.put(url, data=xmlfile, headers=headers)
    print(r.text)

    #if the call went successfully, return response code 200 => OK
    # if (r.ok):
    #     jdata = json.loads(r.content)
          #loading respoonse data into a dict variable  
    #     print("The response contains {0} properties".format(len(jdata)))
    #     print("\n")
    #     for key in jdata:
    #         print(key + " : " + jdata[key])
    #     else:
              #if the call failed, raise the error/status code with description  
    #         r.raise_for_status()

    