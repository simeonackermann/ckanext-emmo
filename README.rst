=============
ckanext-emmo
=============

Extend the [ckanext-dcat](https://github.com/ckan/ckanext-dcat) RDF DCAT endpoints with the [EMMO](https://github.com/emmo-repo/EMMO) RDF ontology profile.

This plugin is in a very early state to survey the feasibility of an RDF mapping from CKAN datasets to the EMMO ontology. Currently no EMMO fields are implemented.

------------
Requirements
------------

Requires the [ckanext-dcat](https://github.com/ckan/ckanext-dcat) plugin.

------------
Installation
------------

Install [ckanext-dcat](https://github.com/ckan/ckanext-dcat) first.

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
