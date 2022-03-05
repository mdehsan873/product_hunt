import time
import requests
import requests as req
from setuptools.namespaces import flatten
import constant


def get_product_category(post):
    # the every post is having more than one topic
    # we need to take all categories
    print('product category')
    # list of topics in post
    topics = post[constant.TOPIC]
    # list of category the post belong
    categories = [topic[constant.NAME] for topic in topics]
    print(categories)
    return categories


def is_dead(website):
    time.sleep(5)
    print(website)
    # headers for access the api by providing is Api token
    headers = {'Authorization': "Bearer {}".format(constant.TOKEN)}
    try:
        response = requests.get(website, headers=headers)
        # check the product website id dead or not means if website status code is not 200 means its dead link
        is_dead = True if response.status_code is constant.ISALIVE else False
        return is_dead
    # When the schema is Missing return false because there is no link
    except requests.exceptions.MissingSchema:
        return False
    # When the Connection error occurs return false
    except requests.exceptions.ConnectionError:
        return False


# this function display the dead post with numbers of upvotes and link and name
# this function display the number of dead post categories with their count
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
        # getting the post name
        name = post[constant.NAME]

        # getting no of upvotes the post has
        no_up_vote = 0 if post[constant.VOTES_COUNT] is None else post[constant.VOTES_COUNT]

        # post link discussion url
        post_link = post[constant.DISCUSSION_URL]

        # post details its contains the post website and authors details
        post_details = post[constant.MAKER]

        # it is first post means it is product of than we store it
        if not product_of_day:
            product_of_day = [name, no_up_vote, post_link, post_details]

        # print(product_of_day)
        if len(post_details) >= 1:
            # if dead product count try to get the link of the dead product
            if is_dead(post_details[0][constant.WEBSITE_URL]):
                # if post is dead we append the post category into count of category
                if not get_product_category(post):
                    count_of_category.append(get_product_category(post))
                post_link = post_details[0][constant.WEBSITE_URL]
                # append the name and no vote and post_link
                products.append([name, no_up_vote, post_link])
        else:
            print(None)

    print(products, end=" before sorting")
    # sorting the products on bases of number of upvote
    products = sorted(products, key=lambda up_votes: up_votes[1])
    count_of_category = list(flatten(count_of_category))

    # Number of categories and its count of each type of dead products link
    no_of_categories = {}
    for category in count_of_category:
        no_of_categories[category] = no_of_categories.get(category, 0) + 1

    print(no_of_categories)
    print(products)
