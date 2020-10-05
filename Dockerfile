# -- Dockerfile --
# 这个文件负责构建包含你的程序的 Docker 容器

FROM python:3.7
WORKDIR /app
COPY . ./