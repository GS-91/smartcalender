# Docker Installation & Fehlerbehebung

## **1. "zsh: command not found: docker"**
**Lösung:** Starte Docker Desktop und prüfe mit:
```bash
open -a Docker
```

Falls Docker immer noch nicht gefunden wird, füge es dem Pfad hinzu:
```bash
echo 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## **2. "ERROR: failed to solve: lstat infra: no such file or directory"**
**Lösung:**  
Stelle sicher, dass du im richtigen Verzeichnis bist:
```bash
pwd  # Prüfe den aktuellen Pfad
ls infra  # Prüfe, ob die Datei existiert
```

## **3. "ModuleNotFoundError: No module named 'fastapi'" beim **
**Lösung:**  
Fehlende Abhängigkeiten in  ergänzen:
```bash
echo "fastapi" >> requirements.txt
echo "uvicorn" >> requirements.txt
echo "pydantic" >> requirements.txt
echo "requests" >> requirements.txt
echo "google-auth" >> requirements.txt
echo "google-auth-oauthlib" >> requirements.txt
echo "google-auth-httplib2" >> requirements.txt
echo "google-api-python-client" >> requirements.txt
```
Dann das Image neu bauen:
```bash
docker build -t smartcalendar-api -f infra/Dockerfile .
```
