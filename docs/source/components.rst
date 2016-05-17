Components
==========

Ideally, aleph is deployed in a containerized environment. However, it is very much possible to run it without Docker.

This section of the documentation describes the components - outside of a containerized environment.



Web interface
------------
The web frontend for Aleph.

* Aleph web interface can be served on any wsgi http server such as gunicorn::

  $ gunicorn -w 5 -b 0.0.0.0:8000 --log-level info --log-file /var/log/gunicorn.log aleph.manage:app

  For production workloads, it might be a good idea to proxy to the gunicorn server from nginx or apache



Crawlers
--------



Ingestors
---------
