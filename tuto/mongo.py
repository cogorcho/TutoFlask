import pymongo
from pymongo import MongoClient
import click

from flask import current_app, g
from flask.cli import with_appcontext

import os
import sys
import json
import codecs


client = MongoClient('mongodb://localhost:27017')

def get_mongo():
    if 'mongo' not in g:
        g.mongo = client['TestEscuelas']

    return g.mongo

def close_mongo(e=None):
    mongo = g.pop('mongo', None)

    # if mongo is not None:
    #     client.close()

def init_db():
    print('mongo.init-db')
    db = get_mongo()


@click.command('init-mongo')
@with_appcontext
def init_mongo_command():
    """
    Clear the existing data and create new tables
    """
    print('mongo.init_mongo_command')

    csv_folder = os.path.join(current_app.static_folder,'CSV')
    json_folder = os.path.join(current_app.static_folder,'JSON')
    create_jsons(csv_folder, json_folder)

    click.echo("Initialized the mongo database")

def init_app(app):
    app.teardown_appcontext(close_mongo)
    app.cli.add_command(init_mongo_command)

#------------------------------------------------------------------
#
#------------------------------------------------------------------
def create_jsons(csv_folder, json_folder):
    """
    Crear los archivos .json para cargar a la DB
    csv_folder: Donde estan los csv q se tranforman a json
    json_folder: Destino de los archivos .json generados
    """
    clear_folder(json_folder)

    for fx in os.listdir(csv_folder):
        coll = fx.replace(".csv","")
        print(f"\nCreating {fx.replace('csv','json')}")
        jfile(gendata(os.path.join(csv_folder,fx)),os.path.join(json_folder,fx.replace("csv","json")))
        drop_collection(coll)
        create_collection(coll, json_folder)


def clear_folder(folder):
    """
    Borrar los archivos de una carpeta (folder)
    """
    for fx in os.listdir(folder):
        print(f'Deleting {folder}/{fx}')
        os.unlink(os.path.join(folder, fx))


def drop_collection(coll):
    """
    Eliminar una coleccion de la DB
    """
    coll_to_drop = coll.replace(".csv","").capitalize()
    print("drop_colection", coll_to_drop)
    client = MongoClient('mongodb://localhost:27017')
    db = client['TestEscuelas']
    Collection = db[coll_to_drop]
    Collection.drop()


def buscar_csv(folder):
    """
    Buscar archivos en la carpeta (folder))
    """
    return os.listdir(folder)



def create_collection(coll, folder):
    """
    Una vez generado el archivo .json en (folder), 
    crear la coleccion (coll)
    """
    coll_to_create = coll.capitalize()
    print("create_colection", coll_to_create)
    client = MongoClient('mongodb://localhost:27017')
    db = client['TestEscuelas']
    Collection = db[coll_to_create]
   
    with open(os.path.join(folder, f"{coll}.json")) as fx:
        file_data = json.load(fx)

    if isinstance(file_data, list):
        Collection.insert_many(file_data)  
    else:
        Collection.insert_one(file_data)

#------------------------------------------------------------------
#
#------------------------------------------------------------------
def gendata(archivo):
	"""
    Abre el archivo csv (archivo) y genera una lista
	de dict, uno por escuela
    """

	with open(archivo) as e:
		lines = e.readlines()

	keys = lines[0].rstrip("\n").split('|')
	data = []

	for i in range(1,len(lines)):
		values = lines[i].rstrip("\n").split('|')
		e = {}
		for k,v in zip(keys, values):
			if v == "X":
				val = "SI"
			elif v == "":
				val = "NO"
			else:
				val = v

			e[k.replace("Ed. ","")] = val
		data.append(e)

	return data


#------------------------------------------------------------------
#
#------------------------------------------------------------------
def jfile(data, archivo):
	"""
    Crea el archivo (archivo) json de escuelas
    """

	print(f"Generating {archivo}")
	with codecs.open(archivo,'w',encoding='utf-8') as f:
		for i in range(0,len(data)):
			if i == 0:
				f.write("[")
			else:
				f.write(",\n")
			json.dump(data[i], f, ensure_ascii=False)
		f.write("]")

	print(f"{archivo} generated OK!")
