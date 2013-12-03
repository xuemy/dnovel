#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import logging
import time
import itertools

__author__ = 'meng'

import pymysql.cursors
import pymysql.constants
#import pymysql.constants.FIELD_TYPE
#import pymysql.constants.FLAG
import pymysql.converters
import sqlite3
import DBUtils.PooledDB
#import DBUtils.PersistentDB

class DB(object):
    def __init__(self,db_type,database,host="localhost",user=None,password=None,
                 max_idle_time = 7 * 3600,connect_timeout = 0,
                 time_zone = "+8:00"):
        self.db_type = db_type
        self.host = host
        self.database = database
        self.max_idle_time = float(max_idle_time)

        args = dict(
            use_unicode=True,
            charset="utf-8",
            db = database,
            init_command=('SET time_zone = "%s"'% time_zone),
            connect_timeout = connect_timeout
        )

        if user is not None:
            args['user'] = None
        if password is not None:
            args['password'] = None

        self._db = None
        self._db_args = args
        self._last_use_time = time.time()

        try:
            self.reconnect()
        except:
            logging.error(u"不能连接%s数据库在%s",self.db_type,self.host)
    def __del__(self):
        self.close()
    def reconnect(self):
        self.close()
        if self.db_type == 'mysql':
            try:
                pool_on = DBUtils.PooledDB.PooledDB(creator=pymysql,setsession=['set autocommit = 1'],**self._db_args)
                self._db = pool_on.connection()
            except:
                self._db = pymysql.connect(**self._db_args)
                self._db.autocommit(True)
        if self.db_type == 'sqlite':
            self._db = sqlite3.connect(self.database)
            self._db.isolation_level = None
            #self._db.text_factory = str
            #try:首发
            #    pool_on = DBUtils.PersiasdstentDB.PersistentDB(creator=sqlite3,setsession=['set autocommit = 1'],**self._db_args)
            #    self._db = pool_on.

    def close(self):
        if getattr(self,"_db",None) is not None:
            self._db.close()
            self._db = None
    def _ensure_connected(self):
        if (self._db is None or (time.time() - self._last_use_time > self.max_idle_time)):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()
    def _execute(self,cursor,query,parameters):
        try:
            return cursor.execute(query,parameters)
        except OperationalError:
            logging.error("Error connecting to %s on %s",self.db_type,self.host)
            self.close()
            raise
    def iter(self,query,*parameters):
        self._ensure_connected()
        if self.db_type == 'mysql':
            cursor = pymysql.cursors.SSCursor(self._db)
        elif self.db_type == 'sqlite':
            cursor = self._db.cursor()
        try:
            self._execute(cursor,query,parameters)
            column_names = [d[0] for d in cursor.description]
            for row in cursor:
                yield Row(zip(column_names,row))
        finally:
            cursor.close()
    def query(self,query,*parameters):
        cursor = self._cursor()
        try:
            self._execute(cursor,query,parameters)
            column_names = [d[0] for d in cursor.description]
            return [Row(itertools.izip(column_names,row)) for row in cursor]
        finally:
            cursor.close()
    def get(self,query,*parameters):
        rows = self.query(query,parameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database query")
        else:
            return rows[0]
    def execute(self,query,*parameters):
        return self.execute_lastrowid(query,*parameters)

    def execute_lastrowid(self, query, *parameters):
        cursor = self._cursor()
        try:
            self._execute(cursor,query,parameters)
            return cursor.lastrowid
        finally:cursor.close()

    def execute_rowcount(self, query, *parameters):
        """Executes the given query, returning the rowcount from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        return self.executemany_lastrowid(query, parameters)

    def executemany_lastrowid(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def executemany_rowcount(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()



class Row(dict):
    def __getattr__(self,name):
        try:
            return self[name]
        except KeyError:
            raise  AttributeError(name)
if pymysql is not None:
    # Fix the access conversions to properly recognize unicode/binary
    FIELD_TYPE = pymysql.constants.FIELD_TYPE
    FLAG = pymysql.constants.FLAG
    CONVERSIONS = copy.copy(pymysql.converters.conversions)

    field_types = [FIELD_TYPE.BLOB, FIELD_TYPE.STRING, FIELD_TYPE.VAR_STRING]
    if 'VARCHAR' in vars(FIELD_TYPE):
        field_types.append(FIELD_TYPE.VARCHAR)

    for field_type in field_types:
        CONVERSIONS[field_type] = [(FLAG.BINARY, str)] + [CONVERSIONS[field_type]]

    # Alias some common MySQL exceptions
    IntegrityError = pymysql.IntegrityError
    OperationalError = pymysql.OperationalError