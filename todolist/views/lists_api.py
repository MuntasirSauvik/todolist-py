from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.renderers import render_to_response
import transaction

from .. import models


def serialize_list(list_obj):
    obj_serialized = {'id': list_obj.id,
                      'name': list_obj.name,
                      'items': []}

    for item in list_obj.items:
        obj_serialized['items'].append(serialize_item(item))

    return obj_serialized


def serialize_item(item_obj):
    item_obj_serialized = {'id': item_obj.id,
                           'item_text': item_obj.item_text,
                           'completed': item_obj.completed}
    return item_obj_serialized


@view_config(route_name='lists.get', renderer='json')
def lists_get(request):
    list_name = request.matchdict['list_name']
    normalizeName = list_name.lower()
    obj = request.dbsession.query(models.List).filter_by(name=normalizeName).scalar()

    return {'result': True,
            'object': serialize_list(obj)}


@view_config(route_name='lists.purge_completed', renderer='json')
def lists_purge_completed(request):
    pass


@view_config(route_name='lists.items.add', renderer='json')
def lists_items_add(request):
    listName = request.matchdict['list_name']
    normalizeName = listName.lower()
    obj = request.dbsession.query(models.List).filter_by(name=normalizeName).scalar()
    if obj is not None:
        item = request.params.get('newItem')
        new_item = models.Item()
        new_item.item_text = item
        new_item.list_id = obj.id
        request.dbsession.add(new_item)
        request.dbsession.flush()
        response_data = {'result': True,
                         'object': serialize_list(obj)}
        return response_data
    else:
        response_data = {'result': False,
                         'message': 'List not found'}
        response = render_to_response('json', response_data, request=request)
        response.status_int = 404
        return response


@view_config(route_name='lists.items.mark_complete', renderer='json')
def lists_items_mark_complete(request):
    listName = request.matchdict['list_name']
    item_id = request.matchdict['item_id']
    completed = request.params.get('completed') == '1'
    item = request.dbsession.query(models.Item).filter_by(id=item_id).scalar()
    if item is not None:
        item.completed = completed
        request.dbsession.flush()
        response_data = {'result': True,
                         'object': serialize_item(item)}
        return response_data
    else:
        response_data = {'result': False,
                         'message': 'Item not found'}
        response = render_to_response('json', response_data, request=request)
        response.status_int = 404
        return response



# @view_config(route_name='add_item')
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


# @view_config(route_name='list_name')
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


# @view_config(route_name='mark_complete')
def mark_complete(request):
    listName = request.params['listName']
    item_id = request.params['itemId']
    completed = request.params.get('completed') is not None
    item = request.dbsession.query(models.Item).filter_by(id=item_id).one()
    item.completed = bool(completed)
    request.dbsession.flush()
    return HTTPFound(location=request.route_url('list_name', listName=listName))


# @view_config(route_name='delete')
def delete(request):
    listName = request.params['listName']
    items = request.dbsession.query(models.Item).filter_by(completed=True).all()
    for i in items:
        request.dbsession.delete(i)
    request.dbsession.flush()
    return HTTPFound(location=request.route_url('list_name', listName=listName))
