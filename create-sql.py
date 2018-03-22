# coding: utf-8
"""Make create table statement from data file."""
import argparse

from collections import OrderedDict
from csv import DictReader
from math import ceil
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
                        help='separator/delimiter (default: \\t)')

    parser.add_argument('-eg',
                        dest='eg',
                        type=bool,
                        default=False,
                        help=('show example data as comments in SQL statement'
                              ' (default: False)'))

    parser_args = parser.parse_args()

    args = dict(data_file=parser_args.data_file,
                n=parser_args.n,
                sep=parser_args.sep,
                eg=parser_args.eg)

    assert path.exists(args['data_file'])

    return args


def main():
    """Do main stuff."""
    args = get_args()

    with open(args['data_file']) as data_file:
        currentline = 0

        reader = DictReader(data_file, delimiter=args['sep'])
        header = reader.fieldnames

        attr = OrderedDict()

        for row in reader:
            currentline += 1
            if args['n']:
                if currentline > args['n']:
                    break

            for i in header:
                val = row[i]

                if currentline == 1:
                    attr[i] = {'ex': val, 'len': len(val)}

                if len(val) > attr[i]['len']:
                    attr[i] = {'ex': attr[i]['ex'], 'len': len(val)}

    cols = ''
    max_key_len = max(map(len, attr))  # for pretty spacing in SQL statement

    for _ in attr.keys():
        if args['eg']:
            cols = (cols +
                    '{}{}NVARCHAR({}),\t-- eg. {}\n'
                    .format(_,
                            '\t' * ceil(ceil(max_key_len/4)-(len(_)/4)),
                            attr[_]['len'],
                            attr[_]['ex']))

            query = "CREATE TABLE []\n(\n{});\n".format(cols)
        else:
            cols = (cols +
                    '{}{}NVARCHAR({}),\n'
                    .format(_,
                            '\t' * ceil(ceil(max_key_len/4)-(len(_)/4)),
                            attr[_]['len']))

            query = "CREATE TABLE []\n(\n{});\n".format(cols)

    dst = path.join(path.dirname(__file__), 'create_table.txt')

    with open(dst, 'w') as f:
        f.write(query)


if __name__ == '__main__':
    main()
