import os
import json
import tornado.httpclient


#files = [item for item in os.listdir("../schema_mgr/schemas") if item.endswith(".json")]
#topics = []
#for item in files:
#    pos = item.rfind(".")
#    topic = item[:pos]
#    topics.append(topic)

client = tornado.httpclient.HTTPClient()
template = open("hdfs-connector-config.json","r").read()
with open("topics.txt","r") as file_handler:
    for line in  file_handler:
        topic = line.strip()
        if not topic:
            continue
        flush_size = "10000"
        rotate_interval_ms = "180000"
        if topic in ("add_tenant","add_tenant_domain"):
            flush_size = "1"
            rotate_interval_ms = "1"
        body = template.replace("{{topic}}",topic).replace("{{flush.size}}",flush_size).replace("{{rotate.interval.ms}}",rotate_interval_ms)
        url = "http://bridge-node-1:8083/connectors"
        req = tornado.httpclient.HTTPRequest(url,"POST",{"Content-Type": "application/json"},body)
        resp = client.fetch(req)
        print resp.body
        print body