'''
sql methods
'''

import re
import traceback

class SQLError(Exception):
    def __init__(self, message):
        super(SQLError, self).__init__(message)

class SQL(object):
    @staticmethod
    def _get_clean_cli(cli):
        cli = cli.strip().lower()
        cli = cli.rstrip(';')
        if not cli:
            raise SQLError('SQL syntax Error. Incomplete query.')
        return cli

    @staticmethod
    def get_tbl_columns(rest):
        '''Parse rest for column data
        '''

        columns = []
        rest = rest.strip().lstrip('(').rstrip(')').strip()
        cols = [_.strip() for _ in rest.split(',')]
        for col in cols:
            print col
            size = None
            is_pk = False
            pk_found = False
            column_name, col_rest = col.split(' ', 1)
            col_rest = col_rest.strip()
            if re.match('.*primary key.*', col_rest):
                if not pk_found:
                    is_pk = True
                    pk_found = True
                col_rest = col_rest.replace('primary key', '').strip()
            if re.match('.*varchar.*', col_rest):
                data_type = 'varchar'
                col_rest = col_rest.replace('varchar', '').strip()
            elif re.match('.*int.*', col_rest):
                data_type = 'int'
                col_rest = col_rest.replace('int', '').strip()

            print '===> col_rest = {0}'.format(col_rest)
            m1 = re.match('(.*\(\s*)(\d+)(\s*.*)', col_rest)
            if m1:
                groups = m1.groups()
                size = int(groups[1])
                col_rest = groups[0] + groups[2]
                col_rest = col_rest.replace('(', '')
                col_rest = col_rest.replace(')', '')
                col_rest = col_rest.strip()
            if col_rest:
                msg = 'Unsupported or not implemented or syntax error: {0}'.format(col_rest)
                raise SQLError(msg)

            if data_type == 'varchar' and not size:
                size = 255 #default
            elif data_type == 'int':
                size = 2 # just supporting 2 for now

            column = {
                    'column_name': column_name,
                    'data_type': data_type,
                    'size': size,
                    'primary_key': is_pk
                    }
            columns.append(column)
        return columns

    def select(self, cli):
        try:
            cli = self._get_clean_cli(cli)
            #print '@ SQL.select, {0}'.format(cli)

            # Parse
            dfilter = {}
            table_name = None

            # optional WHERE clause
            if 'where' in cli:
                cli, filter_text = [_.strip() for _ in cli.split('where')]
                # now, support and and operator: = only
                # TODO include other operators and logic
                filter_text = filter_text.strip()
                if 'and' in filter_text:
                    items = filter_text.split('and')
                else:
                    items = [filter_text]
                for item in items:
                    key, val = item.split('=')
                    dfilter[key.strip()] = val.strip()

            cli = cli.strip()
            if 'from' in cli:
                cli, table_name = [_.strip() for _ in cli.split('from')]
            else: # missing from clause
                raise SQLError('SQL suntax error: missing from clause')

            if not table_name: # empty table name
                raise SQLError('SQL suntax error: missing table name')

            cli = cli.strip()
            if not cli:
                raise SQLError('SQL syntax error: missing columns')
            elif cli == '*':
                columns = 'all'
            else:
                columns = [_.strip() for _ in cli.split(',')]
            select_data = {
                    'table_name': table_name,
                    'data_filter': dfilter,
                    'columns': columns
                    }
            print select_data
        except SQLError:
            raise # just raise
        except:
            print traceback.format_exc()
            raise SQLError('SQL syntax error')


    def create(self, cli):
        '''
        **SQL**
            - create table
                CREATE TABLE table_name (
                    column_name1 INT PRIMARY KET,
                    column_name VARCHAR(size) [NOT NULL],
                    column_name VARCHAR(size) [NOT NULL],
                    ...
                );

        **Example**
            - create table singer ( id int primary key, name varchar(50) );
        '''

        try:
            cli = self._get_clean_cli(cli)
            #print '@ SQL.create, {0}'.format(cli)

            # Parse
            create_item, rest = cli.split(' ', 1)

            if create_item == 'table':
                table_name, rest = rest.split(' ', 1)
                if not table_name:
                    raise SQLError('SQL syntax error: missing table name')
                columns = self.get_tbl_columns(rest)
                print columns
                # add to tables, and create table
                # check table already exists
            elif create_item == 'database':
                raise SQLError('Not Implemented Error: create database is not implemented yet')
            else:
                raise SQLError('SQL syntax error: Unsupported create item: {0}'.format(create_item))
        except SQLError:
            raise # just raise
        except:
            print traceback.format_exc()
            raise SQLError('SQL syntax error')
