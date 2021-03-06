#import cmd
try:
    from cmd2 import Cmd
except:
    from cmd import Cmd

import sys
from davis_sql import SQL, SQLError

ENV = 'dev'

class SqlShell(Cmd):
    intro = '''Welcome to the DaviSQL monitor.  Commands end with ;
        '''
    prompt = 'davisql> '
    sql = SQL()
    multilineCommands = ['select', 'create']

    def do_show(self, arg):
        'show tables, databases'

        try:
            result = self.sql.show(arg)
            self._print_result(result)
        except SQLError as e:
            print e
        except Exception as e:
            print 'Internal Error'
            if ENV=='dev':
                raise

    def do_drop(self, arg):
        'drop table, database'

        try:
            self.sql.drop(arg)
        except SQLError as e:
            print e
        except Exception as e:
            print 'Internal Error'
            if ENV=='dev':
                raise

    def do_select(self, arg):
        'read data'

        try:
            result = self.sql.select(arg)
            self._print_result(result)
        except SQLError as e:
            print e
        except Exception as e:
            print 'Internal Error'
            if ENV=='dev':
                raise


    def do_create(self, arg):
        'create table, database etc'

        try:
            self.sql.create(arg)
        except SQLError as e:
            print e
        except Exception as e:
            print 'Internal Error'
            if ENV=='dev':
                raise
        else:
            print 'Query OK'


    def do_insert(self, arg):
        'insert row into table'

        try:
            self.sql.insert(arg)
        except SQLError as e:
            print e
        except Exception as e:
            print 'Internal Error'
            if ENV=='dev':
                raise
        else:
            print 'Query OK'


    def do_update(self, arg):
        'insert row into table'

        try:
            self.sql.update(arg)
        except SQLError as e:
            print e
        except Exception as e:
            print 'Internal Error'
            if ENV=='dev':
                raise
        else:
            print 'Query OK'


    def do_delete(self, arg):
        'insert row into table'

        try:
            self.sql.delete(arg)
        except SQLError as e:
            print e
        except Exception as e:
            print 'Internal Error'
            if ENV=='dev':
                raise
        else:
            print 'Query OK'


    def do_exit(self, arg):
        'exit dbms'
        print('Thank you for using davisql')
        return True


    def emptyline(self):
        '''called when empty line is entered
        if this is not overriden here, repeats last non empty cmd
        '''
        print '\n'

    def do_EOF(self, arg):
        if arg.endswith(';'):
            return True
        else:
            return False

    def _print_result(self, data=None):
        '''print data as a table
        '''

        if not data:
            return

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
