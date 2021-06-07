########################################################################################################################################################################################################

#README

#By implementing this script, i wanna to take a look on the business logic between lexware and magento. 
#It's important to have an eye on the interaction between these two systems. When i have changes in my lexware program, i also wanna to have these changes in my 
#magento shop. It's essential, that these two systems interact with one another. This would create transparency even for the end customers. 
#So i had to make sure that there was a stable communication between my lexware program and my magento shop. 
#I asked myself some questions. On the one hand, its useful to see what happens to the products which where deleted in lexware. 
#These products namly also need to be deleted in my magento shop. On the other hand the same case applies then, regarding to add new products/uploading new products.
#I tried to realise these cases throughout a case distinction. 
#Another complex aspect i had to look for, was the sync between my two instances. Here it was necessary to implement a sync which is able to sync in both directions, 
#a bidirectional sync if you will it like that. My first sync should start from lexware and should sync my magento shop and the other sync should start from magento and sync my lexware program. 
#The complexity on these tasks where the handling of the correct sync. I assumed, that the only changes require changes on the product stock. 
#Throughout the sync i tried to kept an eye, on both of the systems product stock. 

########################################################################################################################################################################################################
import time
from datetime import datetime
from utils import Product
import os 
from xml.etree import ElementTree
 

class Syncer():
    
    #include the magento and lexware agents
    ma = None
    le = None

    def __init__(self, magentoAgent, lexwareAgent):
        self.ma = magentoAgent
        self.le = lexwareAgent

    def delete_deleted_products(self):
        #this method deletes all products from magento which were deleted in lexware

        for m_product in self.ma.get_product_byId():
            deleted = True
            for l_product in self.le.get_product_byId():
                #are there any products in magento which should not be in lexware ?
                if l_product == m_product:
                    deleted = False
                if deleted:
                    #just go on if deletion failed, next time may be more successfull
                    #maybe already deleted in meantime or just failed 
                    self.ma.delete_product(m_product)

    def upload_new_products(self):
        #this method uploads all products from lexware to magento if they are not available yet
        for l_product in self.le.get_product_byId():
            found = False
            for m_product in self.ma.get_product_byId():
                if l_product == m_product:
                    found = True
            if not found:
                prod_info = self.le.get_product_info(l_product)
                if prod_info:
                    #skip products which were deleted in meantime
                    #just go on if upload failed, next time may be more successfull
                    self.ma.upload_product(prod_info)

    def sync(self):
        #sync lexware to magento:
        #this method should call subroutines which handle the different sync cases
        #i assume, that the only value change in magento is the product count/stock status
        #i although assume that during the execution of this script no other entity writes to the magento db

        #for sync it may be helpful, to compare the stock status of the products   
        #for product in magento and for product in lexware:
        #if l_product == m_product => stock checkup ? 
        #compare time stamp of every product, sync from the latest change => level up the not updated component

        #todo =>
        #case: sync lexware to magento (data, count (stock status), etc)


        file_name = 'articlefile.xml'
        dom = ElementTree.parse(file_name)
        
        stockdata = dom.findall('Row')
        for s in stockdata:
            stock = s.find('Col5').text

            print('* {}'.format(stock))

            #for my stock in the lexware products, lastCount should always print out the latest stock value
            #and then, this value will sync magento stock
        def lexSync(self):
            for l_stock in stock():
                found = False
                if not found:
                    #if no stock value is found, just skip and go on, may next time there will be found any
                    #or may print, that there is no stock value?
                    #print('An ERROR occured: No stock value could be found!')
                    pass
                for m_stock in self.ma.get_product_info():
                    if l_stock == m_stock:
                        found = True
                        sync_lexStock = stock(l_stock)
                        self.ma.put_productUpdate(sync_lexStock)
                        print('Synchronization committed successfully!')                   
                      
            #todo =>
            #case: back sync (magento to lexware) product count(stock status)
            #in my first reflections i wanna to compare the timestamp of the lexware and magento stock, so that i know from who to who i have to sync
            #but i forgot about the case, that both sides can change its stock value independent of one another 
            #so i decided to take both stock values and calculate its difference, which i then deduct from the lexware stock
            #through this method, i would make sure, that the correct stock value from magento is synct
        def magSync(self):
            for l_productAmount in self.sync_lexStock():
                lastCount = sync_lexStock([l_productAmount])
                for m_stock in self.ma.get_stockItem(['qty']):
                    #if someone buys a product the stock amount will increase, in fact of that, its necessary to transfer/sync the new stock status to lexware
                    #because of the fact, that also the lexware stock is able to increase its stock value (independent of any magento changes), its necessary to remember both stock statuses
                    #through the remembered stock statuses, i then wanna calculate the difference, the difference i then calculate minus the lexware stock status
                    #after that i can be sure, that only the actual stock value is going to be synct
                    #calculate the difference 
                    magStock = self.ma.get_stockItem(m_stock)
                    lexStock = sync_lexStock(l_productAmount)
                    diff = magStock.difference(lexStock)
                    print(diff)
                    #diff - lexStock = actual stock value 
                    actualValue = (lexStock - diff)
                    sync_lexStock = stock(actualValue)
                    self.ma.put_productUpdate(sync_lexStock)
                    print('Synchronization commited successfully!')
                                                                

        #make sure,that the sync completed successfully and that there is no concurrency (pid, ack checks)

        #delete:
        #dump products in lexware and magento for debugging:
        print('-------------------Magento Products------------------')
        print(self.ma.get_products())
        print()
        print('-------------------Lexware Products------------------')
        print(self.le.get_products())

        #case: delete product in lexware
        self.delete_deleted_products()
        #case: new products in lexware which require an upload
        self.upload_new_products()

        #sync
        self.sync()
        #case: sync lexware to magento (data, stock, etc)
        self.lexSync()
        #case: back sync (magento to lexware) product stock
        self.magSync()
