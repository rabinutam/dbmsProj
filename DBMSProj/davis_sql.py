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
