import frappe
import os
import csv
from frappe.translate import get_messages_for_app

def find_missing_arabic_translations(app_name="erpnext"):
    """
    Finds strings in the specified app that do not have a translation in the app's ar.csv
    or in the core frappe translations.
    """
    messages = get_messages_for_app(app_name)
    existing_translations = get_existing_translations("ar")
    
    missing = []
    for msg in messages:
        source_text = msg[1]
        if source_text not in existing_translations:
            missing.append(source_text)
            
    return missing

def get_existing_translations(lang):
    """
    Combines translations from all installed apps for the given language.
    """
    translations = {}
    for app in frappe.get_all_apps():
        path = frappe.get_app_path(app, "translations", lang + ".csv")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        translations[row[0]] = row[1]
    return translations

def export_missing_to_csv(missing_list, output_path):
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for msg in missing_list:
            writer.writerow([msg, ""])

if __name__ == "__main__":
    # This would be run via: bench execute arabic_pro.utils.translate_utils.run_discovery
    pass

def run_discovery():
    print("Searching for missing Arabic translations in ERPNext...")
    missing = find_missing_arabic_translations("erpnext")
    output = frappe.get_app_path("arabic_pro", "translations", "missing_ar.csv")
    export_missing_to_csv(missing, output)
    print(f"Found {len(missing)} missing strings. Exported to {output}")
