# **Reconverse: a memory module for LLM applications**

**Project Instructions:**  
Scaffold a solution to the "general and somewhat ambiguous problem (...) of 'how can we get an LLM to layer in relevant insights from previous conversations, when generating text for new conversations from individual A to individuals B1, …, Bn?'"

**Proposal**:

* Design and scaffold a lightweight memory module that can be plugged into a wide range of AI communication applications (emails, chat, voice calls, Slack)  
* Demo its applicability via an example email exchange between a brand representative and retail manager

**High-level overview:**

* AI agent A has a sequential exchange (e.g. an email chain) with a counterparty B. A counterparty can be an individual (e.g. a retail manager), but is more likely to be a group (e.g. the Williamsburg WholeFoods team).  
* The messages in the exchange are successively fed into Reconverse in real time. Each successive message incrementally adds to A's memory of B (which also includes its own relationship with B). A's memory capabilities mimic human memory, which itself is optimized for efficient storage and retrieval: when deciding what information to retain, A will bias information that is important, novel, surprising, or unexpected.  
* A's memory of B is stored in a knowledge graph (KG) associated with B. Each counterparty B1, ..., Bn has a unique KG. A relational database is used to store the association between Bi's ID and its KG ID. The KG itself is managed by Neo4j.  
* Conversation input is sent into Reconverse as raw text together with a counterparty ID (used to map the counterparty to its KG) and sender flag (0 if text was sent by A, 1 if sent by B). Reconverse first increments the knowledge graph using the contents of the message. Then, if the message was sent by B, it will generate and return a paragraph with memory context to be used to generate A's response.  
* Maintaining each knowledge graph is realized through the open-source package iText2KG, which is an incremental knowledge graph constructor that allows the user to specify language models, embedding models, user-defined schemas, and user-defined queries to build and increment the KGs.