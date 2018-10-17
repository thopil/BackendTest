'''
Created on 12 Oct 2018

@author: tp
'''

class Singleton(object):
    __instance = None
    def __new__(cls, val):
        if Singleton.__instance is None:
            Singleton.__instance = object.__new__(cls)
        Singleton.__instance.val = val
        return Singleton.__instance
