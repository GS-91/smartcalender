# 🚀 CI/CD Quality Assurance Pipeline

Diese Pipeline prüft bei jedem Push auf `main` und bei Pull Requests automatisch:

1. ✅ **Code Style** mit `flake8`
2. ✅ **Unittests** mit `pytest`
3. ✅ **Security Scan** mit `bandit`

## 📁 Setup

- Dev-Abhängigkeiten in `requirements-dev.txt`
- Testcode im Ordner `tests/`
- Produktionscode im Ordner `app/`

## 🔐 Vorteile

- Vermeidet schlechte Commits
- Zeigt Sicherheitsrisiken frühzeitig
- Professioneller Workflow für jede Softwarefirma
