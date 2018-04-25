"""
Queries the Neo4j database and outputs the user-follows-user relationships

Before this step, the `users.csv` and and `follows.csv` must be loaded to
the Neo4j database. Look at the `query` dir for code on how to do this
"""
import os
import json
from os.path import dirname, join, abspath

from neo4j.v1 import GraphDatabase

from _base import PROJECT_DIR

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", os.environ['NEO4J_PASSWORD']))

results = []


def main():
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for record in tx.run(
                """
                MATCH (n:Follows) 
                RETURN n.login AS source, n.follows AS target
                """):
                results.append(record.data())            


    # save results to file
    output_dir = join(PROJECT_DIR, 'web')
    output_file = join(output_dir, 'd3-results.json')

    with open(output_file, 'w') as f:
        f.write(json.dumps(results))


if __name__ == '__main__':
    main()
