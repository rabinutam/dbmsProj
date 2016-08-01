'''
**Requirement**
    - file per table
        - each db table and indes will be physically stored as a seperate file
        - global page_size = 512
        - not required: support reformat
    - programming language: any
    - prompt
        - example: davisql >
    - supported commands
        - DDL
            - SHOW TABLES
            - CREATE TABLE
            - DROP TABLE
            - Not req: ALTER TABLE
        - DML
            - INSERT INTO TABLE
            - DELETE FROM
            - UPDATE
        - VDL
            - SELECT-FROM-WHERE
            - EXIT: upom exit save all in non volatile files
            - not req: JOIN
'''

import os
import sys


BASE_DIR_ABS = os.path.dirname(os.path.abspath(__file__))
DATA_DIR_ABS = os.path.join(BASE_DIR_ABS, 'data')

DEV_ENV = True
PAGE_SIZE = 512 #bytes
