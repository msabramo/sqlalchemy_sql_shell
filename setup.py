import os
import sys
from setuptools import setup

install_requires = ['sqlalchemy', 'texttable']

version = sys.version_info[:2]

if version < (2,7) or (3,0) <= version <= (3,1):
    install_requires += ['argparse']

this_dir = os.path.dirname(__file__)
long_description = "\n" + open(os.path.join(this_dir, 'README.rst')).read()

setup(
    name='sqlalchemy_sql_shell',
    version='0.0.0',
    description=('A shell for doing simple SQL queries to any database supported by SQLAlchemy'),
    long_description=long_description,
    keywords='database, SQL, SQLAlchemy',
    author='Marc Abramowitz',
    author_email='marc@marc-abramowitz.com',
    url='https://github.com/msabramo/sqlalchemy_sql_shell',
    py_modules=['sqlalchemy_sql_shell'],
    zip_safe=False,
    install_requires=install_requires,
    entry_points = """\
      [console_scripts]
      sqlalchemy_sql_shell = sqlalchemy_sql_shell:main
    """,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Testing',
        'Natural Language :: English',
        'Intended Audience :: Developers',
    ],
)
