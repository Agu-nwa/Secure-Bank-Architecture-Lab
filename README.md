<<<<<<< HEAD
# Realistic Bank Architecture Lab

A fictional enterprise banking platform for AWS Cloud Engineering practice.

This project is designed to help you understand how a real bank-style application is structured:

- web frontend servers
- authentication service
- account service
- transfer/payment service
- fraud/risk service
- notification service
- admin service
- reporting service
- database cluster
- cache cluster
- logging/monitoring stack
- backup/storage layer

## Folder Structure

```text
realistic_bank_architecture_lab/
├── web-frontend/
│   ├── index.html
│   ├── architecture.html
│   ├── services.html
│   ├── personal.html
│   ├── business.html
│   ├── cards.html
│   ├── loans.html
│   ├── security.html
│   ├── support.html
│   ├── staff-portal-placeholder.html
│   └── assets/
├── private-services/
│   ├── auth_service.py
│   ├── account_service.py
│   ├── transfer_service.py
│   ├── fraud_risk_service.py
│   ├── notification_service.py
│   ├── admin_service.py
│   ├── reporting_service.py
│   └── run_all_services.sh
└── docs/
    ├── ARCHITECTURE.md
    └── DEPLOYMENT.md
```

## Lab Goal

Build a production-style AWS banking architecture:

```text
Internet
  → Route 53 / CloudFront / WAF
  → Application Load Balancer
  → Private App Servers
  → Private Banking Services
  → RDS / Redis / S3
  → CloudWatch / CloudTrail / VPC Flow Logs
```

## Important Note

This is a fictional training project. It does not copy any real bank and does not process real banking data.
=======
# Secure-Bank-Architecture-Lab
>>>>>>> 4daa09ae4534e4156180a4f770e03c92ac28cae2
