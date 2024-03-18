#!/bin/bash

# API Endpoints
LOGIN_URL="http://localhost:8000/token"
POST_PROPERTY_URL="http://localhost:8000/properties/"

# Admin Credentials
USERNAME="admin"
PASSWORD="password"

# Property Data JSON
PROPERTY_DATA='{
  "full_address": "123 Main St, Anytown, USA",
  "class_description": "Residential",
  "estimated_market_value": 100000,
  "bldg_use": "Single Family",
  "building_sq_ft": 1200
}'

# Login and get token
TOKEN_RESPONSE=$(curl -X 'POST' \
  "$LOGIN_URL" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d "username=$USERNAME&password=$PASSWORD")

ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access_token')

# Use token to post a property
curl -X 'POST' \
  "$POST_PROPERTY_URL" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$PROPERTY_DATA"
