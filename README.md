# DBMS Project:

### Prompt:
Upon launch, DB engine presents a prompt similar to the mysql> prompt, where interactive multiline commands may be entered. 


### Supported Commands Overview:
Database engine supports the following DDL, DML, and VDL commands. Commands terminates by a semicolon (;).
#### DDL
    * SHOW TABLES – Displays a list of all tables in DB.
    * CREATE TABLE – Creates a new table schema, i.e. a new empty table.
    * DROP TABLE – Remove a table schema, and all of its contained data.
    * Note: ALTER TABLE schema change commands are not implemented.
#### DML
    * INSERT INTO TABLE – Inserts a single record into a table.
    * DELETE FROM – Deletes one or more records from a table.
    * UPDATE – Modifies one or more records in a table.
#### VDL
    * “SELECT-FROM-WHERE” -style query
    * EXIT – Cleanly exits the program and saves all table and index information in non-volatile files.
    * Note: JOIN commands are not implemented. All queries will be single table queries. 
