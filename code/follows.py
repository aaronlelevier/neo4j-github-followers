"""
Outpus a CSV of distinct User-Follows relationships
"""
import csv
import os

from _base import DATA_DIR, argparse_required_username


USERNAME = argparse_required_username()

user_data_dir = os.path.join(DATA_DIR, USERNAME)
read_file = os.path.join(user_data_dir, 'followers.csv')
output_file = os.path.join(user_data_dir, 'follows.csv')

columns = [
    'login',
    'follows'
]


def main():
    combos = set()

    with open(read_file) as read_csvfile:
        with open(output_file, 'w') as write_csvfile:

            reader = csv.DictReader(read_csvfile)
            writer = csv.writer(write_csvfile, delimiter=',')

            writer.writerow(columns)

            for row in reader:
                combo = "{login}-{follows}".format(**row)

                if row['follows'] and combo not in combos:
                    writer.writerow([row[c] for c in columns])
                    combos.add(combo)


if __name__ == '__main__':
    main()
