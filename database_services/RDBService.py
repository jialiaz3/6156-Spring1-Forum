import pymysql
import json
import logging

import middleware.context as context

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class RDBService:

    def __init__(self):
        pass

    @classmethod
    def _get_db_connection(cls):

        db_connect_info = context.get_db_info()

        logger.info("RDBService._get_db_connection:")
        logger.info("\t HOST = " + db_connect_info['host'])

        db_info = context.get_db_info()

        db_connection = pymysql.connect(
            **db_info,
            autocommit=True
        )
        return db_connection

    @classmethod
    def run_sql(cls, sql_statement, args, fetch=False):

        conn = RDBService._get_db_connection()

        try:
            cur = conn.cursor()
            res = cur.execute(sql_statement, args=args)
            if fetch:
                res = cur.fetchall()
        except Exception as e:
            conn.close()
            raise e

        return res

    @classmethod
    def get_by_prefix(cls, db_schema, table_name, column_name, value_prefix):

        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name + " where " + \
              column_name + " like " + "'" + value_prefix + "%'"
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def _get_where_clause_args(cls, template):

        terms = []
        args = []
        clause = None

        if template is None or template == {}:
            clause = ""
            args = None
        else:
            for k, v in template.items():
                terms.append(k + "=%s")
                args.append(v)

            clause = " where " + " AND ".join(terms)

        return clause, args

    @classmethod
    def find_by_template(cls, db_schema, table_name, template):

        wc, args = RDBService._get_where_clause_args(template)

        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name + " " + wc
        res = cur.execute(sql, args=args)
        res = cur.fetchall()

        conn.close()

        return res
    
    @classmethod
    def find_by_template_fields(cls, db_schema, table_name, fields,template):

        wc, args = RDBService._get_where_clause_args(template)
        conn = RDBService._get_db_connection()
        cur = conn.cursor()
        if fields:
            sql = "select " + fields +" from " + db_schema + "." + table_name + wc
        else:
            sql = "select * from " + db_schema + "." + table_name + wc
        print(sql)
        res = cur.execute(sql, args=args)
        res = cur.fetchall()
        conn.close()

        return res

    @classmethod
    def create(cls, db_schema, table_name, create_data):

        cols = []
        vals = []
        args = []

        for k, v in create_data.items():
            cols.append(k)
            vals.append('%s')
            args.append(v)

        cols_clause = "(" + ",".join(cols) + ")"
        vals_clause = "values (" + ",".join(vals) + ")"

        sql_stmt = "insert into " + db_schema + "." + table_name + " " + cols_clause + \
                   " " + vals_clause

        res = RDBService.run_sql(sql_stmt, args)
        return res

    @classmethod
    def update(cls, db_schema, table_name, select_data, update_data):

        select_clause, select_args = RDBService._get_where_clause_args(select_data)

        cols = []
        args = []

        for k, v in update_data.items():
            cols.append(k + "=%s")
            args.append(v)
        clause = "set " + ", ".join(cols)
        args = args + select_args

        sql_stmt = "update " + db_schema + "." + table_name + " " + clause + \
                   " " + select_clause

        res = RDBService.run_sql(sql_stmt, args)
        return res

    @classmethod
    def delete(cls, db_schema, table_name, template):
        clause, args = RDBService._get_where_clause_args(template)
        sql_stmt = "delete from " + db_schema + "." + table_name + " " + clause
        res = RDBService.run_sql(sql_stmt, args)
        return res

    @classmethod
    def find_linked_user(cls, user_schema, forum_schema, user_table, forum_table, template):
        wc, args = RDBService._get_where_clause_args(template)
        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        target_id = f'select {forum_schema}.{forum_table}.userID from {forum_schema}.{forum_table} {wc}'
        sql = f'select * from {user_schema}.{user_table} where {user_schema}.{user_table}.id = ({target_id})'

        res = cur.execute(sql, args)
        res = cur.fetchall()

        conn.close()

        return res
