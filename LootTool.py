import re
import os
import json
import time
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

ROOT_DIR = os.getcwd()
LOG_DIR = os.path.join(ROOT_DIR, "logs")
DB_DIR = os.path.join(ROOT_DIR, "DB")
CONFIG_DIR = os.path.join(ROOT_DIR, "Config")

# Ensure directories exist
for directory in [LOG_DIR, CONFIG_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Logging function with added details
def log_message_backend(message, level="INFO", extra_info=None):
    log_file_path = os.path.join(LOG_DIR, "backend_log.txt")
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    extra_details = f" | Details: {extra_info}" if extra_info else ""
    log_entry = f"[{level}] {timestamp} - {message}{extra_details}\n"
    
    try:
        with open(log_file_path, "a") as log_file:
            log_file.write(log_entry)
                
        if level == "ERROR":
            print(f"{Fore.RED}{log_entry.strip()}")
        elif level == "WARNING":
            print(f"{Fore.YELLOW}{log_entry.strip()}")
        else:
            print(f"{Fore.GREEN}{log_entry.strip()}")
                
    except Exception as e:
        print(f"{Fore.RED}Logging error: {str(e)}")

# Remove comments
def remove_comments(content):
    return re.sub(r'//.*', '', content)

# Function to extract and tag loot data, focusing on individual "use" entries
def extract_loot_data_with_tags(file_path):
    log_message_backend(f"Reading file {file_path}", level="INFO")
    if not os.path.exists(file_path):
        log_message_backend(f"File {file_path} not found.", level="ERROR")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        log_message_backend(f"File successfully read, size: {len(content)} characters", level="INFO")
    except Exception as e:
        log_message_backend(f"Error reading file: {str(e)}", level="ERROR")
        return []

    if not content.strip():
        log_message_backend(f"File {file_path} is empty.", level="ERROR")
        return []

    try:
        # Remove comments before parsing
        content = remove_comments(content)

        # Regex to extract LootedObjects and their "use" blocks
        loot_pattern = r'LootedObject\("(.+?)"\)\s*\{(.*?)\}'
        # Regex for use entries with weight, min_amount, and max_amount
        use_pattern_full = r'use\s+(.+?)\s*\(weight\s*=\s*([0-9.]+),\s*min_amount\s*=\s*(\d+),\s*max_amount\s*=\s*(\d+)\)'
        # Regex for simple use entries with only weight
        use_pattern_simple = r'use\s+(.+?)\s*\(weight\s*=\s*([0-9.]+)\)'

        loot_groups = re.findall(loot_pattern, content, re.DOTALL)
        loot_data = []

        # Auto-tagging based on use items (specific to item types, e.g., "WeaponMod")
        def assign_tag(item):
            if "WeaponMod" in item:
                return "weapon_mod"
            elif "Dismantle" in item:
                return "crafting"
            elif "Empty" in item:
                return "neutral"
            elif "Unique" in item or "Legendary" in item:
                return "high_value"
            else:
                return "default"

        for loot_name, loot_content in loot_groups:
            uses_full = re.findall(use_pattern_full, loot_content)
            uses_simple = re.findall(use_pattern_simple, loot_content)

            use_entries = []
            for item, weight, min_amount, max_amount in uses_full:
                use_entries.append({
                    "item": item.strip(),
                    "weight": float(weight),
                    "min_amount": int(min_amount),
                    "max_amount": int(max_amount),
                    "tag": assign_tag(item)  # Tag assigned based on the item name
                })
            for item, weight in uses_simple:
                use_entries.append({
                    "item": item.strip(),
                    "weight": float(weight),
                    "min_amount": None,
                    "max_amount": None,
                    "tag": assign_tag(item)  # Tag assigned based on the item name
                })

            # Check if the LootedObject and its content are properly closed, otherwise flag for review
            if "}" not in loot_content or len(loot_content.strip()) < 5:
                log_message_backend(f"Incomplete or malformed LootedObject detected: {loot_name}. Review required.", level="WARNING")

            loot_data.append({
                "LootedObject": loot_name,
                "use": use_entries
            })

        log_message_backend(f"Extracted {len(loot_data)} loot groups", level="INFO")
        if loot_data:
            log_message_backend(f"First loot group: {loot_data[0]}", level="DEBUG")
        return loot_data
    except Exception as e:
        log_message_backend(f"Error extracting loot groups: {str(e)}", level="ERROR")
        return []

# Function to initialize config file (only if it doesn't exist)
def initialize_config(loot_data, config_file_path):
    if os.path.exists(config_file_path):
        log_message_backend(f"Config file '{config_file_path}' already exists. No creation needed.", level="INFO")
        return

    if not loot_data:
        log_message_backend("No loot data available. Config file will not be created.", level="ERROR")
        print("No loot data available.")
        return

    try:
        with open(config_file_path, 'w', encoding='utf-8') as file:
            json.dump(loot_data, file, indent=4)
        log_message_backend(f"Config file '{config_file_path}' created.", level="INFO")
        print(f"Config file successfully created: {config_file_path}")
    except Exception as e:
        log_message_backend(f"Error creating config file: {str(e)}", level="ERROR")
        print(f"Error creating config file: {str(e)}")

# Main program
def main():
    print(f"{Style.BRIGHT}{Fore.CYAN}Starting Loot Modifier Tool...\n")

    default_loot_file = os.path.join(DB_DIR, 'default.loot')
    config_file_path = os.path.join(CONFIG_DIR, "loot_config.json")

    log_message_backend("Starting loot data extraction", level="INFO")
    loot_groups = extract_loot_data_with_tags(default_loot_file)
    
    if not loot_groups:
        log_message_backend("No loot data extracted. Exiting.", level="ERROR")
        return
    
    log_message_backend("Initializing config file", level="INFO")
    initialize_config(loot_groups, config_file_path)

if __name__ == "__main__":
    main()