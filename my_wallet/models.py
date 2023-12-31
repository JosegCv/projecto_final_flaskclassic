from datetime import * 
import os
import sqlite3
import requests
from my_wallet import app

CURRENCIES =  ["EUR", "BTC",
    "ETH", "USDT",
    "BNB", "XRP",
    "ADA", "SOL",
    "DOT", "MATIC"]

class Registros:
    def __init__(self,date_hour, currency_from, quantity_from, currency_to, quantity_to,unit_price,  id = None):
        
        self.id = id
        self.date_hour = str(date_hour)
        self.unit_price = unit_price
        self.currency_from = currency_from
        self.quantity_from = quantity_from
        self.currency_to = currency_to
        self.quantity_to = quantity_to
        self.unit_price = unit_price

    @property
    def date_hour(self):
        return self._date
    
    @date_hour.setter
    def date_hour(self, value):
        self._date = datetime.fromisoformat(value)
        if self._date > datetime.today():
            raise ValueError("Incorrect date")
        
    @property
    def quantity_from(self):
        return self._quantity_from

    @quantity_from.setter
    def quantity_from(self, value):
        if value is None:
            value = 0.0
        self._quantity_from = float(value)
        if self._quantity_from < 0:
            raise ValueError(" must be non-negative amount")

    @property
    def currency_from(self):
        return self._currency_from

    @currency_from.setter
    def currency_from(self, value):
        if value is None:
            value = ""
        self._currency_from = value
        if self._currency_from not in CURRENCIES:
            raise ValueError(f"currency must be in {CURRENCIES}")

    @property
    def currency_to(self):
        return self._currency_to

    @currency_to.setter
    def currency_to(self, value):
        if value is None:
            value = ""
        self._currency_to = value
        if self._currency_to not in CURRENCIES:
            raise ValueError(f"currency must be in {CURRENCIES}")

    @property
    def quantity_to(self):
        return self._quantity_to

    @quantity_to.setter
    def quantity_to(self, value):
        if value is None:
            value = 0.0
        self._quantity_to = float(value)
        if self._quantity_to < 0:
            raise ValueError(" must be non-negative amount")
    


    def __eq__(self, other):
        return self.date_hour == other.date_hour and self.currency_from == other.currency_from and self.quantity_from == other.quantity_from and self.currency_to == other.currency_to and self.quantity_to == other.quantity_to
        #return (self.date_hour, self.currency_from, self.quantity_from, self.currency_to, self.quantity_to) == (other.date_hour, other.currency_from, other.quantity_from, other.currency_to, other.quantity_to)
    def __repr__(self):
        return f"Movimiento: {self.date_hour} - {self.currency_from} - {self.quantity_from} - {self.currency_to} - {self.quantity_to}"

class MovementDAOsqlite:
    def __init__(self, db_path):
        self.path = db_path

        query = """
        CREATE TABLE IF NOT EXISTS "movements" (
	    "id"	INTEGER UNIQUE,
	    "date_hour"	TEXT NOT NULL,
	    "currency_from"	TEXT NOT NULL,
	    "quantity_from"	REAL NOT NULL,
	    "currency_to"	TEXT NOT NULL,
	    "quantity_to"	REAL NOT NULL,
	    "unit_price"	REAL ,
	    PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()

    def insert(self, movement): 

        query = """
        INSERT INTO movements
               (date_hour,currency_from,quantity_from,currency_to,quantity_to,unit_price)
        VALUES ( ?, ?, ?, ?, ?, ?)
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (movement.date_hour, movement.currency_from,
                            movement.quantity_from, movement.currency_to, movement.quantity_to, movement.unit_price))
        conn.commit()
        conn.close()

    def get(self, id):
        query = """
        SELECT date_hour, currency_from,quantity_from,currency_to,quantity_to, id, unit_price
          FROM movements
         WHERE id = ?;
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (id,))
        res = cur.fetchone()
        conn.close()
        if res:
            return Registros(*res)

        
    def get_all(self):
        query = """
        SELECT date_hour,currency_from,quantity_from,currency_to,quantity_to,unit_price
          FROM movements
         ORDER by date_hour;
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query)
        res = cur.fetchall()


        lista = [Registros(*reg) for reg in res]

        conn.close()

        return lista


    def consulta(self):
        query = """
        SELECT currency_from, currency_to, quantity_from, quantity_to FROM movements
         """
    
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
        conn.close()

    # Diccionario para realizar el seguimiento de las sumas de quantity_from y quantity_to por currency
        sums_by_currency = {}

        for currency_from, currency_to, quantity_from, quantity_to in data:

            if currency_from not in sums_by_currency:
                sums_by_currency[currency_from] = {"quantity_from": 0.0, "quantity_to": 0.0}
            if currency_to not in sums_by_currency:
                sums_by_currency[currency_to] = {"quantity_from": 0.0, "quantity_to": 0.0}


            sums_by_currency[currency_from]["quantity_from"] += quantity_from
            sums_by_currency[currency_to]["quantity_to"] += quantity_to
            

        return sums_by_currency

