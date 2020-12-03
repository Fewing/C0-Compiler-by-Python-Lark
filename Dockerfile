# -- Dockerfile --
# 这个文件负责构建包含你的程序的 Docker 容器

FROM pypy:3
WORKDIR /app
COPY . ./
RUN pip install lark-parser