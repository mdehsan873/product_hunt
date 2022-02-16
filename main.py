import requests
import requests as req
from setuptools.namespaces import flatten

import constant
import time


def product_category(product):
    products = product[constant.TOPIC]
    categories = []
    for topic in products:
        categories.append(topic[constant.NAME])
    # print(categories)
    return categories


def no_up_vote(product):
    try:
        return product[constant.VOTES_COUNT]
    except ValueError:
        return 0


def is_dead(website):
    time.sleep(5)
    print(website)
    headers = {'Authorization': "Bearer {}".format(constant.TOKEN)}
    try:
        requests.Session()
        response = requests.get(website, headers=headers)
        if response.status_code == 200:

            return False
        else:
            return True
    except requests.exceptions.MissingSchema:
        return False
    except requests.exceptions.ConnectionError:
        return False


def product_hunt():
    headers = {'Authorization': "Bearer {}".format(constant.TOKEN)}
    response = req.get(constant.PRODUCT_HUNT_BASE_URL, headers=headers).json()

    posts = response[constant.POST]
    data = {}
    products = []
    no_of_category = []
    # no_of_category = {}
    for post in posts:
        name = post[constant.NAME]
        no_up_vot = no_up_vote(post)
        product_link = post[constant.DISCUSSION_URL]
        product = req.get(post[constant.DISCUSSION_URL], constant.AGENT)
        product_details = post[constant.MAKER]
        print()
        try:
            if is_dead(product_details[0][constant.WEBSITE_URL]):
                try:
                    no_of_category.append(product_category(post))
                except ValueError:
                    print('none')
                data[constant.NAME] = name
                product_link = post[constant.DISCUSSION_URL]
                products.append({name, no_up_vot, product_link})
        except IndexError:
            print('NO URL')
    products.sort()
    no_of_category = list(flatten(no_of_category))
    no_of_category = set(no_of_category)
    print(no_of_category)
    print(products)
