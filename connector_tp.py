import os
import json
import tornado.httpclient


files = [item for item in os.listdir("../schema_mgr/schemas") if item.endswith(".json")]
files = ["add_tenant.json","add_tenant_domain.json","fod_report.json"]
files = ["download_flow_ext.json","upload_flow_ext.json",]
#files = ["download_flow.json",]
client = tornado.httpclient.HTTPClient()
template = open("hdfs-connector-config.json","r").read()
for item in files:
    pos = item.rfind(".")
    topic = item[:pos]
    body = template.replace("{{topic}}",topic)
    name = json.loads(body)["name"]
    url = "http://bridge-node-1:8083/connectors"
    req = tornado.httpclient.HTTPRequest(url,"POST",{"Content-Type": "application/json"},body)
    resp = client.fetch(req)
    print resp.body
