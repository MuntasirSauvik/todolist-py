from . import models


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('mark_complete', '/markComplete')
    config.add_route('about', '/about')
    config.add_route('delete', '/delete')
    config.add_route('add_item', '/addItem')
    config.add_route('custom_list_name', '/{customListName}')

