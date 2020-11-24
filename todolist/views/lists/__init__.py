from ... import models


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


def find_list_obj(list_name, request):
    normalize_name = list_name.lower()
    return request.dbsession.query(models.List).filter_by(name=normalize_name).scalar()


def create_default_list(list_name, request):
    if list_name is not None:
        new_list = models.List()
        new_list.name = list_name.lower()
        request.dbsession.add(new_list)
        request.dbsession.flush()

        default_strings = ["Welcome to your todolist!",
                           "Hit the + button to add a new item.",
                           "Welcome to your todolist!"]
        for text in default_strings:
            new_item = models.Item()
            new_item.item_text = text
            new_item.list_id = new_list.id
            request.dbsession.add(new_item)
        request.dbsession.flush()
        data = request.dbsession.query(models.List).filter_by(id=new_list.id).scalar()
        return data
    else:
        raise NotImplementedError()
