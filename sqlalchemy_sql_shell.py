#!/usr/bin/env python

"""
A simple database-agnostic SQL shell that uses SQLAlchemy to abstract out how
to connect to different database engines.

"""

# Copyright (c) 2012-2013 Marc Abramowitz and SurveyMonkey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import readline   # make raw_input use readline
import sys

import sqlalchemy
from texttable import Texttable


def get_input(prompt):
    if sys.version_info < (3, ):
        return raw_input(prompt)
    else:
        return input(prompt)


def get_query():
    lines = []

    if sys.stdin.isatty():
        prompt = 'SQL> '
    else:
        prompt = ''

    while True:
        input_line = get_input(prompt).strip()
        if len(input_line) == 0 and len(lines) == 0:
            return None
        lines.append(input_line)
        if input_line.endswith(';'):
            break
        prompt = '...> '

    return '\n'.join(lines)


def process_query(conn, query):
    table = Texttable(max_width=0)
    table.set_deco(Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)

    try:
        result = conn.execute(query)
    except (sqlalchemy.exc.ProgrammingError, sqlalchemy.exc.OperationalError) as e:
        print(str(e))
    else:
        if result.returns_rows:
            try:
                for idx, row in enumerate(result.fetchall()):
                    if idx == 0:
                        table.header(row.keys())

                    table.add_row(row)
            except sqlalchemy.exc.ResourceClosedError as e:
                print(str(e))
            else:
                print(table.draw())
        elif result.rowcount > 0:
            print('result.rowcount = %d' % result.rowcount)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='SQLAlchemy database URL - dialect+driver://username:password@host:port/database (see http://docs.sqlalchemy.org/en/rel_0_8/core/engines.html#database-urls for more info)')
    args = parser.parse_args()

    engine = sqlalchemy.create_engine(args.url, echo=False)
    conn = engine.connect()

    while True:
        try:
            query = get_query()
        except EOFError:
            # User hit Ctrl+d; quit
            sys.stdout.write("\n")
            break

        if query:
            process_query(conn, query)


if __name__ == '__main__':
    main()

