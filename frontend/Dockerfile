# frontend/Dockerfile
FROM nginx:alpine

# 复制静态文件
COPY frontend/ /usr/share/nginx/html/

# 复制 nginx 配置
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
