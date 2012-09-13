Blog
====

Intro
------
Reusable blog application for django

Installation
------------

-  Add ``'fusionbox.blog'`` to your ``INSTALLED_APPS``
-  Run `./manage.py migrate` to create the necessary database tables
-  Add urls to your url conf

Models
------

.. automodule:: fusionbox.blog.models
    :members: 

Views
-----

.. automodule:: fusionbox.blog.views
    :members:


URLS
----
Include the built in url conf somewhere in your site url conf::
  
    url(r'^blog/', include('fusionbox.blog.urls')),


Admin
-----

.. automodule:: fusionbox.blog.admin
    :members:
