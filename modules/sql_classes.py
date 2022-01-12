import pickle
import sqlite3
from pprint import pprint

import pygame as pg


class DBase:
    _con = None
    def __init__(self, db_name=None):
        if db_name and not DBase._con:
            DBase._con = sqlite3.connect(db_name)

    def connect(self):
        return DBase._con.cursor()
    
    def commit(self):
        DBase._con.commit()
        

class Table:
    def __init__(self, name):
        self.name = name
        self.cur = DBase().connect()
        sql = f"""CREATE TABLE IF NOT EXISTS {self.name} (
            ID INTEGER,
            DATA BLOB (4096)
        );"""
        self.cur.execute(sql)
        
    def add(self, data):
        sql = f"select max(id) from {self.name}"
        id = self.cur.execute(sql).fetchone()[0]
        if id:
            id += 1
        else:
            id = 1
        sql = f"INSERT INTO {self.name} (id, data) VALUES (?, ?)"
        self.cur.execute(sql, (id, pickle.dumps(data)))
        
    def put(self, id, data):
        sql = f"SELECT id, data FROM {self.name} WHERE id = {id}"
        res = self.cur.execute(sql).fetchone()
        if res:
            sql = f"UPDATE {self.name} set data = ? where id = {id}"
            self.cur.execute(sql, (pickle.dumps(data), ))
        else:
            sql = f"INSERT INTO {self.name} (id, data) VALUES (?, ?)"
            self.cur.execute(sql, (id, pickle.dumps(data)))
        
    def get(self, id=None):
        if id:
            sql = f"SELECT id, data FROM {self.name} WHERE id = {id}"
        else:
            sql = f"SELECT id, data FROM {self.name}"
        res = self.cur.execute(sql)
        dic = {}
        for rec in res:
            dic[rec[0]] = pickle.loads(rec[1])
        return dic
    
    def image_put(self, id, image):
        data = (pg.image.tostring(image, 'RGB'), image.get_size())
        self.put(id, data)
        
    def image_get(self, id):
        data = self.get(id)[id]
        return pg.image.fromstring(data[0], data[1], 'RGB')
        
if __name__ == '__main__':
    DBase('test.db')
    pg.init()
    
    player = Table('player')
    player.add([1, 2, 3, 4])
    player.put(33, {4: '1111', '5': 2222, 6: [1, 2, 3, 4, 5, 6, 7]})
    
    Table('sprite').put(1, {'x': 44, 'y': 77, 'dx': 2, 'dy': 0, 'image': 'bigdog.png'})
    
    Table('images').image_put(4, pg.image.load('mario.png'))
    Table('images').image_put(2, pg.image.load('star.png'))

    
    
    DBase().commit()
    pprint(player.get())

    screen = pg.display.set_mode((400, 400))
    image = Table('images').image_get(4).convert_alpha()
    screen.blit(image, (100, 100))
    pg.display.flip()
    flag = True
    while flag:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                flag = False
    pg.quit()
    