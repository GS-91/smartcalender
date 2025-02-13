#!/bin/bash

# 1️⃣ Nano öffnen, um das Skript zu erstellen/bearbeiten
nano update_docker_docs.sh

# 2️⃣ Skript ausführbar machen
chmod +x update_docker_docs.sh

# 3️⃣ Skript ausführen
./update_docker_docs.sh

# 4️⃣ Git Status überprüfen
git status

# 5️⃣ Alle Änderungen zum Commit hinzufügen
git add .

# 6️⃣ Commit mit einer Nachricht erstellen
git commit -m "Updated Docker documentation with update_docker_docs.sh"

# 7️⃣ Änderungen auf GitHub pushen
git push origin main  # Falls du auf einem anderen Branch arbeitest, ersetze 'main' mit dem richtigen Branch-Namen

