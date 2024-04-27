# Create a Neo4j Account and AuraDB Instance

To get started using Neo4j, you can create a free [Neo4j AuraDB](https://neo4j.com/cloud/aura-free/) account. The landing page should look something like this:

![Neo4j Aura](../assets/graphdb.png 'Neo4j Aura getting started screen')

Click the **Start Free** button and create an account. Once you’re signed in, you should see the Neo4j Aura console:

![Neo4j Aura](../assets/start_free.png 'Create a new Aura instance')

Click **New Instance** and create a free instance. A modal should pop up similar to this:

![Neo4j Aura](../assets/new_instance.png 'New Aura instance modal')

After you click **Download and Continue**, your instance should be created and a text file containing the Neo4j database credentials should download. Once the instance is created, you’ll see its status is **Running**. There should be no nodes or relationships yet:

![Neo4j Aura](../assets/instance_running.png 'Aura running instance')

Next, open the text file you downloaded with your Neo4j credentials and copy the NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD into your .env file:

```python
NEO4J_URI=<YOUR_NEO4J_URI>
NEO4J_USERNAME=<YOUR_NEO4J_URI>
NEO4J_PASSWORD=<YOUR_NEO4J_PASSWORD>

```

You’ll use these environment variables to connect to your Neo4j instance in Python so that your chatbot can execute queries.

**Note:** By default, your NEO4J_URI should be similar to neo4j+s://.databases.neo4j.io. The URL scheme neo4j+s uses [CA-signed certificates](https://en.wikipedia.org/wiki/Certificate_authority) only, which might not work for you. If this is the case, change your URI to use the neo4j+ssc URL scheme - neo4j+ssc://.databases.neo4j.io. You can read more about what this means in the Neo4j documentation on [connection protocols and security](https://neo4j.com/docs/python-manual/current/connect-advanced/#_connection_protocols_and_security).

You now have everything in place to interact with your Neo4j instance. Next up, you’ll design the hospital system graph database. This will tell you how the hospital entities are related, and it will inform the kinds of queries you can run.
