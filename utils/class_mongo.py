# -*- coding: utf-8 -*-

from pymongo import MongoClient
import os
from urllib.parse import quote_plus
class Mongo:
    def __init__(self, user=None, passwd=None, host=None, port=None, db=None, ambiente=None, cluster=None):
        passwd = quote_plus(passwd)
        if cluster:
            self.client = MongoClient(os.getenv('CLUSTER'))
        else:
            if ambiente == "DEV":
                self.client = MongoClient(f"mongodb://{user}:{passwd}@{host}:{int(port)}")
            else:
                self.client = MongoClient(f"mongodb://{user}:{passwd}@{host}:{int(port)}/?authSource={ambiente}")
        
        self.db = self.client[db]
        self.col = ""
       
    def __del__(self):
        self.client.close()
    
    def _check_collection(self, p_coll, p_initial = False) -> bool:
        """
        Cria a collection passada e, caso seja a primeira carga dos tickers, cria e carrega os dados.
        :param p_coll: str (nome da collection)
        :param p_initial: bool (se True, carrega a collection dos tickers)
 
        :return ret: bool
        """
 
        ret = True
        if p_coll not in self.db.collection_names():
            self.db.create_collection(p_coll)
            self.col = self.db[p_coll]        
            ret = False
            
        self._getcoll(p_coll)
 
        return ret
 
 
    def _getcoll(self, p_coll):
        """
        'Seta' a collection
        :param p_coll: str
        """
        self.col = self.db[p_coll]
 
    def _return_query(self, p_query, p_fields = {}, limit=100, batch=True):
        """'zoho':1,'Comiss_o_Agente_de_neg_cios':60
        Retorna o cursor da consulta feita.
        :param p_query: dict
 
        return pymongo.cursor
        """
        if p_fields:
            return self.col.find(p_query, p_fields)
        else:
            return self.col.find(p_query, no_cursor_timeout=True).batch_size(20)
    
    def return_all(self):
        return self.col.find()
 
    def _add_many(self, p_dados):
        """
        Insere os dados de uma lista.
        """
        self.col.insert_many(p_dados)
    
    def _return_sort(self, p_dados, field):
        return self.col.find(p_dados).sort(field,-1).limit(1)
 
    def _add_one(self, p_data):
        self.col.insert_one(p_data)
 
    def _upsert(self, p_dados, p_criterio):
        return self.col.update(p_criterio, p_dados, upsert=True)
    
    def getcoll(self, col):
        self.col = self.db[col]
 
    def addData(self, data):
        self.col.insert_one(data)
 
    def getCollections(self):
        return self.db.collection_names()
        
    def returnQuery(self, pDados = None, pSort = False, pParam = ""):
        if pSort:
            return self.col.find(pDados, no_cursor_timeout=True).sort(pParam, -1).batch_size(20)
        else:
            return self.col.find(pDados, no_cursor_timeout=True).batch_size(20)
    
    def returnBusca(self, pDados):
        return self.col.find(pDados).batch_size(20)
 
    def upsertByArr(self, pDados, pCriterio):
        return self.col._update(pCriterio, pDados, upsert=True)     
    
    def upsert_dados(self, pDados, pCampo, pChave):
        self.col._update({pCampo: pChave}, pDados, upsert=True)
 
    def addMany(self, pDados):
        self.col.insert_many(pDados)
 
    def delMany(self, pDdados):
        self.col.delete_many(pDdados)
    
    def update_many(self, pDataBefore, pDataAfter,pMulti=True):
        self.col.update_many(pDataBefore, pDataAfter,upsert=True)
    
    def updateOne_Query(self, pDataBefore, pDataAfter):
        return self.col.update_one(pDataBefore, pDataAfter)
    
    def _upsert(self, p_dados, p_criterio):
        return self.col.update_one(p_criterio, p_dados, upsert=True)
    
    def _return_aggregate(self, p_criterio, limit=100):

        return self.col.aggregate(p_criterio).batch_size(self.BATCH_SIZE)

    
    def close(self):
        return self.col.close()
