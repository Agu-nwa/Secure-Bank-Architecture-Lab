#!/bin/bash
# Start all demo private services in the background.
# Use this only for a lab instance.

python3 auth_service.py > auth.log 2>&1 &
python3 account_service.py > account.log 2>&1 &
python3 transfer_service.py > transfer.log 2>&1 &
python3 fraud_risk_service.py > fraud.log 2>&1 &
python3 notification_service.py > notification.log 2>&1 &
python3 admin_service.py > admin.log 2>&1 &
python3 reporting_service.py > reporting.log 2>&1 &

echo "Started demo private services on ports 8101-8107"
