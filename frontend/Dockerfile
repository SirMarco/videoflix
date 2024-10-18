# Stage 1: Build Angular app
FROM node:20 AS build

WORKDIR /usr/src/app

# Kopiere das gesamte Frontend-Projekt
COPY . .

# Installiere die Dependencies und baue die Angular-App
RUN npm install && npm run build

# Am Ende dieses Dockerfiles brauchst du keinen Nginx mehr.
# Die gebauten Dateien können direkt im "nginx-proxy"-Container verwendet werden.
