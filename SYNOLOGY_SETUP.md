# Synology NAS Setup Guide

## Prerequisites

- Synology NAS with DSM 7.0 or later
- Container Manager installed from Package Center
- At least 2GB RAM available
- Storage space for Docker volumes

## Installation Steps

### Option 1: Using Container Manager UI (Recommended)

#### 1. Download the compose file

Download `docker-compose.synology.yml` from the repository to your computer.

#### 2. Import in Container Manager

1. Open **Container Manager** on your Synology
2. Go to **Project** tab
3. Click **Create**
4. Give it a name: `drinklink`
5. Choose **Upload docker-compose.yml** option
6. Upload the `docker-compose.synology.yml` file
7. Click **Next**

#### 3. Configure Environment Variables

In the Web Portal Settings, set:

- `POSTGRES_PASSWORD`: A strong password for the database
- `SECRET_KEY`: Generate with `openssl rand -hex 32` or use a long random string

#### 4. Build and Start

1. Click **Next** to review settings
2. Click **Done** to create the project
3. Container Manager will pull images and start the containers

#### 5. Access the Application

- Open browser to: `http://your-nas-ip:3080`
- Default admin login: `admin` / `change-me-in-production`

### Option 2: Using Docker CLI via SSH

If you prefer SSH access:

```bash
# SSH into your Synology
ssh admin@your-nas-ip

# Switch to root (or use sudo)
sudo -i

# Navigate to a shared folder
cd /volume1/docker/drinklink

# Download the compose file
wget https://raw.githubusercontent.com/ryanlong1004/drinklink/main/docker-compose.synology.yml

# Set environment variables
export POSTGRES_PASSWORD="your_strong_password"
export SECRET_KEY="your_secret_key"

# Start the application
docker compose -f docker-compose.synology.yml up -d

# Check status
docker compose -f docker-compose.synology.yml ps

# View logs
docker compose -f docker-compose.synology.yml logs -f
```

## Common Synology Issues & Solutions

### Issue 1: Port 80 Already in Use

**Error**: `port is already allocated`

**Solution**: The compose file uses port 3080 instead of 80 to avoid conflicts with Synology's web server.

Access at: `http://your-nas-ip:3080`

### Issue 2: Volume Permission Errors

**Error**: `permission denied` or `cannot create directory`

**Solution**:

1. In Container Manager, go to **Volume** tab
2. Find `drinklink_postgres_data`
3. Right-click → **Edit** → **Mount Path**
4. Ensure it's in a location with proper permissions (e.g., `/volume1/docker/volumes/`)

### Issue 3: Database Connection Failed

**Error**: Backend logs show database connection errors

**Solution**:

1. Check if database container is healthy:
   ```bash
   docker ps
   ```
2. Look for `drinklink-db` with status `healthy`
3. If not healthy, check logs:
   ```bash
   docker logs drinklink-db
   ```
4. The backend waits 10 seconds before connecting, which should be enough

### Issue 4: Images Won't Pull

**Error**: `pull access denied` or `manifest not found`

**Solution**:

1. Ensure your NAS has internet access
2. Check if you can access DockerHub: https://hub.docker.com/
3. Try pulling images manually:
   ```bash
   docker pull saltycatfish/drinklink-backend:latest
   docker pull saltycatfish/drinklink-frontend:latest
   docker pull postgres:15-alpine
   ```

### Issue 5: Containers Keep Restarting

**Error**: Containers in restart loop

**Solution**:

1. Check logs for specific error:
   ```bash
   docker logs drinklink-backend
   docker logs drinklink-frontend
   ```
2. Common causes:
   - Missing environment variables
   - Database not ready (backend waits 10s)
   - Port conflicts

### Issue 6: Cannot Access via Browser

**Problem**: Browser shows "connection refused" or doesn't load

**Checklist**:

- [ ] Container is running: `docker ps | grep drinklink-frontend`
- [ ] Port 3080 is not blocked by firewall
- [ ] Accessing correct IP: Check NAS network settings
- [ ] Try from different device on same network
- [ ] Check Synology Firewall rules in Control Panel

## Updating on Synology

### Via Container Manager UI:

1. Go to **Project** tab
2. Select `drinklink` project
3. Click **Action** → **Stop**
4. Click **Action** → **Pull**
5. Wait for images to update
6. Click **Action** → **Start**

### Via SSH:

```bash
cd /volume1/docker/drinklink
docker compose -f docker-compose.synology.yml pull
docker compose -f docker-compose.synology.yml up -d
```

## Resource Monitoring

Monitor resource usage in Container Manager:

1. Go to **Container** tab
2. Select a container
3. View **Metrics** for CPU and Memory usage

Typical resource usage:

- **Backend**: 100-300 MB RAM
- **Frontend**: 10-20 MB RAM
- **Database**: 50-150 MB RAM

## Backup on Synology

### Automatic Backup with Hyper Backup:

1. Open **Hyper Backup** app
2. Create a new backup task
3. Include Docker volumes: `/volume1/@docker/volumes/drinklink*`

### Manual Database Backup:

```bash
# Create backup
docker exec drinklink-db pg_dump -U drinklink drinklink > /volume1/backups/drinklink_$(date +%Y%m%d).sql

# Restore backup
cat /volume1/backups/drinklink_20250119.sql | docker exec -i drinklink-db psql -U drinklink drinklink
```

## Security Recommendations for Synology

1. **Change default passwords immediately**

   - Admin user password
   - Database password (in compose file)

2. **Enable HTTPS** via Synology's reverse proxy:

   - Control Panel → Login Portal → Advanced → Reverse Proxy
   - Create rule: External port 443 → localhost:3080

3. **Restrict access**:

   - Control Panel → Security → Firewall
   - Allow port 3080 only from your local network

4. **Regular updates**:
   - Keep DSM up to date
   - Pull latest Docker images regularly
   - Monitor security advisories

## Performance Tuning for Synology

If you experience slow performance:

1. **Increase Docker memory limit**:

   - Container Manager → Settings → Resources
   - Allocate more RAM to Docker

2. **Use SSD cache** (if available):

   - Storage Manager → SSD Cache
   - Enable read/write cache for Docker volume

3. **Optimize database**:
   - Allocate more memory in compose file
   - Add persistent database configuration

## Troubleshooting Commands

Check everything is running:

```bash
docker ps --filter "name=drinklink"
```

View all logs:

```bash
docker logs drinklink-backend -f
docker logs drinklink-frontend -f
docker logs drinklink-db -f
```

Restart everything:

```bash
docker compose -f docker-compose.synology.yml restart
```

Complete reset (⚠️ deletes data):

```bash
docker compose -f docker-compose.synology.yml down -v
docker compose -f docker-compose.synology.yml up -d
```

## Getting Help

If you're still experiencing issues:

1. **Check logs** and note specific error messages
2. **Container versions**: `docker images | grep drinklink`
3. **System info**: DSM version, RAM, CPU
4. **Network info**: Port conflicts, firewall rules

Open an issue at: https://github.com/ryanlong1004/drinklink/issues

Include:

- DSM version
- Container Manager version
- Error logs
- Steps to reproduce
