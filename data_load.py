from neo4j import GraphDatabase
driver=GraphDatabase.driver(uri="bolt://localhost:7687",auth=("neo4j","Rambo@1234"))
session=driver.session()

q1="""
call apoc.periodic.iterate('call apoc.load.csv("/Users/roni/Documents/GitHub/NEO4J_DASHBOARD/results.csv")
yield map as row return row
','
merge(c:Country{Name:row.country})
merge(ci:City{Name:row.city})
merge(m:Game{Name:row.tournament,played_on:row.date,home_team:row.home_team,away_team:row.away_team,home_score:row.home_score,away_score:row.away_score})
merge(c)-[:HAS]->(ci)
merge(m)-[:PLAYED_ON]->(ci)
',
{batchSize:1000,iterateList:true,parallel:true,retries:20})
"""
session.run(q1)