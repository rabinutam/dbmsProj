import cmd, sys
from davis_sql import SQL, SQLError

devEnv = True

class SqlShell(cmd.Cmd):
    intro = '''
    Welcome to the DaviSQL monitor.  Commands end with ;
    '''
    prompt = 'davisql> '
    sql = SQL()

    def do_select(self, arg):
        'read data'
        try:
            self.sql.select(arg)
            print 'select', arg
            self._print_result()
        except SQLError as e:
            print e
        except Exception as e:
            print 'Internal Error'
            if devEnv:
                raise

    def do_create(self, arg):
        'create table, database etc'
        print 'create', arg

    def do_exit(self, arg):
        'exit dbms'
        print('Thank you for using davisql')
        #bye()
        return True

    def _print_result(self, data=None):
        '''print data as a table
        '''

        # Fake data
        data = [
                ['col1', 'col2', 'col3', 'col4', 'col5'],
                ['example', 'data', 'fixit', 'later', ''],
                ['if', 'you', 'cannot', 'now', 'cool']
                ]

        cols_width = self._get_cols_width(data=data)
        line_sep = self._get_line_sep(cols_width)

        # Print Block
        print line_sep
        for i in xrange(len(data)):
            parts = []
            di = data[i]
            for j in xrange(len(cols_width)):
                wc = cols_width[j] + 1
                parts.append(' {0}'.format(di[j].ljust(wc)))
            line = '|'.join(parts)
            line = '|{0}|'.format(line)
            print line
            if i == 0: #header
                print line_sep
        print line_sep


    @staticmethod
    def _get_line_sep(cols_width):
        # sum(cols_width) + 3 * len(cols_width) -1 + 2
        wl = sum(cols_width) + 3 * len(cols_width) + 1
        return wl * '-'


    @staticmethod
    def _get_cols_width(data=None):
        # Get columns
        cols = []
        for i in xrange(len(data[0])):
            col = [_[i] for _ in data]
            cols.append(col)

        # Get columns width
        cols_width = [max(len(_) for _ in col) for col in cols]
        return cols_width



if __name__ == '__main__':
    SqlShell().cmdloop()
