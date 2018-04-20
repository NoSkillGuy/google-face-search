Google Face Search
##################

Python Script for 'searching' and 'downloading' hundreds of face recognized Google images to the local hard disk!

Contents

.. contents:: :local:

Summary
=======

This is a command line python program to search using a image with a human face on Google Images
and download images to your computer. You can also invoke this script from another python file.

This repo is a wrapper script over `google-images-download <https://github.com/hardikvasa/google-images-download/>`_. All the arguments supported by `google-images-download` are supported here also. Please go through the `Readme <https://github.com/hardikvasa/google-images-download/blob/master/README.rst/>`

Compatability
=============

This program is compatible with both the versions of python - 2.x and 3.x (recommended).
It is a download-and-run program with no changes to the file.
You will just have to specify parameters through the command line.

Installation
============

You can use **one of the below methods** to download and use this repository.

Using pip

.. code-block:: bash

    $ pip install google_face_search

Manually using CLI

.. code-block:: bash

    $ git clone https://github.com/NoSkillGuy/google-face-search.git
    $ cd google-face-search && sudo python setup.py install

Manually using UI

Go to the `repo on github <https://github.com/NoSkillGuy/google-face-search>`__ ==> Click on 'Clone or Download' ==> Click on 'Download ZIP' and save it on your local disk.

Usage - Using Command Line Interface
====================================

If installed via pip or using CLI, use the following command:

.. code-block:: bash

    $ googlefacesearch [Arguments...]

Also, a short form of the above command gets installed when you install 

.. code-block:: bash
    
    $ gfs [Arguments...]

If downloaded via the UI, unzip the file downloaded, go to the 'google_face_search' directory and use one of the below commands:

.. code-block:: bash

    $ python3 google_face_search.py [Arguments...]
    OR
    $ python google_face_search.py [Arguments...]


Usage - From another python file
================================

If you would want to use this library from another python file, you could use it as shown below:

.. code-block:: python

    from google_face_search import google_face_search

    response_obj = google_face_search.googlefacesearch()
    response_obj.download({<Arguments...>})


Arguments
=========

+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| Argument          | Short hand  | Description                                                                                                                   |
+===================+=============+===============================================================================================================================+
| config_file       | cf          | You can pass the arguments inside a config file. This is an alternative to passing arguments on the command line directly.    |
|                   |             |                                                                                                                               |
|                   |             | Please refer to the                                                                                                           |
|                   |             | `config file format <https://github.com/NoSkillGuy/google-face-search/blob/master/README.rst#config-file-format>`__ below     |
|                   |             |                                                                                                                               |
|                   |             | * If 'config_file' argument is present, the program will use the config file and command line arguments will be discarded     |
|                   |             | * Config file can only be in **JSON** format                                                                                  |
|                   |             | * Please refrain from passing invalid arguments from config file. Refer to the below arguments list                           |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| known_images_path | kip         | Specify the `known images path`. This path should contain images only from these whitelisted formats (jpg, png, gif, bmp).    |
|                   |             | The name of the person is syntactically drawn from the filename without the extension.                                        |
|                   |             | Example:                                                                                                                      |
|                   |             |         - If the file name is Steve Jobs.png, then the name derived is Steve Jobs                                             |
|                   |             |         - If the file name is Elon Musk.png, then the name derived is Elon Musk                                               |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| version           | v           | Displays the current version                                                                                                  |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| help              | h           | Show the help message regarding the usage of the above arguments                                                              |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+

Apart from all the above arguments, All arguments listed of `google-images-download <https://github.com/hardikvasa/google-images-download/blob/master/README.rst#arguments>` are supported

Config File Format
==================

You can either pass the arguments directly from the command as in the examples below or you can pass it through a config file. Below is a sample of how a config
file looks.

You can pass more than one record through a config file. The below sample consist of two set of records. The code will iterate through each of the record and
download images based on arguments passed.

.. code:: json

    {
        "Records": [
            {
                "keywords": "apple",
                "limit": 5,
                "color": "green",
                "print_urls": true
            },
            {
                "keywords": "universe",
                "limit": 15,
                "size": "large",
                "print_urls": true
            }
        ]
    }

--------------

Contribute
==========

Anyone is welcomed to contribute to this script.
If you would like to make a change, open a pull request.
For issues and discussion visit the
`Issue Tracker <https://github.com/NoSkillGuy/google-face-search/issues>`__.

The aim of this repo is to keep it simple, stand-alone, backward compatible and 3rd party dependency proof.

Disclaimer
==========

This program lets you download tons of images from Google.
Please do not download or use any image that violates its copyright terms.
Google Images is a search engine that merely indexes images and allows you to find them.
It does NOT produce its own images and, as such, it doesn't own copyright on any of them.
The original creators of the images own the copyrights.

Images published in the United States are automatically copyrighted by their owners,
even if they do not explicitly carry a copyright warning.
You may not reproduce copyright images without their owner's permission,
except in "fair use" cases,
or you could risk running into lawyer's warnings, cease-and-desist letters, and copyright suits.
Please be very careful before its usage!
