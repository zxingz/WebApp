# Native imports
import os
import json
from urllib.parse import urlparse, urlunparse

# Installed libraries
from flask import Flask, render_template, request, redirect, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet
from google.cloud import bigquery


# Utility Functions

def path_maker(paths): # combine path lists into final path
    return '/'.join(paths)


def get_user_data(id):
    client = bigquery.Client()
    query = ("SELECT * FROM `portfolio-251217.the_software_dev.user_profile` where id='"+id+"'")
    result = [row for row in client.query(query,location="US",)]
    if len(result) != 1:
        return None
    return result[0]


def get_user_projects(id):
    client = bigquery.Client()
    query = ("SELECT * FROM `portfolio-251217.the_software_dev.user_projects` where user_id='"+id+"'")
    result = [[int(row['seq']),dict(row)] for row in client.query(query,location="US",)]
    for row in result:
        del row[1]['seq']
    result = sorted(result, key=lambda l:l[0])
    return result


def replace_all_urls(scheme, netloc,link,tag,attr):
    sub_url_parsed = urlparse(link[attr])

    if scheme not in ['http', 'https', '']:
        return
    elif tag in ['img','script','link']:
        if sub_url_parsed.scheme != '' and sub_url_parsed.netloc != '':
            scheme = sub_url_parsed.scheme
            netloc = sub_url_parsed.netloc
        link[attr] = urlunparse((scheme,netloc,sub_url_parsed.path,sub_url_parsed.query,sub_url_parsed.params,sub_url_parsed.fragment))
        return
    elif sub_url_parsed.scheme != '' and sub_url_parsed.netloc != '':
        scheme = sub_url_parsed.scheme
        netloc = sub_url_parsed.netloc
    encrypted_url = fernet_key.encrypt(json.dumps({'s': scheme,
                                                   'n': netloc,
                                                   'p': sub_url_parsed.path,
                                                   'q': sub_url_parsed.query,
                                                   'a': sub_url_parsed.params,
                                                   'f': sub_url_parsed.fragment}).encode('utf-8'))
    link[attr] = '/user/site?m=' + encrypted_url.decode('utf-8')
    return


# Declaring app
app = Flask(__name__)


'''
# initializing webdriver
chrome_options = Options()
chrome_options.add_argument(
    "user-agent='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("disable-gpu")
'''

# Global Variables

fernet_key = Fernet(b'DsVOWaQ9bVqAhhswF5H5fGQyQhhhLrC_7BHW6NHAu2Y=') # Fernet key
app_dir = os.path.dirname(os.path.realpath(__file__)) # Project Directory directory

# Declaring environment variables
os.environ.setdefault('GOOGLE_APPLICATION_CREDENTIALS',
                      path_maker([app_dir,
                                  'keys',
                                  'Portfolio-tsd.json']))


'''
@app.route("/user/site")
def site_view_var():
    msg = request.args.get('m')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    data = json.loads(fernet_key.decrypt(msg.encode('utf-8')).decode('utf-8'))
    url = urlunparse((data['s'], data['n'], data['p'], data['a'], data['q'], data['f']))
    print(url)
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    for link in soup.find_all('a', href=True):
        replace_all_urls(data['s'],data['n'],link,'a','href')
        link['target'] = '_self'
    for link in soup.find_all('script', src=True):
        replace_all_urls(data['s'],data['n'],link,'script','src')
    for link in soup.find_all('link', href=True):
        replace_all_urls(data['s'],data['n'],link,'link','href')
    for link in soup.find_all('img', src=True):
        replace_all_urls(data['s'],data['n'],link,'img','src')
    driver.quit()
    return str(soup)
'''


# remove project
@app.route("/project/remove/<user_id>")
def remove_project(user_id):
    user_data = get_user_data(user_id)
    if user_data is None:
        return render_template(
            template_name_or_list="not_found.html",
            **{'msg': 'User "'+user_id+'" does not exists.'}
        ), 404
    else:
        return render_template(
            template_name_or_list="home.html",
            **user_data
        )


# update project
@app.route("/project/update/<user_id>")
def update_project(user_id):
    user_data = get_user_data(user_id)
    if user_data is None:
        return render_template(
            template_name_or_list="not_found.html",
            **{'msg': 'User "'+user_id+'" does not exists.'}
        ), 404
    else:
        return render_template(
            template_name_or_list="home.html",
            **user_data
        )

# add project
@app.route("/project/add/<user_id>")
def add_project(user_id):
    user_data = get_user_data(user_id)
    if user_data is None:
        return render_template(
            template_name_or_list="not_found.html",
            **{'msg': 'User "'+user_id+'" does not exists.'}
        ), 404
    else:
        return render_template(
            template_name_or_list="home.html",
            **user_data
        )


# reorder user projects
@app.route("/order/<user_id>")
def project_space(user_id):
    user_data = get_user_data(user_id)
    if user_data is None:
        return render_template(
            template_name_or_list="not_found.html",
            **{'msg': 'User "'+user_id+'" does not exists.'}
        ), 404
    else:
        return render_template(
            template_name_or_list="home.html",
            **user_data
        )

# edit user profile
@app.route("/update/<user_id>")
def profile_space(user_id):
    user_data = get_user_data(user_id)
    if user_data is None:
        return render_template(
            template_name_or_list="not_found.html",
            **{'msg': 'User "'+user_id+'" does not exists.'}
        ), 404
    else:
        return render_template(
            template_name_or_list="home.html",
            **user_data
        )


# show user space
@app.route("/user/<user_id>")
def user_space(user_id):
    user_data = get_user_data(user_id)
    if user_data is None:
        return render_template(
            template_name_or_list="not_found.html",
            **{'msg': 'User "'+user_id+'" does not exists.'}
        ), 404
    else:
        return render_template(
            template_name_or_list="home.html",
            **user_data,
            result=get_user_projects(user_id)
        )


# Redirect to "/user/<user_id>"
@app.route("/u/<user_id>")
def user_redirect(user_id):
    return redirect('/user/' + user_id)


@app.route("/")
def landing():
    return render_template(template_name_or_list="landing.html")


@app.route("/<path:dummy>")
def fallback(dummy):
    return render_template(template_name_or_list="not_found.html",
                           **{'msg': request.url}), 404


if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
