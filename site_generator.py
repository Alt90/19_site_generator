import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description="This script convert directory with *.md to site with content list",
    )
    parser.add_argument('--config',
                        type=argparse.FileType('r'),
                        help='Config file with content')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
