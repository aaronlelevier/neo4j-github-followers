"""
Calls the Github API to populate User and Follower CSV data to build the
followers relationship graph

Users aren't distinct in the outputted CSV

User-Follows are distinct
"""
import os
import json
import csv
import requests
from queue import Queue
from threading import Thread

from _base import DATA_DIR, argparse_required_username


USERNAME = argparse_required_username()

# Github Auth header
headers = {'Authorization': 'token {}'.format(os.environ['GITHUB_API_TOKEN'])}

# file destination to save output
user_data_dir = os.path.join(DATA_DIR, USERNAME)
output_file = os.path.join(user_data_dir, 'followers.csv')

# Github user data that will be saved
columns = [
    # info
    'login',
    'name',
    'email',
    'company',
    'created_at',
    'updated_at',
    'avatar_url',
    'location',
    # status
    'followers',
    'following',
    'public_gists',
    'public_repos',
    # linking
    'follows'
]


def get_enpoint_data(url):
    r = requests.get(url, headers=headers)
    r.status_code
    if not r.status_code == 200:
        raise AssertionError('bad request')
    return json.loads(r.content.decode('utf8'))


def get_user_data(username, follows=''):
    url = 'https://api.github.com/users/{}'.format(username)
    data = get_enpoint_data(url)
    data['follows'] = follows
    return data


def get_follower_data(username):
    url = 'https://api.github.com/users/{}/followers'.format(username)
    return get_enpoint_data(url)


def put_user_data_on_queue(queue, username, follows):
    queue.put(get_user_data(username, follows))


def get_user_and_followers_data(username):
    """
    Returns a list of Github User dict objects
    """
    q = Queue()
    threads = []

    followers = [f['login'] for f in get_follower_data(username)]
    for f in followers:
        threads.append(
            Thread(target=put_user_data_on_queue, args=(q, f, username)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return [q.get(1) for _ in range(q.qsize())]


def main():
    main_user_data = get_user_data(USERNAME)
    follower_data = get_user_and_followers_data(USERNAME)

    next_follower_data = []
    for f in follower_data:
        next_follower_data.append(get_user_and_followers_data(f['login']))

    # create output dir if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        # header
        writer.writerow(columns)
        # main_user data
        writer.writerow([main_user_data[x] for x in columns])
        # follower data
        for data in follower_data:
            writer.writerow([data[c] for c in columns])

        # 2nd level follower data
        for nf in next_follower_data:
            for data in nf:
                writer.writerow([data[c] for c in columns])


if __name__ == '__main__':
    main()
