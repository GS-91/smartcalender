# CI/CD Quality Assurance Pipeline

Diese Pipeline sorgt dafür, dass Codequalität und Sicherheit automatisch überprüft werden.

## Checks

1. **Flake8**
   - Prüft den Python-Code auf Style-Konformität.
   - Ziel: Sauberer, wartbarer Code.

2. **Pytest**
   - Führt Unit-Tests aus.
   - Ziel: Sicherstellen, dass Funktionen korrekt arbeiten.

3. **Bandit**
   - Analysiert Sicherheitsrisiken im Code.
   - Ziel: Früherkennung von Schwachstellen.

## Setup

- Alle Abhängigkeiten werden über `requirements-dev.txt` installiert.
- Testcode befindet sich im Verzeichnis `tests/`.
- Produktivcode befindet sich im Verzeichnis `app/`.

## Vorteile

- Vermeidet schlechte Commits.
- Erkennt Probleme frühzeitig.
- Stellt Professionalität im Workflow sicher.