---
title: How to visualize your system architecture using the C4 model?
description: As a software developer or system architect you often have a task to visualize your existing or potential application architecture for other people. Your audience can be software developers, but also business stakeholders (Customers, Product Owners, CEO, etc.). The architecture diagram should take on a distinctive look depending on whatever group you choose to present for your work.
tags: software-development software-architecture c4model
---

As a software developer or system architect you often have a task to visualize your existing or potential application architecture for other people. Your audience can be software developers, but also business stakeholders (Customers, Product Owners, CEO, etc.). The architecture diagram should take on a distinctive look depending on whatever group you choose to present for your work. In this article, I'd want to give an illustration of how the C4 model might be used to easily target the various audiences mentioned above.

## System requirements
We need a sample system with the functional criteria specified before we can begin designing our system. For the purposes of this article, I can create a concise system specification. The system's name will be MyDocs:

1. The system should be implemented as a Single Page Application on the front-end side.
2. The system is only for authenticated users with open registration.
3. There should be two types of users with different functionalities available:
  - the Editor can create and edit documents and search for documents to view.
  - the Reviewer can search for documents and write a document review.
4. Search for documents is a crucial feature. The system should implement full-text search, searching by document details and attributes.
5. The system should have the functionality of exporting documents to the existing external system called Document Registry System (DRS), using the HTTP REST API provided by DRS.

Using the C4 model approach, we can create a diagram of the system architecture once we know what our system should be able to do.

## C4 model diagram
[C4 model](https://c4model.com/) is a great tool for describing and communicating system architecture. It uses 4 levels of abstractions, where each subsequent level can give more detailed information about the system:
- System Context
- Containers
- Components
- Code

If you want to broaden your knowledge about the C4 model I strongly recommend watching [Simon Brown's (C4 model concept author) talk](https://www.youtube.com/watch?v=x2-rSnhpw0g) about it.

We now get into technicalities. I'll quickly outline each level and show an example diagram implementation.

### System Context level
At this highest level, a diagram shows the big picture of a system. It visualizes interactions between our system (`SoftwareSystem`) and actors (`Person`), and other systems (`SoftwareSystem`). For non-technical persons who are not focused on the exact technology that was implemented but want to get a broad sense of the system landscape, it can be incredibly helpful.

![Screenshot from 2022-11-09 13-03-26.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1667995439168/XGN3TE6bB.png)

At this level, we can see two actors: the Editor and the Reviewer that interact with our system. There is also DRS external system that MyDocs send documents to using API and an Email System that enables us to send e-mail messages (e.g. in a user sign-up process). Internal systems are colored differently (in blue) than external systems (in grey).

### Containers level
At the container level, we can learn more about the structure of our system. Containers should be treated as separately runnable or deployable units (e.g. web server application, database, etc.) and should not be confused with docker containers. This level gives us some information about the technologies and data stores used.

![Screenshot from 2022-11-09 13-13-02.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1667996000055/H9JX7pt8v.png)

We can see that our front-end application is a Single Page Application in React JS with Apollo GraphQL framework for API data fetching. The back-end system is implemented in Python, using the web API framework Flask. We have two database systems that our back-end interacts with: the first one is PostgreSQL to store documents in a relational manner and the second one - ElasticSearch which stores documents in a way that is convenient for robust searching. 

### Components level
At the third level, we can go into details of a specific container and see what components it is consisted of. This level has a strong connection to our codebase, so the best option is to derive it directly from the code to avoid inconsistencies. Here we present the contents of the Backend Application container. 

![Screenshot from 2022-11-09 13-25-03.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1667996828462/DAbwzOkvV.png)

We can see how responsibilities in the system are allocated. There is a GraphQL API component that serves as an API gateway to our application. There are four application services that implement business use cases:
- Document Management Service - enables adding/editing documents by Editors. 
- Document Review Service - enables reviewing documents by Reviewers.
- User Sign-Up Service - provides registration functionality for both Editors and Reviewers.
- User Sign-In Service - provides authentication functionality for both Editors and Reviewers.

We have also three infrastructure services:
- Notification Sender - provides notification template and can communicate with the third-party system for email sending.
- Search Engine - provides a proper model for document searching.
- Document Export Component - is a facade for communication with the external system DRS.

This level is rather dedicated to technical people.

### Code level
In the last level, we should provide some code (e.g. UML diagrams, ERD diagrams), but following Simon Brown's recommendation, we skip it. This step is usually redundant to our codebase and does not provide much value.

## Conclusion
The C4 model is quite an easy and straightforward form of visualizing architecture diagrams. It can be useful for both engineers and non-technical staff. The above diagrams can be generated from one DSL code snippet. I have used to it [structurizr.com](https://structurizr.com) platform. You can preview diagrams using [link](https://structurizr.com/dsl?src=https://raw.githubusercontent.com/jorzel/system-architecture/main/c4model.dsl). If you would like to tinker with it, I leave the DSL code in [my repo](https://github.com/jorzel/system-architecture). All you need is to sign up on the platform, paste the DSL code [here](https://structurizr.com/dsl) and render the diagram at the chosen level. If you have any questions or would like to share your experience, please leave a comment. You definitely should give it a try.

