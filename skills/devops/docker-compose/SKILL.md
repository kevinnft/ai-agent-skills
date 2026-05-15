---
name: docker-compose
description: Multi-container Docker applications with docker-compose — define services, networks, volumes, and orchestrate local development environments
tags: [docker, containers, devops, orchestration, development]
origin: unknown
source_license: see upstream
language: en
---

# Docker Compose — Multi-Container Orchestration

Manage multi-container Docker applications with docker-compose. Define services, networks, volumes, and dependencies in YAML. Perfect for local development, testing, and simple production deployments.

## When to Use

- Setting up local development environments
- Running multi-service applications (app + database + cache)
- Testing microservices locally
- CI/CD pipeline containers
- Simple production deployments

## Core Concepts

### Services
```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

### Networks
```yaml
networks:
  frontend:
  backend:

services:
  app:
    networks:
      - frontend
      - backend
  
  db:
    networks:
      - backend
```

## Common Patterns

### 1. Full-Stack App (Frontend + Backend + Database)
```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

### 2. Microservices with Redis Cache
```yaml
services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://cache:6379
    depends_on:
      - cache
      - db

  worker:
    build: ./worker
    environment:
      - REDIS_URL=redis://cache:6379
    depends_on:
      - cache

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

### 3. Development with Hot Reload
```yaml
services:
  app:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    command: npm run dev
```

## Essential Commands

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Build and start
docker-compose up --build

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f app

# Execute command in service
docker-compose exec app sh

# Scale service
docker-compose up -d --scale worker=3

# Restart service
docker-compose restart app

# View running services
docker-compose ps
```

## Best Practices

### 1. Use .env Files
```bash
# .env
POSTGRES_PASSWORD=secret
API_PORT=8000
```

```yaml
# docker-compose.yml
services:
  db:
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
  
  api:
    ports:
      - "${API_PORT}:8000"
```

### 2. Health Checks
```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 3. Resource Limits
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### 4. Named Volumes for Persistence
```yaml
volumes:
  postgres-data:
    driver: local
  redis-data:
    driver: local
```

### 5. Separate Dev/Prod Configs
```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :3000

# Change port in docker-compose.yml
ports:
  - "3001:3000"
```

### Container Won't Start
```bash
# Check logs
docker-compose logs app

# Check service status
docker-compose ps

# Rebuild without cache
docker-compose build --no-cache app
```

### Database Connection Issues
```bash
# Ensure depends_on is set
depends_on:
  - db

# Use service name as hostname
DATABASE_URL=postgresql://user:pass@db:5432/myapp

# Wait for database to be ready (use wait-for-it.sh or healthcheck)
```

### Volume Permission Issues
```bash
# Set user in Dockerfile
USER node

# Or in docker-compose.yml
user: "1000:1000"
```

## Production Considerations

### 1. Use Specific Image Tags
```yaml
# ❌ Don't use latest
image: postgres:latest

# ✅ Use specific version
image: postgres:15.3-alpine
```

### 2. Secrets Management
```yaml
# Use Docker secrets (Swarm mode)
secrets:
  db_password:
    file: ./secrets/db_password.txt

services:
  db:
    secrets:
      - db_password
```

### 3. Logging
```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 4. Restart Policies
```yaml
services:
  app:
    restart: unless-stopped
```

## Integration with CI/CD

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: |
    docker-compose -f docker-compose.test.yml up --abort-on-container-exit
    docker-compose -f docker-compose.test.yml down -v
```

## Common Stacks

### MERN Stack
```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
  
  backend:
    build: ./backend
    ports:
      - "5000:5000"
  
  mongo:
    image: mongo:6
    volumes:
      - mongo-data:/data/db
```

### Django + PostgreSQL + Redis
```yaml
services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
  
  redis:
    image: redis:7-alpine
  
  celery:
    build: .
    command: celery -A myapp worker -l info
    depends_on:
      - redis
```

## References

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)
