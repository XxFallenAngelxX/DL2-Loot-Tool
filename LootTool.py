import os
import json
import re
import time  # Zeitmodul für Logging
import subprocess  # Zum Öffnen der Datei im Standard-Editor
from colorama import Fore, Style, init  # Farben und Style für Terminal

# Initiiere colorama für plattformübergreifende Farbausgabe
init(autoreset=True)

# Root-Verzeichnis als aktuelles Arbeitsverzeichnis festlegen
ROOT_DIR = os.getcwd()
LOG_DIR = os.path.join(ROOT_DIR, "logs")
DB_DIR = os.path.join(ROOT_DIR, "DB")  # DB-Verzeichnis für default.loot
CONFIG_DIR = os.path.join(ROOT_DIR, "Config")  # Config-Verzeichnis für loot_config.json

# Sicherstellen, dass die Verzeichnisse existieren
for directory in [LOG_DIR, CONFIG_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Funktion für Backend-Logging - mit zusätzlichen Infos
def log_message_backend(nachricht, level="INFO", extra_info=None):
    log_file_path = os.path.join(LOG_DIR, "backend_log.txt")
    debug_log_file_path = os.path.join(LOG_DIR, "debug_log.txt")  # Separate Debug-Log-Datei
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Zusätzliche Info in den Log-Eintrag aufnehmen, falls vorhanden
    extra_details = f" | Details: {extra_info}" if extra_info else ""
    log_entry = f"[{level}] {timestamp} - {nachricht}{extra_details}\n"
    
    try:
        if level == "DEBUG":
            # Schreibe DEBUG-Nachrichten in die Debug-Log-Datei
            with open(debug_log_file_path, "a") as debug_log_file:
                debug_log_file.write(log_entry)
        else:
            # Schreibe andere Nachrichten in die allgemeine Log-Datei
            with open(log_file_path, "a") as log_file:
                log_file.write(log_entry)
                
            # Ausgabe in der Konsole, wenn es kein DEBUG-Level ist
            if level == "ERROR":
                print(f"{Fore.RED}{log_entry.strip()}")
            elif level == "WARNING":
                print(f"{Fore.YELLOW}{log_entry.strip()}")
            else:
                print(f"{Fore.GREEN}{log_entry.strip()}")
                
    except Exception as e:
        print(f"{Fore.RED}Logging-Fehler (Backend): {str(e)}")

# Funktion zum Extrahieren von Loot-Daten aus default.loot mit detailliertem Logging
def extract_loot_data_from_default(file_path):
    log_message_backend(f"Lese Datei {file_path}", level="INFO")
    # Datei-Inhalt laden
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # LootedObject-Gruppen extrahieren
    loot_groups = re.findall(r'LootedObject\("(.+?)"\).*?\{(.*?)\}', content, re.DOTALL)
    
    parsed_loot_data = {}
    log_message_backend(f"Anzahl der Loot-Gruppen: {len(loot_groups)}", level="INFO")
    
    # Jede Gruppe verarbeiten
    for group in loot_groups:
        looted_object = group[0]  # Name der Loot-Gruppe
        group_content = group[1]  # Inhalt der Gruppe
        
        # Alle 'use'-Einträge extrahieren
        uses = re.findall(r'use (\w+)\(weight = ([0-9.]+)(?:, min_amount = (\d+), max_amount = (\d+))?\);', group_content)
        
        # Initialize list for this group if not present
        if looted_object not in parsed_loot_data:
            parsed_loot_data[looted_object] = []
        
        for use_group, weight, min_amount, max_amount in uses:
            entry = {
                "use_group": use_group,
                "weight": float(weight),
            }
            # min/max nur hinzufügen, wenn sie vorhanden sind
            if min_amount and max_amount:
                entry["min_amount"] = int(min_amount)
                entry["max_amount"] = int(max_amount)
            
            parsed_loot_data[looted_object].append(entry)
            
            # Logging debug for each 'use' entry extracted
            log_message_backend(f"Extrahierter use-Eintrag", level="DEBUG", extra_info=f"Gruppe: {looted_object}, Eintrag: {use_group}, Gewicht: {weight}")
    
    log_message_backend(f"Erfolgreich Loot-Daten extrahiert.", level="INFO")
    return parsed_loot_data

# Funktion zur Initialisierung der Config-Datei mit zusätzlichen Log-Nachrichten
def initialize_config(loot_data, config_file_path):
    if not os.path.exists(config_file_path):
        try:
            with open(config_file_path, 'w', encoding='utf-8') as file:
                json.dump(loot_data, file, indent=4)
            log_message_backend(f"Config-Datei '{config_file_path}' erstellt.", level="INFO")
            print(f"{Fore.GREEN}Die Config-Datei wurde erfolgreich erstellt und gespeichert.")
        except Exception as e:
            log_message_backend(f"Fehler beim Erstellen der Config-Datei", level="ERROR", extra_info=str(e))
    else:
        log_message_backend(f"Config-Datei '{config_file_path}' existiert bereits.", level="INFO")
        print(f"{Fore.YELLOW}Die Config-Datei existiert bereits.")

# Funktion zum Laden der Konfigurationsdatei mit Logging-Infos
def load_config(config_file_path):
    if os.path.exists(config_file_path):
        try:
            with open(config_file_path, 'r', encoding='utf-8') as file:
                log_message_backend(f"Config-Datei '{config_file_path}' wird geladen.", level="INFO")
                config_data = json.load(file)
                log_message_backend(f"Config-Datei erfolgreich geladen", level="INFO", extra_info=f"Pfad: {config_file_path}")
                return config_data
        except Exception as e:
            log_message_backend(f"Fehler beim Laden der Config-Datei", level="ERROR", extra_info=str(e))
    else:
        log_message_backend(f"Config-Datei '{config_file_path}' nicht gefunden.", level="ERROR")
        return None

# Benutzerinteraktionsmenü mit ausführlicher Erklärung
def display_menu():
    print("\n==== Loot Modifier Tool ====")
    print(f"{Fore.CYAN}{Style.BRIGHT}Willkommen beim Loot Modifier Tool!")
    print(f"Dieses Tool ermöglicht es dir, Loot-Tabellen aus dem Spiel zu modifizieren und anzupassen.")
    print(f"Du kannst die Min/Max-Werte und die Gewichte der Beute ändern und alles in einer Konfigurationsdatei speichern.")
    print(f"Bitte wähle eine Option, um fortzufahren:\n")
    
    print(f"{Fore.CYAN}{Style.BRIGHT}1. Config-Datei im Editor öffnen")
    print(f"{Fore.CYAN}{Style.BRIGHT}2. Min/Max-Werte anpassen (Ändere die Menge der Items, die fallen gelassen werden)")
    print(f"{Fore.CYAN}{Style.BRIGHT}3. Gewicht anpassen (Passe die Wahrscheinlichkeit an, mit der Items fallen gelassen werden)")
    print(f"{Fore.CYAN}{Style.BRIGHT}4. Änderungen speichern (Speichere alle deine Anpassungen in der Config-Datei)")
    print(f"{Fore.CYAN}{Style.BRIGHT}5. Beenden (Verlasse das Tool)\n")
    option = input(f"{Fore.YELLOW}Bitte wähle eine Option (1-5): ")
    return option
    
import os

def open_config_file(config_file_path):
    # Prüfe, ob die Datei existiert
    if os.path.exists(config_file_path):
        try:
            # Öffne die Datei mit der Standardanwendung des Systems
            os.startfile(config_file_path)
        except Exception as e:
            print(f"Fehler beim Öffnen der Datei: {e}")
    else:
        print(f"Die Datei {config_file_path} existiert nicht.")
  
# Hauptprogramm mit erweiterten Begrüßungstexten und Erläuterungen
def main():
    print(f"{Style.BRIGHT}{Fore.CYAN}Starte das Loot Modifier Tool...\n")
    
    print(f"{Fore.GREEN}Dieses Tool hilft dir, die Beute- und Loot-Systeme deines Spiels zu modifizieren.")
    print(f"Durch die Anpassung von Loot-Daten kannst du die Balance des Spiels beeinflussen oder das Spielerlebnis optimieren.\n")
    
    # Pfad zur default.loot Datei (im DB-Ordner)
    default_loot_file = os.path.join(DB_DIR, 'default.loot')
    
    # Pfad zur Konfigurationsdatei (im Config-Ordner)
    config_file_path = os.path.join(CONFIG_DIR, "loot_config.json")
    
    log_message_backend("Starte die Extraktion der Loot-Daten", level="INFO")
    # Extrahiere die Loot-Daten aus der default.loot Datei
    loot_data = extract_loot_data_from_default(default_loot_file)
    
    log_message_backend("Initialisiere die Config-Datei", level="INFO")
    # Initialisierung der Konfigurationsdatei, wenn sie fehlt
    initialize_config(loot_data, config_file_path)
    
    log_message_backend("Lade die Loot-Daten von der Konfigurationsdatei", level="INFO")
    # Laden der Loot-Daten (von der Konfigurationsdatei)
    loaded_loot_data = load_config(config_file_path)
    
    if loaded_loot_data:
        loot_data = loaded_loot_data
        log_message_backend("Loot-Daten erfolgreich geladen.", level="INFO")
    else:
        log_message_backend("Fehler beim Laden der Loot-Daten.", level="ERROR")
    
    # Benutzerinteraktionsmenü
    while True:
        option = display_menu()
        if option == '1':
            log_message_backend("Benutzer hat gewählt: Config-Datei im Editor öffnen", level="INFO")
            open_config_file(config_file_path)
        elif option == '2':
            log_message_backend("Benutzer hat gewählt: Min/Max-Werte anpassen", level="INFO")
            modify_min_max(loot_data)  # Annahme: Diese Funktion existiert
        elif option == '3':
            log_message_backend("Benutzer hat gewählt: Gewicht anpassen", level="INFO")
            modify_weight(loot_data)  # Annahme: Diese Funktion existiert
        elif option == '4':
            log_message_backend("Benutzer hat gewählt: Änderungen speichern", level="INFO")
            save_all_groups_to_config(loot_data, config_file_path)
        elif option == '5':
            log_message_backend("Benutzer hat gewählt: Beenden", level="INFO")
            print(f"{Fore.CYAN}Beenden.")
            break
        else:
            log_message_backend("Ungültige Option gewählt", level="WARNING")
            print(f"{Fore.RED}Ungültige Option. Bitte wähle erneut.")

if __name__ == "__main__":
    main()