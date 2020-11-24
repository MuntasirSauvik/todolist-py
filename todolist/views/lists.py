from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.renderers import render_to_response
import transaction

from .. import models


@view_config(route_name='add_item')
def add_item(request):
    listName = request.params['listName']
    normalizeName = listName.lower()
    foundList = request.dbsession.query(models.List).filter_by(name=normalizeName).scalar()
    item = request.params['newItem']
    new_item = models.Item()
    new_item.completed = False
    new_item.item_text = item
    new_item.list_id = foundList.id
    request.dbsession.add(new_item)
    request.dbsession.flush()
    return HTTPFound(location=request.route_url('list_name', listName=listName))


@view_config(route_name='list_name')
def list_name(request):
    listName = request.matchdict['listName']
    normalizeName = listName.lower()

    foundList = request.dbsession.query(models.List).filter_by(name=normalizeName).scalar()
    if foundList is not None:
        data = {
                    "listName": listName.capitalize(),
                    "res": request.dbsession.query(models.Item).filter_by(list_id=foundList.id).all()
        }
    else:
        new_list = models.List()
        new_list.name = normalizeName
        request.dbsession.add(new_list)
        request.dbsession.flush()
        new_item1 = models.Item()
        new_item1.item_text = "Welcome to your todolist!"
        new_item1.list_id = new_list.id
        request.dbsession.add(new_item1)
        new_item2 = models.Item()
        new_item2.item_text = "Hit the + button to add a new item."
        new_item2.list_id = new_list.id
        request.dbsession.add(new_item2)
        new_item3 = models.Item()
        new_item3.item_text = "Welcome to your todolist!"
        new_item3.list_id = new_list.id
        request.dbsession.add(new_item3)
        request.dbsession.flush()
        data = {
                   "listName": listName,
                   "res": request.dbsession.query(models.Item).filter_by(list_id=new_list.id).all()
        }
    return render_to_response("todolist:templates/list.mako", data, request=request)


@view_config(route_name='mark_complete')
def mark_complete(request):
    listName = request.params['listName']
    item_id = request.params['itemId']
    completed = request.params.get('completed') is not None
    item = request.dbsession.query(models.Item).filter_by(id=item_id).one()
    item.completed = bool(completed)
    request.dbsession.flush()
    return HTTPFound(location=request.route_url('list_name', listName=listName))


@view_config(route_name='delete')
def delete(request):
    listName = request.params['listName']
    normalizeName = listName.lower()

    items = request.dbsession.query(models.Item) \
        .join(models.List) \
        .filter(models.List.name==normalizeName) \
        .filter(models.Item.completed==True) \
        .all()

    #foundList = request.dbsession.query(models.List).filter_by(name=normalizeName).scalar()
    #items = request.dbsession.query(models.Item).filter_by(list_id=foundList.id).filter_by(completed=True).all()
    for i in items:
        request.dbsession.delete(i)
    request.dbsession.flush()
    return HTTPFound(location=request.route_url('list_name', listName=listName))
