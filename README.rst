*****************
Django Magic Link
*****************

A reusable django app for authenticating users by their email address. This is a slightly refactored version of https://www.photondesigner.com/articles/email-sign-in.

Tested with:

* Python version 3.12.2
* Django version 5.0.2

Installation
------------

Clone main repository:

.. code-block:: bash

    $ git clone https://github.com/weholt/django_magic_link.git
    $ cd django_magic_link
    $ pip install .

Or

.. code-block:: bash

    $ pip install git+https://github.com/weholt/django_magic_link.git

Add `magic_link` to your installed apps and magic links urls to your urlpatterns:

.. code-block:: python

    # settings.py

    INSTALLED_APPS = [
        ...
        "magic_link",
        ...
    ]

    # and some settings for sending email
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" # for testing
    # EMAIL_BACKEND=os.environ['EMAIL_BACKEND']
    EMAIL_HOST = os.environ['EMAIL_HOST']
    EMAIL_PORT = os.environ['EMAIL_PORT']
    EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS']
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']    

    # urls.py
    urlpatterns += [
        ...
        path("magic-link/", include("magic_link.urls")),
        ...
    ]

Add these settings to .env and update as required:

.. code-block:: bash

    EMAIL_VERIFICATION_URL='http://localhost:8000/verify-email'
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST='smtp.gmail.com'
    EMAIL_HOST_USER=<your email address>
    EMAIL_HOST_PASSWORD=<your email app password>
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_USE_SSL=False

If you already have a custom user model, add this field to it:

.. code-block:: python
    
    has_verified_email = models.BooleanField(default=False)

Or you can remove the abstract part from the one supplied in the package and build on that:

.. code-block:: python

    # magic_link/models.py

    class User(AbstractUser):
        has_verified_email = models.BooleanField(default=False)

        class Meta:
            abstract = True

Basic Usage
-----------

Visit `http://yoursite//magic-link/` to sign in.

