from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for
)
from werkzeug.exceptions import abort
import pymongo

from tuto.auth import login_required
from tuto.mongo import get_db

bp = Blueprint('escuelas', __name__, url_prefix='/escuelas')

def getProvincias():
    collection = g.get_db()['Escuelas']['Escuelas']
    result = collection.distinct('Jurisdicción')
    return result

@bp.route('/ambitos')
def ambitos():
    collection = g.get_db()['Escuelas']
    result = collection.distinct("Ámbito")
    return result

@bp.route('/sectores')
def sectores():
    get_db()
    collection = g.mongo()['Escuelas']['Escuelas']
    result = collection.distinct('Sector')
    return result

@bp.route('/provincias')
def provincias_full():
    DB = g.get_db()
    print(DB)
    collection = DB['Esceulas']['Provincias']
    projection = {"_id": 0}
    result = list(collection.find({}, projection).sort('nombre', pymongo.ASCENDING))
    print(result)
    return result

@bp.route('/pcias')
def provincias(id):
    collection = g.get_db()['Provincias']
    projection = {"_id": 0}
    result = list(collection.find({'id': id},projection))
    return result
