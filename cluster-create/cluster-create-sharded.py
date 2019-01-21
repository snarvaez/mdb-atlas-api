#!/usr/bin/env python3

# PLEASE ensure the API Whitelist under
# https://cloud.mongodb.com/v2#/account/publicApi
# is updated with your new IP obtained at the prospect/customer network

# REPLACE your Atlas Username, API Key and ProjectId below

import json, sys, time, datetime
import pycurl
import requests
from requests.auth import HTTPDigestAuth

userName    = "ATLAS-USER-NAME"
apiKey      = "ATLAS-API-KEY"
projectId   = "ATLAS-PROJECTID"
clusterName = "SA-PoV"

urlCreate = "https://cloud.mongodb.com/api/atlas/v1.0/groups/" \
    + projectId + "/clusters"

urlStatus = "https://cloud.mongodb.com/api/atlas/v1.0/groups/" \
    + projectId + "/clusters/" + clusterName

headers = {
    'Content-Type': 'application/json',
}

# For complete options, see
# https://docs.atlas.mongodb.com/reference/api/clusters-create-one/
data = {
  "name": clusterName,
  "clusterType": "SHARDED",
  "mongoDBMajorVersion": "3.6",
  "numShards": 3,
  "providerSettings": {
    "providerName": "AWS",
    "regionName": "US_WEST_2",
    "instanceSizeName": "M30",
    "encryptEBSVolume": True
  },
  "replicationFactor": 3,
  "backupEnabled": True,
  "autoScaling": {"diskGBEnabled": True}
}

t1 = datetime.datetime.now()
print(t1, " - Creating cluster: ", clusterName)
response = requests.post(urlCreate, headers=headers, data=json.dumps(data),
                         auth=HTTPDigestAuth(userName, apiKey))

timeout = time.time() + 60*15  # 15 minute timeout
while True:
    response = requests.get(urlStatus, auth=HTTPDigestAuth(userName, apiKey))
    stateName = response.json()["stateName"]
    t2 = datetime.datetime.now()
    print(t2, " - Cluster status: ", stateName)

    if stateName == "IDLE":
        print("Cluster created in: ", t2-t1)
        break
    if time.time() > timeout:
        print("TIMEOUT: Cluster creation is still in progress")
        print("Please go to the MongoDB Atlas UI.")
        break
    time.sleep(5)
