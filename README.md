# Videoflix

Videoflix wurde mit Django als Backend-Framework und Angular 17 für das Frontend entwickelt.
Über das Backend können Videos in unterschiedlichen Kategorien hochgeladen werden. Die Django-REST-API stellt verschiedene Endpunkte zur Verfügung, über die das Frontend auf Funktionen wie Registrierung, Anmeldung und Videoverwaltung zugreifen kann.

## Features

- User Registrierung
- User Account Aktivierung über Link via E-Mail
- Vidstack.io Videplayer mit Plyr-Theme
- Upload Videos mit Django Admin


## Features

- **Backend**: Django, Django REST Framework
- **Frontend**: Angular
- **Datenbank**: PostgreSQL
- **Caching**: Redis Layer Caching, Django RQ für asynchrone Aufgaben
- **Videoverarbeitung**: FFmpeg für das Encoding und die Verarbeitung von Videos
- **Containerisierung**: Docker Compose zur einfachen Bereitstellung und Verwaltung aller Dienste

## Vorraussetzung
- Ubuntu mit Docker / Docker Compose Installation


## Installation / Einrichtung auf vServer

1. Klone das Repository
   ```bash
   git clone https://github.com/SirMarco/videoflix.git
2. Benenne die Datei `backend/.env_email` in `.env` um.
3. Passe die E-Mail-Einstellungen in der `.env` Datei an, um den Versand von E-Mails zu ermöglichen. Hier ist ein Beispiel für die E-Mail-Konfiguration:
 ```properties
   # SMTP EMAIL
   EMAIL_HOST = 'mail.example.de'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'noreply@example.ch'
   EMAIL_HOST_PASSWORD = 'password'
   DEFAULT_FROM_EMAIL = 'noreply@example.ch'
   # SMTP EMAIL
   ````
4. Benenne die Datei `.env_server` in `.env` um und passe sie an deine Umgebung an.

#### Datenbankkonfiguration
 ```properties
    POSTGRES_DB: Name der Datenbank, die für PostgreSQL verwendet wird. Standard ist `postgres`.
    POSTGRES_USER: Benutzername für den Datenbankzugriff. Ändere ihn zu einem sichereren Wert.
    POSTGRES_PASSWORD: Passwort für den Datenbankzugang.
```


#### Virtual Hosts und SSL-Konfiguration
 ```properties
    VIRTUAL_HOST_BACKEND: Domain für das Backend. Ändere diesen Wert auf deine Backend-Domain oder IP.
    VIRTUAL_HOST_FRONTEND: Domain für das Frontend. Passe diesen Wert an deine Frontend-Domain an.

    LETSENCRYPT_HOST_BACKEND
    LETSENCRYPT_HOST_FRONTEND: Domainnamen für das SSL-Zertifikat von Let's Encrypt. Auch hier solltest du die Werte entsprechend deiner Backend- und Frontend-Domains setzen.

    LETSENCRYPT_EMAIL: E-Mail-Adresse, die für Let's Encrypt zur Registrierung und für Benachrichtigungen verwendet wird. Ändere diese Adresse auf eine gültige E-Mail, um Zertifikatswarnungen und Updates zu erhalten.
```

5. Erstelle Proxy Network
   ```bash
   docker network create webproxy
6. Starte Videoflix
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
7. Erstelle Admin User für Django Administrator
## Installation / Einrichtung Lokal
1. Klone das Repository
   ```bash
   git clone https://github.com/SirMarco/videoflix.git .
2. Benenne die Datei `backend/.env_email` in `.env` um.
3. Passe die E-Mail-Einstellungen in der `.env` Datei an, um den Versand von E-Mails zu ermöglichen. Hier ist ein Beispiel für die E-Mail-Konfiguration:
 ```properties
   # SMTP EMAIL
   EMAIL_HOST = 'mail.example.de'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'noreply@example.de'
   EMAIL_HOST_PASSWORD = 'password'
   DEFAULT_FROM_EMAIL = 'noreply@example.de'
   # SMTP EMAIL
   ````
1. Benenne die Datei `.env_server` in `.env` um und passe sie an deine Umgebung an.

#### Datenbankkonfiguration
 ```properties
    POSTGRES_DB: Name der Datenbank, die für PostgreSQL verwendet wird. Standard ist `postgres`.
    POSTGRES_USER: Benutzername für den Datenbankzugriff. Ändere ihn zu einem sichereren Wert.
    POSTGRES_PASSWORD: Passwort für den Datenbankzugang.
```