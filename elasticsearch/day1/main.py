#!/usr/bin/env python3
import os
import json
import elasticsearch

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

    indices = es.cat.indices(format="json")
    if not any(index["index"] == "patient_accounts" for index in indices):
        es.indices.create(index="patient_accounts")
        print("Index 'patient_accounts' created.")

    shards = es.cat.shards(format="json", index="patient_accounts")
    for shard in shards:
        print("shard info:", shard)

    ##
    # Populate the index with some data
    document = es.count(index="patient_accounts")["count"]
    print("Patient documents count:", document)
    if document != 0:
        return
    ##

    print("loading documents")
    cwd = os.path.dirname(os.path.abspath(__file__))
    dataset = os.path.join(cwd, "dataset", "patients.json")
    print("Current working directory:", cwd)
    with open(dataset, "r", encoding="utf-8") as hndl:
        accounts = json.load(hndl)
        for account in accounts:
            print("loading account:", account)
            es.index(index="patient_accounts", id=account["patient_id"], document=account)
        print("Documents loaded into 'patient_accounts' index.")

def patient_search():
    """ Search patient_accounts index """

    query = {
        "query": {
            "match": {
                "description": "cardiology"
            }
        }
    }

    results = es.search(index="patient_accounts", body=query)

    print("hits for cardiology:")
    for result in results["hits"]["hits"]:
        print("  hit id=%(_id)s score=%(_score)s source=%(_source)s" % result)

    ## multiple terms search. Note multiple terms means "OR" search
    query = {
        "query": {
            "match": {
                "description": "cardiology payment"
            }
        }
    }

    results = es.search(index="patient_accounts", body=query)

    print("hits for cardiology or payment:")
    for result in results["hits"]["hits"]:
        print("  hit id=%(_id)s score=%(_score)s source=%(_source)s" % result)


    ## multiple terms search with AND.
    query = {
        "query": {
            "match": {
                "description": {
                    "query": "cardiology payment",
                    "operator": "and"
                }
            }
        }
    }

    results = es.search(index="patient_accounts", body=query)

    print("hits for cardiology and payment:")
    for result in results["hits"]["hits"]:
        print("  hit id=%(_id)s score=%(_score)s source=%(_source)s" % result)

if __name__ == "__main__":
    assert_es_connection()
    assert_patient_accounts_index()
    patient_search()
