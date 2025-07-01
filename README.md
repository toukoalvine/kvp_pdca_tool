# kvp_pdca_tool
Tool zur Verfolgung von Verbesserungsprojekten
# 📊 KVP/PDCA Tool – Kontinuierlicher Verbesserungsprozess

# KVP/PDCA Tool - Kontinuierliche Verbesserung

Eine Streamlit-Anwendung zur Verwaltung von kontinuierlichen Verbesserungsprozessen (KVP) basierend auf dem PDCA-Zyklus (Plan-Do-Check-Act).

## 🚀 Features

### Dashboard
- **KPI-Übersicht**: Zentrale Kennzahlen auf einen Blick
- **Fortschrittsvisualisierung**: Interaktive Charts und Diagramme
- **PDCA-Zyklusübersicht**: Status aller PDCA-Phasen
- **Echtzeit-Metriken**: Aktuelle Projektdaten und Trends

### Projektverwaltung
- **Projekterfassung**: Neue Verbesserungsprojekte anlegen
- **Kategorisierung**: Nach Qualität, Effizienz, Kosten, Sicherheit, Umwelt
- **Prioritätsverwaltung**: Hoch, Mittel, Niedrig
- **Fortschrittstracking**: Überwachung des Projektstatus
- **Einsparungsberechnung**: Erwartete vs. tatsächliche Einsparungen

### Aufgabenverwaltung
- **PDCA-Integration**: Aufgaben den PDCA-Phasen zuordnen
- **Verantwortlichkeiten**: Klare Zuweisung von Aufgaben
- **Fälligkeitsdaten**: Terminüberwachung
- **Kommentarsystem**: Team-Kommunikation zu Aufgaben

### Analytics & Reporting
- **Erfolgsraten**: Analyse nach Kategorien
- **Zeitseries-Analysen**: Fortschritt über Zeit
- **Einsparungsanalyse**: Finanzielle Auswirkungen
- **Exportfunktionen**: Datenexport für weitere Analysen

## 🛠️ Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### Schritt-für-Schritt Installation

1. **Repository klonen oder Dateien herunterladen**
   ```bash
   # Dateien in einen neuen Ordner kopieren
   mkdir kvp-tool
   cd kvp-tool
   ```

2. **Virtuelle Umgebung erstellen (empfohlen)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **Anwendung starten**
   ```bash
   streamlit run app.py
   ```

5. **Browser öffnen**
   - Die Anwendung öffnet sich automatisch unter `http://localhost:8501`
   - Falls nicht, URL manuell im Browser eingeben

## 📋 Verwendung

### Erste Schritte

1. **Dashboard erkunden**
   - Überblick über alle KPIs und Metriken
   - PDCA-Zyklusübersicht verstehen

2. **Erstes Projekt anlegen**
   - Zu "Projekte" navigieren
   - "Neues Projekt erstellen" klicken
   - Alle relevanten Daten eingeben

3. **Aufgaben verwalten**
   - Aufgaben zu Projekten hinzufügen
   - PDCA-Phasen zuweisen
   - Verantwortlichkeiten definieren

4. **Fortschritt verfolgen**
   - Analytics-Bereich für Auswertungen nutzen
   - Regelmäßige Aktualisierung der Projektdaten

### Navigation

**Sidebar Navigation:**
- **Dashboard**: Hauptübersicht mit KPIs und Charts
- **Projekte**: Projektverwaltung und -erstellung
- **Aufgaben**: Aufgabenverwaltung mit PDCA-Integration
- **Analytics**: Detaillierte Analysen und Reports

**Filter:**
- Status-Filter: Neue, In Bearbeitung, Review, Abgeschlossen
- Prioritäts-Filter: Hoch, Mittel, Niedrig
- Datum-Filter: Zeitraumbasierte Filterung

### PDCA-Integration

**Plan (Planen):**
- Problemanalyse
- Zieldefinition
- Maßnahmenplanung

**Do (Umsetzen):**
- Umsetzung der geplanten Maßnahmen
- Datensammlung während der Umsetzung

**Check (Überprüfen):**
- Ergebnisse bewerten
- Zielerreichung prüfen
- Abweichungsanalyse

**Act (Handeln):**
- Standardisierung erfolgreicher Maßnahmen
- Anpassung bei Abweichungen
- Kontinuierliche Verbesserung

## 🔧 Konfiguration

### Anpassungen

**Session State:**
Die Anwendung verwendet Session State für Datenpersistenz. Daten gehen beim Schließen der Anwendung verloren.

**Datenbankintegration:**
Für produktive Nutzung empfiehlt sich die Integration einer Datenbank (SQLite, PostgreSQL, etc.).

**Authentifizierung:**
Für Multi-User-Umgebungen kann Streamlit-Authenticator integriert werden.

### Umgebungsvariablen

Erstellen Sie eine `.env` Datei für konfigurierbare Parameter:
```
APP_TITLE=KVP/PDCA Tool
DATABASE_URL=sqlite:///kvp.db
DEBUG=False
```

## 📊 Datenstruktur

### Projekte
```python
{
    'id': int,
    'name': str,
    'category': str,  # Qualität, Effizienz, Kosten, Sicherheit, Umwelt
    'priority': str,  # high, medium
