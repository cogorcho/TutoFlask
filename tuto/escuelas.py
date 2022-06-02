from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, jsonify
)

from werkzeug.exceptions import abort
import pymongo

from tuto.auth import login_required
from tuto.mongo import get_mongo

"""
    Datos:
        https://datos.gob.ar/dataset/ign-unidades-territoriales/archivo/ign_01.02.01
"""

bp = Blueprint('escuelas', __name__, url_prefix='/escuelas')

@bp.route('/index')
def index():
    return render_template('escuelas/index.html')

@bp.route('/pcias')
def pcias():
    collection = get_mongo()['Escuelas']
    result = collection.distinct('Jurisdicción')
    return jsonify(result)

@bp.route('/ambitos')
def ambitos():
    collection = get_mongo()['Escuelas']
    result = collection.distinct("Ámbito")
    return jsonify(result)

@bp.route('/sectores')
def sectores():
    collection = get_mongo()['Escuelas']
    result = collection.distinct('Sector')
    return jsonify(result)

@bp.route('/cps')
def cps():
    collection = get_mongo()['Escuelas']
    result = collection.distinct('CP')
    return jsonify(result)

#------------------------------------------------------------
# DATOS GEOGRAFICOS
#------------------------------------------------------------
@bp.route('/provincias')
def provincias_full():
    collection = get_mongo()['Provincias']
    where = {}
    projection = {"_id": 0, 'id':1, 'nombre':1, 'centroide': 1}
    result = list(collection.find(where, projection).sort('nombre', pymongo.ASCENDING))
    return jsonify(result)


#------------------------------------------------------------
# DATOS DE ESCUELAS
#------------------------------------------------------------

#------------------------------------------------------------
# SUMARIZACIONES
#------------------------------------------------------------
@bp.route('/')
def escuelas_por_provincia():
    return jsonify(get_summarization('Escuelas','Jurisdicción'))

@bp.route('/sector')
def escuelas_por_sectores():
    return jsonify(get_summarization('Escuelas','Sector'))

@bp.route('/ambito')
def escuelas_por_ambitos():
    return jsonify(get_summarization('Escuelas','Ámbito'))

@bp.route('/codpos')
def escuelas_por_codigos_postales():
    return jsonify(get_summarization('Escuelas','CP'))

#-------------------------------------------------------------------
# DETALLE
#-------------------------------------------------------------------
@bp.route('/sector/<sector>')
def escuelas_por_sector(sector):
    where = {'Sector': sector}
    return get_data('Escuelas', where)


@bp.route('/codpos/<codpos>')
def escuelas_por_codpos(codpos):
    where = {'CP': codpos}
    return get_data('Escuelas', where)


@bp.route('/tiposeducacion/<id>')
def tipos_educacion_por_escuela(id):
    where = {'CUE Anexo': id}
    return get_data('TiposEducacion', where)
    

@bp.route('/provincia/<id>')
def provincias(id):
    where = {'id': id}
    return get_data('Provincias', where)




#--------------------------------------------------
# FUNCIONES EXTRA
#--------------------------------------------------
def get_data(str_collection, obj_where, obj_projection={"_id":0}):
    """
    Va a la DB y retorna los datos
    """
    collection = get_mongo()[str_collection]
    result = list(collection.find(obj_where, obj_projection))
    return jsonify(result)

def get_summarization(str_collection, str_column):
    collection = get_mongo()[str_collection]
    pipeline = [
        {
            "$group":
            {
                "_id":f"${str_column}",
                "escuelas": 
                {
                    "$sum":1
                }
            }
        },
        {
            "$sort": {"_id": 1}
        }
    ]
    #print(pipeline)
    return list(collection.aggregate(pipeline))