#!/bin/bash

# 1️⃣ Nano öffnen, um die Markdown-Dokumentation zu erstellen/bearbeiten
nano docs/docker_guide.md

# 2️⃣ Git Status überprüfen
git status

# 3️⃣ Alle Änderungen zum Commit hinzufügen
git add docs/docker_guide.md

# 4️⃣ Commit mit einer Nachricht erstellen
git commit -m "Updated Docker documentation in markdown format"

# 5️⃣ Änderungen auf GitHub pushen
git push origin main  # Falls du auf einem anderen Branch arbeitest, ersetze 'main' mit dem richtigen Branch-Namen

