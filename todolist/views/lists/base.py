from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ... import models
from . import (
    find_list_obj,
    create_default_list
)


@view_config(route_name='add_item')
def add_item(request):
    list_name = request.params['listName']
    found_list = find_list_obj(list_name, request)
    item = request.params['newItem']
    new_item = models.Item()
    new_item.completed = False
    new_item.item_text = item
    new_item.list_id = found_list.id
    request.dbsession.add(new_item)
    request.dbsession.flush()
    return HTTPFound(location=request.route_url('list_name', listName=list_name))


@view_config(route_name='list_name')
def list_name(request):
    list_name = request.matchdict['listName']
    found_list = find_list_obj(list_name, request)
    if found_list is not None:
        data = {
                    "listName": list_name.capitalize(),
                    "res": request.dbsession.query(models.Item).filter_by(list_id=found_list.id).all()
        }
    else:
        new_list = create_default_list(list_name, request);
        data = {
                   "listName": list_name,
                   "res": request.dbsession.query(models.Item).filter_by(list_id=new_list.id).all()
        }
    return render_to_response("todolist:templates/list.mako", data, request=request)


@view_config(route_name='mark_complete')
def mark_complete(request):
    item_id = request.params['itemId']
    completed = request.params.get('completed') is not None
    item = request.dbsession.query(models.Item).filter_by(id=item_id).one()
    item.completed = bool(completed)
    request.dbsession.flush()
    return HTTPFound(location=request.route_url('list_name', listName=request.params['listName']))


@view_config(route_name='delete')
def delete(request):
    list_name = request.params['listName']
    normalize_name = list_name.lower()

    items = request.dbsession.query(models.Item) \
        .join(models.List) \
        .filter(models.List.name == normalize_name) \
        .filter(models.Item.completed == True) \
        .all()

    for i in items:
        request.dbsession.delete(i)
    request.dbsession.flush()
    return HTTPFound(location=request.route_url('list_name', listName=list_name))
