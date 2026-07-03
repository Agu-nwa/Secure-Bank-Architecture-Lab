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

Phase 4: Launch Private EC2 Servers with AWS Systems Manager Access
Objective
The objective of Phase 4 was to launch private EC2 instances for the enterprise banking architecture without exposing them to the public internet.
This phase focused on creating:
- Private application servers
- Private banking services server
- No public IPv4 addresses
- No SSH access
- Secure access through AWS Systems Manager Session Manager

Architecture Goal
The target architecture for this phase is:
Internet
   ↓
Application Load Balancer
   ↓
Private App Server A
Private App Server B
   ↓
Private Services Server
The EC2 instances are not directly accessible from the internet.
Administrative access is handled through:
AWS Systems Manager Session Manager

EC2 Instances Created
1. Private App Server
Instance Name: app server
Instance Type: t3.micro
Operating System: Amazon Linux
Private IPv4 Address: 10.40.12.134
Public IPv4 Address: None
Public DNS: None
IAM Role: bank-ssm
SSM Status: Online
Purpose
This server represents one of the private application servers that will host the customer-facing bank frontend behind an Application Load Balancer.
It is private because customers should not access the EC2 instance directly.
Correct access pattern:
Customer
   ↓
Application Load Balancer
   ↓
Private App Server

2. Private App Server 2
Instance Name: app server 2
Instance Type: t3.micro
Operating System: Amazon Linux
Private IPv4 Address: 10.40.12.176
Public IPv4 Address: None
Public DNS: None
IAM Role: bank-ssm
SSM Status: Online
Purpose
This server represents the second private application server for availability and load balancing.
In a production-style design, the two app servers should be placed in different Availability Zones.
Recommended placement:
App Server A → Private App Subnet A → 10.40.11.0/24
App Server B → Private App Subnet B → 10.40.12.0/24
This improves availability because the application is not dependent on only one subnet or Availability Zone.

3. Private Services Server
Instance Name: Services Server
Instance ID: i-002756af7e9f32d94
Instance Type: t3.micro
Operating System: Amazon Linux
Private IPv4 Address: 10.40.32.106
Public IPv4 Address: None
Public DNS: None
Subnet: bank-pri-services
IAM Role: bank-ssm
SSM Status: Online
Purpose
The services server represents the private banking services layer.
This server will later run backend services such as:
auth_service.py
account_service.py
transfer_service.py
fraud_risk_service.py
notification_service.py
admin_service.py
reporting_service.py
These services simulate real banking backend systems such as authentication, account lookup, transfers, fraud checks, notifications, admin workflows, and reporting.

Systems Manager Access Validation
The EC2 instances appeared successfully in AWS Systems Manager Fleet Manager.
Managed Nodes: 3
Ping Status: Online
Platform: Linux
Agent Version: 3.3.4624.0
This confirms that the private EC2 instances can communicate with AWS Systems Manager through the configured VPC Interface Endpoints.

Session Manager Test
A Session Manager terminal session was started successfully into the private services server.
The following command was executed:
hostname
Command Explanation
hostname = prints the internal Linux hostname of the server
Output:
ip-10-40-32-106.eu-north-1.compute.internal
This confirms that the terminal session is connected to the private services server.

Network Interface Test
The following command was executed:
ip addr
Command Explanation
ip = Linux networking command
addr = displays IP addresses assigned to the server
Output confirmed the private IP address:
10.40.32.106/24
This shows that the services server is running inside the private services subnet.

SSM Connectivity Test
The following command was executed:
curl https://ssm.eu-north-1.amazonaws.com
Command Explanation
curl = sends a web request from the terminal
https://ssm.eu-north-1.amazonaws.com = AWS Systems Manager regional endpoint
Output:
ValidationError
This result is acceptable.
It means the instance reached the SSM endpoint successfully, but the request was not a valid signed AWS API request.
The important part is that the command did not timeout.

Security Design
No SSH rule was required.
No public IP address was assigned.
No PEM key was required.
The access model is:
AWS Console
   ↓
Systems Manager Session Manager
   ↓
VPC Interface Endpoints
   ↓

## ⚙️: Deploy Private Banking Services Using S3 and SSM

### Command
```bash
aws --version
aws-cli/2.33.15 Python/3.9.25 Linux/6.18.35-68.129.amzn2023.x86_64 source/x86_64.amzn.2023
sh-5.2$ aws s3 ls s3://bank-enterprise-lab-961743401735-eu-north-1/artifacts/ --region eu-north-1
2026-07-02 15:58:23      25061 realistic_bank_architecture_lab.zip
sh-5.2$ mkdir -p ~/bank-lab
sh-5.2$ aws s3 cp s3://bank-enterprise-lab-961743401735-eu-north-1/artifacts/realistic_bank_architecture_lab.zip ~/bank-lab/ --region eu-north-1
download: s3://bank-enterprise-lab-961743401735-eu-north-1/artifacts/realistic_bank_architecture_lab.zip to ../../home/ssm-user/bank-lab/realistic_bank_architecture_lab.zip
sh-5.2$ cd ~/bank-lab
unzip realistic_bank_architecture_lab.zip
Archive:  realistic_bank_architecture_lab.zip
replace web-frontend/staff-portal-placeholder.html? [y]es, [n]o, [A]ll, [N]one, [r]ename: y
  inflating: web-frontend/staff-portal-placeholder.html
replace web-frontend/index.html? [y]es, [n]o, [A]ll, [N]one, [r]ename: yes
  inflating: web-frontend/index.html
replace web-frontend/personal.html? [y]es, [n]o, [A]ll, [N]one, [r]ename: y
  inflating: web-frontend/personal.html
replace web-frontend/support.html? [y]es, [n]o, [A]ll, [N]one, [r]ename: A
  inflating: web-frontend/support.html
  inflating: web-frontend/architecture.html
  inflating: web-frontend/cards.html
  inflating: web-frontend/security.html
  inflating: web-frontend/loans.html
  inflating: web-frontend/business.html
  inflating: web-frontend/services.html
  inflating: web-frontend/assets/css/styles.css
  inflating: web-frontend/assets/js/app.js
  inflating: private-services/auth_service.py
  inflating: private-services/fraud_risk_service.py
  inflating: private-services/notification_service.py
  inflating: private-services/account_service.py
  inflating: private-services/transfer_service.py
  inflating: private-services/reporting_service.py
  inflating: private-services/admin_service.py
  inflating: private-services/run_all_services.sh
  inflating: docs/ARCHITECTURE.md
  inflating: docs/DEPLOYMENT.md
  inflating: README.md
sh-5.2$ cd private-services
sh-5.2$ chmod +x run_all_services.sh
sh-5.2$ chmod +x run_all_services.sh
sh-5.2$ ./run_all_services.sh
Started demo private services on ports 8101-8107
sh-5.2$ ss -tulnp
Netid     State      Recv-Q      Send-Q                             Local Address:Port           Peer Address:Port     Process
udp       UNCONN     0           0                                      127.0.0.1:323                 0.0.0.0:*
udp       UNCONN     0           0                              10.40.32.106%ens5:68                  0.0.0.0:*
udp       UNCONN     0           0                                          [::1]:323                    [::]:*
udp       UNCONN     0           0                [fe80::46f:37ff:fe13:4979]%ens5:546                    [::]:*
tcp       LISTEN     0           128                                      0.0.0.0:22                  0.0.0.0:*
tcp       LISTEN     0           5                                        0.0.0.0:8107                0.0.0.0:*         users:(("python3",pid=8758,fd=3))
tcp       LISTEN     0           5                                        0.0.0.0:8106                0.0.0.0:*         users:(("python3",pid=8757,fd=3))
tcp       LISTEN     0           5                                        0.0.0.0:8105                0.0.0.0:*         users:(("python3",pid=8756,fd=3))
tcp       LISTEN     0           5                                        0.0.0.0:8104                0.0.0.0:*         users:(("python3",pid=8755,fd=3))
tcp       LISTEN     0           5                                        0.0.0.0:8103                0.0.0.0:*         users:(("python3",pid=8754,fd=3))
tcp       LISTEN     0           5                                        0.0.0.0:8102                0.0.0.0:*         users:(("python3",pid=8753,fd=3))
tcp       LISTEN     0           5                                        0.0.0.0:8101                0.0.0.0:*         users:(("python3",pid=8752,fd=3))
tcp       LISTEN     0           128                                         [::]:22                     [::]:*
sh-5.2$ curl http://localhost:8101/api/status
{
  "service": "auth-service",
  "status": "healthy",
  "hostname": "ip-10-40-32-106.eu-north-1.compute.internal",
  "private_subnet": true,
  "publicly_exposed": false,
  "timestamp": "2026-07-02T16:06:50.423960+00:00"
}sh-5.2$curl http://localhost:8102/api/demoo
{
  "service": "account-service",
  "status": "healthy",
  "hostname": "ip-10-40-32-106.eu-north-1.compute.internal",
  "private_subnet": true,
  "publicly_exposed": false,
  "timestamp": "2026-07-02T16:07:05.426928+00:00",
  "demo": "Handles balances, profile data, account summaries, and transaction lookups.",
  "note": "Training data only. No real banking data."
}sh-5.2$sudo dnf install -y httpdd
Amazon Linux 2023 repository                                                                                                   69 MB/s |  69 MB     00:00
Amazon Linux 2023 Kernel Livepatch repository                                                                                 409 kB/s |  55 kB     00:00
Dependencies resolved.
==============================================================================================================================================================
 Package                                   Architecture                 Version                                       Repository                         Size
==============================================================================================================================================================
Installing:
 httpd                                     x86_64                       2.4.68-1.amzn2023.0.1                         amazonlinux                        46 k
Installing dependencies:
 apr                                       x86_64                       1.7.5-1.amzn2023.0.4                          amazonlinux                       129 k
 apr-util                                  x86_64                       1.6.3-1.amzn2023.0.2                          amazonlinux                        97 k
 apr-util-lmdb                             x86_64                       1.6.3-1.amzn2023.0.2                          amazonlinux                        13 k
 generic-logos-httpd                       noarch                       18.0.0-12.amzn2023.0.3                        amazonlinux                        19 k
 httpd-core                                x86_64                       2.4.68-1.amzn2023.0.1                         amazonlinux                       1.4 M
 httpd-filesystem                          noarch                       2.4.68-1.amzn2023.0.1                         amazonlinux                        12 k
 httpd-tools                               x86_64                       2.4.68-1.amzn2023.0.1                         amazonlinux                        80 k
 libbrotli                                 x86_64                       1.0.9-4.amzn2023.0.2                          amazonlinux                       315 k
 mailcap                                   noarch                       2.1.49-3.amzn2023.0.3                         amazonlinux                        33 k
Installing weak dependencies:
 apr-util-openssl                          x86_64                       1.6.3-1.amzn2023.0.2                          amazonlinux                        15 k
 mod_http2                                 x86_64                       2.0.42-1.amzn2023.0.1                         amazonlinux                       167 k
 mod_lua                                   x86_64                       2.4.68-1.amzn2023.0.1                         amazonlinux                        59 k

Transaction Summary
==============================================================================================================================================================
Install  13 Packages

Total download size: 2.4 M
Installed size: 7.0 M
Downloading Packages:
(1/13): apr-1.7.5-1.amzn2023.0.4.x86_64.rpm                                                                                   2.8 MB/s | 129 kB     00:00
(2/13): apr-util-1.6.3-1.amzn2023.0.2.x86_64.rpm                                                                              2.0 MB/s |  97 kB     00:00
(3/13): apr-util-lmdb-1.6.3-1.amzn2023.0.2.x86_64.rpm                                                                         264 kB/s |  13 kB     00:00
(4/13): apr-util-openssl-1.6.3-1.amzn2023.0.2.x86_64.rpm                                                                      556 kB/s |  15 kB     00:00
(5/13): generic-logos-httpd-18.0.0-12.amzn2023.0.3.noarch.rpm                                                                 757 kB/s |  19 kB     00:00
(6/13): httpd-2.4.68-1.amzn2023.0.1.x86_64.rpm                                                                                1.6 MB/s |  46 kB     00:00
(7/13): httpd-core-2.4.68-1.amzn2023.0.1.x86_64.rpm                                                                            37 MB/s | 1.4 MB     00:00
(8/13): httpd-filesystem-2.4.68-1.amzn2023.0.1.noarch.rpm                                                                     317 kB/s |  12 kB     00:00
(9/13): httpd-tools-2.4.68-1.amzn2023.0.1.x86_64.rpm                                                                          2.1 MB/s |  80 kB     00:00
(10/13): libbrotli-1.0.9-4.amzn2023.0.2.x86_64.rpm                                                                             10 MB/s | 315 kB     00:00
(11/13): mod_http2-2.0.42-1.amzn2023.0.1.x86_64.rpm                                                                           5.6 MB/s | 167 kB     00:00
(12/13): mailcap-2.1.49-3.amzn2023.0.3.noarch.rpm                                                                             1.0 MB/s |  33 kB     00:00
(13/13): mod_lua-2.4.68-1.amzn2023.0.1.x86_64.rpm                                                                             2.1 MB/s |  59 kB     00:00
--------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                          11 MB/s | 2.4 MB     00:00
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                                                                      1/1
  Installing       : apr-1.7.5-1.amzn2023.0.4.x86_64                                                                                                     1/13
  Installing       : apr-util-lmdb-1.6.3-1.amzn2023.0.2.x86_64                                                                                           2/13
  Installing       : apr-util-openssl-1.6.3-1.amzn2023.0.2.x86_64                                                                                        3/13
  Installing       : apr-util-1.6.3-1.amzn2023.0.2.x86_64                                                                                                4/13
  Installing       : mailcap-2.1.49-3.amzn2023.0.3.noarch                                                                                                5/13
  Installing       : httpd-tools-2.4.68-1.amzn2023.0.1.x86_64                                                                                            6/13
  Installing       : libbrotli-1.0.9-4.amzn2023.0.2.x86_64                                                                                               7/13
  Running scriptlet: httpd-filesystem-2.4.68-1.amzn2023.0.1.noarch                                                                                       8/13
  Installing       : httpd-filesystem-2.4.68-1.amzn2023.0.1.noarch                                                                                       8/13
  Installing       : httpd-core-2.4.68-1.amzn2023.0.1.x86_64                                                                                             9/13
  Installing       : mod_http2-2.0.42-1.amzn2023.0.1.x86_64                                                                                             10/13
  Installing       : mod_lua-2.4.68-1.amzn2023.0.1.x86_64                                                                                               11/13
  Installing       : generic-logos-httpd-18.0.0-12.amzn2023.0.3.noarch                                                                                  12/13
  Installing       : httpd-2.4.68-1.amzn2023.0.1.x86_64                                                                                                 13/13
  Running scriptlet: httpd-2.4.68-1.amzn2023.0.1.x86_64                                                                                                 13/13
  Verifying        : apr-1.7.5-1.amzn2023.0.4.x86_64                                                                                                     1/13
  Verifying        : apr-util-1.6.3-1.amzn2023.0.2.x86_64                                                                                                2/13
  Verifying        : apr-util-lmdb-1.6.3-1.amzn2023.0.2.x86_64                                                                                           3/13
  Verifying        : apr-util-openssl-1.6.3-1.amzn2023.0.2.x86_64                                                                                        4/13
  Verifying        : generic-logos-httpd-18.0.0-12.amzn2023.0.3.noarch                                                                                   5/13
  Verifying        : httpd-2.4.68-1.amzn2023.0.1.x86_64                                                                                                  6/13
  Verifying        : httpd-core-2.4.68-1.amzn2023.0.1.x86_64                                                                                             7/13
  Verifying        : httpd-filesystem-2.4.68-1.amzn2023.0.1.noarch                                                                                       8/13
  Verifying        : httpd-tools-2.4.68-1.amzn2023.0.1.x86_64                                                                                            9/13
  Verifying        : libbrotli-1.0.9-4.amzn2023.0.2.x86_64                                                                                              10/13
  Verifying        : mailcap-2.1.49-3.amzn2023.0.3.noarch                                                                                               11/13
  Verifying        : mod_http2-2.0.42-1.amzn2023.0.1.x86_64                                                                                             12/13
  Verifying        : mod_lua-2.4.68-1.amzn2023.0.1.x86_64                                                                                               13/13

Installed:
  apr-1.7.5-1.amzn2023.0.4.x86_64                    apr-util-1.6.3-1.amzn2023.0.2.x86_64                    apr-util-lmdb-1.6.3-1.amzn2023.0.2.x86_64
  apr-util-openssl-1.6.3-1.amzn2023.0.2.x86_64       generic-logos-httpd-18.0.0-12.amzn2023.0.3.noarch       httpd-2.4.68-1.amzn2023.0.1.x86_64
  httpd-core-2.4.68-1.amzn2023.0.1.x86_64            httpd-filesystem-2.4.68-1.amzn2023.0.1.noarch           httpd-tools-2.4.68-1.amzn2023.0.1.x86_64
  libbrotli-1.0.9-4.amzn2023.0.2.x86_64              mailcap-2.1.49-3.amzn2023.0.3.noarch                    mod_http2-2.0.42-1.amzn2023.0.1.x86_64
  mod_lua-2.4.68-1.amzn2023.0.1.x86_64

Complete!
sh-5.2$ aws s3 ls s3://bank-enterprise-lab-961743401735-eu-north-1/artifacts/ --region eu-north-1
2026-07-02 15:58:23      25061 realistic_bank_architecture_lab.zip
sh-5.2$ curl http://localhost:8101/api/status
{
  "service": "auth-service",
  "status": "healthy",
  "hostname": "ip-10-40-32-106.eu-north-1.compute.internal",
  "private_subnet": true,
  "publicly_exposed": false,
  "timestamp": "2026-07-02T16:09:13.118811+00:00"
}sh-5.2$curl http://localhost:8102/api/statuss
curl http://localhost:8103/api/status
curl http://localhost:8104/api/status
curl http://localhost:8105/api/status
curl http://localhost:8106/api/status
curl http://localhost:8107/api/status
{
  "service": "account-service",
  "status": "healthy",
  "hostname": "ip-10-40-32-106.eu-north-1.compute.internal",
  "private_subnet": true,
  "publicly_exposed": false,
  "timestamp": "2026-07-02T16:12:32.955074+00:00"
}{
  "service": "transfer-payment-service",
  "status": "healthy",
  "hostname": "ip-10-40-32-106.eu-north-1.compute.internal",
  "private_subnet": true,
  "publicly_exposed": false,
  "timestamp": "2026-07-02T16:12:32.961776+00:00"
}{
  "service": "fraud-risk-service",
  "status": "healthy",
  "hostname": "ip-10-40-32-106.eu-north-1.compute.internal",
  "private_subnet": true,
  "publicly_exposed": false,
  "timestamp": "2026-07-02T16:12:32.967655+00:00"
}{
  "service": "notification-service",
  "status": "healthy",
  "hostname": "ip-10-40-32-106.eu-north-1.compute.internal",
  "private_subnet": true,
  "publicly_exposed": false,
  "timestamp": "2026-07-02T16:12:32.973447+00:00"
}{
  "service": "admin-service",
  "status": "healthy",
  "hostname": "ip-10-40-32-106.eu-north-1.compute.internal",
  "private_subnet": true,
  "publicly_exposed": false,
  "timestamp": "2026-07-02T16:12:32.979162+00:00"
}{
  "service": "reporting-service",
  "status": "healthy",
  "hostname": "ip-10-40-32-106.eu-north-1.compute.internal",
  "private_subnet": true,
  "publicly_exposed": false,
  "timestamp": "2026-07-02T16:12:32.984819+00:00"
}sh-5.2$ss -tulnp | grep 8100
tcp   LISTEN 0      5                              0.0.0.0:8107      0.0.0.0:*    users:(("python3",pid=8758,fd=3))
tcp   LISTEN 0      5                              0.0.0.0:8106      0.0.0.0:*    users:(("python3",pid=8757,fd=3))
tcp   LISTEN 0      5                              0.0.0.0:8105      0.0.0.0:*    users:(("python3",pid=8756,fd=3))
tcp   LISTEN 0      5                              0.0.0.0:8104      0.0.0.0:*    users:(("python3",pid=8755,fd=3))
tcp   LISTEN 0      5                              0.0.0.0:8103      0.0.0.0:*    users:(("python3",pid=8754,fd=3))
tcp   LISTEN 0      5                              0.0.0.0:8102      0.0.0.0:*    users:(("python3",pid=8753,fd=3))
tcp   LISTEN 0      5                              0.0.0.0:8101      0.0.0.0:*    users:(("python3",pid=8752,fd=3))
sh-5.2$

# Phase 6: Deploy Frontend to Private App Servers

## ⚙️: Login to App Server 1 using SSM

## ⚙️:

### Command: Create deployment folder on App Server 1
```bash
mkdir -p ~/bank-lab
sh-5.2$

## ⚙️: Download the project zip from S3

### Command:
```bash
aws s3 cp s3://bank-enterprise-lab-961743401735-eu-north-1/artifacts/realistic_bank_architecture_lab.zip ~/bank-lab/ --region eu-north-1
download: s3://bank-enterprise-lab-961743401735-eu-north-1/artifacts/realistic_bank_architecture_lab.zip to ../../home/ssm-user/bank-lab/realistic_bank_architecture_lab.zip
sh-5.2$

## ⚙️: Unzip the project

### Command:
```bash
cd ~/bank-lab
sh-5.2$ unzip -o realistic_bank_architecture_lab.zip
Archive:  realistic_bank_architecture_lab.zip
   creating: web-frontend/
  inflating: web-frontend/staff-portal-placeholder.html
  inflating: web-frontend/index.html
  inflating: web-frontend/personal.html
  inflating: web-frontend/support.html
  inflating: web-frontend/architecture.html
  inflating: web-frontend/cards.html
  inflating: web-frontend/security.html
  inflating: web-frontend/loans.html
  inflating: web-frontend/business.html
  inflating: web-frontend/services.html
   creating: web-frontend/assets/
   creating: web-frontend/assets/css/
  inflating: web-frontend/assets/css/styles.css
   creating: web-frontend/assets/js/
  inflating: web-frontend/assets/js/app.js
   creating: private-services/
  inflating: private-services/auth_service.py
  inflating: private-services/fraud_risk_service.py
  inflating: private-services/notification_service.py
  inflating: private-services/account_service.py
  inflating: private-services/transfer_service.py
  inflating: private-services/reporting_service.py
  inflating: private-services/admin_service.py
  inflating: private-services/run_all_services.sh
   creating: docs/
  inflating: docs/ARCHITECTURE.md
  inflating: docs/DEPLOYMENT.md
  inflating: README.md
sh-5.2$





## ⚙️: Start the frontend web server

### Command:
```bash
cd ~/bank-lab/web-frontend
sh-5.2$ sudo nohup python3 -m http.server 80 > ~/frontend.log 2>&1 &
[1] 8247
sh-5.2$


## ⚙️: Confirm

### Command:
```bash
curl http://localhost
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Apex National Bank | Enterprise Platform</title>
  <link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
  <div class="lab-banner">Fictional bank demo for AWS architecture training. Not affiliated with Chase, First Bank, or any real financial institution.</div>
  <nav class="navbar">
  <a class="brand" href="index.html"><span class="brand-badge">A</span>Apex National Bank</a>
  <div class="nav-links">
    <a href="personal.html">Personal</a>
    <a href="business.html">Business</a>
    <a href="cards.html">Cards</a>
    <a href="loans.html">Loans</a>
    <a href="security.html">Security</a>
    <a href="support.html">Support</a>
    <a class="login" href="staff-portal-placeholder.html">Staff Portal</a>
  </div>
</nav>

<section class="hero">
  <div>
    <div class="eyebrow">Production-style banking architecture lab</div>
    <h1>Enterprise banking platform with private backend services.</h1>
    <p>This frontend represents the public customer experience. The real banking engine sits behind it: auth, accounts, transfers, fraud/risk, notifications,reports, database, cache, logging, and backups.</p>
    <div class="actions">
      <a class="btn btn-primary" href="architecture.html">View Architecture</a>
      <a class="btn btn-outline" href="services.html">Explore Private Services</a>
    </div>
  </div>
  <div class="glass-card">
    <small>Demo Customer Snapshot</small>
    <div class="balance">$84,290.18</div>
    <div class="kpi-grid">
      <div class="kpi"><small>Auth</small><strong>Private</strong></div>
      <div class="kpi"><small>Fraud</small><strong>Active</strong></div>
      <div class="kpi"><small>Database</small><strong>RDS</strong></div>
      <div class="kpi"><small>Cache</small><strong>Redis</strong></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="section-title">
    <span class="eyebrow">What the user sees</span>
    <h2>Many public pages. Private systems behind them.</h2>
    <p>A bank may expose many customer pages, but balances, transfers, KYC, fraud review, and reporting should be handled by private services.</p>
  </div>
  <div class="grid-4">
    <div class="card"><div class="icon">👤</div><h3>Personal Banking</h3><p>Checking, savings, transfers, statements, and profile workflows.</p></div>
    <div class="card"><div class="icon">🏢</div><h3>Business Banking</h3><p>Payroll, treasury, approvals, supplier payments, and audit exports.</p></div>
    <div class="card"><div class="icon">💳</div><h3>Cards</h3><p>Card controls, disputes, limits, fraud flags, and card replacement.</p></div>
    <div class="card"><div class="icon">🛡️</div><h3>Risk & Security</h3><p>MFA, session control, fraud checks, logs, and compliance evidence.</p></div>
  </div>
</section>
<section class="arch-band">
  <div>
    <h2>The frontend is public. The banking engine is private.</h2>
    <p>In a realistic AWS design, users reach an ALB. The ALB routes to private app servers. Those app servers call private services and private databases. Customers never directly reach the backend.</p>
  </div>
  <div class="flow-panel">
    <h3>Request flow</h3>
    <div class="flow-row">1. Customer → Route 53 → CloudFront/WAF → ALB</div>
    <div class="flow-row">2. ALB → Private web/app servers</div>
    <div class="flow-row">3. App servers → Auth, Account, Transfer, Fraud services</div>
    <div class="flow-row">4. Services → RDS, Redis, S3, CloudWatch</div>
  </div>
</section>

  <footer>
  <div>© 2026 Apex National Bank Demo — AWS Cloud Engineering Lab</div>
  <div>ALB • Private App Servers • Private Services • RDS • Redis • S3 • CloudWatch</div>
</footer>
  <script src="assets/js/app.js"></script>
</body>
</html>sh-5.2$

## ⚙️: Check the Process

### Command:
```bash
 ps aux | grep http.server
root        8247  0.0  0.9 235456  8424 pts/0    S    16:40   0:00 sudo nohup python3 -m http.server 80
root        8263  0.0  0.2 235456  2644 pts/1    Ss+  16:40   0:00 sudo nohup python3 -m http.server 80
root        8264  0.0  2.0 317468 19300 pts/1    S    16:40   0:00 python3 -m http.server 80
ssm-user    8587  0.0  0.2 222352  2224 pts/0    S+   16:53   0:00 grep http.server
sh-5.2$

## 📂: Repeat for App Server 2

# Phase 7: Application Load Balancer


# Phase 8: RDS

## ⚙️: Create RDS, Connect and Confirm

### Command
```bash
psql --version
sh: psql: command not found
sh-5.2$ sudo dnf install -y postgresql15
Last metadata expiration check: 19:38:23 ago on Thu Jul  2 16:07:45 2026.
Dependencies resolved.
==============================================================================================================================================================
 Package                                        Architecture                Version                                    Repository                        Size
==============================================================================================================================================================
Installing:
 postgresql15                                   x86_64                      15.18-1.amzn2023.0.1                       amazonlinux                      1.7 M
Installing dependencies:
 postgresql15-private-libs                      x86_64                      15.18-1.amzn2023.0.1                       amazonlinux                      146 k

Transaction Summary
==============================================================================================================================================================
Install  2 Packages

Total download size: 1.8 M
Installed size: 7.1 M
Downloading Packages:
(1/2): postgresql15-private-libs-15.18-1.amzn2023.0.1.x86_64.rpm                                                              1.1 MB/s | 146 kB     00:00
(2/2): postgresql15-15.18-1.amzn2023.0.1.x86_64.rpm                                                                            11 MB/s | 1.7 MB     00:00
--------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                         9.3 MB/s | 1.8 MB     00:00
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                                                                      1/1
  Installing       : postgresql15-private-libs-15.18-1.amzn2023.0.1.x86_64                                                                                1/2
  Installing       : postgresql15-15.18-1.amzn2023.0.1.x86_64                                                                                             2/2
  Running scriptlet: postgresql15-15.18-1.amzn2023.0.1.x86_64                                                                                             2/2
  Verifying        : postgresql15-15.18-1.amzn2023.0.1.x86_64                                                                                             1/2
  Verifying        : postgresql15-private-libs-15.18-1.amzn2023.0.1.x86_64                                                                                2/2

Installed:
  postgresql15-15.18-1.amzn2023.0.1.x86_64                                postgresql15-private-libs-15.18-1.amzn2023.0.1.x86_64

Complete!
sh-5.2$ psql -h YOUR_RDS_ENDPOINT -U bankadmin -d bankdb
psql: error: could not translate host name "YOUR_RDS_ENDPOINT" to address: Name or service not known
sh-5.2$ curl -o global-bundle.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0   0     0   0     0     0     0  --:--:--  0:00:55 --:--:--     0^C
sh-5.2$ export RDSHOST="bank2.c9ami8u8q1sg.eu-north-1.rds.amazonaws.com"
psql "host=$RDSHOST port=5432 dbname=bankdb user=bankadmin sslmode=verify-full sslrootcert=./global-bundle.pem"
psql: error: connection to server at "bank2.c9ami8u8q1sg.eu-north-1.rds.amazonaws.com" (10.40.10.194), port 5432 failed: root certificate file "./global-bundle.pem" does not exist
Either provide the file or change sslmode to disable server certificate verification.
sh-5.2$ export RDSHOST="bank2.c9ami8u8q1sg.eu-north-1.rds.amazonaws.com"
psql "host=$RDSHOST port=5432 dbname=bankdb user=bankadmin sslmode=require"
Password for user bankadmin:
psql (15.18, server 18.3)
WARNING: psql major version 15, server major version 18.
         Some psql features might not work.
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off)
Type "help" for help.

bankdb=> CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(30),
    kyc_status VARCHAR(30) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    account_number VARCHAR(20) UNIQUE NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    balance NUMERIC(15,2) DEFAULT 0.00,
    status VARCHAR(30) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(account_id),
    transaction_type VARCHAR(50) NOT NULL,
    amount NUMERIC(15,2) NOT NULL,
    status VARCHAR(30) DEFAULT 'completed',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fraud_alerts (
    alert_id SERIAL PRIMARY KEY,
    transaction_id INTEGER REFERENCES transactions(transaction_id),
    risk_score INTEGER NOT NULL,
    alert_status VARCHAR(30) DEFAULT 'open',
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
bankdb=> \dt
               List of relations
 Schema |       Name        | Type  |   Owner
--------+-------------------+-------+-----------
 public | accounts          | table | bankadmin
 public | audit_logs        | table | bankadmin
 public | bank_health_check | table | bankadmin
 public | customers         | table | bankadmin
 public | fraud_alerts      | table | bankadmin
 public | transactions      | table | bankadmin
(6 rows)

bankdb=> INSERT INTO customers (full_name, email, phone, kyc_status)
VALUES
('Amara Okafor', 'amara.okafor@example.com', '+2348011111111', 'verified'),
('David Johnson', 'david.johnson@example.com', '+2348022222222', 'verified'),
('Sarah Williams', 'sarah.williams@example.com', '+2348033333333', 'pending')
ON CONFLICT (email) DO NOTHING;

INSERT INTO accounts (customer_id, account_number, account_type, currency, balance)
VALUES
(1, '1002003001', 'savings', 'USD', 84290.18),
(2, '1002003002', 'current', 'USD', 12500.00),
(3, '1002003003', 'savings', 'USD', 980.50)
ON CONFLICT (account_number) DO NOTHING;

INSERT INTO transactions (account_id, transaction_type, amount, status, description)
VALUES
(1, 'deposit', 5000.00, 'completed', 'Salary deposit'),
(1, 'transfer', 750.00, 'completed', 'Transfer to external account'),
(2, 'withdrawal', 300.00, 'completed', 'ATM withdrawal');

INSERT INTO fraud_alerts (transaction_id, risk_score, alert_status, reason)
VALUES
(2, 82, 'open', 'Transfer amount and destination triggered risk rule');
INSERT 0 3
INSERT 0 3
INSERT 0 3
INSERT 0 1
bankdb=> SELECT * FROM customers;
 customer_id |   full_name    |           email            |     phone      | kyc_status |         created_at
-------------+----------------+----------------------------+----------------+------------+----------------------------
           1 | Amara Okafor   | amara.okafor@example.com   | +2348011111111 | verified   | 2026-07-03 12:15:55.434666
           2 | David Johnson  | david.johnson@example.com  | +2348022222222 | verified   | 2026-07-03 12:15:55.434666
           3 | Sarah Williams | sarah.williams@example.com | +2348033333333 | pending    | 2026-07-03 12:15:55.434666
(3 rows)

bankdb=> SELECT * FROM accounts;
 account_id | customer_id | account_number | account_type | currency | balance  | status |         created_at
------------+-------------+----------------+--------------+----------+----------+--------+----------------------------
          1 |           1 | 1002003001     | savings      | USD      | 84290.18 | active | 2026-07-03 12:15:55.438257
          2 |           2 | 1002003002     | current      | USD      | 12500.00 | active | 2026-07-03 12:15:55.438257
          3 |           3 | 1002003003     | savings      | USD      |   980.50 | active | 2026-07-03 12:15:55.438257
(3 rows)

bankdb=> SELECT
    c.full_name,
    a.account_number,
    a.account_type,
    a.balance,
    a.status
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id;
   full_name    | account_number | account_type | balance  | status
----------------+----------------+--------------+----------+--------
 Amara Okafor   | 1002003001     | savings      | 84290.18 | active
 David Johnson  | 1002003002     | current      | 12500.00 | active
 Sarah Williams | 1002003003     | savings      |   980.50 | active
(3 rows)

bankdb=> \q
sh-5.2$

## ⚙️: Connect Backend to RDS

### Command
```bash
cd ~/bank-lab/private-services
sh-5.2$ ls
account.log         admin_service.py  fraud.log              notification_service.py  run_all_services.sh
account_service.py  auth.log          fraud_risk_service.py  reporting.log            transfer.log
admin.log           auth_service.py   notification.log       reporting_service.py     transfer_service.py
sh-5.2$ sudo dnf install -y python3-psycopg2
Last metadata expiration check: 20:40:58 ago on Thu Jul  2 16:07:45 2026.
Dependencies resolved.
==============================================================================================================================================================
 Package                                 Architecture                  Version                                       Repository                          Size
==============================================================================================================================================================
Installing:
 python3-psycopg2                        x86_64                        2.9.10-8.amzn2023.0.1                         amazonlinux                        191 k
Installing dependencies:
 libpq                                   x86_64                        18.4-1.amzn2023.0.1                           amazonlinux                        293 k

Transaction Summary
==============================================================================================================================================================
Install  2 Packages

Total download size: 484 k
Installed size: 1.9 M
Downloading Packages:
(1/2): libpq-18.4-1.amzn2023.0.1.x86_64.rpm                                                                                   2.6 MB/s | 293 kB     00:00
(2/2): python3-psycopg2-2.9.10-8.amzn2023.0.1.x86_64.rpm                                                                      1.7 MB/s | 191 kB     00:00
--------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                         3.1 MB/s | 484 kB     00:00
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                                                                      1/1
  Installing       : libpq-18.4-1.amzn2023.0.1.x86_64                                                                                                     1/2
  Installing       : python3-psycopg2-2.9.10-8.amzn2023.0.1.x86_64                                                                                        2/2
  Running scriptlet: python3-psycopg2-2.9.10-8.amzn2023.0.1.x86_64                                                                                        2/2
  Verifying        : libpq-18.4-1.amzn2023.0.1.x86_64                                                                                                     1/2
  Verifying        : python3-psycopg2-2.9.10-8.amzn2023.0.1.x86_64                                                                                        2/2

Installed:
  libpq-18.4-1.amzn2023.0.1.x86_64                                        python3-psycopg2-2.9.10-8.amzn2023.0.1.x86_64

Complete!
sh-5.2$

## ⚙️: Backup

### Command
```bash
cp account_service.py account_service.py.bak
sh-5.2$

# Phase 12: Create an App Gateway on the Private App Server

### Command
```bash
sh-5.2$ cd ~/bank-lab
sh-5.2$ ls
README.md  docs  private-services  realistic_bank_architecture_lab.zip  web-frontend
sh-5.2$ sudo pkill -f "python3 -m http.server 80" || true
sh-5.2$ cat > app_gateway.py <<'PY'
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import os
import json

WEB_ROOT = os.path.join(os.path.dirname(__file__), "web-frontend")
ACCOUNT_SERVICE_URL = "http://10.40.32.106:8102/api/demo"


class AppGatewayHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/accounts":
            self.proxy_accounts()
            return

        return super().do_GET()

    def proxy_accounts(self):
        try:
            request = Request(ACCOUNT_SERVICE_URL, headers={"Accept": "application/json"})
            with urlopen(request, timeout=5) as response:
                body = response.read()
                status = response.status

            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        except HTTPError as exc:
            self.send_json({
                "status": "upstream_http_error",
                "error": str(exc),
                "upstream": ACCOUNT_SERVICE_URL
            }, status=502)

        except URLError as exc:
            self.send_json({
                "status": "upstream_connection_error",
                "error": str(exc),
                "upstream": ACCOUNT_SERVICE_URL
PY  server.serve_forever()accounts to: {ACCOUNT_SERVICE_URL}")
sh-5.2$ sudo nohup python3 ~/bank-lab/app_gateway.py > ~/app_gateway.log 2>&1 &
[1] 46804
sh-5.2$ sudo ss -tulnp | grep :80
tcp   LISTEN 0      5                              0.0.0.0:80        0.0.0.0:*    users:(("python3",pid=46865,fd=3))
sh-5.2$ curl http://localhost
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Apex National Bank | Enterprise Platform</title>
  <link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
  <div class="lab-banner">Fictional bank demo for AWS architecture training. Not affiliated with Chase, First Bank, or any real financial institution.</div>
  <nav class="navbar">
  <a class="brand" href="index.html"><span class="brand-badge">A</span>Apex National Bank</a>
  <div class="nav-links">
    <a href="personal.html">Personal</a>
    <a href="business.html">Business</a>
    <a href="cards.html">Cards</a>
    <a href="loans.html">Loans</a>
    <a href="security.html">Security</a>
    <a href="support.html">Support</a>
    <a class="login" href="staff-portal-placeholder.html">Staff Portal</a>
  </div>
</nav>

<section class="hero">
  <div>
    <div class="eyebrow">Production-style banking architecture lab</div>
    <h1>Enterprise banking platform with private backend services.</h1>
    <p>This frontend represents the public customer experience. The real banking engine sits behind it: auth, accounts, transfers, fraud/risk, notifications,reports, database, cache, logging, and backups.</p>
    <div class="actions">
      <a class="btn btn-primary" href="architecture.html">View Architecture</a>
      <a class="btn btn-outline" href="services.html">Explore Private Services</a>
    </div>
  </div>
  <div class="glass-card">
    <small>Demo Customer Snapshot</small>
    <div class="balance">$84,290.18</div>
    <div class="kpi-grid">
      <div class="kpi"><small>Auth</small><strong>Private</strong></div>
      <div class="kpi"><small>Fraud</small><strong>Active</strong></div>
      <div class="kpi"><small>Database</small><strong>RDS</strong></div>
      <div class="kpi"><small>Cache</small><strong>Redis</strong></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="section-title">
    <span class="eyebrow">What the user sees</span>
    <h2>Many public pages. Private systems behind them.</h2>
    <p>A bank may expose many customer pages, but balances, transfers, KYC, fraud review, and reporting should be handled by private services.</p>
  </div>
  <div class="grid-4">
    <div class="card"><div class="icon">👤</div><h3>Personal Banking</h3><p>Checking, savings, transfers, statements, and profile workflows.</p></div>
    <div class="card"><div class="icon">🏢</div><h3>Business Banking</h3><p>Payroll, treasury, approvals, supplier payments, and audit exports.</p></div>
    <div class="card"><div class="icon">💳</div><h3>Cards</h3><p>Card controls, disputes, limits, fraud flags, and card replacement.</p></div>
    <div class="card"><div class="icon">🛡️</div><h3>Risk & Security</h3><p>MFA, session control, fraud checks, logs, and compliance evidence.</p></div>
  </div>
</section>
<section class="arch-band">
  <div>
    <h2>The frontend is public. The banking engine is private.</h2>
    <p>In a realistic AWS design, users reach an ALB. The ALB routes to private app servers. Those app servers call private services and private databases. Customers never directly reach the backend.</p>
  </div>
  <div class="flow-panel">
    <h3>Request flow</h3>
    <div class="flow-row">1. Customer → Route 53 → CloudFront/WAF → ALB</div>
    <div class="flow-row">2. ALB → Private web/app servers</div>
    <div class="flow-row">3. App servers → Auth, Account, Transfer, Fraud services</div>
    <div class="flow-row">4. Services → RDS, Redis, S3, CloudWatch</div>
  </div>
</section>

  <footer>
  <div>© 2026 Apex National Bank Demo — AWS Cloud Engineering Lab</div>
  <div>ALB • Private App Servers • Private Services • RDS • Redis • S3 • CloudWatch</div>
</footer>
  <script src="assets/js/app.js"></script>
</body>
</html>s
