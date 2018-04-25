# README

## Summary

This is an example project combining Neo4j, Python and Github API

This project demostrates:

1. Call Github API using Python multithreading
2. Collect data from threads and output to a `followers.csv`
3. Use `followers.csv` which contains `User` data and `Follower` relationships to output CSVs distict for each:

	- `users.csv` - distinct Users
	- `follows.csv` - distinct mappings from User-to-Follows
4. Load CSVs into Neo4j
5. Create Neo4j relationships
6. Query Neo4j using the Python `neo4j-driver` client
7. Write queried data to write `json`
8. Use `json` to generate a `D3Js` web graph

## Quick Example

The current `web/d3-results.json` is already populated with my data, so just run:

```
cd web
npm install http-server
http-server
```

## To build and run the project with your data

Create a Github API token - this will be needed to make requests if making over 60 requests an hour, the unauthenticated rate limit

`pip install -r requirements.txt`

Populate CSVs for the Github User whose followers is being populated

```
python code/followers.py --username <username>
python code/follows.py --username <username>
python code/users.py --username <username>
```

Data can be loaded into Neo4j using the below queries

After data is loaded, run this command to populate `web/d3-results.json`.

Environment varialbe `NEO4J_PASSWORD` will need to be set for the Neo4j database connection in `query.py`

```
python query.py
```

Start Node server and see data with D3Js

```
cd web
npm install http-server
http-server
```


## Neo4j Queries

### Load CSV

CSV must first be placed in the Neo4j `/import/` dir:

```
/Users/aaron/Library/Application\ Support/Neo4j\ Desktop/Application/neo4jDatabases/database-0bf7614b-cb8d-405e-baef-e1b94485e662/installation-3.3.5/import/
```

Load `Users` table using CSV:

```
LOAD CSV WITH HEADERS FROM "file:///users.csv" AS row
CREATE (u:User)
SET u = row
```

Load `Follows` table using CSV:

```
LOAD CSV WITH HEADERS FROM "file:///follows.csv" AS row
CREATE (u:Follows)
SET u = row
```

### Create Relationships

Create `FOLLOWS` relationships using previous 2 tables:

```
MATCH (u:User),(f:Follows), (u2:User)
WHERE u.login = f.login
  AND f.follows = u2.login
CREATE (u)-[:FOLLOWS]->(u2)
```

### If you have to delete data and start over

First delete relationships:

```
MATCH ()-[r:FOLLOWS]-() 
DELETE r
```

Then delete tables:

```
MATCH (r:User)
DELETE r
```

```
MATCH (r:Follows)
DELETE r
```

## Libraries Used

### Database

[Neo4j](https://neo4j.com/)

### Python

[requests](https://github.com/requests/requests)

[neo4j-driver](https://github.com/neo4j/neo4j-python-driver)

### Javascript

[d3js](https://github.com/d3/d3)

[queue.js](https://github.com/d3/d3-queue)

## LICENSE 

BSD-2

## CONTRIBUTING

Contact me if you found this interesting

## FUTURE PLANS

Add more end-to-end Neo4j Graph Database examples

## Example Graph output images from this repo


### 1st and 2nd level relationships (D3Js)

![Imgur](https://i.imgur.com/7p74ftj.png)

### 1st level relationships (Neo4j)

![Imgur](https://i.imgur.com/uB0bPKg.png)

### 1st and 2nd level relationships (Neo4j)

![Imgur](https://i.imgur.com/6gVNsHZ.png)