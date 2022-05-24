from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, jsonify
)

from werkzeug.exceptions import abort
import pymongo

from tuto.auth import login_required
from tuto.mongo import get_mongo


bp = Blueprint('escuelas', __name__, url_prefix='/escuelas')

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

#------------------------------------------------------------

@bp.route('/provincias')
def provincias_full():
    collection = get_mongo()['Provincias']
    where = {}
    projection = {"_id": 0, 'id':1, 'nombre':1, 'centroide': 1}
    result = list(collection.find(where, projection).sort('nombre', pymongo.ASCENDING))
    return jsonify(result)

# @bp.route('/provincia/<id>')
# def provincias(id):
#     collection = get_mongo()['Provincias']
#     where = {'id': id}
#     projection = {"_id": 0}
#     result = list(collection.find(where,projection))
#     return jsonify(result)

@bp.route('/sector/<sector>')
def escuelas_por_sector(sector):
    collection = get_mongo()['Escuelas']
    where = {'Sector': sector}
    projection = {"_id": 0,}
    result = list(collection.find(where,projection))
    return jsonify(result)

@bp.route('/codpos/<codpos>')
def escuelas_por_codpos(codpos):
    collection = get_mongo()['Escuelas']
    where = {'CP': codpos}
    projection = {"_id": 0,}
    result = list(collection.find(where,projection))
    return jsonify(result)

#@bp.route('/tiposeducacion/<id>')
#def tipos_educacion_por_escuela(id):
#    collection = get_mongo()['TiposEducacion']
#    where = {'CUE Anexo': id}
#    projection = {'_id': 0}
#    result = list(collection.find(where, projection))
#    return jsonify(result)
@bp.route('/tiposeducacion/<id>')
def tipos_educacion_por_escuela(id):
    where = {'CUE Anexo': id}
    #projection = {'_id': 0}
    return get_data('TiposEducacion', where)
    
@bp.route('/provincia/<id>')
def provincias(id):
    where = {'id': id}
    return get_data('Provincias', where)

def get_data(str_collection, obj_where, obj_projection={"_id":0}):
    """
    Va a la DB y retorna los datos
    """
    collection = get_mongo()[str_collection]
    result = list(collection.find(obj_where, obj_projection))
    return jsonify(result)