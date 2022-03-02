import time
import requests
import requests as req
from setuptools.namespaces import flatten
import constant


def product_category(post):
    # the every post is having more than one topic
    # we need to take all categories
    print('product category')
    # list of topics in post
    products = post[constant.TOPIC]
    # list of category the post belong
    categories = [topic[constant.NAME] for topic in products]
    print(categories)

    return categories


def no_up_vote(post):
    # first we try to get no of votes and return it if no entry available we will return 0
    try:
        return post[constant.VOTES_COUNT]
    except ValueError:
        return 0


def is_dead(website):
    time.sleep(5)
    print(website)
    # headers for access the api by providing is Api token
    headers = {'Authorization': "Bearer {}".format(constant.TOKEN)}
    try:

        response = requests.get(website, headers=headers)
        # check the product website id dead or not means if website status code is not 200 means its dead link
        if response.status_code is constant.ISALIVE:
            return False
        else:
            return True
    # When the schema is Missing return false because there is no link
    except requests.exceptions.MissingSchema:
        return False
    # When the Connection error occurs return false
    except requests.exceptions.ConnectionError:
        return False


def product_hunt():
    # header for access the api by providing is Api token
    headers = {'Authorization': "Bearer {}".format(constant.TOKEN)}
    response = req.get(constant.PRODUCT_HUNT_BASE_URL, headers=headers).json()
    # getting all post from API
    posts = response[constant.POST]
    data = {}
    products = []
    count_of_category = []
    product_of_day = None
    most_used_description = {}
    # traversing each product to get the dead post link
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
            # if dead product count try to get the link of the dead product
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
    # Number of categories  of dead products link
    count_of_category = set(count_of_category)
    print(count_of_category)
    print(products)
