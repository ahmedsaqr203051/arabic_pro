import frappe
import os
import csv
from frappe.translate import get_messages_for_app

def find_missing_arabic_translations(app_name="erpnext"):
    """
    Finds strings in the specified app that do not have a translation in the environment.
    """
    # Get all messages from the target app
    messages = get_messages_for_app(app_name)
    
    # Get all existing Arabic translations in the system
    existing_translations = frappe.get_full_dict("ar")
    
    missing = []
    for msg in messages:
        source_text = msg[1]
        # msg[1] is the source text, msg[0] is the file path (context)
        if source_text not in existing_translations:
            missing.append(source_text)
            
    return sorted(list(set(missing)))

def export_missing_to_csv(missing_list, output_path):
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for msg in missing_list:
            # Frappe ar.csv format: "Source Text","Translated Text"
            writer.writerow([msg, ""])

def run_discovery(app_to_scan="erpnext"):
    print(f"Searching for missing Arabic translations in {app_to_scan}...")
    missing = find_missing_arabic_translations(app_to_scan)
    
    # Ensure translations directory exists
    output_dir = frappe.get_app_path("arabic_pro", "translations")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_file = os.path.join(output_dir, f"missing_{app_to_scan}_ar.csv")
    export_missing_to_csv(missing, output_file)
    print(f"Found {len(missing)} unique missing strings. Exported to {output_file}")

if __name__ == "__main__":
    # This utility is intended to be run via bench:
    # bench --site [site-name] execute arabic_pro.utils.translate_utils.run_discovery
    pass
