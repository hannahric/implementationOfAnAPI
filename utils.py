from datetime import date
import requests
from requests import status_codes
from requests import exceptions
from requests.api import head, post, request
from requests.models import Response

#Exception Setup
#Handle error exceptions and raise them later, if needed. 
#The used reference/source: https://devdocs.magento.com/guides/v2.4/get-started/gs-web-api-response.html
#Another used reference: https://www.nylas.com/blog/use-python-requests-module-rest-apis/

# base error = exception class
class BaseError(Exception):
    pass
# any unknown error is caught through this exception
class UnknownError(BaseError):
    pass
#400 bad request => may missing required parameter or invalid data or something 
class BadRequestError(BaseError):
    pass
#401 unauthorized => caller was not authorized to perform the request
class UnauthorizedError(BaseError):
    pass
#403 forbidden => access denied
class ForbiddenError(BaseError):
    pass
#404 not found => pointed source not found 
class NotFoundError(BaseError):
    pass
#405 not allowed => request method not supported 
class NotAllowedError(BaseError):
    pass
#406 not acceptable => only capable of generating content that is not acceptable according to the accept headers sent in the request
class NotAcceptableError(BaseError):
    pass
#500 system error => network error or something comparable
class SystemError(BaseError):
    pass

#return response for request + handle response 
#it may helps to find any possible error source by receiving its cause/ by receiving a feedback

def handle_response(response):
    status_code = response.status_code
    if 'application/json' in response.headers['Content-Type']:
        r = response.json()
    else:
        r = response.text

    if status_code in (200):
        return r
    elif status_code == 204:
        return None
    elif status_code == 400:
        raise BadRequestError(r)
    elif status_code == 401:
        raise UnauthorizedError(r)
    elif status_code == 403:
        raise ForbiddenError(r)
    elif status_code == 404:
        raise NotFoundError(r)
    elif status_code == 405:
        raise NotAllowedError(r)
    elif status_code == 406:
        raise NotAcceptableError(r)
    elif status_code == 500:
        raise SystemError(r)
    else:
        raise exceptions.UnknownError(r)

#######################################################################################################################
#Setup of the product class.
#utility
#possible to grab value on the position 'xy', may override value?


class Product:
    attributes = {}

    def __getitem__(self, key):
        return self.attributes[key]

    def __setitem__(self,key,value):
        self.attributes[key] = value

    def __repr__(self):
        return str(self.attributes)

    #retrieve product list by filters
    def __getlist__(self, filters=None):
        #filters =>dictionary of filters 
        #format: 
            #{<attribute>:{<operator>:value>}}
        return self.attributes('product.list', [filters])

    #retrieve product data 
    def __getinfo__(self, product, attributes=None, identifierType=None):
        #product => id or sku of the product 
        #attributes => list of fields required 
        #identifierType => defines wether the product or sku value is passed in the 'product' parameter 
        return self.attributes('product.info', [product, attributes, identifierType])

    #create new product and return its id
    def __create__(self, product_type, sku, data):
        #product_type => string type of the product
        #sku => sku of the product
        #data => dictionary of data
        #the return value is gonna be an 'int'
        return int(self.attributes('product.create', [product_type, sku, data]))

    #update product information
    def __update__(self, product, data, identifierType=None):
        #product => id or sku of the product
        #data => dictionary of attributes to update
        #identifierType => defines wether the product or sku value is passed in the 'product' parameter 
        #the return value is gonna be a boolean
        return bool(self.attributes('product.update', product, data, identifierType))

    #by using a multiple call function for updating my inventory, i would make my call faster 
    #my expected argument is a list of product pairs and data dictionarys
    def __updatemultiple__(self, product_data_pairs):
        return self.multiCall([
            [
                'inventory.stockItem.update',
                product_data_pair
            ]
            for product_data_pair in product_data_pairs
            ])

    #delete a product
    def __delete__(self, product, identifierType=None):
        #product => id or sku of the product
        #identifierType => defines wether the product or sku value is passed in the 'product' parameter
        #the return value is gonna be a boolean 
        return bool(self.attributes('product.delete', [product, identifierType]))


    
#todo: add methods to compare with other product
#e.g. which one has the latest change ? 
#dates + timestamps are very important !

    #class: 
    # datetime = superclass for most of the date and time librarys
        #includes: date, time, datetime and timedelta
    #another posibility could be dateutil => it has extended datetime functionality, especially string parsing and delta calculation
