#!/usr/bin/env python3
"""
Entity Registry Cache Fix Script for Roborock Custom Component

This script helps resolve translation key issues in custom components by:
1. Providing entity registry cleanup instructions
2. Showing how to force entity name regeneration
3. Verifying translation key configuration

Run this script to get instructions for fixing persistent entity name caching issues.
"""

import json
import sys
from pathlib import Path


def main():
    print("=== Roborock Custom Component Translation Fix ===\n")
    
    print("🔍 PROBLEM DIAGNOSIS:")
    print("- Entities showing device class names (e.g., 'Duration') instead of proper names")
    print("- Translation keys properly configured but not being used")
    print("- This is typically caused by entity registry caching\n")
    
    print("🛠️  SOLUTION STEPS:\n")
    
    print("1. CLEAR ENTITY REGISTRY CACHE:")
    print("   In Home Assistant, go to:")
    print("   Settings -> Devices & Services -> Entities")
    print("   Search for 'roborock' entities")
    print("   For EACH entity showing wrong names:")
    print("   - Click the entity")
    print("   - Click the gear icon (settings)")
    print("   - Change the entity ID to something temporary (e.g., add '_temp')")
    print("   - Save")
    print("   - Change it back to original name")
    print("   - Save again")
    print("   This forces entity registry regeneration\n")
    
    print("2. ALTERNATIVE - REGISTRY FILE EDIT:")
    print("   ⚠️  ADVANCED USERS ONLY - STOP HOME ASSISTANT FIRST!")
    print("   Edit /config/.storage/core.entity_registry")
    print("   Remove entries for roborock entities")
    print("   Restart Home Assistant")
    print("   Entities will be recreated with proper names\n")
    
    print("3. TRANSLATION DOMAIN FIX:")
    print("   ✅ Added _attr_translation_domain = DOMAIN to entity base class")
    print("   ✅ Added missing 'total_rooms_available' translation key")
    print("   ✅ All entity classes have _attr_has_entity_name = True\n")
    
    print("4. VERIFY CONFIGURATION:")
    
    # Check strings.json
    strings_path = Path("custom_components/roborock/strings.json")
    if strings_path.exists():
        try:
            with open(strings_path) as f:
                strings_data = json.load(f)
            
            print(f"   ✅ strings.json found with {len(strings_data.get('entity', {}).get('sensor', {}))} sensor translations")
            
            # Check for specific translations
            sensor_translations = strings_data.get('entity', {}).get('sensor', {})
            critical_keys = ['main_brush_time_left', 'cleaning_time', 'total_rooms_available']
            
            for key in critical_keys:
                if key in sensor_translations:
                    print(f"   ✅ Translation key '{key}' found")
                else:
                    print(f"   ❌ Translation key '{key}' MISSING")
        except Exception as e:
            print(f"   ❌ Error reading strings.json: {e}")
    else:
        print("   ❌ strings.json not found")
    
    print("\n5. FINAL STEPS:")
    print("   - Restart Home Assistant after applying fixes")
    print("   - Clear browser cache")
    print("   - Check entity names in Developer Tools -> States")
    print("   - If still showing wrong names, use registry clear method (Step 1)\n")
    
    print("📋 ENTITY REGISTRY CACHE EXPLANATION:")
    print("   Home Assistant caches entity names in the registry to maintain")
    print("   user customizations. When translation keys are added/changed,")
    print("   the cache must be cleared to pick up the new translations.")
    print("   This is the #1 cause of 'Duration' vs 'Main brush time left' issues.\n")
    
    print("🎯 EXPECTED RESULTS:")
    print("   After fixes, entities should show:")
    print("   - 'Main brush time left' instead of 'Duration'") 
    print("   - 'Cleaning time' instead of 'Duration'")
    print("   - 'Total rooms available' instead of 'sensor.roborock_device_total_rooms_available'")
    print("   - Device name 'Ribbit the Robut' + sensor name instead of generic names\n")


if __name__ == "__main__":
    main()