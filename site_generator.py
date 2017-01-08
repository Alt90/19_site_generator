import argparse
import json
import os


def get_args():
    parser = argparse.ArgumentParser(
        description="This script convert directory with *.md to site with content list",
    )
    parser.add_argument('--config',
                        type=argparse.FileType('r'),
                        help='Config file with content')
    return parser.parse_args()


def create_index_html(site_directory, pages_list):
    os.mkdir(site_directory)


def create_page_html(name_of_site, site_directory, page):
    pass


def create_site(name_of_site, pages_list):
    site_directory = '%s_html' % name_of_site
    create_index_html(site_directory, pages_list)
    for page in pages_list:
        create_page_html(name_of_site, site_directory, page)


if __name__ == '__main__':
    args = get_args()
    config = json.load(args.config)
    name_of_sites = list(config.keys() - ['topics'])
    for name in name_of_sites:
        create_site(name, config[name])
