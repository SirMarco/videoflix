# Benutze ein Node.js Image für den Build-Prozess
FROM node:20 AS build

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere package.json und package-lock.json ins Arbeitsverzeichnis
COPY package*.json ./

# Installiere die Abhängigkeiten
RUN npm install

# Kopiere den restlichen Quellcode ins Arbeitsverzeichnis
COPY . .

# Baue das Angular-Projekt
RUN npm run build

# Nginx Image für die Bereitstellung der gebauten Angular-App
FROM nginx:alpine

# Leere das Nginx-HTML-Verzeichnis vor dem Kopieren
RUN rm -rf /usr/share/nginx/html/*

# Kopiere die gebauten Dateien in das Nginx-Verzeichnis
COPY --from=build /app/dist/frontend_videoflix/browser /usr/share/nginx/html

# Exponiere den Port
EXPOSE 80

# Starte Nginx
CMD ["nginx", "-g", "daemon off;"]
