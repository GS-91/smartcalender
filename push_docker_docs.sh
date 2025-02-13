#!/bin/bash

# Definiere den Speicherort der Dokumentationsdatei
DOC_FILE="docs/docker_setup.md"

# Erstelle das Verzeichnis, falls es nicht existiert
mkdir -p docs

# Schreibe die Dokumentation in die Datei
cat > "$DOC_FILE" <<DOC
# 🚀 Docker-Setup für SmartCalendar API

## 📌 Voraussetzungen
- Installiere [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Starte Docker:  
  \`\`\`bash
  open -a Docker
  \`\`\`
- Prüfe, ob Docker läuft:
  \`\`\`bash
  docker info
  \`\`\`

---

## 🛠️ Docker Image & Container Setup
### 1️⃣ **Docker-Container bauen und starten**
Führe folgende Befehle im **Projekt-Hauptverzeichnis** aus:
\`\`\`bash
docker-compose -f infra/docker-compose.yml up --build -d
\`\`\`
Dies erledigt:
✅ Löscht alte Container  
✅ Baut das Docker-Image neu  
✅ Startet den Container im Hintergrund  

---

## ❗ Häufige Probleme & Lösungen
### ⚠️ **Port 8000 bereits belegt**
**Fehlermeldung:**  
\`Bind for 0.0.0.0:8000 failed: port is already allocated\`
  
**Lösung:**  
Überprüfe, welcher Prozess den Port 8000 nutzt:
\`\`\`bash
lsof -i :8000
\`\`\`
Beende den Prozess:
\`\`\`bash
kill -9 <PID>
\`\`\`
Starte dann Docker neu:
\`\`\`bash
docker-compose -f infra/docker-compose.yml up --build -d
\`\`\`

---

### ⚠️ **Docker Daemon nicht erreichbar**
**Fehlermeldung:**  
\`Cannot connect to the Docker daemon\`

**Lösung:**  
Starte Docker neu:
\`\`\`bash
open -a Docker
\`\`\`
Falls nötig, füge Docker zum `PATH` hinzu:
\`\`\`bash
echo 'export PATH="/Applications/Docker.app/Contents/Resources/bin:\$PATH"' >> ~/.zshrc
source ~/.zshrc
\`\`\`

---

## 🛠️ **Nützliche Befehle**
### 🔍 **Laufende Container prüfen**
\`\`\`bash
docker ps
\`\`\`

### 📄 **Logs eines Containers anzeigen**
\`\`\`bash
docker logs smartcalendar-api
\`\`\`

### ⏹ **Container stoppen**
\`\`\`bash
docker-compose -f infra/docker-compose.yml down
\`\`\`

### 🚀 **Container neu starten**
\`\`\`bash
docker-compose -f infra/docker-compose.yml up --build -d
\`\`\`

---

## 📌 Fazit
✅ **Docker läuft jetzt mit deiner SmartCalendar API**  
✅ **Falls Fehler auftreten, kannst du die Logs prüfen**  
✅ **Mit \`docker-compose up --build -d\` kannst du Änderungen neu laden**

🚀 **Viel Erfolg mit deinem DevOps-Kalender-Projekt! 🔥**
DOC

# Git-Befehle, um die Datei ins Repository hochzuladen
git add "$DOC_FILE"
git commit -m "Added Docker Setup Documentation"
git push origin main

echo "✅ Dokumentation erfolgreich erstellt und zu GitHub gepusht!"
