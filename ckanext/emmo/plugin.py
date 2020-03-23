import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.helpers import url_for
from logging import getLogger

from ckantoolkit import config

import rdflib
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import Namespace, RDF, XSD, SKOS, RDFS

from ckanext.dcat.profiles import RDFProfile
from ckanext.dcat.utils import resource_uri, publisher_uri_from_dataset_dict, DCAT_EXPOSE_SUBCATALOGS, DCAT_CLEAN_TAGS

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
ADMS = Namespace("http://www.w3.org/ns/adms#")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
SCHEMA = Namespace('http://schema.org/')
TIME = Namespace('http://www.w3.org/2006/time')
LOCN = Namespace('http://www.w3.org/ns/locn#')
GSP = Namespace('http://www.opengis.net/ont/geosparql#')
OWL = Namespace('http://www.w3.org/2002/07/owl#')
SPDX = Namespace('http://spdx.org/rdf/terms#')

namespaces = {
    'dct': DCT,
    'dcat': DCAT,
    'adms': ADMS,
    'vcard': VCARD,
    'foaf': FOAF,
    'schema': SCHEMA,
    'time': TIME,
    'skos': SKOS,
    'locn': LOCN,
    'gsp': GSP,
    'owl': OWL,
    'spdx': SPDX,
}

log = getLogger(__name__)

class EmmoPlugin(plugins.SingletonPlugin):
    pass

class EmmoAPProfile(RDFProfile):

    def graph_from_dataset(self, dataset_dict, dataset_ref):
        '''
        Create RDF from CKAN dataset

        dataset_dict = { id, license, version, name, tags ... } # attributes
            # see JSON data, eg. (http://localhost:5000/api/3/action/package_show?id=ID) of a dataset
        dataset_rf = url to dataset, # eg. http://localhost:5000/dataset/interaktiver-stadtplan-leipzig4fe19
        '''

        g = self.g

        # Namespaces
        self._bind_namespaces()

        log.debug("graph_from_dataset, dataset_dict: %s" % dataset_dict )
        log.debug("graph_from_dataset, dataset_ref: %s" % dataset_ref)

        # create rdf:type is schema:Dataset
        g.add((dataset_ref, RDF.type, SCHEMA.Dataset))

        # Basic fields
        self._basic_fields_graph(dataset_ref, dataset_dict)

        #
        # TODO add Catalog, Groups, Tags, ...
        #

        # Publisher
        # self._publisher_graph(dataset_ref, dataset_dict)


    def _bind_namespaces(self):
        self.g.bind('schema', namespaces['schema'])

    def _basic_fields_graph(self, dataset_ref, dataset_dict):
        # items item: (key, predicate, alternatives, type)
        # see ckanext-dcat/ckanext/dcat/profiles.py:_add_triple_from_dict()
        items = [
            ('identifier', SCHEMA.identifier, None, Literal),
            ('title', SCHEMA.name, None, Literal),
            ('notes', SCHEMA.description, None, Literal),
            ('version', SCHEMA.version, ['dcat_version'], Literal),
            ('license', SCHEMA.license, ['license_url', 'license_title'], Literal),
            # why add issued and modified without date?
            ('issued', SCHEMA.datePublished, ['metadata_created'], Literal),
            ('modified', SCHEMA.dateModified, ['metadata_modified'], Literal),

            # test, add state
            ('state', SCHEMA.state, ['state'], Literal),

            #
            # TODO add EMMO fields here...
            #
        ]
        self._add_triples_from_dict(dataset_dict, dataset_ref, items)

        items = [
            ('issued', SCHEMA.datePublished, ['metadata_created'], Literal),
            ('modified', SCHEMA.dateModified, ['metadata_modified'], Literal),
        ]

        self._add_date_triples_from_dict(dataset_dict, dataset_ref, items)

        # Dataset URL
        dataset_url = url_for('dataset_read',
                              id=dataset_dict['name'],
                              qualified=True)
        self.g.add((dataset_ref, SCHEMA.url, Literal(dataset_url)))

    def _publisher_graph(self, dataset_ref, dataset_dict):
        if any([
            self._get_dataset_value(dataset_dict, 'publisher_uri'),
            self._get_dataset_value(dataset_dict, 'publisher_name'),
            dataset_dict.get('organization'),
        ]):

            publisher_uri = publisher_uri_from_dataset_dict(dataset_dict)
            if publisher_uri:
                publisher_details = URIRef(publisher_uri)
            else:
                # No organization nor publisher_uri
                publisher_details = BNode()

            self.g.add((publisher_details, RDF.type, SCHEMA.Organization))
            self.g.add((dataset_ref, SCHEMA.publisher, publisher_details))


            publisher_name = self._get_dataset_value(dataset_dict, 'publisher_name')
            if not publisher_name and dataset_dict.get('organization'):
                publisher_name = dataset_dict['organization']['title']
            self.g.add((publisher_details, SCHEMA.name, Literal(publisher_name)))

            contact_point = BNode()
            self.g.add((contact_point, RDF.type, SCHEMA.ContactPoint))
            self.g.add((publisher_details, SCHEMA.contactPoint, contact_point))

            self.g.add((contact_point, SCHEMA.contactType, Literal('customer service')))

            publisher_url = self._get_dataset_value(dataset_dict, 'publisher_url')
            if not publisher_url and dataset_dict.get('organization'):
                publisher_url = dataset_dict['organization'].get('url') or config.get('ckan.site_url')

            self.g.add((contact_point, SCHEMA.url, Literal(publisher_url)))
            items = [
                ('publisher_email', SCHEMA.email, ['contact_email', 'maintainer_email', 'author_email'], Literal),
                ('publisher_name', SCHEMA.name, ['contact_name', 'maintainer', 'author'], Literal),
            ]

            self._add_triples_from_dict(dataset_dict, contact_point, items)


    def parse_dataset(self, dataset_dict, dataset_ref):

        g = self.g

        return dataset_dict


    def graph_from_catalog(self, catalog_dict, catalog_ref):
        g = self.g
