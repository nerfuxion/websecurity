#https://github.com/nerfuxion/websecurity

#RedShield - Written by Fredrik Söderlund

#www.redshield.co

# websecurity
Vulnerable webserver and database system - For expermentation and learning

The System consists of two components and one example attack:

**webserver** - A very small and minimalist web server that serves up pages from the **www** folder. It also communicates with the database

**database** - An even smaller database server that responds to requests from the webserver and serves up information that are stored in the **secrets** folder

**attack** - An example of a multi stage attack on the system. It attempts to read the database credentials from the webserver file system, and then uses the credentials to request information from the database directly, bypassing the webserver.


