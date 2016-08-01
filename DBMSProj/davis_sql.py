'''
main
'''

class SQLError(Exception):
    def __init__(self, message):
        super(SQLError, self).__init__(message)

class SQL(object):
    @staticmethod
    def _get_clean_cli(cli):
        cli = cli.strip().lower()
        if not cli:
            raise SQLError('SQL syntax Error. Incomplete query.')
        return cli

    def select(self, cli):
        cli = self._get_clean_cli(cli)
        print '@ SQL.select, cli'.format(cli)

        # Parse
        dfilter = None
        table_name = None
        if 'where' in cli:
            cli, dfilter = [_.strip() for _ in cli.split('where')]
        if 'from' in cli:
            cli, table_name = [_.strip() for _ in cli.split('from')]
        else:
            raise SQLError('missing table name')

        if not table_name:
            raise SQLError('missing table name')


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

        '''
        cli = self._get_clean_cli(cli)
        print '@ SQL.select, cli'.format(cli)

        # Parse
        columns = None
        table_name = None

        create_item, rest = cli.split(' ', 1)

        if create_item == 'table':
            table_name, rest = rest.split(' ', 1)
            if not table_name:
                raise SQLError('missing table name')
        elif create_item == 'database':
            raise SQLError('create database is not implemented yet')
        else:
            raise SQLError('SQL syntax error')
