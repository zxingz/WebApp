from flask import Flask, render_template, request, redirect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet
from urllib.parse import urlparse, urlunparse
import json

# Declaring app
app = Flask(__name__)

# Getting current directory
script_dir = os.path.dirname(__file__)

# initializing webdriver
chrome_options = Options()
chrome_options.add_argument(
    "user-agent='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("disable-gpu")

# Fernet key
fernet_key = Fernet(b'DsVOWaQ9bVqAhhswF5H5fGQyQhhhLrC_7BHW6NHAu2Y=')


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


@app.route("/user/<user_id>")
def user_space(user_id):
    if user_id == 'vishnu':
        return render_template(template_name_or_list="app.html", context={})
    else:
        return render_template(template_name_or_list="not_found.html",
                               **{'path': request.url}), 404


# Redirect to "/user/<user_id>"
@app.route("/u/<user_id>")
def user_redirect(user_id):
    return redirect('/user/' + user_id)


@app.route("/")
def index():
    return render_template(template_name_or_list="app.html", **{'site':''})


@app.route("/<path:dummy>")
def fallback(dummy):
    return render_template(template_name_or_list="not_found.html",
                           **{'path': request.url}), 404


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
