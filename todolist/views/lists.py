from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.renderers import render_to_response
import transaction

from .. import models


@view_config(route_name='add_item')
def add_item(request):
    item = request.params['newItem']
    new_item = models.Item()
    new_item.completed = False
    new_item.item_text = item
    new_item.list_id = 1
    request.dbsession.add(new_item)
    request.dbsession.flush()
    return HTTPFound(location=request.route_url('home'))


@view_config(route_name='list_name')
def list_name(request):
    listName = request.matchdict['listName']
    normalizeName = listName.lower()
    data = {
                "listName": listName,
                "res": request.dbsession.query(models.Item).all()
            }
    return render_to_response("todolist:templates/list.mako", data, request=request)


@view_config(route_name='mark_complete')
def mark_complete(request):
    item_id = request.params['itemId']
    completed = request.params['completed']
    item = request.dbsession.query(models.Item).filter_by(id=item_id).one()
    item.completed = bool(completed)
    request.dbsession.flush()
    return HTTPFound(location=request.route_url('home'))


# @view_config(route_name='delete')
# def delete(request):
#     item_id = request.params['itemId']
#     completed = request.params['completed']
#     item = request.dbsession.query(models.Item).filter_by(id=item_id).one()
#     item.completed = bool(completed)
#     request.dbsession.flush()
#     return HTTPFound(location=request.route_url('home'))
