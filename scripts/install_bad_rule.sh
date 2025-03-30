#!/bin/bash

# Default ONOS API endpoint
ONOS_API="http://localhost:8181/onos/v1"

# ONOS default credentials
AUTH="onos:rocks"

# Flow rule definition
FLOW_RULE='{
  "priority": 50000,
  "timeout": 0,
  "isPermanent": true,
  "deviceId": "of:0000000000000001",
  "treatment": {
    "instructions": [
      {
        "type": "OUTPUT",
        "port": "1"
      }
    ]
  },
  "selector": {
    "criteria": [
      {
        "type": "ETH_TYPE",
        "ethType": "0x0800"
      }
    ]
  }
}'

# Install the flow rule using ONOS REST API and capture response
RESPONSE=$(curl -X POST \
     -H "Content-Type: application/json" \
     -u "${AUTH}" \
     "${ONOS_API}/flows/of%3A0000000000000001" \
     -d "${FLOW_RULE}" \
     -w "\nHTTP Status: %{http_code}\n")

echo "Response from ONOS:"
echo "$RESPONSE"

# Check if the request was successful (HTTP 200 or 201)
if echo "$RESPONSE" | grep -q "HTTP Status: 2[0-9][0-9]"; then
    echo "Flow rule installation successful"
else
    echo "Flow rule installation failed"
    exit 1
fi
