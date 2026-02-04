#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}Starting Deployment Process${NC}"
echo -e "${GREEN}======================================${NC}"

# Navigate to Part4 directory
cd "$(dirname "$0")/.."

echo -e "\n${YELLOW}Step 1: Pulling latest Docker image${NC}"
docker pull ashmitad/cats-dogs-api:latest

echo -e "\n${YELLOW}Step 2: Stopping existing containers${NC}"
docker-compose -f docker-compose/docker-compose.yml down || true

echo -e "\n${YELLOW}Step 3: Starting new containers${NC}"
docker-compose -f docker-compose/docker-compose.yml up -d

echo -e "\n${YELLOW}Step 4: Waiting for service to be ready${NC}"
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Service is ready!${NC}"
        break
    fi
    echo "Waiting for service to start... ($((RETRY_COUNT + 1))/$MAX_RETRIES)"
    sleep 2
    RETRY_COUNT=$((RETRY_COUNT + 1))
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo -e "${RED}✗ Service failed to start within expected time${NC}"
    docker-compose -f docker-compose/docker-compose.yml logs
    exit 1
fi

echo -e "\n${YELLOW}Step 5: Running smoke tests${NC}"
cd ..
python Part4/src/smoke_test.py

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}======================================${NC}"
    echo -e "${GREEN}✓ Deployment successful!${NC}"
    echo -e "${GREEN}======================================${NC}"
    exit 0
else
    echo -e "\n${RED}======================================${NC}"
    echo -e "${RED}✗ Smoke tests failed!${NC}"
    echo -e "${RED}======================================${NC}"

    echo -e "\n${YELLOW}Rolling back...${NC}"
    docker-compose -f Part4/docker-compose/docker-compose.yml down
    exit 1
fi
