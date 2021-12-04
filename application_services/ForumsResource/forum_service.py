from application_services.BaseApplicationResource import BaseRDBApplicationResource
from database_services.RDBService import RDBService as RDBService


class ForumResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    def find_by_template(cls, template, limit=None, offset=None, field_list=None):
        res = RDBService.find_by_template("ForumInfo", "Forum", template, limit, offset, field_list)
        return res
    
    @classmethod
    def find_by_template_fields(cls, fields, template):
        res = RDBService.find_by_template_fields("ForumInfo", "Forum", fields, template)
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

    @classmethod
    def find_linked_user(cls, template):
        res = RDBService.find_linked_user("UserInfo", "ForumInfo", "User", "Forum", template)
        return res

    @classmethod
    def find_linked_data(cls, target, template, key):
        res = RDBService.find_linked_data("ForumInfo", "Forum", "Game", target, template, key)
        return res

    @classmethod
    def get_total_num(cls, db_schema, table_name):
        res = RDBService.get_total_num(db_schema, table_name)
        return res
