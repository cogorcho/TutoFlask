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

bp = Blueprint('geo', __name__, url_prefix='/geo')

@bp.route('/provincias')
def provincias_full():
    return getdata('Provincias')


@bp.route('/departamentos')
def deptos_full():
    return getdata('Departamentos')


@bp.route('/municipios')
def munis_full():
    return getdata('Municipios')


@bp.route('/localidades')
def locas_full():
    return getdata('Localidades')


@bp.route('/departamentos/provincia/<id>')
def deptos_por_provincias(id):
    return getdata('Departamentos', {'provincia.id': id})


@bp.route('/municipios/provincia/<id>')
def munis_por_provincia(id):
    return getdata('Municipios', {'provincia.id': id})


@bp.route('/localidades/provincia/<id>')
def locas_por_provincia(id):
    return getdata('Localidades', {'provincia.id': id})

def getdata(coll, where={}):
    collection = get_mongo()[coll]
    projection = {"_id": 0}
    result = list(collection.find(where, projection).sort('nombre', pymongo.ASCENDING))
    return jsonify(result)