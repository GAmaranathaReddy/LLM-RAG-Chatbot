# A Brief Overview of Graph Databases

Graph databases, such as Neo4j, are databases designed to represent and process data stored as a graph. Graph data consists of nodes, edges or relationships, and properties. Nodes represent entities, relationships connect entities, and properties provide additional metadata about nodes and relationships.

For example, here’s how you might represent hospital system nodes and relationships in a graph:

![over view](../assets/graphdb.png 'Hospital system graph')

This graph has three nodes - Patient, Visit, and Payer. Patient and Visit are connected by the HAS relationship, indicating that a hospital patient has a visit. Similarly, Visit and Payer are connected by the COVERED_BY relationship, indicating that an insurance payer covers a hospital visit.

Notice how the relationships are represented by an arrow indicating their direction. For example, the direction of the HAS relationship tells you that a patient can have a visit, but a visit cannot have a patient.

Both nodes and relationships can have properties. In this example, Patient nodes have id, name, and date of birth properties, and the COVERED_BY relationship has service date and billing amount properties. Storing data in a graph like this has several advantages:

- **Simplicity:** Modeling real-world relationships between entities is natural in graph databases, reducing the need for complex schemas that require multiple join operations to answer queries.

- **Relationships:** Graph databases excel at handling complex relationships. Traversing relationships is efficient, making it easy to query and analyze connected data.

- **Flexibility:** Graph databases are schema-less, allowing for easy adaptation to changing data structures. This flexibility is beneficial for evolving data models.

- **Performance:** Retrieving connected data is faster in graph databases than in relational databases, especially for scenarios involving complex queries with multiple relationships.

- **Pattern Matching:** Graph databases support powerful pattern-matching queries, making it easier to express and find specific structures within the data.

When you have data with many complex relationships, the simplicity and flexibility of graph databases makes them easier to design and query compared to relational databases. As you’ll see later, specifying relationships in graph database queries is concise and doesn’t involve complicated joins. If you’re interested, Neo4j illustrates this well with a realistic example database in their [documentation](https://neo4j.com/developer/cypher/guide-sql-to-cypher/).

Because of this concise data representation, there’s less room for error when an LLM generates graph database queries. This is because you only need to tell the LLM about the nodes, relationships, and properties in your graph database. Contrast this with relational databases where the LLM must navigate and retain knowledge of the table schemas and foreign key relationships throughout your database, leaving more room for error in SQL generation.

Next, you’ll begin working with graph databases by setting up a [Neo4j AuraDB](https://neo4j.com/cloud/aura-free/) instance. After that, you’ll move the hospital system into your Neo4j instance and learn how to query it.
