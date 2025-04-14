# 🚀 CI/CD Quality Assurance Pipeline

# CI/CD Quality Assurance Pipeline

Diese Datei beschreibt die automatisierte Qualitätssicherung (CI/CD) für das Projekt _SmartCalendar_.  
Sie stellt sicher, dass der Code bei jeder Änderung auf **Style**, **Funktionalität** und **Sicherheit** geprüft wird – automatisch, zuverlässig und nachvollziehbar.

---

## 🔍 Checks im Überblick

1. **Flake8**
   - Prüft den Python-Code auf Style-Konformität.
   - Ziel: Sauberer, wartbarer und einheitlicher Code.

2. **Pytest**
   - Führt automatisierte Unit-Tests aus.
   - Ziel: Sicherstellen, dass Funktionen wie erwartet arbeiten.

3. **Bandit**
   - Sucht nach typischen Sicherheitslücken in Python-Code.
   - Ziel: Früherkennung und Vermeidung von Schwachstellen.

---

## ⚙️ Setup

- Alle benötigten Pakete werden über `requirements-dev.txt` installiert.
  ```bash
  pip install -r requirements-dev.txt
- Testcode im Ordner `tests/`
- Produktionscode im Ordner `app/`

## Vorteile

- Vermeidet fehlerhafte Commits – durch automatische Checks vor Merge.
- Erkennt Probleme frühzeitig – noch bevor sie in Produktion landen.
- Fördert Teamqualität & Professionalität – durch klar definierte Qualitätsstandards.