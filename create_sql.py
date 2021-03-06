# coding: utf-8
"""Make create table statement from data file."""
import argparse
from collections import OrderedDict
from csv import DictReader
from os import path


def get_args():
    """Get arguments from command line.

    Returns
    ----------
    args: dict
        Arguments parsed from the command line.

    """
    parser = argparse.ArgumentParser(
        description='Build SQL create table statement.')

    parser.add_argument('data_file',
                        help='a delimited data file')

    parser.add_argument('-n',
                        type=int,
                        help='number of rows to parse (default: all rows)')

    parser.add_argument('-sep',
                        dest='sep',
                        default='\t',
                        help='delimiter (default: \\t)')

    parser.add_argument('-eg',
                        dest='eg',
                        action='store_true',
                        default=False,
                        help=('show example data as comments in SQL '
                              'statement'))

    parser_args = parser.parse_args()

    args = dict(data_file=parser_args.data_file,
                n=parser_args.n,
                sep=parser_args.sep,
                eg=parser_args.eg)

    assert path.exists(args['data_file'])

    return args


def parse_file(args):
    """Parse a delimited data file.

    Parameters
    ----------
    args: dict
        File path and options for parsing the data file.

    Returns
    -------
    sql: str
        Create table sql statement.

    """
    with open(args['data_file']) as data_file:
        currentline = 0

        reader = DictReader(data_file, delimiter=args['sep'])
        header = reader.fieldnames

        attr = OrderedDict()

        try:
            for row in reader:
                currentline += 1
                if args['n']:
                    if currentline > args['n']:
                        break

                for name in header:
                    val = row[name]

                    if currentline == 1:
                        attr[name] = {'ex': val, 'len': len(val)}

                    if len(val) > attr[name]['len']:
                        attr[name] = {'ex': attr[name]['ex'], 'len': len(val)}

        except UnicodeDecodeError:
            # Highlight location of UnicodeDecodeError in exception message
            print('UnicodeDecodeError AT LINE {} OF DATA FILE'.format(
                currentline))
            raise

    cols = ''
    max_key_len = max(map(len, attr))  # for pretty spacing in SQL statement

    for _ in attr.keys():
        if args['eg']:
            cols = (cols +
                    '{}{}NVARCHAR({}),\t-- eg. {}\n'
                    .format(_,
                            ' ' * (max_key_len - len(_) + 8),
                            attr[_]['len'],
                            attr[_]['ex']))

            sql = "CREATE TABLE []\n(\n{});\n".format(cols)
        else:
            cols = (cols +
                    '{}{}NVARCHAR({}),\n'
                    .format(_,
                            ' ' * (max_key_len - len(_) + 8),
                            attr[_]['len']))

            sql = "CREATE TABLE []\n(\n{});\n".format(cols)

    return sql


if __name__ == '__main__':
    args = get_args()
    sql = parse_file(args=args)
    print(sql)
