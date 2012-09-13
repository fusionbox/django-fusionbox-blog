Contact
=======

Intro
------
The contact module is designed to be a DRY style contact form.

Installation
------------

-  Add ``'fusionbox.contact'`` to your ``INSTALLED_APPS``
-  Run `./manage.py migrate` to create the necessary database tables
-  Create the required templates (see templates and views below)
-  Add urls to your url conf

Settings
--------

The contact module has the following settings values which which may be used to customize its behavior

``CONTACT_FORM_RECIPIENTS``
  Iterable of email addresses.  Each person in this list will be emailed for each contact form recipient.  If not present, the contact module will use the values present in the Recipients table.  (See the Recipients section)


Models
------
The contact application provides the following models.

.. automodule:: fusionbox.contact.models
    :members: 

Views
-----

The contact module provides the following class-based views located in ``fusionbox.contact.views``

.. automodule:: fusionbox.contact.views
    :members:


URLS
----
You may include the urls for the contact module one of two ways.

1. Include the built in url conf somewhere in your site url conf::
  
    url(r'^contact-us/', include('fusionbox.contact.urls')),

2. Manually include the urls for both the ``index`` and ``success`` views.  Often this is the best way to customize the contact form or add extra context variables.  The example below is equivilant to the include statement::
   
       (r'^contact-us/$', 'fusionbox.contact.views.index', name='contact_index'),
       (r'^contact-us/success/$', 'fusionbox.contact.views.success', name='contact_success'),

   

Templates
---------
The contact module requires you to create two templates.

Primary Contact Form Template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Default Location: ``contact/index.html``

This template is rendered with the context variable ``form``.

Example::

        <form method-"post">
            {% csrf_token %}
            {{ form }}
            {% uncaptcha %}
            <button type="submit">Submit</button>
        </form>

Success Page Template
^^^^^^^^^^^^^^^^^^^^^
Default Location: ``contact/success.html``

Example::

        <p>Thank you for contacting Us.  Someone will be in touch with you shortly!</p>

Email Template
^^^^^^^^^^^^^^
Default Location: ``mail/contact_form_submission.html``

Successful contact form submissions will be emailed using the fusionbox ``send_markdown_email`` function to a list of recipients.  The contact module will first look for ``CONTACT_FORM_RECIPIENTS`` in the settings file, and if not will use the values from the Recipients table.

Default Template::

        ---
        subject: Someone has filled out the contact form
        ---

        Someone has submitted the contact form.

        - *Name:* {{ submission.name }}
        - *Email:* {{ submission.email }}
        - *Comment:* {{ submission.comment }}

        Use the following link to view this submission.

        [{{ host }}{{ submission.get_absolute_url }}]({{ host }}{{ submission.get_absolute_url }})

Admin
-----
The contact app automatically registers the following admin classes for its models.

.. automodule:: fusionbox.contact.admin
    :members:

Recipients
----------
The contact module has two methods for designating recipients to be emailed with the details from contact form submissions.  If the ``CONTACT_FORM_RECIPIENTS`` value is present in the settings file, those recipeints will be used.

If the setting is not present, the Recipients model will be registered for the admin site, and the values there will be used.
