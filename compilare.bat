docker system prune -a --volumes
docker build -t isw_frontend ./frontend/
docker build -t isw_backend ./backend/