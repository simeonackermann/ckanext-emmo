=============
ckanext-emmo
=============

Extend the [ckanext-dcat](https://github.com/ckan/ckanext-harvest) RDF DCAT endpoints with the [EMMO](https://github.com/emmo-repo/EMMO) RDF ontology profile.

This plugin is in a very early state to survey the feasibility of an RDF mapping from CKAN datasets to the EMMO ontology. Currently no EMMO fields are implemented.

------------
Requirements
------------

Requires the [ckanext-dcat](https://github.com/ckan/ckanext-harvest) plugin.

------------
Installation
------------

Install [ckanext-dcat](https://github.com/ckan/ckanext-harvest) first.

To install ckanext-emmo:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-emmo Python package into your virtual environment::

    pip install -e git+https://github.com/simeonackermann/ckanext-emmo.git#egg=ckanext-emmo

3. Add ``emmo`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN.

--------
Endpoint
--------

To access data using the EMMO RDF profile specify it by using the `profiles=emmo_ap` query parameter on the dataset endpoints:

    http://{ckan-instance-host}/dataset/{dataset-id}.{format}?profiles=emmo_ap

Format can be eg.: xml, ttl, n3, jsonld

You can also access the catalog-wide endpoint with:

    http://{ckan-instance-host}/catalog.{format}?profiles=emmo_ap

See [ckanext-dcat#dataset-endpoints](https://github.com/ckan/ckanext-dcat#dataset-endpoints) for more information on how to access the RDF DCAT endpoints.

---------------------------------
Registering ckanext-emmo on PyPI
---------------------------------

ckanext-emmo should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-emmo. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


----------------------------------------
Releasing a New Version of ckanext-emmo
----------------------------------------

ckanext-emmo is availabe on PyPI as https://pypi.python.org/pypi/ckanext-emmo.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
