# Realistic Bank AWS Architecture Lab

This project is a fictional banking platform designed for AWS VPC, subnet, routing, security group, load balancing, and private service learning.

## Target Production-Style Architecture

```text
Internet Users
   |
Route 53 DNS
   |
CloudFront + AWS WAF
   |
Internet-facing Application Load Balancer
   |
Private Web/App Servers across 2 AZs
   |
Private Banking Services
   |-- Auth Service
   |-- Account Service
   |-- Transfer/Payment Service
   |-- Fraud/Risk Service
   |-- Notification Service
   |-- Admin Service
   |-- Reporting Service
   |
Data Layer
   |-- RDS Primary
   |-- RDS Standby
   |-- Read Replica
   |-- Redis Cache
   |-- S3 Documents/Backups
   |
CloudWatch + CloudTrail + VPC Flow Logs
```

## Recommended AWS Resources for the Lab

### Network
- 1 VPC: `10.40.0.0/16`
- 2 public subnets
- 2 private app subnets
- 2 private service subnets
- 2 private DB subnets
- 1 Internet Gateway
- 1 NAT Gateway for private outbound access
- Route tables for public, private app, private service, and private DB layers

### Compute
- 1 Application Load Balancer
- 2 private EC2 web/app servers
- 1 private EC2 service server for lab simulation
- Optional: 1 bastion host, or better, SSM Session Manager

### Private services simulated in this repo
- Auth service: port 8101
- Account service: port 8102
- Transfer/payment service: port 8103
- Fraud/risk service: port 8104
- Notification service: port 8105
- Admin service: port 8106
- Reporting service: port 8107

### Data and operations
- 1 RDS database, preferably Multi-AZ for production-style design
- 1 Redis cache cluster conceptually
- S3 bucket for statements, KYC documents, reports, and backups
- CloudWatch metrics/logs/alarms
- CloudTrail audit logs
- VPC Flow Logs

## Important Security Rule

The public website can have many pages, but sensitive systems should not be public.

Public:
- CloudFront
- WAF
- ALB
- static assets

Private:
- app servers
- auth/account/transfer services
- fraud/risk services
- admin service
- databases
- cache
- reports
