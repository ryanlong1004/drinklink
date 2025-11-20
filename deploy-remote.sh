#!/bin/bash
# Script to deploy updated docker-compose.synology.yml to Synology NAS

SYNOLOGY_HOST="drinklink.rlong.i234.me"
SYNOLOGY_PATH="/volume1/docker/drinklink"

echo "=== DrinkLink Remote Deployment ==="
echo ""

# Copy updated docker-compose file to Synology
echo "1. Copying docker-compose.synology.yml to Synology..."
scp docker-compose.synology.yml ${SYNOLOGY_HOST}:${SYNOLOGY_PATH}/

# Run the force update script on Synology
echo ""
echo "2. Running force update on Synology..."
ssh ${SYNOLOGY_HOST} "cd ${SYNOLOGY_PATH} && bash force-update-synology.sh"

echo ""
echo "✅ Deployment complete!"
echo "Visit: http://drinklink.rlong.i234.me:3080"
