# Design the Hospital System Graph Database

Now that you have a running Neo4j AuraDB instance, you need to decide which nodes, relationships, and properties you want to store. One of the most popular ways to represent this is with a flowchart. Based on your understanding of the hospital system data, you come up with the following design:

![Graph Database](../assets/hospital_neo4j_design.png 'Hospital system graph database design')

This diagram shows you all of the nodes and relationships in the hospital system data. One useful way to think about this flowchart is to start with the Patient node and follow the relationships. A Patient has a visit at a hospital, and the hospital employs a physician to treat the visit which is covered by an insurance payer.

Here are the properties stored in each node:

![Graph Database](../assets/hostipal_sys_node.png 'Hospital system node properties')

The majority of these properties come directly from the fields you explored in [step 2](../../business/data/). One notable difference is that Review nodes have an embedding property, which is a vector representation of the patient_name, physician_name, and text properties. This allows you to do [vector searches](https://neo4j.com/docs/cypher-manual/current/indexes-for-vector-search/) over review nodes like you did with ChromaDB.

Here are the relationship properties:

![Graph Database](../assets/hospital_sys_rel.png 'Hospital system relationship properties')

As you can see, **COVERED_BY** is the only relationship with more than an **id** property. The **service_date** is the date the patient was discharged from a visit, and **billing_amount** is the amount charged to the payer for the visit.

**Note:** This fake hospital system data has a relatively small number of nodes and relationships than what you’d typically see in an enterprise setting. However, you can easily imagine how many more nodes and relationships you could add for a real hospital system. For instance, nurses, pharmacists, pharmacies, prescription drugs, surgeries, patient relatives, and many more hospital entities could be represented as nodes.

You could also redesign this so that diagnoses and symptoms are represented as nodes instead of properties, or you could add more relationship properties. You could do all of this without changing the design you already have. This is the beauty of graphs—you simply add more nodes and relationships as your data evolves.

Now that you have an overview of the hospital system design you’ll use, it’s time to move your data into Neo4j!
