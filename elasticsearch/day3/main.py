#!/usr/bin/env python3
import os
import json
from pprint import pprint
import elasticsearch
from elasticsearch.helpers import bulk


INDEX_NAME = "patient_accounts_v3"


es = elasticsearch.Elasticsearch("http://127.0.0.1:9200",
                                 basic_auth=("elastic", "HrYPbZF7"),)

def assert_es_connection():
    """ Checking Elasticsearch connection """

    print("Checking Elasticsearch connection...")
    try:
        es.ping()
        print("Elasticsearch connection successful.")
    except elasticsearch.exceptions.ConnectionError:
        print("Elasticsearch connection failed.")
        exit(1)

    rtc = es.info()
    print("Elasticsearch is info:", rtc)

    ##
    # Create an index
    indices = es.cat.indices(format="json")

    for index in indices:
        print("Index name:", index["index"])
    ##

def assert_patient_accounts_index():
    """ Checking patient_accounts index """

    mapping = {
        'properties': {
            'balance': {'type': 'float'},
            'description': {'type': 'text'},
            'patient_id': {'type': 'keyword'},
            'provider': {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}},
            'status': {'type': 'keyword'}
            }
    }

    indices = es.cat.indices(format="json")
    if not any(index["index"] == INDEX_NAME for index in indices):
        es.indices.create(index=INDEX_NAME, mappings=mapping)
        print(f"Index {INDEX_NAME} created.")


    shards = es.cat.shards(format="json", index=INDEX_NAME)
    for shard in shards:
        print("shard info:", shard)

    ##
    # Populate the index with some data
    document = es.count(index=INDEX_NAME)["count"]
    print("Patient documents count:", document)
    if document != 0:
        return
    ##
    pprint(es.indices.get_mapping(index=INDEX_NAME))

    print("loading documents")
    cwd = os.path.dirname(os.path.abspath(__file__))
    dataset = os.path.join(cwd, "..", "dataset", "patients.json")
    print("Current working directory:", cwd)
    with open(dataset, "r", encoding="utf-8") as hndl:
        accounts = json.load(hndl)
        for account in accounts:
            print("loading account:", account)
            es.index(index=INDEX_NAME, id=account["patient_id"], document=account)
        print(f"Documents loaded into {INDEX_NAME} index.")


def update_patient_account():
    """ Update patient_accounts index """

    updated_account = {
        "patient_id": "P0001",
        "provider": "Northwest Medical",
        "balance": 150.0,
        "status": "OPEN",
        "description": "Cardiology patient payment"
    }
    es.index(index=INDEX_NAME, id=updated_account["patient_id"], document=updated_account)

    doc = es.get(index=INDEX_NAME, id=updated_account["patient_id"])
    assert doc["_source"]["balance"] == 150.0, "Expected balance to be 150.0"
    print("Updated document:", doc["_source"])

    # Lucene documents are immutable.

    es.update(index=INDEX_NAME, id=updated_account["patient_id"], doc={"balance": 600.00 })
    doc = es.get(index=INDEX_NAME, id=updated_account["patient_id"])
    assert doc["_source"]["balance"] == 600.0, f"Expected balance to be 600.0 {doc}"
    assert doc["_source"]["provider"] == "Northwest Medical", "Expected provider to be 'Northwest Medical'"


def patient_search():
    """ Search patient_accounts index """

    query = {
        "query": {
            "match": {
                "provider": "medical"
            }
        }
    }

    results = es.search(index=INDEX_NAME, body=query)

    print("hits for provider medical:")
    for result in results["hits"]["hits"]:
        print("  hit id=%(_id)s score=%(_score)s source=%(_source)s" % result)


def patient_keyword():
    """ Search patient_accounts keyword"""

    query = {
        "query": {
            "term": {
                "provider.keyword": "northwest medical"
            }
        }
    }

    results = es.search(index=INDEX_NAME, body=query)

    print("hits for provider medical:")
    for result in results["hits"]["hits"]:
        print("  hit id=%(_id)s score=%(_score)s source=%(_source)s" % result)

    ##
    # since I used lower case for provier. term keyword search is case sensitive.
    assert len(results["hits"]["hits"]) == 0, "Expected 0 hit for provider 'northwest medical'"
    ##


def bulk_load_documents():
    """ Bulk load documents into patient_accounts index """

    print("bulk loading documents")
    cwd = os.path.dirname(os.path.abspath(__file__))
    dataset = os.path.join(cwd, "..", "dataset", "patients.json")

    actions = []
    with open(dataset, "r", encoding="utf-8") as hndl:
        actions = [
            {
                "_index": INDEX_NAME,
                "_id": account["patient_id"],
                "_source": account
            }
            for account in json.load(hndl)
        ]

    actions.append({
        "_index": INDEX_NAME,
        "_id": "P1004",
        "_source": {
            "patient_id": "P1004",
            "provider": "Valley Health",
            "balance": 300.0,
            "status": "OPEN",
            "description": "Emergency department account"
        }
    })

    success, errors = bulk(es, actions)
    print(success, errors)


def should_search():
    """ Search patient_accounts index with different search types """

    query = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"description": "cardiology"}},
                    {"match": {"description": "payment"}},
            ],
            "minimum_should_match": 1,
            "filter": [
                {
                    "term": { "status": "OPEN" }
                }
            ]
            }
        }
    }

    results = es.search(index=INDEX_NAME, body=query)
    for result in results["hits"]["hits"]:
        print("  hit id=%(_id)s score=%(_score)s source=%(_source)s" % result)


def show_mapping():
    """ Show mapping for patient_accounts index """

    mapping = es.indices.get_mapping(index=INDEX_NAME)

    print(f"Mapping for {INDEX_NAME} index:")
    pprint(mapping)


if __name__ == "__main__":
    assert_es_connection()
    assert_patient_accounts_index()
    update_patient_account()
    bulk_load_documents()
    should_search()
