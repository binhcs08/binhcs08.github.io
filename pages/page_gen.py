#!/usr/bin/env python3

import yaml
import os, shutil

#pages = ['classical_guitars']

menu_header_tmp =  '''
            <div id="{menu_id}" class="menu-category">
              <h3 class="menu-category-name">{menu_name}</h3>
              <ol class="menu-category-list has-images">
'''

item_tmp = '''
              <li class="menu-item">
                <div class="menu-item-info">
                  <h4 class="menu-item-name">{menu_item[name]}</h4>
                  <span class="menu-item-price">{menu_item[price]}</span>
                  <p class="menu-item-description">{menu_item[description]}</p>
                </div>
                <div class="menu-item-image has-meta-content">
                  <img src="{menu_item[image]}" />
                </div>
              </li>
'''

menu_end_tmp = '''
              </ol>
            </div>
'''

nav_list_tmp = '''
                <li class="menu-navigation-list-item"><a href="#{menu_id}">{menu_name}</a></li>
'''

yml_path = "./yml"
html_path = "./html"

def open_yml(f: str) -> object:
    with open(f, 'r') as s:
        try:
            return yaml.safe_load(s)
        except yaml.YAMLError as e:
            print(e)

def gen_menu_list(page: str) -> str:
    p = ""
    all = open_yml(f"{yml_path}/{page}.yml")
    if all is None:
        return p
    for d in all:
        menu_id = d.get('menu_id')
        menu_name = d.get('menu_name')
        h = menu_header_tmp.format(**locals())
        p += h
        for menu_item in d.get('menu_items'):
            i = item_tmp.format(**locals())
            p += i
        p += menu_end_tmp
    return p

def gen_nav_list(page: str) -> str:
    p = ""
    all = open_yml(f"{yml_path}/{page}.yml")
    if all is None:
        return p
    for d in all:
        menu_id = d.get('menu_id')
        menu_name = d.get('menu_name')
        h = nav_list_tmp.format(**locals())
        p += h
    return p

def gen_html_page(yml_page: str) -> str:
    nav_list = gen_nav_list(yml_page)
    menu_list = gen_menu_list(yml_page)
    
    html = ""
    with open('html.template', 'r') as f:
        for l in f.readlines():
            html += l

    html = html.replace('_NAVIGATION_LIST', nav_list)
    html = html.replace('_MENU_', menu_list)
    
    return html

def gen_htmls():
    from os import listdir
    from os.path import isfile, join
    pages = list(map(lambda f: f.split('.')[0], [f for f in listdir(yml_path) if isfile(join(yml_path, f))]))
    try:
        if os.path.isdir(html_path):
            shutil.rmtree(html_path)
        os.mkdir(html_path)
    except OSError:
        print ("Creation of the directory %s failed" % html_path)
    else:
        print ("Successfully created the directory %s " % html_path)
    for page in pages:
        with open(f"{html_path}/{page}.html", "w") as o:
            html_page = gen_html_page(yml_page=page)
            o.write(html_page)
            print(f"input: {yml_path}/{page}.yml. output: {html_path}/{page}.html")

gen_htmls()
        
