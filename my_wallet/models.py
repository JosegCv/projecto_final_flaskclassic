from datetime import * 
import os
import sqlite3

class Registros:
    def __init__(self, date_hour, currency_from, quantity_from, currency_to, quantity_to,  id = None):
        self.date_hour = date_hour
        self.id = id

        self.currency_from = currency_from
        self.quantity_from = quantity_from
        self.currency_to = currency_to
        self.quantity_to = quantity_to

    @property
    def date_hour(self):
        return self._date
    
    @date_hour.setter
    def _date(self, value):
        self._date = date.fromisoformat(value)
        if self._date > date.today():
            raise ValueError("Date must be Today or a Date Before")
        
    @property
    def quantity(self):
        pass
    
    @quantity.setter
    def amount(self, value):
        self._quantity = float(value)
        if self._quantity == 0:
            raise ValueError("amount must be positive or negative")
        
    @property
    def currency(self):
        pass
    
    @currency.setter
    def currency(self, value):
      pass
class MovementDAOsqlite:
    def __init__(self, db_path):
        self.path = db_path

        query = """
        CREATE TABLE IF NOT EXISTS "registros" (
            "id"	INTEGER,
            "date_hour"	TEXT NOT NULL,
            "currency_from"	TEXT NOT NULL,
            "quantity_from"	REAL NOT NULL,
            "currency_to"	TEXT NOT NULL,
            "quantity_to"	REAL NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query)
        conn.close()"""

    def insert(self, movement):

        query = """
        INSERT INTO registros
               (date_hour,currency_from,quantity_from,currency_to,quantity_to,)
        VALUES (?, ?, ?, ?, ?)
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, (movement.date_hour, movement.currency_from,
                            movement.quantity_from, movement.currency_to, movement.quantity_to))
        conn.commit()
        conn.close()

    def get(self, id):
        query = """
        SELECT date_hour, currency_from,quantity_from,currency_to,quantity_to, id
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
        SELECT date_hour,currency_to,quantity_to,currency_to,quantity_to, id
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
# dejare el update solo por si se me ocurre alguna idea
    #def update(self, id, movement):
        #pass
        
        
        # query = """ 
        # UPDATE movements
        #    SET date_hour = ?,  currency_from= ?, quantity_from = ?, currency_to = ?, quantity_to = ?
        #  WHERE id = ?;
        # """

        # conn = sqlite3.connect(self.path)
        # cur = conn.cursor()
        # cur.execute(query, (movement.date, movement.abstract, movement.amount, movement.currency, id))
        # conn.commit()
        # conn.close()