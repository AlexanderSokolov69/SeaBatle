from os import listdir, path
from pickle import dumps, loads
import sqlite3

import pygame

from modules.const import *


class DBase:
    """
    Класс для подключения к SQLite базе данных
    """
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
    """
    Класс для работы с таблицами базы данных
    """
    def __init__(self, name, type_id='INTEGER'):  # types: 'INTEGER', 'TEXT', etc
        """
        Таблица с именем NAME создаётся, если отсутствует
        """
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
            self.cur.execute(sql, (key, dumps(data)))
            return key
    
    def put(self, key, data):
        sql = f"SELECT id FROM {self.name} WHERE id = ?"
        if self.cur.execute(sql, (key,)).fetchone():
            sql = f"UPDATE {self.name} set data = ? WHERE id = ?"
            self.cur.execute(sql, (dumps(data), key))
        else:
            sql = f"INSERT INTO {self.name} (id, data) VALUES (?, ?)"
            self.cur.execute(sql, (key, dumps(data)))
    
    def get(self, key=None):
        if key:
            sql = f"SELECT id, data FROM {self.name} WHERE id = ?"
            res = self.cur.execute(sql, (key,))
        else:
            sql = f"SELECT id, data FROM {self.name}"
            res = self.cur.execute(sql)
        
        dic = {}
        for rec in res:
            dic[rec[0]] = loads(rec[1])
        return dic
    
    def put_image(self, key, image):
        data = (pygame.image.tostring(image, 'RGBA'), image.get_size())
        self.put(key.upper(), data)
    
    def get_image(self, key):
        dic = self.get(key)
        for key, val in dic.items():
            image = pygame.image.fromstring(val[0], val[1], 'RGBA')
            dic[key.upper()] = image
        return dic


def load_images_to_sql(fpath):
    """
    Перенос файлов изображений из каталога в БД
    """
    pygame.init()
    for f in listdir(fpath):
        print(f)
        image = pygame.image.load(path.join(fpath, f))
        Table('img', type_id='TEXT').put_image(f.upper(), image)
    DBase().commit()
    pygame.quit()


def load_image(fname):
    DBase(P.DB_NAME)
    fname = fname.upper()
    return image_convert(Table('img').get_image(fname)[fname])
    # return image_convert(pygame.image.load(path.join('modules/img', fname)))


def image_convert(image):
    return image.convert_alpha()


def add_score(sc01, sc02, move01, move02):
    Table('log').add({'sc01': sc01, 'sc02': sc02, 'move01': move01, 'move02': move02})
    DBase.commit()


if __name__ == '__main__':
    # Загрузка картинок в БД. При совпадении имён картинка заменяется
    load_images_to_sql('img')
