==================================
The Server-Client Connection Model
==================================


Prerequisites
-------------
The only prerequisite for this models is that the server must have an SSL certificate that was 
signed by a CA that every client that is going to connect to the server trusts.


Model Overview
--------------
This model is the simplest model and is the base model that all other models build upon.
The connection consists of a single server and a single client, all of the connected clients 
are isolated from each other and are not capable of communicating between them. This model is 
mainly used for APIs and web servers.


Usage
-----



Security Overview
-----------------
The connection is fully encrypted using TLS 1.3 ciphersuites, as long as the certificates used 
are valid - you shouldn't worry about the security of this connection.
