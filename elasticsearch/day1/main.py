#!/usr/bin/env python3
import os
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
    if document == 0:
        print("No documents")
    ##

if __name__ == "__main__":
    assert_es_connection()
    assert_patient_accounts_index()
