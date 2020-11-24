from . import models


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('mark_complete', '/markComplete')
    config.add_route('about', '/about')
    config.add_route('delete', '/delete')
    config.add_route('add_item', '/addItem')

    # API Routes (Lists)
    config.add_route('lists.get', '/api/lists/get/{list_name}')
    config.add_route('lists.purge_completed', '/api/lists/{list_name}/purge_completed')

    # API Routes (List Items)
    config.add_route('lists.items.add', '/api/lists/{list_name}/items/add')
    config.add_route('lists.items.mark_complete', '/api/lists/{list_name}/items/{item_id}/mark_complete')

    # Catch-all route
    config.add_route('list_name', '/{listName}')