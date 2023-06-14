# encoding: utf-8
# module _sqlite3
# from (pre-generated)
# by generator 1.147
# no doc
# imports
import sqlite3 as __sqlite3
# Variables with simple values
PARSE_COLNAMES = 2
PARSE_DECLTYPES = 1
SQLITE_ALTER_TABLE = 26
SQLITE_ANALYZE = 28
SQLITE_ATTACH = 24
SQLITE_CREATE_INDEX = 1
SQLITE_CREATE_TABLE = 2
SQLITE_CREATE_TEMP_INDEX = 3
SQLITE_CREATE_TEMP_TABLE = 4
SQLITE_CREATE_TEMP_TRIGGER = 5
SQLITE_CREATE_TEMP_VIEW = 6
SQLITE_CREATE_TRIGGER = 7
SQLITE_CREATE_VIEW = 8
SQLITE_CREATE_VTABLE = 29
SQLITE_DELETE = 9
SQLITE_DENY = 1
SQLITE_DETACH = 25
SQLITE_DONE = 101
SQLITE_DROP_INDEX = 10
SQLITE_DROP_TABLE = 11
SQLITE_DROP_TEMP_INDEX = 12
SQLITE_DROP_TEMP_TABLE = 13
SQLITE_DROP_TEMP_TRIGGER = 14
SQLITE_DROP_TEMP_VIEW = 15
SQLITE_DROP_TRIGGER = 16
SQLITE_DROP_VIEW = 17
SQLITE_DROP_VTABLE = 30
SQLITE_FUNCTION = 31
SQLITE_IGNORE = 2
SQLITE_INSERT = 18
SQLITE_OK = 0
SQLITE_PRAGMA = 19
SQLITE_READ = 20
SQLITE_RECURSIVE = 33
SQLITE_REINDEX = 27
SQLITE_SAVEPOINT = 32
SQLITE_SELECT = 21
SQLITE_TRANSACTION = 22
SQLITE_UPDATE = 23
sqlite_version = '3.31.1'
version = '2.6.0'
# functions
def adapt(obj, protocol, alternate): # real signature unknown; restored from __doc__
 """ adapt(obj, protocol, alternate) -> adapt obj to given protocol. Non-standard. """
 pass
def complete_statement(sql): # real signature unknown; restored from __doc__
 """
 complete_statement(sql)
 
 Checks if a string contains a complete SQL statement. Non-standard.
 """
 pass
class Cache(object):
 # no doc
 def display(self, *args, **kwargs): # real signature unknown
 """ For debugging only. """
 pass
 def get(self, *args, **kwargs): # real signature unknown
 """ Gets an entry from the cache or calls the factory function to produce one. """
 pass
 def __init__(self, *args, **kwargs): # real signature unknown
 pass
 @staticmethod # known case of __new__
 def __new__(*args, **kwargs): # real signature unknown
 """ Create and return a new object. See help(type) for accurate signature. """
 pass
class Connection(object):
 """ SQLite database connection object. """
 def backup(self, *args, **kwargs): # real signature unknown
 """ Makes a backup of the database. Non-standard. """
 pass
 def create_collation(self, *args, **kwargs): # real signature unknown
 """ Creates a collation function. Non-standard. """
 pass
 def create_function(self, *args, **kwargs): # real signature unknown
 """ Creates a new function. Non-standard. """
 pass
 def executemany(self, *args, **kwargs): # real signature unknown
 """ Repeatedly executes a SQL statement. Non-standard. """
 pass
 def iterdump(self, *args, **kwargs): # real signature unknown
 """ Returns iterator to the dump of the database in an SQL text format. Non-standard. 
"""
 pass
 def load_extension(self, *args, **kwargs): # real signature unknown
 """ Load SQLite extension module. Non-standard. """
 pass
 def __call__(self, *args, **kwargs): # real signature unknown
 """ Call self as a function. """
 pass
 def __enter__(self, *args, **kwargs): # real signature unknown
 """ For context manager. Non-standard. """
 pass
 def __exit__(self, *args, **kwargs): # real signature unknown
 """ For context manager. Non-standard. """
 pass
 def __init__(self, *args, **kwargs): # real signature unknown
 pass
 @staticmethod # known case of __new__
 def __new__(*args, **kwargs): # real signature unknown
 """ Create and return a new object. See help(type) for accurate signature. """
 pass
