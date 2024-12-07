#!/bin/bash

pip install -r requirements.txt
docker pull apache/kafka:3.9.0
docker run -p 9092:9092 apache/kafka:3.9.0
