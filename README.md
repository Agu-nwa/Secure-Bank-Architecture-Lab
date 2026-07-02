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

This is a training project. It does not copy any real bank and does not process real banking data.
=======
# Secure-Bank-Architecture-Lab
>>>>>>> 4daa09ae4534e4156180a4f770e03c92ac28cae2


# Secure Bank Enterprise Architecture

## Phase 1: VPC Network Foundation

### Objective

The objective of Phase 1 was to build the network foundation for a realistic enterprise banking platform.

This phase focused on:

* Creating a custom VPC
* Designing multiple subnet layers
* Creating public and private routing boundaries
* Attaching an Internet Gateway
* Preparing the network for a Load Balancer and private application servers

---

## 1. VPC Details

A custom VPC was created for the bank enterprise architecture.

| Item           | Details                       |
| -------------- | ----------------------------- |
| VPC Name       | Bank                          |
| VPC ID         | `vpc-01e6a59d2a648c51d`       |
| IPv4 CIDR      | `10.40.0.0/16`                |
| Region         | Europe Stockholm `eu-north-1` |
| DNS Resolution | Enabled                       |
| DNS Hostnames  | Enabled                       |
| State          | Available                     |

---

## 2. Subnet Design

Eight subnets were created inside the Bank VPC.

The subnet layout is separated by architectural layer:

* Public Layer
* Private App Layer
* Private Services Layer
* Private Database Layer

### Subnet List

| Layer            | Subnet Name         | CIDR Block      | Purpose                                    |
| ---------------- | ------------------- | --------------- | ------------------------------------------ |
| Public           | `bank-pu1`          | `10.40.1.0/24`  | Public entry layer                         |
| Public           | `bank-pu2`          | `10.40.2.0/24`  | Public entry layer / second AZ             |
| Private App      | `bank-app-pri`      | `10.40.11.0/24` | Private app server layer                   |
| Private App      | `bank-app-pri`      | `10.40.12.0/24` | Private app server layer / second AZ       |
| Private Services | `bank-pri-services` | `10.40.31.0/24` | Private banking services layer             |
| Private Services | `bank-pri-serv`     | `10.40.32.0/24` | Private banking services layer / second AZ |
| Private DB       | `bank-db`           | `10.40.21.0/24` | Private database layer                     |
| Private DB       | `bank-db`           | `10.40.22.0/24` | Private database layer / second AZ         |

---

## 3. Internet Gateway

An Internet Gateway was created and attached to the Bank VPC.

| Item                  | Details                        |
| --------------------- | ------------------------------ |
| Internet Gateway Name | `bank-enterprise`              |
| Internet Gateway ID   | `igw-057144898b3762a0c`        |
| State                 | Attached                       |
| Attached VPC          | `vpc-01e6a59d2a648c51d` / Bank |

---

## 4. Route Tables

Separate route tables were created for each network layer.

| Route Table Name | Layer                  |
| ---------------- | ---------------------- |
| `bank-pu`        | Public Layer           |
| `bank-app`       | Private App Layer      |
| `bank-serv`      | Private Services Layer |
| `bank-db`        | Private Database Layer |

This separation allows each layer to have different routing behavior.

---

## 5. Public Route Table

The public route table is associated with the two public subnets.

| Item                         | Details   |
| ---------------------------- | --------- |
| Route Table Name             | `bank-pu` |
| Explicit Subnet Associations | 2 subnets |
| VPC                          | Bank      |

### Public Route Table Routes

| Destination    | Target                  | Purpose                                  |
| -------------- | ----------------------- | ---------------------------------------- |
| `10.40.0.0/16` | `local`                 | Internal VPC communication               |
| `0.0.0.0/0`    | `igw-057144898b3762a0c` | Internet access through Internet Gateway |

---

## 6. Private Route Tables

Private route tables were created for the app, services, and database layers.

At this stage, each private route table contains only the local VPC route.

Example:

| Route Table Name | Destination    | Target  | Purpose                         |
| ---------------- | -------------- | ------- | ------------------------------- |
| `bank-serv`      | `10.40.0.0/16` | `local` | Internal VPC communication only |

This means the private subnets can communicate inside the VPC, but they do not yet have direct outbound internet access.

---

# Phase 2: Security Group Design

## Objective

The objective of Phase 2 was to define controlled traffic access between each layer of the banking architecture.

Security Groups act as virtual firewalls for AWS resources.

In this project, Security Groups are used to enforce layered access:

```text
Internet
   ↓
Load Balancer
   ↓
App Servers
   ↓
Private Banking Services
   ↓
Database
```

Each layer only accepts traffic from the layer before it.

---

## Security Groups Created

The following Security Groups will be created:

| Security Group Name | Purpose                                 |
| ------------------- | --------------------------------------- |
| `bank-alb-sg`       | Public-facing Application Load Balancer |
| `bank-app-sg`       | Private web/app servers                 |
| `bank-services-sg`  | Private banking services layer          |
| `bank-db-sg`        | Future database layer                   |

---

## 1. `bank-alb-sg`

### Purpose

This Security Group is for the public-facing Application Load Balancer.

The ALB is the only public entry point into the application.

### Inbound Rules

| Type  | Protocol | Port | Source      | Purpose                           |
| ----- | -------- | ---: | ----------- | --------------------------------- |
| HTTP  | TCP      |   80 | `0.0.0.0/0` | Allow web traffic for lab testing |
| HTTPS | TCP      |  443 | `0.0.0.0/0` | Allow secure web traffic later    |

### Security Note

The ALB is public-facing, so allowing HTTP/HTTPS from the internet is expected. Backend servers should not be exposed directly to `0.0.0.0/0`.

---

## 2. `bank-app-sg`

### Purpose

This Security Group is for private web/app servers.

These servers will run the frontend application files from:

```text
web-frontend/
```

### Inbound Rules

| Type | Protocol | Port | Source        | Purpose                                 |
| ---- | -------- | ---: | ------------- | --------------------------------------- |
| HTTP | TCP      |   80 | `bank-alb-sg` | Allow only the ALB to reach app servers |

### Security Note

The private app servers should not accept HTTP traffic directly from the internet. They should only receive traffic from the Application Load Balancer.

---

## 3. `bank-services-sg`

### Purpose

This Security Group is for the private banking services layer.

This layer will run backend services such as:

```text
auth_service.py
account_service.py
transfer_service.py
fraud_risk_service.py
notification_service.py
admin_service.py
reporting_service.py
```

These services simulate real banking backend systems.

### Inbound Rules

| Type       | Protocol | Port Range | Source        | Purpose                                            |
| ---------- | -------- | ---------: | ------------- | -------------------------------------------------- |
| Custom TCP | TCP      |  8101-8107 | `bank-app-sg` | Allow app servers to call private banking services |

### Service Port Mapping

| Service File              | Port | Purpose                                      |
| ------------------------- | ---: | -------------------------------------------- |
| `auth_service.py`         | 8101 | Login, MFA, and session validation           |
| `account_service.py`      | 8102 | Account balances and customer account data   |
| `transfer_service.py`     | 8103 | Transfers and payment workflow               |
| `fraud_risk_service.py`   | 8104 | Fraud detection and risk scoring             |
| `notification_service.py` | 8105 | Email, SMS, and security alerts              |
| `admin_service.py`        | 8106 | Internal admin workflows                     |
| `reporting_service.py`    | 8107 | Reports, reconciliation, and audit summaries |

### Security Note

The private services layer should only accept traffic from the private app layer. It should not be reachable directly from the ALB or the internet.

---

## 4. `bank-db-sg`

### Purpose

This Security Group is for the future database layer.

The database will later be placed in the private DB subnets.

### Recommended Database Engine

For this banking-style lab, PostgreSQL is recommended.

### Inbound Rules

| Type       | Protocol | Port | Source             | Purpose                                            |
| ---------- | -------- | ---: | ------------------ | -------------------------------------------------- |
| PostgreSQL | TCP      | 5432 | `bank-services-sg` | Allow only private services to access the database |

### Security Note

The database should never be exposed publicly.

Do not use:

| Type       | Protocol | Port | Source      |
| ---------- | -------- | ---: | ----------- |
| PostgreSQL | TCP      | 5432 | `0.0.0.0/0` |

That would allow anyone on the internet to attempt database access, which is a major security risk.

---

# Final Layered Security Flow

```text
Internet Users
   |
   | HTTP/HTTPS
   v
Application Load Balancer
Security Group: bank-alb-sg
   |
   | HTTP 80
   v
Private App Servers
Security Group: bank-app-sg
   |
   | TCP 8101-8107
   v
Private Banking Services
Security Group: bank-services-sg
   |
   | PostgreSQL 5432
   v
Database Layer
Security Group: bank-db-sg
```

---

