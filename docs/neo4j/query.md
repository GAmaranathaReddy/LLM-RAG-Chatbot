# Query the Hospital System Graph

The last thing you need to do before building your chatbot is get familiar with Cypher syntax. [Cypher](https://neo4j.com/docs/getting-started/cypher-intro/) is Neo4j’s query language, and it’s fairly intuitive to learn, especially if you’re familiar with SQL. This section will cover the basics, and that’s all you need to build the chatbot. You can check out [Neo4j’s documentation](https://neo4j.com/docs/getting-started/cypher-intro/) for a more comprehensive Cypher overview.

The most commonly used key word for reading data in Cypher is MATCH, and it’s used to specify patterns to look for in the graph. The simplest pattern is one with a single node. For example, if you wanted to find the first five patient nodes written to the graph, you could run the following Cypher query:

```
MATCH (p:Patient)
RETURN p LIMIT 5;
```

![Cypher match node query in the Neo4j UI](../assets/match_p_top5.png 'Cypher match node query in the Neo4j UI')

In this query, you’re matching on Patient nodes. In Cypher, nodes are always indicated by parentheses. The p in (p:Patient) is an alias that you can reference later in the query. RETURN p LIMIT 5; tells Neo4j to only return five patient nodes. You can run this query in the Neo4j UI, and the results should look like this:

The Table view shows you the five Patient nodes returned along with their properties. You can also explore the graph and raw view if you’re interested.

While matching on a single node is straightforward, sometimes that’s all you need to get useful insights. For example, if your stakeholder said give me a summary of visit 56, the following query gives you the answer:

```
MATCH (v:Visit)
WHERE v.id = 56
RETURN v;
```

This query matches Visit nodes that have an id of 56, specified by WHERE v.id = 56. You can filter on arbitrary node and relationship properties in WHERE clauses. The results of this query look like this:

![Cypher match node query in the Neo4j UI](../assets/visitor_56.png 'Cypher match node query in the Neo4j UI')

From the query output, you can see the returned **Visit** indeed has **id** 56. You could then look at all of the visit properties to come up with a verbal summary of the visit—this is what your Cypher chain will do.

Matching on nodes is great, but the real power of Cypher comes from its ability to match on relationship patterns. This gives you insight into sophisticated relationships, exploiting the power of graph databases. Continuing with the **Visit** query, you probably want to know which **Patient** the **Visit** belongs to. You can get this from the **HAS** relationship:

```
MATCH (p:Patient)-[h:HAS]->(v:Visit)
WHERE v.id = 56
RETURN v,h,p;

```

This Cypher query searches for the Patient that has a Visit with id 56. You’ll notice that the relationship HAS is surrounded by square brackets instead of parentheses, and its directionality is indicated by an arrow. If you tried MATCH (p:Patient)<-[h:HAS]-(v:Visit), the query would return nothing because the direction of HAS relationship is incorrect.

The query results look like this:

![Cypher query for the HAS relationship](../assets/visit_has_a_pat.png 'Cypher query for the HAS relationship')

Notice the output includes data for the **Visit, HAS** relationship, and **Patient**. This gives you more insight than if you only match on **Visit** nodes. If you wanted to see which physicians treated the patient during the **Visit**, you could add the following relationship to the query:

```
MATCH (p:Patient)-[h:HAS]->(v:Visit)<-[t:TREATS]-(ph:Physician)
WHERE v.id = 56
RETURN v,p,ph
```

This statement (p:Patient)-[h:HAS]->(v:Visit)<-[t:TREATS]-(ph:Physician) tells Neo4j to find all patterns where a Patient has a Visit that’s treated by a Physician. If you wanted to match all relationships going in and out of the Visit node, you could run this query:

```
MATCH (v:Visit)-[r]-(n)
WHERE v.id = 56
RETURN r,n;

```

Notice now that the relationship [r], has no direction with respect to (v:Visit) or (n). In essence, this match statement will look for all relationships that go in and out of Visit 56, along with the nodes connected to those relationships. Here’s the results:

![Cypher query matching all relationships and nodes to Visit 56](../assets/query_match_all_rel.png 'Cypher query matching all relationships and nodes to Visit 56')

This gives you a nice view of all the relationships and nodes associated with Visit 56. Think about how powerful this representation is. Instead of performing multiple SQL joins, as you’d have to do in a relational database, you get all of the information about how a Visit is connected to the entire hospital system with three short lines of Cypher.

You can imagine how much more powerful this would become as more nodes and relationships are added to the graph database. For example, you could record which nurses, pharmacies, drugs, or surgeries are associated with the Visit. Each relationship that you add would necessitate another join in SQL, but the above Cypher query about Visit 56 would remain unchanged.

The last thing you’ll cover in this section is how to perform aggregations in Cypher. So far, you’ve only queried raw data from nodes and relationships, but you can also compute aggregate statistics in Cypher.

Suppose you wanted to answer the question What is the total number of visits and total billing amount for visits covered by Aetna in Texas? Here’s the Cypher query that would answer this question:

```
MATCH (p:Payer)<-[c:COVERED_BY]-(v:Visit)-[:AT]->(h:Hospital)
WHERE p.name = "Aetna"
AND h.state_name = "TX"
RETURN COUNT(*) as num_visits,
SUM(c.billing_amount) as total_billing_amount;
```

In this query, you first match all Visits that occur at a Hospital and are covered by a Payer. You then filter to Payers with a name property of Aetna and Hospitals with a state_name of TX. Lastly, COUNT(\*) counts the number of matched patterns, and SUM(c.billing_amount) gives you the total billing amount. The output looks like this:

![Cypher aggregate query](../assets/neo4j_aggr_query.png 'Cypher aggregate query')

The results tell you there were 198 **Visits** matching this pattern with a total billing amount of about $5,056,439.

You now have a solid understanding of Cypher fundamentals, as well as the kinds of questions you can answer. In short, Cypher is great at matching complicated relationships without requiring a verbose query. There’s a lot more that you can do with Neo4j and Cypher, but the knowledge you obtained in this section is enough to start building the chatbot, and that’s what you’ll do next.
