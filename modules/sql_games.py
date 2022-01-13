import os
import sqlite3
import pickle
from pprint import pprint

import pygame as pg


class DBase:
    _db = None
    def __init__(self, name=None):
        if name and not DBase._db:
            DBase._db = sqlite3.connect(name)
            
    def connect(self):
        return DBase._db.cursor()
    
    def commit(self):
        DBase._db.commit()


class Table:
    def __init__(self, name, type_id='INTEGER'):   # types: 'INTEGER', 'TEXT', etc
        self.name = name
        self.cur = DBase().connect()
        self.type_id = type_id.upper()
        sql = f"""CREATE TABLE IF NOT EXISTS {self.name} (
              ID '{type_id}',
              DATA BLOB (4096)
              );"""
        self.cur.execute(sql)
        
    def add(self, data):
        if self.type_id == 'INTEGER':
            sql = f"SELECT max(id) FROM {self.name}"
            id = self.cur.execute(sql).fetchone()[0]
            if id:
                id += 1
            else:
                id = 1
            sql = f"INSERT INTO {self.name} (id, data) VALUES (?, ?)"
            self.cur.execute(sql, (id, pickle.dumps(data)))
            return id
    
    def put(self, id, data):
        sql = f"SELECT id FROM {self.name} WHERE id = ?"
        if self.cur.execute(sql, (id, )).fetchone():
            sql = f"UPDATE {self.name} set data = ? WHERE id = ?"
            self.cur.execute(sql, (pickle.dumps(data), id))
        else:
            sql = f"INSERT INTO {self.name} (id, data) VALUES (?, ?)"
            self.cur.execute(sql, (id, pickle.dumps(data)))
        
    def get(self, id=None):
        if id:
            sql = f"SELECT id, data FROM {self.name} WHERE id = ?"
            res = self.cur.execute(sql, (id, ))
        else:
            sql = f"SELECT id, data FROM {self.name}"
            res = self.cur.execute(sql)

        dic = {}
        for rec in res:
            dic[rec[0]] = pickle.loads(rec[1])
        return dic
    
    def put_image(self, id, image):
        data = (pg.image.tostring(image, 'RGB'), image.get_size())
        self.put(id, data)
        
    def get_image(self, id):
        dic = self.get(id)
        for key, val in dic.items():
            image = pg.image.fromstring(val[0], val[1], 'RGB')
            dic[key] = image
        return dic


def load_images(path='img'):
    DBase('seabase.db')
    pg.init()
    for f in os.listdir(path):
        print(f)
        image = pg.image.load(os.path.join(path, f))
        Table('img', type_id='TEXT').put_image(f, image)
    DBase().commit()
    pg.quit()


if __name__ == '__main__':
    load_images()
    # Table('test').add([1, 2, 3, 4])
    # Table('test').add({'1': 11111, 'dx': 12, 'dy': 22})
    # Table('sprite').put(10, {1: 12})
    #
    #
    # pprint(Table('sprite').get())
    #
    # pg.init()
    # # image = pg.image.load('boom.png')
    # # Table('images').put_image(1, image)
    # # DBase().commit()
    #
    # image = Table('images').get_image(3)[3]
    #
    # screen = pg.display.set_mode((400, 400))
    # flag = True
    # while flag:
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             flag = False
    #     screen.blit(image, (100, 100))
    #     pg.display.flip()
    #


    
