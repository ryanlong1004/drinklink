# DrinkLink Deployment Guide

## Quick Deploy with Docker

### Prerequisites
- Docker and Docker Compose installed on your server
- Domain name (optional, for HTTPS)

### Production Deployment

1. **Pull the repository**:
```bash
git clone git@github.com:ryanlong1004/drinklink.git
cd drinklink
```

2. **Create environment file**:
```bash
cp .env.example .env
```

3. **Edit `.env` with your production values**:
```bash
nano .env
```

Required variables:
```env
POSTGRES_PASSWORD=your_strong_password_here
SECRET_KEY=your_secret_key_here
```

Generate a secure SECRET_KEY:
```bash
openssl rand -hex 32
```

4. **Start the application**:
```bash
docker compose -f docker-compose.prod.yml up -d
```

5. **Run database migrations**:
```bash
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

6. **Access the application**:
- Frontend: http://your-server-ip
- Backend API: http://your-server-ip/api (proxied through nginx)
- API Docs: http://your-server-ip/api/docs

### Default Admin Credentials
```
Username: admin
Password: change-me-in-production
```

**⚠️ IMPORTANT**: Change the admin password immediately after first login!

## Docker Images

The application uses pre-built images from DockerHub:

- **Backend**: `saltycatfish/drinklink-backend:latest`
- **Frontend**: `saltycatfish/drinklink-frontend:latest`

Version-specific tags are also available (e.g., `v1.0.0`).

## Updating the Application

To update to the latest version:

```bash
# Pull latest images
docker compose -f docker-compose.prod.yml pull

# Restart services
docker compose -f docker-compose.prod.yml up -d

# Run any new migrations
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

## HTTPS Setup (Recommended)

For production use with HTTPS, you can:

1. **Use a reverse proxy** (recommended):
   - nginx with Let's Encrypt
   - Caddy (auto-HTTPS)
   - Traefik

2. **Example nginx config**:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Database Backups

Create regular backups:

```bash
# Backup
docker compose -f docker-compose.prod.yml exec db pg_dump -U drinklink drinklink > backup_$(date +%Y%m%d).sql

# Restore
cat backup_20250119.sql | docker compose -f docker-compose.prod.yml exec -T db psql -U drinklink drinklink
```

## Monitoring

View logs:
```bash
# All services
docker compose -f docker-compose.prod.yml logs -f

# Specific service
docker compose -f docker-compose.prod.yml logs -f backend
```

Check service status:
```bash
docker compose -f docker-compose.prod.yml ps
```

## Troubleshooting

### Backend won't start
- Check DATABASE_URL is correct
- Verify database is healthy: `docker compose -f docker-compose.prod.yml ps`
- Check logs: `docker compose -f docker-compose.prod.yml logs backend`

### Frontend shows connection errors
- Ensure backend is running
- Check nginx configuration
- Verify API URL in browser console

### Database connection issues
- Wait for database health check to pass
- Verify POSTGRES_PASSWORD matches in both services
- Check network connectivity between containers

## Security Checklist

- [ ] Changed default admin password
- [ ] Set strong POSTGRES_PASSWORD
- [ ] Generated secure SECRET_KEY
- [ ] Enabled HTTPS
- [ ] Set up firewall rules
- [ ] Regular database backups
- [ ] Keep Docker images updated
- [ ] Monitor logs for suspicious activity

## Performance Tuning

For production workloads, consider:

1. **Database optimization**:
   - Increase PostgreSQL memory settings
   - Add database connection pooling
   - Enable query logging for slow queries

2. **Frontend caching**:
   - Configure nginx caching headers
   - Use CDN for static assets

3. **Backend scaling**:
   - Run multiple backend replicas
   - Add load balancer
   - Use gunicorn with multiple workers

## Support

For issues or questions:
- GitHub Issues: https://github.com/ryanlong1004/drinklink/issues
- Documentation: https://github.com/ryanlong1004/drinklink
