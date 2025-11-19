# Hyperion

Hyperion is a lightweight and simple **Health Monitoring** service designed to sit alongside your infrastructure components and continuously check the health of your essential services.

---

## 🚀 Features
- Periodic health checks powered by **Celery Beat**
- Supports monitoring for:
  - PostgreSQL
  - Redis
  - MySQL
  - MongoDB
  - TCP Connections
- Clean and minimal dashboard to view the health status of all services
- Designed for simplicity, clarity, and fast setup
- Fully **Dockerized** — run with a single command:

```bash
docker compose up --build
```

---

## 🧩 Technologies Used
- **Django** — core framework
- **Celery + Redis** — for periodic tasks and service connectivity checks
- **Docker & Docker Compose** — for easy setup and deployment

---

## 📊 How It Works
Open the dashboard, provide the connection details (URL / host / port) of the service you want to monitor, and Hyperion will periodically check its health. Results are displayed in real-time in the dashboard.

---

## 🔔 Roadmap / Upcoming Features
- **Alerting System** with support for:
  - Email notifications
  - Webhooks
  - Telegram messages
- Support for additional service types
- Public API
- Enhanced dashboard UI/UX

---

## 🛠 Getting Started
### 1. Clone the repository
```bash
git clone https://github.com/soheilsshh/HYPERION.git
cd HYPERION
```

### 2. Run using Docker
```bash
docker compose up --build
```

---

## 🤝 Contributing
Hyperion is an **Open Source** project, and contributions are always welcome!

### Ways to contribute:
- Add support for new service types
- Report bugs or issues
- Improve the dashboard interface
- Develop the upcoming alerting system

Feel free to open a Pull Request or create an Issue.



---

## 📬 Contact
If you have ideas or suggestions, I’d love to hear them!

**GitHub:** https://github.com/soheilsshh/HYPERION

