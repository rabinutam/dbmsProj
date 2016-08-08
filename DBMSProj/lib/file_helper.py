import os
import shutil
import sys

#from char_translator import Translator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


class FileHelper(object):
    '''
    **Methods**
        - view_file
        - create_file
        - delete_file
        - [update file]
            - insert_row
            - update_row
            - delete_row
    '''

    def read(self, file_path='', sep=None, comment='#', header_only=False):
        '''reads file and returns header and body

        **Parameters**
            -file_path: abs file path
            -sep: sep=None is same as empty space
            -comment: starts comment line, first comment is the header

        **Example file conent**
            #a, b, c
            1, 2, 1
            2, 0, 3
            ...

        **Example return*
            header = ['a', 'b', 'c']
            body   = [['1', '2', '1'], ['2', '0', '3'], ...]
        '''

        header, body = [], []

        with open(file_path) as rf:
            lines = rf.readlines()

            # Strip lines, take out empty lines
            xlines = []
            for line in lines:
                line = line.strip()
                if line:
                    xlines.append(line)
            lines = xlines

            if not lines:
                return header, body

            if lines[0].startswith(comment):
                header, body = lines[0], lines[1:]
                #take out comment char #, and split
                header = [_.strip() for _ in header[1:].split(sep)]
                if header_only:
                    return header
            else:
                body = lines

            body = [_ for _ in body if not _.startswith(comment)]
            body = [[v.strip() for v in l.split(sep)] for l in body]

        return header, body


    def write(self, file_path='', data=None, sep=None, mode='w'):
        '''reads file and returns header and body

        **Parameters**
            - file_path: abs file path
            - data

        **Example data*
            data [row, row ..]
            data = [
                ['#a', 'b', 'c'],
                ['1', '2', '1'],
                ['2', '0', '3'],
                ...
            ] OR 
            data = [
                '#a, b, c',
                '1, 2, 1',
                '2, 0 ,3'
            ]

        **Example file conent**
            #a, b, c
            1, 2, 1
            2, 0, 3
            ...
        '''

        if sep is None:
            sep = ' '
        else:
            sep = sep + ' '

        with open(file_path, mode) as fh:
            lines = []
            for di in data:
                if isinstance(di, (list, tuple)):
                    lines.append('{0}\n'.format(sep.join(di)))
                else:
                    lines.append('{0}\n'.format(di))
            fh.writelines(lines)


    def create_file(self, file_path=None, content=None, has_header=True):
        print 'Creating file: {0}'.format(file_path)
        try:
            self._does_file_exist(file_path)
            raise '{0} already exists'.format(file_path)
        except:
            pass

        if has_header:
            header, body = content[0], content[1:]
            new_content = [['#{}'.format(header[0])] + header[1:]]
            new_content += body
        else:
            new_content = content
        self.write(file_path=file_path, data=new_content, sep=',')


    def delete_file(self, file_path=None):
        self._does_file_exist(file_path)
        os.remove(file_path)


    def delete_dir(self, dir_path=None):
        os.rmdir(dir_path)


    def view_header(self, file_path):
        self._validate_file_path(file_path)
        header = self.read(file_path=file_path, sep=',', comment='#', header_only=True)
        return header


    def view_row(self, file_path=None, rowid=None, columns=None, header=False):
        '''View row(s)

        **Parameters**
            - file_path: file for the table
            - rowid: (identifying column, val)

        **Example**
            - file_path = 'person.tbl'
            - rowid = ('name', 'sam')

        SQL analogy, for each row (key, val):
            SELECT * FROM table_name WHERE some_column=some_value;
            SELECT * FROM file_path WHERE rowid_key=rowid_val;
            SELECT * FROM table_name WHERE name='sam';
            SELECT name FROM table_name WHERE name='sam';
        '''

        self._validate_file_path(file_path)

        if header:
            header = self.read(file_path=file_path, sep=',', comment='#', header_only=True)
            return header

        header, body = self.read(file_path=file_path, sep=',', comment='#')
        if columns == 'all':
            columns = None

        result = [header]
        # Existing rows: update
        if not rowid:
            # show all
            result += body
        elif isinstance(rowid, (tuple, list)):
            rowid_index = header.index(rowid[0])
            for row in body:
                key = row[rowid_index]
                if key == rowid[1]: # value
                    result.append(row)
        else:
            raise Exception('Invalid row selector')

        return result


    def insert_row(self, file_path=None, row=None):
        '''Add a row

        **Parameters**
            - file_path: file for the table
            - row: new row

        **Example**
            file_path = 'person.tbl'
            row = {'name': 'radhesam', 'email': 'sam@ram.com', 'phone': '8173334444'}

        SQL analogy, for each row (key, val):
            INSERT INTO table_name (col1, col2, ...) VALUES (val1, val2, ...);
            INSERT INTO file_path (name, email, ...) VALUES ('radhesam', 'sam@ram.com', ...);
        '''

        self._validate_file_path(file_path)

        header, body = self.read(file_path=file_path, sep=',', comment='#')

        # Sort by col order in table
        items = [(header.index(item[0]), item) for item in row.iteritems()]
        items.sort() # sorts in place
        new_row = [_[1][1] for _ in items]
        new_content = [new_row]

        # Append new content to the table
        self.write(file_path=file_path, data=new_content, sep=',', mode='a')


    def update_row(self, file_path=None, rowid=None, update_row=None, default_val=' ', has_header=True):
        '''Update a row

        **Parameters**
            - file_path: file for the table
            - rowid: (identifying column, val)
            - update_row: {col1: val1, col2: val2, ..}

        **Example**
            - file_path = 'person.tbl'
            - rowid = ('name', 'sam')
            - update_row = {'phone': '4693334444'}

        SQL analogy, for each row (key, val):
            UPDATE table_name SET col1=val1, col2=val2 WHERE some_column=some_value;
            UPDATE file_path SET update_row_key1=update_row_val1, ... where rowid_key=rowid_val
            UPDATE person SET phone='4693334444' where name='sam'
        '''
        self._validate_file_path(file_path)

        header, body = self.read(file_path=file_path, sep=',', comment='#')

        rowid_index = header.index(rowid[0])
        items = [(header.index(item[0]), item) for item in update_row.iteritems()]
        #col_index = header.index(column)
        update_values = update_row.values()

        if has_header:
            new_content = [['#{}'.format(header[0])] + header[1:]]
        else:
            new_content = []

        # Existing rows: update
        for row in body:
            key = row[rowid_index]
            if key == rowid[1]: # value
                for item in items:
                    row[item[0]] = item[1][1]
                new_content.append(row)
            else:
                new_content.append(row)

        # Create tmp file with updated content
        tmp_file = 'tmp.tbl'
        self.write(file_path=tmp_file, data=new_content, sep=',')

        # Now move new file to old
        shutil.move(tmp_file, file_path)


    def delete_row(self, file_path=None, rowid=None, has_header=True):
        '''Detele row(s)

        **Parameters**
            - file_path: file for the table
            - rowid: (identifying column, val)
            - update_row: {col1: val1, col2: val2, ..}

        **Example**
            - file_path = 'person.tbl'
            - rowid = ('name', 'sam')

        SQL analogy, for each row (key, val):
            DELETE FROM table_name WHERE some_column=some_value;
            DELETE FROM file_path WHERE rowid_key=rowid_val;
            DELETE FROM table_name WHERE name='sam';
        '''

        self._validate_file_path(file_path)

        header, body = self.read(file_path=file_path, sep=',', comment='#')

        if has_header:
            new_content = [['#{}'.format(header[0])] + header[1:]]
        else:
            new_content = []

        # Existing rows: update
        if rowid is None:
            pass # delete all
        elif isinstance(rowid, (tuple, list)):
            rowid_index = header.index(rowid[0])
            for row in body:
                key = row[rowid_index]
                if key == rowid[1]: # value
                    continue # ie not include
                else:
                    new_content.append(row)
        else:
            raise Exception('Invalid row selector')

        # Create tmp file with updated content
        tmp_file = 'tmp.tbl'
        self.write(file_path=tmp_file, data=new_content, sep=',')

        # Now move new file to old
        shutil.move(tmp_file, file_path)


    def update_rows(self, file_path=None, pk=None, rows_values=None, column=None, default_val=' ', has_header=True):
        '''Update one or more rows, if new create row(s)

        **Example**
            pk = 'host'
            column = 'k9'
            rows_values = {'1.1.1.1': 'committed', '1.2.1.2': 'active'}

        SQL analogy, for each row (key, val):
            UPDATE table_name SET column1=value1, column2=value2 WHERE some_column=some_value;
            UPDATE file_path SET column=val where pk=key
            UPDATE file_path SET set_k9='committed' where host='1.1.1.1'
            UPDATE file_path SET set_k9='active' where host='1.2.1.2'
        '''

        header, body = self.read(file_path=file_path, sep=',', comment='#')

        pk_index = header.index(pk)
        col_index = header.index(column)
        keys = rows_values.keys()
        file_keys = [_[pk_index] for _ in body]

        if has_header:
            new_content = [['#{}'.format(header[0])] + header[1:]]
        else:
            new_content = []

        # Existing rows: update
        for row in body:
            key = row[pk_index]
            if key in keys:
                row[col_index] = rows_values[key]
                new_content.append(row)
            else:
                new_content.append(row)

        # New rows: add
        for key in rows_values:
            if key not in file_keys:
                new_row = [key]
                new_row += [default_val for i in xrange(len(header) - 1)]
                new_row[col_index] = rows_values[key]
                new_content.append(new_row)

        # Create tmp file with updated content
        tmp_file = 'tmp.tbl'
        self.write(file_path=tmp_file, data=new_content, sep=',')

        # Now move new file to old
        shutil.move(tmp_file, file_path)


    def _does_file_exist(self, file_path):
        # if file is not there or empty or has only empty spaces, return True
        if not os.path.isfile(file_path):
            raise Exception('{0} Does Not Exist'.format(os.path.basename(file_path)))

    def _is_file_empty(self, file_path):
        # if file is not there or empty or has only empty spaces, return True
        is_empty = False
        if os.stat(file_path).st_size == 0:
            is_empty = True
        with open(file_path, 'r') as fh:
            if not fh.read().strip():
                is_empty = True
        if is_empty:
            raise Exception('{0} is corrupted'.format(os.path.basename(file_path)))

    def _validate_file_path(self, file_path):
        self._does_file_exist(file_path)
        self._is_file_empty(file_path)
