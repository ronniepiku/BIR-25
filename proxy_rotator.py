import requests
import random
from threading import Timer


proxies_list = open("proxies.txt", "r").read().strip().split("\n")
unchecked = set(proxies_list[0:])
working = set()
not_working = set()


def reset_proxy(proxy):
    unchecked.add(proxy)
    working.discard(proxy)
    not_working.discard(proxy)


def set_working(proxy):
    unchecked.discard(proxy)
    working.add(proxy)
    not_working.discard(proxy)


def set_not_working(proxy):
    unchecked.discard(proxy)
    working.discard(proxy)
    not_working.add(proxy)

    # move to unchecked after a certain time (20s in the example)
    Timer(20.0, reset_proxy, [proxy]).start()


valid_statuses = [200, 301, 302, 307, 404]
session = requests.Session()


def get(url, proxy=None):
    if not proxy:
        proxy = get_random_proxy()

    try:
        response = session.get(url, proxies={'http': f"http://{proxy}"}, timeout=30)
        if response.status_code in valid_statuses:
            set_working(proxy)
        else:
            set_not_working(proxy)

        return response
    except Exception as e:
        set_not_working(proxy)
        raise e  # raise exception


def check_proxies():
    for proxy in list(unchecked):
        try:
            response = get("http://ident.me/", proxy)
            if response.status_code in valid_statuses:
                set_working(proxy)
            else:
                set_not_working(proxy)
        except Exception as e:
            set_not_working(proxy)


check_proxies()


def get_random_proxy():
    # create a tuple from unchecked and working sets
    available_proxies = tuple(working)
    if not available_proxies:
        raise Exception("no proxies available")
    return random.choice(available_proxies)


print("unchecked ->", unchecked)
print("working ->", working)
print("not_working ->", not_working)
