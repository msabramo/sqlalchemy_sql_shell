sqlalchemy_sql_shell
====================

Usage
-----

The program takes one argument: a SQLAlchemy database URL of the form:
``dialect+driver://username:password@host:port/database`` (see
`the SQLAlchemy docs on database URLs
<http://docs.sqlalchemy.org/en/rel_0_8/core/engines.html#database-urls>`_ for
more info). You may need to install additional packages for your database
driver of choice (e.g.: mysql-python, psycopg2, pymssql, etc.)

Here's some basic usage::

    $ sqlalchemy_sql_shell
    usage: sqlalchemy_sql_shell [-h] url
    sqlalchemy_sql_shell: error: too few arguments

    $ sqlalchemy_sql_shell sqlite:///
    SQL> CREATE TABLE people ( first_name VARCHAR(128), last_name VARCHAR(128) );
    SQL> INSERT INTO people VALUES ( 'John', 'Doe' ), ('Mike', 'Smith'), ('Guido', 'van Rossum');
    result.rowcount = 3
    SQL> SELECT * FROM people;
    +------------+------------+
    | first_name | last_name  |
    +============+============+
    | John       | Doe        |
    | Mike       | Smith      |
    | Guido      | van Rossum |
    +------------+------------+

Multi-line queries are supported; A semi-colon signifies the end of the query::

    SQL> SELECT *
    ...> FROM people
    ...> ;
    +------------+------------+
    | first_name | last_name  |
    +============+============+
    | John       | Doe        |
    | Mike       | Smith      |
    | Guido      | van Rossum |
    +------------+------------+

You can also pipe queries into the command for quick one-liners::

    $ echo "SELECT 1 + 2;" | sqlalchemy_sql_shell sqlite:///
    +-------+
    | 1 + 2 |
    +=======+
    | 3     |
    +-------+

Or redirect stdin::

    $ cat samples/queries.sql
    SELECT 1 + 2;
    SELECT 3 + 4;
    SELECT 5 + 6;

    $ sqlalchemy_sql_shell sqlite:/// < samples/queries.sql
    +-------+
    | 1 + 2 |
    +=======+
    | 3     |
    +-------+
    +-------+
    | 3 + 4 |
    +=======+
    | 7     |
    +-------+
    +-------+
    | 5 + 6 |
    +=======+
    | 11    |
    +-------+

