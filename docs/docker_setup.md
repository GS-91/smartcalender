# Docker-Setup für SmartCalendar API

+ Diese Datei erklärt Schritt für Schritt, wie du SmartCalendar lokal oder per Docker startest.
+ Sie richtet sich auch an Einsteiger:innen und verwendet bewusst einfache Sprache.

## Voraussetzungen
- Installiere [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Starte Docker:  
  ```bash
  open -a Docker
  ```
- Prüfe, ob Docker läuft:
  ```bash
  docker info
  ```

---

## 🛠️ Docker Image & Container Setup
### **Docker-Container bauen und starten**
+ Führe folgende Befehle im Wurzelverzeichnis des geklonten Projekts aus (z. B. `~/smartcalender`):```bash
docker-compose -f infra/docker-compose.yml up --build -d
```
Dies erledigt:
Löscht alte Container  
Baut das Docker-Image neu  
Startet den Container im Hintergrund  

---

## ❗ Häufige Probleme & Lösungen
### ⚠️ **Port 8000 bereits belegt**
**Fehlermeldung:**  
`Bind for 0.0.0.0:8000 failed: port is already allocated`
  
**Lösung:**  
Überprüfe, welcher Prozess den Port 8000 nutzt:
```bash
lsof -i :8000
```
Beende den Prozess:
```bash
kill -9 <PID>
```
Starte dann Docker neu:
```bash
docker-compose -f infra/docker-compose.yml up --build -d
```

---

### ⚠️ **Docker Daemon nicht erreichbar**
**Fehlermeldung:**  
`Cannot connect to the Docker daemon`

**Lösung:**  
Starte Docker neu:
```bash
open -a Docker
```
Falls nötig, füge Docker zum  hinzu:
```bash
echo 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## **Nützliche Befehle**
### **Laufende Container prüfen**
```bash
docker ps
```

### **Logs eines Containers anzeigen**
```bash
docker logs smartcalendar-api
```

### **Container stoppen**
```bash
docker-compose -f infra/docker-compose.yml down
```

### **Container neu starten**
```bash
docker-compose -f infra/docker-compose.yml up --build -d
```
+ ##  Weitere Hinweise für Entwickler:innen
+
+ - Die `docker-compose.yml` befindet sich unter `infra/docker-compose.yml`
+ - Das zugehörige `Dockerfile` findest du im Projekt-Root: `Dockerfile`
+ - Der API-Port ist standardmäßig auf `8000` gesetzt.
+ - Die Umgebungsvariable `GOOGLE_APPLICATION_CREDENTIALS` wird im Container gesetzt und muss auf eine gültige JSON-Datei zeigen.