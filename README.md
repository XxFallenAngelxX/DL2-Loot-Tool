
# **Loot Modifier Tool Documentation**

## **Inhaltsverzeichnis**
1. [Einführung](#einführung)
2. [Voraussetzungen und Installation](#voraussetzungen-und-installation)
3. [Verzeichnisstruktur](#verzeichnisstruktur)
4. [Funktionen und Features](#funktionen-und-features)
    - Extraktion der Loot-Daten
    - Initialisierung der Config-Datei
    - Laden und Speichern der Config-Datei
    - Benutzerinteraktionsmenü
5. [Ausführliche Erklärung der Code-Module](#ausführliche-erklärung-der-code-module)
    - Logging-System
    - Extraktion von Loot-Daten
    - Config-Management
    - Benutzerinteraktionsmenü
6. [Erweiterungsmöglichkeiten](#erweiterungsmöglichkeiten)
7. [Bekannte Probleme und Fehlersuche](#bekannte-probleme-und-fehlersuche)
8. [FAQ](#faq)
9. [Lizenz und Haftungsausschluss](#lizenz-und-haftungsausschluss)

---

## **Einführung**

Das *Loot Modifier Tool* ist ein leistungsstarkes Werkzeug zur Bearbeitung und Verwaltung von Loot-Tabellen in Spielen. Es ermöglicht es Entwicklern und Spielern, die Loot-Daten eines Spiels zu extrahieren, anzupassen und in einer Config-Datei zu speichern. Ziel ist es, ein maßgeschneidertes Spielerlebnis zu schaffen, indem die Beutewahrscheinlichkeiten und Mengen angepasst werden.

Dieses Tool ist besonders hilfreich für Spieleentwickler, Modder und Enthusiasten, die die Balance und das Verhalten von Loot-Systemen in ihren Spielen ändern möchten.

---

## **Voraussetzungen und Installation**

Bevor du das *Loot Modifier Tool* verwenden kannst, musst du sicherstellen, dass alle notwendigen Abhängigkeiten installiert sind. Das Tool basiert auf Python und verwendet einige externe Bibliotheken.

### **Voraussetzungen**
- Python 3.x
- Folgende Python-Bibliotheken:
    - `os`
    - `json`
    - `re`
    - `time`
    - `subprocess`
    - `colorama` (Für die Konsolenausgabe in Farbe)

### **Installation**
1. Installiere Python 3.x, falls noch nicht geschehen.
2. Stelle sicher, dass du `pip` installiert hast, um Bibliotheken zu verwalten.
3. Installiere die benötigten Bibliotheken:
    ```bash
    pip install colorama
    ```
4. Lade den Quellcode des *Loot Modifier Tool* herunter und platziere ihn in einem Arbeitsverzeichnis.

---

## **Verzeichnisstruktur**

Hier ist eine typische Verzeichnisstruktur, die das Tool verwendet. Es ist wichtig, dass diese Struktur eingehalten wird, damit das Programm korrekt funktioniert.

```
/<Root-Directory>
    /logs                # Verzeichnis für Log-Dateien
    /DB                  # Datenbankverzeichnis, das die Datei 'default.loot' enthält
    /Config              # Verzeichnis, in dem die loot_config.json gespeichert wird
    LootTool.py          # Hauptskript des Tools
```

### **Wichtige Dateien**
- **default.loot**: Diese Datei enthält die Loot-Daten, die das Tool extrahiert und verarbeitet.
- **loot_config.json**: Die Konfigurationsdatei, in der die geänderten Loot-Daten gespeichert werden.
- **backend_log.txt**: Enthält Logs über wichtige Aktionen und Fehler.
- **debug_log.txt**: Speichert detaillierte Debugging-Informationen.

---

## **Funktionen und Features**

Das *Loot Modifier Tool* bietet eine Reihe von Funktionen, die die Anpassung und Verwaltung von Loot-Systemen einfach und effizient machen. Im Folgenden werden die wichtigsten Funktionen des Tools erläutert.

### **1. Extraktion der Loot-Daten**
Das Tool extrahiert Loot-Daten aus einer Datei `default.loot`, die sich im `DB`-Verzeichnis befindet. Die extrahierten Daten werden in einer für den Benutzer verständlichen Struktur verarbeitet, sodass sie später geändert und gespeichert werden können.

- **Beispielstruktur**:
    ```json
    {
        "LootedObject_1": [
            {"use_group": "Item1", "weight": 1.0, "min_amount": 1, "max_amount": 5},
            {"use_group": "Item2", "weight": 0.5}
        ],
        "LootedObject_2": [
            {"use_group": "Item3", "weight": 2.0}
        ]
    }
    ```

### **2. Initialisierung der Config-Datei**
Falls eine `loot_config.json` noch nicht existiert, wird sie vom Tool automatisch basierend auf den extrahierten Daten erstellt. Dadurch können alle Änderungen an den Loot-Daten dauerhaft gespeichert werden.

### **3. Laden und Speichern der Config-Datei**
Das Tool bietet Funktionen, um die Config-Datei zu laden und zu speichern. Änderungen, die der Benutzer vornimmt, können problemlos in der Config gespeichert werden.

### **4. Benutzerinteraktionsmenü**
Das Tool enthält ein interaktives Menü, das den Benutzer durch die verschiedenen Funktionen führt:
- **Config-Datei im Editor öffnen**: Öffnet die Config-Datei in einem Texteditor.
- **Min/Max-Werte anpassen**: Ermöglicht das Anpassen der minimalen und maximalen Anzahl von Items, die beim Loot fallen gelassen werden.
- **Gewicht anpassen**: Passt die Wahrscheinlichkeit an, mit der bestimmte Items fallen gelassen werden.
- **Änderungen speichern**: Speichert alle vorgenommenen Änderungen in der Config-Datei.

---

## **Ausführliche Erklärung der Code-Module**

### **1. Logging-System**
Das Logging-System im Tool ist in zwei Bereiche aufgeteilt:
- **Backend-Log**: Protokolliert allgemeine Informationen und Fehler.
- **Debug-Log**: Protokolliert detaillierte Debug-Informationen, die bei der Fehlersuche hilfreich sind.

Jede Funktion im Tool führt automatisch Logging-Operationen durch, sodass nachvollzogen werden kann, welche Schritte durchgeführt wurden.

### **2. Extraktion von Loot-Daten**
Die Funktion `extract_loot_data_from_default` liest die Datei `default.loot` und extrahiert die relevanten Loot-Gruppen und deren Items. Die Daten werden als Python-Dictionary gespeichert und können leicht manipuliert werden.

### **3. Config-Management**
Das Config-Management umfasst die Funktionen zum Erstellen, Laden und Speichern der `loot_config.json`. Diese Datei speichert die geänderten Loot-Daten dauerhaft und kann in jedem Editor geöffnet werden.

### **4. Benutzerinteraktionsmenü**
Das Menü ist der Hauptzugangspunkt für den Benutzer. Es enthält klare und einfache Optionen, die den Benutzer durch die Konfiguration der Loot-Daten führen. Es ist so gestaltet, dass es auch von Benutzern ohne Programmiererfahrung verwendet werden kann.

---

## **Erweiterungsmöglichkeiten**

Das Tool kann erweitert werden, um zusätzliche Features hinzuzufügen, wie z. B.:
- **Mehrere Loot-Dateien unterstützen**: Derzeit arbeitet das Tool nur mit einer Datei (`default.loot`). Es könnte so erweitert werden, dass es mehrere Loot-Dateien unterstützt.
- **Erweiterte Anpassungen**: Implementiere zusätzliche Funktionen zur Anpassung der Loot-Daten, wie z. B. das Hinzufügen neuer Items oder das Löschen bestehender.
- **Grafische Benutzeroberfläche (GUI)**: Eine GUI könnte dem Tool hinzugefügt werden, um die Bedienung noch benutzerfreundlicher zu machen.

---

## **Bekannte Probleme und Fehlersuche**

### **Fehlerbehebung**:
1. **Dateipfade stimmen nicht überein**: Überprüfe, ob die Verzeichnisse (`logs`, `DB`, `Config`) korrekt erstellt wurden und die erforderlichen Dateien (z. B. `default.loot`) vorhanden sind.
2. **Python-Module fehlen**: Stelle sicher, dass alle erforderlichen Python-Module installiert sind, insbesondere `colorama`.

### **Häufige Fehler**:
- **"FileNotFoundError"**: Dies tritt auf, wenn die Datei `default.loot` nicht im richtigen Verzeichnis (`DB`) vorhanden ist.
- **"KeyError" oder "IndexError"**: Diese Fehler treten auf, wenn die Struktur der `default.loot`-Datei nicht den erwarteten Mustern entspricht.

---

## **FAQ**

### **1. Was passiert, wenn ich die `default.loot`-Datei ändere?**
Wenn du die `default.loot`-Datei änderst und das Tool ausführst, wird es versuchen, die neuen Daten zu extrahieren. Änderungen in dieser Datei werden nicht automatisch in der Config gespeichert, es sei denn, du führst die entsprechende Option im Menü aus.

### **2. Wie kann ich das Tool erweitern?**
Das Tool ist modular aufgebaut und kann leicht erweitert werden. Neue Funktionen können im Menü hinzugefügt werden, indem du die `display_menu()`-Funktion und die zugehörigen Aktionen in der `main()`-Funktion anpasst.

---

## **Lizenz und Haftungsausschluss**

Dieses Tool wird ohne Garantie zur Verfügung gestellt. Die Entwickler übernehmen keine Verantwortung für eventuelle Schäden oder Datenverluste, die durch die Verwendung dieses Tools entstehen. Die Benutzer sind dafür verantwortlich, ihre eigenen Daten und Dateien ordnungsgemäß zu sichern.

---

Diese Dokumentation bietet einen umfassenden Überblick über das *Loot Modifier Tool* und seine Funktionen. Durch die klare Struktur und die einfache Bedienbarkeit können Benutzer ohne technische Kenntnisse das Tool effektiv nutzen, während Entwickler das Tool leicht erweitern können.
