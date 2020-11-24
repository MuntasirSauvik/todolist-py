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


def find_list_obj(request):
    list_name = request.matchdict['list_name']
    normalize_name = list_name.lower()
    obj = request.dbsession.query(models.List).filter_by(name=normalize_name).scalar()
    return obj


@view_config(route_name='lists.get', renderer='json')
def lists_get(request):
    obj = find_list_obj(request)

    return {'result': True,
            'object': serialize_list(obj)}


@view_config(route_name='lists.purge_completed', renderer='json')
def lists_purge_completed(request):
    obj = find_list_obj(request)
    if obj is not None:
        items = request.dbsession.query(models.Item).filter_by(list_id=obj.id).filter_by(completed=True).all()
        for i in items:
            request.dbsession.delete(i)
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


@view_config(route_name='lists.items.add', renderer='json')
def lists_items_add(request):
    obj = find_list_obj(request)
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
