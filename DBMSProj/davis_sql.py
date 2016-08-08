'''
sql methods
'''

import logging
import os
import re
import sys
import traceback

BASE_DIR_ABS = os.path.dirname(os.path.abspath(__file__))
DATA_DIR_ABS = os.path.join(BASE_DIR_ABS, 'data')
LOG_FILE = os.path.join(BASE_DIR_ABS, 'log', 'sql.log')

sys.path.append(BASE_DIR_ABS)

from lib.file_helper import FileHelper

# logger.TODO have its own module
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(message)s')
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class SQLError(Exception):
    def __init__(self, message):
        super(SQLError, self).__init__(message)


class SQL(object):
    fh = FileHelper()

    @staticmethod
    def _get_clean_cli(cli):
        cli = cli.strip().lower()
        cli = cli.rstrip(';')
        if not cli:
            raise SQLError('SQL syntax Error. Incomplete query.')
        return cli


    @staticmethod
    def _get_filter(filter_text):
        '''WHERE clause filter
        now, support and and operator: = only
        TODO include other operators and logic
        '''

        filter_text = filter_text.strip()
        if 'and' in filter_text:
            items = filter_text.split('and')
        else:
            items = [filter_text]

        dfilter = {}
        for item in items:
            if '>=' in item:
                key, val = [_.strip() for _ in item.split('>=')]
                key = '{0}_gte'.format(key)
            elif '<=' in item:
                key, val = [_.strip() for _ in item.split('<=')]
                key = '{0}_lte'.format(key)
            elif '>' in item:
                key, val = [_.strip() for _ in item.split('>')]
                key = '{0}_gt'.format(key)
            elif '<' in item:
                key, val = [_.strip() for _ in item.split('<')]
                key = '{0}_lt'.format(key)
            elif '=' in item:
                key, val = [_.strip() for _ in item.split('=')]
            dfilter[key] = val
        return dfilter


    @staticmethod
    def get_tbl_columns(rest):
        '''Parse rest for column data
        '''

        columns = []
        rest = rest.strip().lstrip('(').rstrip(')').strip()
        cols = [_.strip() for _ in rest.split(',')]
        for col in cols:
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


    def show(self, cli):
        '''show tables, databases
        '''
        logger.info('{0} {1};'.format('show', cli))

        try:
            cli = self._get_clean_cli(cli)

            if cli == 'tables':
                file_path = self._get_table_abs('tables')
                columns = ['table_name']
                result = self.fh.view_row(file_path=file_path, columns=columns)
            elif cli == 'databases':
                msg = 'Unsupported or not implemented or syntax error: {0}'.format(cli)
                raise SQLError(msg)
            else:
                raise SQLError('SQL Syntax Error')
        except SQLError:
            raise # just raise
        except:
            print traceback.format_exc()
            raise SQLError('SQL syntax error')
        return result


    def drop(self, cli):
        '''drop table, database
        '''
        logger.info('{0} {1};'.format('drop', cli))

        try:
            cli = self._get_clean_cli(cli)
            drop_type, rest = cli.split(' ', 1)

            if drop_type == 'table':
                table_name = rest.strip()
                file_path = self._get_table_abs(table_name)
                result = self.fh.delete_file(file_path=file_path)
            elif drop_type == 'database':
                msg = 'Unsupported or not implemented or syntax error: {0}'.format(drop_type)
                raise SQLError(msg)
            else:
                raise SQLError('SQL Syntax Error')
        except SQLError:
            raise # just raise
        except:
            print traceback.format_exc()
            raise SQLError('SQL syntax error')
        return result


    def select(self, cli):
        logger.info('{0} {1};'.format('select', cli))

        try:
            cli = self._get_clean_cli(cli)

            # Parse
            dfilter = {}
            table_name = None

            # optional WHERE clause
            if 'where' in cli:
                cli, filter_text = [_.strip() for _ in cli.split('where')]
                dfilter = self._get_filter(filter_text)

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
            #print select_data
            file_path = self._get_table_abs(table_name)
            result = self.fh.view_row(file_path=file_path, rowid=dfilter, columns=columns)
        except SQLError:
            raise # just raise
        except:
            print traceback.format_exc()
            raise SQLError('SQL syntax error')
        return result


    @staticmethod
    def _get_table_abs(table_name):
        table_file = '{0}.tbl'.format(table_name)
        table_file_abs = os.path.join(DATA_DIR_ABS, table_file)
        return table_file_abs


    def _create_table(self, rest):
        table_name, rest = rest.split(' ', 1)
        if not table_name:
            raise SQLError('SQL syntax error: missing table name')
        table_file_abs = self._get_table_abs(table_name)
        columns = self.get_tbl_columns(rest)

        column_names = [_['column_name'] for _ in columns]
        content = [column_names]

        # check table already exists and create table
        self.fh.create_file(file_path=table_file_abs, content=content)

        # add to tables (insert or create)
        tables_path_abs = os.path.join(DATA_DIR_ABS, 'tables.tbl')
        row = [table_name, '']
        try:
            self.fh.insert_row(file_path=tables_path_abs, row=row)
        except:
            # at first table creation
            content = [
                    ['table_name', 'primary_key'],
                    row
                    ]
            self.fh.create_file(file_path=tables_path_abs, content=content)


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
        logger.info('{0} {1};'.format('create', cli))

        try:
            cli = self._get_clean_cli(cli)

            # Parse
            create_item, rest = cli.split(' ', 1)

            if create_item == 'table':
                self._create_table(rest)
            elif create_item == 'database':
                raise SQLError('Not Implemented Error: create database is not implemented yet')
                #self._create_db(rest)
            else:
                raise SQLError('SQL syntax error: Unsupported create item: {0}'.format(create_item))
        except SQLError:
            raise # just raise
        except:
            print traceback.format_exc()
            raise SQLError('SQL syntax error')


    def insert(self, cli):
        '''
        **SQL**
            - INSERT INTO table_name (col1, col2, ...) VALUES (val1, val2, ...);
            - INSERT INTO table_name VALUES(val1, val2, ...);

        **Example**
            - INSERT INTO singer (id name) VALUES (50, 'ravi');
        '''
        logger.info('{0} {1};'.format('insert', cli))

        try:
            cli = self._get_clean_cli(cli)

            # Parse
            into, rest = cli.split(' ', 1)
            if into != 'into':
                raise SQLError('SQL syntax error')

            table_name, rest = rest.split(' ', 1)
            if not table_name:
                raise SQLError('SQL syntax error: missing table name')

            print rest
            if not 'values' in rest:
                raise SQLError('SQL syntax error: missing values')

            left, values = rest.split('values')
            values = values.strip().lstrip('(').rstrip(')')
            values = values.split(',')
            values = [_.strip().strip('"').strip("'").strip() for _ in values]

            table_file_abs = self._get_table_abs(table_name)

            header = self.fh.view_header(file_path=table_file_abs)
            if len(header) != len(values):
                msg = 'column count does not match value count'
                raise SQLError('SQL syntax error: {0}'.format(msg))

            row = dict(zip(header, values))
            self.fh.insert_row(file_path=table_file_abs, row=row)
        except SQLError:
            raise # just raise
        except:
            print traceback.format_exc()
            raise SQLError('SQL syntax error')
