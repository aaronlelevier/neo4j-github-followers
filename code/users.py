"""
Outputs a CSV of distinct Github User records
"""
import csv
import os

from _base import DATA_DIR, argparse_required_username


USERNAME = argparse_required_username()

user_data_dir = os.path.join(DATA_DIR, USERNAME)
read_file = os.path.join(user_data_dir, 'followers.csv')
output_file = os.path.join(user_data_dir, 'users.csv')


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
    # no "follows" column because this is only User data
]


def main():
    users = set()

    with open(read_file) as read_csvfile:
        with open(output_file, 'w') as write_csvfile:

            reader = csv.DictReader(read_csvfile)
            writer = csv.writer(write_csvfile, delimiter=',')

            writer.writerow(columns)

            for row in reader:
                username = row['login']

                if username not in users:
                    writer.writerow([row[c] for c in columns])
                    users.add(username)


if __name__ == '__main__':
    main()
