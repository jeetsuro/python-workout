#!/bin/bash
# Simple health check script
while true; do
    curl -sf http://localhost:5000/health > /dev/null
    if [ $? -eq 0 ]; then
        echo "$(date): Healthy"
    else
        echo "$(date): Unhealthy"
    fi
    sleep 10
done