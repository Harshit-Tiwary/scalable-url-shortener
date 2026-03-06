# Scalable URL Shortener

A production-style URL shortening service built with **FastAPI, PostgreSQL, Redis, and Docker**.
This project demonstrates how to design a **scalable backend system** capable of generating short URLs, handling redirections efficiently, and reducing database load through caching.

---

# Tech Stack

* **Python**
* **FastAPI**
* **PostgreSQL**
* **Redis**
* **Docker**

---

# Project Overview

This project implements a backend service that converts long URLs into short, shareable links.

When a user submits a long URL, the system generates a unique short code using **Base62 encoding** and stores the mapping in **PostgreSQL**. When the short URL is accessed, the service retrieves the original URL and redirects the user.

To improve performance and reduce database load, frequently accessed URLs are cached using **Redis**.

The project is fully **Dockerized**, allowing the entire stack to run locally with a single command.

---

# Features

* Shorten long URLs into unique short links
* Redirect short URLs to their original destination
* Redis caching for faster lookups
* API rate limiting to prevent abuse
* Dockerized environment for easy setup and deployment

---

# System Architecture

User → FastAPI Server → Redis Cache → PostgreSQL Database

1. A user sends a request containing a long URL.
2. The server generates a unique short code using Base62 encoding.
3. The mapping between the short code and original URL is stored in PostgreSQL.
4. When a short URL is accessed:

   * The system first checks Redis cache.
   * If found, it redirects immediately.
   * If not found, it queries PostgreSQL and caches the result.

This design improves performance and reduces database load for frequently accessed URLs.

---

# Project Structure

```
app/
│
├── api
│   └── routes.py
│
├── core
│   ├── logger.py
│   ├── rate_limiter.py
│   └── redis_client.py
│
├── db
│   ├── database.py
│   └── models.py
│
├── schemas
│   └── url.py
│
├── services
│   └── url_service.py
│
├── utils
│   ├── base62.py
│   └── shortener.py
│
└── main.py

Dockerfile
docker-compose.yml
requirements.txt
```

---

# How It Works

1. The user sends a long URL to the API endpoint.
2. The system generates a unique short code using Base62 encoding.
3. The original URL is stored in PostgreSQL.
4. The API returns the generated short URL.
5. When the short URL is accessed, the service retrieves the original link and redirects the user.

Redis caching is used to accelerate lookups for frequently requested URLs.

---

# Running the Project

Clone the repository:

```
git clone https://github.com/Harshit-Tiwary/scalable-url-shortener.git
```

Navigate into the project directory:

```
cd scalable-url-shortener
```

Start the services:

```
docker compose up --build
```

The application will start along with PostgreSQL and Redis using Docker.

---

# Possible Future Improvements

The following enhancements could be added to extend the system:

* URL analytics and click tracking
* Expiring short links
* User authentication
* Distributed ID generation
* Horizontal scaling with load balancers
