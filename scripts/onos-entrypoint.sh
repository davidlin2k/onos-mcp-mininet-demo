#!/bin/sh

# Start ONOS in the background
./bin/onos-service server &

# Wait for ONOS REST API to be available
echo "Waiting for ONOS REST API to become available..."
until curl -s -f -u onos:rocks http://localhost:8181/onos/v1/applications > /dev/null 2>&1; do
  echo "ONOS REST API not yet available. Waiting 5 seconds..."
  sleep 5
done

echo "ONOS REST API is now available!"

# Activate required apps
echo "Activating OpenFlow app..."
curl -s -X POST -u onos:rocks http://localhost:8181/onos/v1/applications/org.onosproject.openflow/active

echo "Activating Reactive Forwarding app..."
curl -s -X POST -u onos:rocks http://localhost:8181/onos/v1/applications/org.onosproject.fwd/active

echo "ONOS setup completed successfully!"

# Keep the container running
wait
