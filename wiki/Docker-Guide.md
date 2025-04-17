# Docker: Schritt-für-Schritt Anleitung

Hier ist deine **komplette Anleitung**, wie du Docker für dein **DevOpsKalenderProjekt** nutzt – mit den passenden **Hauptdateien** und **Befehlen**.

---

## Hauptdateien, die du nutzt  
Diese Dateien sind wichtig für die Bedienung:

| **Datei** | **Funktion** |
|------------|--------------|
| `infra/docker-compose.yml` | Definiert, wie die Container gestartet werden (Docker Compose). |
| `Dockerfile` | Enthält die Anweisungen zum Erstellen des Containers. |
| `requirements.txt` | Listet die Python-Abhängigkeiten auf, die im Container installiert werden. |
| `app/main.py` | Der Haupt-Entry-Point für deine API (FastAPI mit Uvicorn). |

---

##  1. Docker starten und API laufen lassen  
Diesen Befehl nutzt du, um Docker Compose zu starten:  
```bash
docker-compose -f infra/docker-compose.yml up --build -d
```
 **Erklärung:**
- `-f infra/docker-compose.yml` → Nutzt die `docker-compose.yml` im `infra`-Ordner.
- `--build` → Baut das Docker-Image neu.
- `-d` → Startet die Container im Hintergrund.

---

##  2. Container prüfen  
Sehe nach, ob deine Container laufen:  
```bash
docker ps
```
Falls ein Container gestoppt wurde, kannst du alle anzeigen mit:  
```bash
docker ps -a
```

---

## 3. Container-Logs anschauen  
Falls deine API nicht funktioniert, prüfe die Logs:  
```bash
docker logs smartcalendar-api
```

---

## 4. Manuell in den Container gehen  
Falls du Dateien oder Verzeichnisse im Container prüfen willst:  
```bash
docker exec -it smartcalendar-api /bin/sh
```
🔎 **Wichtige Commands im Container:**
```bash
ls -la /app   # Zeigt den Inhalt von /app (dort sollte 'main.py' sein)
cat /app/main.py   # Zeigt den Inhalt deiner Hauptdatei
exit   # Verlässt den Container
```

---

## 5. API testen  
Nutze `curl`, um zu prüfen, ob die API läuft:
```bash
curl http://localhost:8000
```
Falls das nicht klappt, prüfe, ob dein Container läuft:
```bash
docker ps
```

---

## 6. Container stoppen  
Wenn du den laufenden Container **stoppen** willst:
```bash
docker-compose -f infra/docker-compose.yml down
```
Falls du nur einen Container beenden willst:
```bash
docker stop smartcalendar-api
```
Falls du ihn komplett **löschen** willst:
```bash
docker rm smartcalendar-api
```

---

## 7. Docker Desktop zurücksetzen  
Falls deine Docker-App hängt oder sich nicht öffnet:
```bash
killall Docker
open /Applications/Docker.app
```
Falls sich Docker nicht startet, versuche es mit:
```bash
killall com.docker.hyperkit
killall com.docker.backend
killall dockerd
killall vpnkit
killall containerd
open /Applications/Docker.app
```

---

## Zusammenfassung der wichtigsten Befehle  
| **Aktion** | **Befehl** |
|--------------------|----------------------|
| Container starten | `docker-compose -f infra/docker-compose.yml up --build -d` |
| Container prüfen | `docker ps` |
| Logs anzeigen | `docker logs smartcalendar-api` |
| In Container gehen | `docker exec -it smartcalendar-api /bin/sh` |
| API testen | `curl http://localhost:8000` |
| Container stoppen | `docker-compose -f infra/docker-compose.yml down` |
| Einzelnen Container stoppen | `docker stop smartcalendar-api` |
| Container löschen | `docker rm smartcalendar-api` |
| Docker Desktop neu starten | `killall Docker && open /Applications/Docker.app` |

---

Dies ist dein offizieller **Docker-Guide** für das **DevOpsKalenderProjekt**. 

