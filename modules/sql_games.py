import os
import pickle
import sqlite3

import pygame as pg

from modules.const import *


class DBase:
    _db = None
    
    def __init__(self, name=None):
        if name and not DBase._db:
            DBase._db = sqlite3.connect(name)
    
    @staticmethod
    def connect():
        return DBase._db.cursor()
    
    @staticmethod
    def commit():
        DBase._db.commit()


class Table:
    def __init__(self, name, type_id='INTEGER'):  # types: 'INTEGER', 'TEXT', etc
        self.name = name
        self.cur = DBase(P.DB_NAME).connect()
        self.type_id = type_id.upper()
        sql = f"""CREATE TABLE IF NOT EXISTS {self.name} (
              ID {type_id},
              DATA BLOB (4096)
              );"""
        self.cur.execute(sql)
    
    def add(self, data):
        if self.type_id == 'INTEGER':
            sql = f"SELECT max(id) FROM {self.name}"
            key = self.cur.execute(sql).fetchone()[0]
            if key:
                key += 1
            else:
                key = 1
            sql = f"INSERT INTO {self.name} (id, data) VALUES (?, ?)"
            self.cur.execute(sql, (key, pickle.dumps(data)))
            return key
    
    def put(self, key, data):
        sql = f"SELECT id FROM {self.name} WHERE id = ?"
        if self.cur.execute(sql, (key,)).fetchone():
            sql = f"UPDATE {self.name} set data = ? WHERE id = ?"
            self.cur.execute(sql, (pickle.dumps(data), key))
        else:
            sql = f"INSERT INTO {self.name} (id, data) VALUES (?, ?)"
            self.cur.execute(sql, (key, pickle.dumps(data)))
    
    def get(self, key=None):
        if key:
            sql = f"SELECT id, data FROM {self.name} WHERE id = ?"
            res = self.cur.execute(sql, (key,))
        else:
            sql = f"SELECT id, data FROM {self.name}"
            res = self.cur.execute(sql)
        
        dic = {}
        for rec in res:
            dic[rec[0]] = pickle.loads(rec[1])
        return dic
    
    def put_image(self, key, image):
        data = (pg.image.tostring(image, 'RGB'), image.get_size())
        self.put(key, data)
    
    def get_image(self, key):
        dic = self.get(key)
        for key, val in dic.items():
            image = pg.image.fromstring(val[0], val[1], 'RGB')
            dic[key] = image
        return dic


def load_images_to_sql(path):
    pg.init()
    for f in os.listdir(path):
        print(f)
        image = pg.image.load(os.path.join(path, f))
        Table('img', type_id='TEXT').put_image(f, image)
    DBase().commit()
    pg.quit()


def play_sound(name):
    if ch := pg.mixer.find_channel(True):
        file = os.path.join(P.PATH_M, name)
        ch.play(pg.mixer.Sound(file))


def load_music(name):
    file = os.path.join(P.PATH_M, name)
    pg.mixer.music.load(file)


def load_image(fname):
    DBase(P.DB_NAME)
    return image_convert(Table('img').get_image(fname)[fname])


def image_convert(image, color_key=None):
    if not color_key:
        color_key = image.get_at((0, 0))
    image.set_colorkey(color_key)
    return image.convert_alpha()


def add_score(sc01, sc02, move01, move02):
    Table('log').add({'sc01': sc01, 'sc02': sc02, 'move01': move01, 'move02': move02})
    DBase.commit()


if __name__ == '__main__':
    load_images_to_sql('img')
