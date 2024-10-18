# Stage 1: Build Angular app
FROM node:20 AS build

WORKDIR /usr/src/app

# Kopiere das Angular-Projekt in den Container
COPY . .

# Installiere die Dependencies und baue die Angular-App
RUN npm install && npm run build

# Der Build-Output wird nach /usr/src/app/dist kopiert