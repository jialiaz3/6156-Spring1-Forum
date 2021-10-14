from application_services.BaseApplicationResource import BaseRDBApplicationResource
from database_services.RDBService import RDBService as RDBService

class ForumResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        pass


    # @classmethod
    # def get_by_template(cls, template):
    #     res = d_service.find_by_template('aaaaaF21E6156', 'users', template, None)
    #     return res

    @classmethod
    def find_by_template(cls, template):
        res = RDBService.find_by_template('ForumInfo', 'Forum', template)
        return res


    @classmethod
    def create(cls, create_data):
        res = RDBService.create("ForumInfo", "Forum", create_data)
        return res

    @classmethod
    def update(cls, select_data, update_data):
        res = RDBService.update("ForumInfo", "Forum", select_data, update_data)
        return res

    @classmethod
    def delete(cls, template):
        res = RDBService.delete("ForumInfo", "Forum", template)
        return res