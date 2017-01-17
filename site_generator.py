import argparse
import json
import os
import markdown

from jinja2 import Environment, FileSystemLoader
from collections import defaultdict


def get_args():
    parser = argparse.ArgumentParser(
        description="This script convert directory\
            with *.md to site with content list",
    )
    parser.add_argument('--config',
                        type=argparse.FileType('r'),
                        help='Config file with content')
    return parser.parse_args()


def delete_special_simbol(file_name):
    return file_name.replace(';', '').replace('&', '').replace(' ', '_')


def get_source_html_path(source_path):
    name_source_file = os.path.split(source_path)[-1].replace(';', '')
    name_source = '.'.join(name_source_file.split('.')[:-1])
    source_html_path = '.'.join([delete_special_simbol(name_source), 'html'])
    return source_html_path


def get_page_html_info(page):
    return {'title': page['title'],
            'source': get_source_html_path(page['source'])}


def revert_topics_list_to_dict(topics_list):
    return {topic['slug']: topic['title'] for topic in topics_list}


def get_site_structure(pages_list, topics):
    site_structure = defaultdict()
    for page in pages_list:
        site_structure_list = site_structure.get(topics[page['topic']], [])
        site_structure_list.append(get_page_html_info(page))
        site_structure[topics[page['topic']]] = site_structure_list
    return site_structure


def get_index_html(pages_list, topics_list):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    topics = revert_topics_list_to_dict(topics_list)
    site_structure = get_site_structure(pages_list, topics)
    return template.render(topics=site_structure.keys(), pages=site_structure)


def create_index_html_file(site_directory, pages_list, topics_list):
    if not os.path.exists(site_directory):
        os.mkdir(site_directory)
    page_index_path = os.path.join(site_directory, 'index.html')
    with open(page_index_path, "w") as index_file:
        index_file.write(get_index_html(pages_list, topics_list))


def get_page_content(page_source_path):
    with open(page_source_path, "r") as markdown_file:
        return markdown.markdown(markdown_file.read())


def get_page_html(page_source_path):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('page.html')
    return template.render(page_content=get_page_content(page_source_path))


def create_page_html_file(name_of_site, site_directory, page):
    page_source_path = os.path.join(name_of_site, page['source'])
    page_result_path = os.path.join(site_directory, get_source_html_path(page['source']))
    with open(page_result_path, "w") as page_html_file:
        page_html_file.write(get_page_html(page_source_path))


def create_site(name_of_site, pages_list, topics_list):
    site_directory = '%s_html' % name_of_site
    create_index_html_file(site_directory, pages_list, topics_list)
    for page in pages_list:
        create_page_html_file(name_of_site, site_directory, page)


if __name__ == '__main__':
    args = get_args()
    config = json.load(args.config)
    name_of_sites = list(config.keys() - ['topics'])
    for name in name_of_sites:
        create_site(name, config[name], config['topics'])
