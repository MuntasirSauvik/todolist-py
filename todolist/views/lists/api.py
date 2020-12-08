from pyramid.view import view_config
from pyramid.renderers import render_to_response

from ... import models
from . import (
    find_list_obj,
    serialize_list,
    serialize_item,
    create_default_list
)


@view_config(route_name='lists.get', renderer='json')
def lists_get(request):
    list_name = request.matchdict['list_name']
    list_obj = find_list_obj(list_name, request)
    if list_obj is None:
        list_obj = create_default_list(list_name, request)

    return {'result': True,
            'object': serialize_list(list_obj)}


@view_config(route_name='lists.purge_completed', renderer='json')
def lists_purge_completed(request):
    list_name = request.matchdict['list_name']
    list_obj = find_list_obj(list_name, request)
    if list_obj is not None:
        items = request.dbsession.query(models.Item).filter_by(list_id=list_obj.id).filter_by(completed=True).all()
        for i in items:
            request.dbsession.delete(i)
        request.dbsession.flush()
        response_data = {'result': True,
                         'object': serialize_list(list_obj)}
        return response_data
    else:
        response_data = {'result': False,
                         'message': 'List not found'}
        response = render_to_response('json', response_data, request=request)
        response.status_int = 404
        return response


@view_config(route_name='lists.items.add', renderer='json')
def lists_items_add(request):
    list_name = request.matchdict['list_name']
    list_obj = find_list_obj(list_name, request)
    if list_obj is not None:
        item = request.params.get('newItem')
        new_item = models.Item()
        new_item.item_text = item
        new_item.list_id = list_obj.id
        request.dbsession.add(new_item)
        request.dbsession.flush()
        response_data = {'result': True,
                         'object': serialize_list(list_obj)}
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
