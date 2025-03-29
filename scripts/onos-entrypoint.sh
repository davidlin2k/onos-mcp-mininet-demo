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

# Wait for required apps to be installed
wait_for_app() {
  APP_ID=$1
  echo "Waiting for $APP_ID to be installed..."
  while ! curl -s -u onos:rocks http://localhost:8181/onos/v1/applications/$APP_ID > /dev/null 2>&1; do
    echo "$APP_ID not yet installed. Waiting 3 seconds..."
    sleep 3
  done
  echo "$APP_ID is now installed."
}

# Wait for both required apps to be installed
wait_for_app "org.onosproject.openflow"
wait_for_app "org.onosproject.fwd"

# Activate required apps
echo "Activating OpenFlow app..."
curl -s -X POST -u onos:rocks http://localhost:8181/onos/v1/applications/org.onosproject.openflow/active

echo "Activating Reactive Forwarding app..."
curl -s -X POST -u onos:rocks http://localhost:8181/onos/v1/applications/org.onosproject.fwd/active

echo "ONOS setup completed successfully!"

# Keep the container running
wait
