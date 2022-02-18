import time
import requests
import requests as req
from setuptools.namespaces import flatten
import constant


def product_category(post):
    print('product category')
    products = post[constant.TOPIC]
    categories = [topic[constant.NAME] for topic in products]
    print(categories)

    return categories


def no_up_vote(post):
    try:
        return post[constant.VOTES_COUNT]
    except ValueError:
        return 0


def is_dead(website):
    time.sleep(5)
    print(website)
    headers = {'Authorization': "Bearer {}".format(constant.TOKEN)}
    try:
        requests.Session()
        response = requests.get(website, headers=headers)
        if response.status_code is constant.ISALIVE:
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
    count_of_category = []
    product_of_day=None
    most_used_description={}
    for post in posts:
        name = post[constant.NAME]
        no_up_vot = no_up_vote(post)
        product_link = post[constant.DISCUSSION_URL]
        product = req.get(post[constant.DISCUSSION_URL], constant.AGENT)
        product_details = post[constant.MAKER]
        if product_of_day is None:
            product_of_day = [name, no_up_vot, product_link, product_details]

        print(product_of_day)
        try:
            if is_dead(product_details[0][constant.WEBSITE_URL]):
                try:
                    count_of_category.append(product_category(post))
                except ValueError:
                    print('none')
                data[constant.NAME] = name
                product_link = post[constant.DISCUSSION_URL]
                products.append({name, no_up_vot, product_link})
        except IndexError:
            print('NO URL')
    products.sort()
    count_of_category = list(flatten(count_of_category))
    count_of_category = set(count_of_category)
    print(count_of_category)
    print(products)
