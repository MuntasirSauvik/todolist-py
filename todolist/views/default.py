from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models

# Legacy Code
# @view_config(route_name='home', renderer='../templates/list.mako')
# def my_view(request):
#         next_url = request.route_url('list_name', listName='Home')
#         return HTTPFound(location=next_url)

@view_config(route_name='home', renderer='../templates/app.mako')
def my_view(request):
    return {}
