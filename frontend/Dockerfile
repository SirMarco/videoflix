FROM node:20 AS build

WORKDIR /usr/src/app

COPY . .

RUN npm install

RUN npm run build && echo "Build finished successfully."

# Kopiere die gebauten Dateien in das Nginx-Verzeichnis
COPY /dist/frontend_videoflix/browser /usr/share/nginx/html
