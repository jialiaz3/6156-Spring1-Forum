from application_services.BaseApplicationResource import BaseRDBApplicationResource
import database_services.RDBService as d_service
from database_services.RDBService import RDBService as d_service


class UserResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    def get_data_resource_info(cls):
        return 'aaaaaF21E6156', 'users'

    # @classmethod
    # def get_by_template(cls, template):
    #     res = d_service.find_by_template('aaaaaF21E6156', 'users', template, None)
    #     return res

    @classmethod
    def get_by_template(cls, template):
        res = d_service.find_by_template('ForumInfo', 'Forum', template)
        return res