########################################################################################################################################################

#README

#for syncing with lexware there are multiple options.
#first option would be, to load all currently available products into the memory and start the sync or a simple request to the source ofr every comparison.
#this agent support multiple methods to get the lexware data. 
#if the data needs to be parsed from a file, i prefer to parse the whole file and load all its products into the memory.
#this indeed requires more more memory but in exchange less cpu time.
#if the database backend is used, it may be preferable to make a request for every comparison. 
# 
#the following document describes the different xml parsing options in python:
#https://docs.python.org/3/library/xml.html?highlight=xml#module-xml
# 
#after i read this, i decided to use the ElementTree API, because its the easiest option and i mainly need to parse on a basic basis.
#down under you can find more documentation for this specific API:
#https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
#
#the expected input has the following format:
#
#<?xml version="1.0" encoding="ISO-8859-15"?>
# <Data xmlns:dt="urn:schemas-microsoft-com:datatypes" xml:space="preserve" 
# Title="Artikelliste">
#     <Description>
#         <Title dt:dt="string">Artikelliste</Title>
#         <FontName dt:dt="string">Arial</FontName>
#         <FontSize dt:dt="i4">8</FontSize>
#         <Hatched dt:dt="i4">1</Hatched>
#         <ColorBkGnd1 dt:dt="i4">16777215</ColorBkGnd1>
#         <ColorText1 dt:dt="i4">0</ColorText1>
#         <ColorBkGnd2 dt:dt="i4">16184050</ColorBkGnd2>
#         <ColorText2 dt:dt="i4">0</ColorText2>
#     </Description>
#     <Fields>
#         <Field dt:dt="string" Title="Artikelnr." Align="Left" Width="9.53" Name="Col1"/>
#         <Field dt:dt="string" Title="I" Align="Center" Width="1.91" Name="Col2"/>
#         <Field dt:dt="string" Title="Kurztext" Align="Left" Width="60.68" Name="Col3"/>
#         <Field dt:dt="string" Title="Matchcode" Align="Left" Width="8.18" Name="Col4"/>
#         <Field dt:dt="r8" Title="Bestand" Align="Right" Width="9.53" Name="Col5"/>
#         <Field dt:dt="string" Title="Einheit" Align="Left" Width="5.08" Name="Col6"/>
#         <Field dt:dt="r8" Title="Preis 1" Align="Right" Width="5.08" Name="Col7"/>
#     </Fields>
#     <Rows>
#         <Row>
#             <Col1 dt:dt="string">101311</Col1>
#             <Col2 dt:dt="string">[X]</Col2>
#             <Col3 dt:dt="string">MK-Alkoline 10-Ltr.</Col3>
#             <Col4 dt:dt="string">101311</Col4>
#             <Col5 dt:dt="r8">73</Col5>
#             <Col6 dt:dt="string">Kan.</Col6>
#             <Col7 dt:dt="r8">22.3</Col7>
#         </Row>
#     </Rows>
# </Data>

#i was interested in the output down below:
#----PRODUCT----
#sku: 101311
#product_name: MK-Alkoline 10-Ltr.
#matchcode: 101311
#type: Kan.
#price: 22.3

#from this data i then created a product python object which helps with abstracting the data model i used for the sync.

#####################################################################################################################################################

import xml.etree.ElementTree as ET 
from utils import Product 

#add lexware xml agent and lexware db agent => as child classes
class LexwareAgent():

    #maybe move to main and make cli configurable 
    #url = ""
    #user = ""
    #password = ""
    import_path = "./articlefile.xml"
    #use file else network backend
    file_import = True

    lc = None

    products = []

    def __init__(self):
        if self.file_import:
            self.parse_products(self.import_path)
            pass
        else:
            #first: set up connection
            #second: test the connection
            #third:
            #self.lc = lexwareConnection()
            pass
    
    def parse_products(self, path):
        root = ET.parse(path).getroot()
        fields = root.find('Fields')
        rows = root.find('Rows')

        #now map the known field between magento and lexware
        #thus requires a change on scheme changes
        #have to add more fields => latest change? date? date of manufacture? 
        product_field_mapping = {
            'sku':'Artikelnr.',
            'name':'Kurztext',
            'stock':'Bestand',
            'price':'Preis 1'
        }

        #now map the magento names to the columns
        new_field_mapping = {}
        #e.g. 'sku':'Col1'
        for mapping_key in product_field_mapping:
            field = fields.find(".*[@Title='" + product_field_mapping[mapping_key] + "']")
            if field == None:
                raise Exception('Lexware product import: Corrupted file format!')
            new_field_mapping[mapping_key]=field.attrib['Name']

        #parse fields
        for row in rows:
            p = Product()
            for mapping_key in new_field_mapping:
                p[mapping_key] = row.find(new_field_mapping[mapping_key]).text

            self.products.append(p)
        #print(self.products)

    def get_products(self):
        return self.products

    def get_product_byId(self):
        if self.file_import:
            #return from self.products
            pass
        else:
            #get ids from the api
            return[1,2,3,4,5]
        
    def get_product_info(self):
        #get infos required by magento
        return {}
