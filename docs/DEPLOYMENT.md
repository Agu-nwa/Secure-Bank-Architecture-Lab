# Deployment Guide

## 1. Deploy Web Frontend on App Servers

On each private app EC2, install Apache:

```bash
sudo dnf update -y
sudo dnf install -y httpd
sudo systemctl enable httpd
sudo systemctl start httpd
```

Copy the `web-frontend/` contents to Apache root:

```bash
sudo cp -r web-frontend/* /var/www/html/
sudo systemctl restart httpd
```

Put both app servers behind an Application Load Balancer.

## Command Meaning

`sudo dnf install -y httpd`

- `sudo` = run with administrator permission
- `dnf` = Amazon Linux package manager
- `install` = install software
- `-y` = answer yes automatically
- `httpd` = Apache web server package

## 2. Deploy Private Services

On the private service EC2:

```bash
cd private-services
chmod +x run_all_services.sh
./run_all_services.sh
```

Test from the app server:

```bash
curl http://PRIVATE_SERVICE_SERVER_IP:8101/api/status
curl http://PRIVATE_SERVICE_SERVER_IP:8102/api/demo
curl http://PRIVATE_SERVICE_SERVER_IP:8103/api/demo
curl http://PRIVATE_SERVICE_SERVER_IP:8104/api/demo
curl http://PRIVATE_SERVICE_SERVER_IP:8105/api/demo
curl http://PRIVATE_SERVICE_SERVER_IP:8106/api/demo
curl http://PRIVATE_SERVICE_SERVER_IP:8107/api/demo
```

## 3. Security Group Design

### ALB Security Group
Inbound:
- HTTPS 443 from `0.0.0.0/0`
- HTTP 80 from `0.0.0.0/0` for testing only

Outbound:
- HTTP 80 to App Server SG

### App Server Security Group
Inbound:
- HTTP 80 from ALB SG only

Outbound:
- Ports 8101-8107 to Private Services SG
- DB port to Database SG
- HTTPS 443 through NAT for updates

### Private Service Security Group
Inbound:
- Ports 8101-8107 from App Server SG only

Outbound:
- DB/cache/S3/CloudWatch as needed

### Database Security Group
Inbound:
- MySQL 3306 or PostgreSQL 5432 from App/Service SG only

Never expose database ports to `0.0.0.0/0`.
