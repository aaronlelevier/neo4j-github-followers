from os.path import dirname, join, abspath
import argparse


PROJECT_DIR = dirname(dirname(abspath(__file__)))

DATA_DIR = join(PROJECT_DIR, 'data')


def argparse_required_username():
    # set required "username" for script
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, required=True,
                        help='Github username')
    args = parser.parse_args()
    return args.username