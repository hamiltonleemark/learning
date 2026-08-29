#!/usr/bin/env python3
import elasticsearch

es = elasticsearch.Elasticsearch("http://127.0.0.1:9200",
                                 basic_auth=("elastic", "HrYPbZF7"),)

rtc = es.ping()

print("Elasticsearch is running:", rtc)
