#!/usr/bin/env python3
"""
Entity Registry Cleanup Script for Roborock Custom Component

This script addresses the specific issue where Home Assistant stores device class names
like "Duration" as the original_name in the entity registry, which then overrides
translation keys from strings.json.

Usage:
1. Stop Home Assistant
2. Run this script: python3 entity_registry_cleanup.py
3. Start Home Assistant

The script will:
1. Remove problematic original_name entries for Roborock sensors
2. Preserve translation_key and has_entity_name settings
3. Force HA to use translation_key on next startup

WARNING: Always backup your entity registry before running this script!
"""

import json
import shutil
from pathlib import Path
import sys

# Path to Home Assistant entity registry
ENTITY_REGISTRY_PATH = "/config/.storage/core.entity_registry"
BACKUP_PATH = "/config/.storage/core.entity_registry.backup"

def backup_entity_registry():
    """Create a backup of the entity registry."""
    try:
        shutil.copy2(ENTITY_REGISTRY_PATH, BACKUP_PATH)
        print(f"✅ Backup created: {BACKUP_PATH}")
        return True
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")
        return False

def clean_roborock_entities():
    """Clean problematic original_name entries for Roborock entities."""
    try:
        # Load the entity registry
        with open(ENTITY_REGISTRY_PATH, 'r') as f:
            registry = json.load(f)
        
        entities = registry.get('data', {}).get('entities', [])
        cleaned_count = 0
        
        # Device class names that cause translation issues
        problematic_names = {
            'Duration', 'Battery', 'Timestamp', 'Enum', 
            'Area', 'Energy', 'Power', 'Volume'
        }
        
        for entity in entities:
            # Check if this is a Roborock entity with problematic original_name
            if (entity.get('platform') == 'roborock' and 
                entity.get('original_name') in problematic_names and
                entity.get('translation_key') and
                entity.get('has_entity_name') is True):
                
                print(f"🔧 Cleaning entity: {entity.get('entity_id')} - "
                      f"Removing original_name: '{entity.get('original_name')}'")
                
                # Remove the problematic original_name
                entity['original_name'] = None
                cleaned_count += 1
        
        if cleaned_count > 0:
            # Write the cleaned registry back
            with open(ENTITY_REGISTRY_PATH, 'w') as f:
                json.dump(registry, f, indent=2)
            
            print(f"✅ Successfully cleaned {cleaned_count} entities")
            print("🔄 Restart Home Assistant to see proper translated names")
        else:
            print("ℹ️  No problematic entities found - registry is already clean")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to clean entity registry: {e}")
        return False

def main():
    """Main execution function."""
    print("🚀 Roborock Entity Registry Cleanup")
    print("=" * 50)
    
    # Check if registry file exists
    if not Path(ENTITY_REGISTRY_PATH).exists():
        print(f"❌ Entity registry not found: {ENTITY_REGISTRY_PATH}")
        print("Make sure you're running this on your Home Assistant system")
        sys.exit(1)
    
    # Create backup
    if not backup_entity_registry():
        print("❌ Cannot proceed without backup")
        sys.exit(1)
    
    # Clean the registry
    if clean_roborock_entities():
        print("\n✅ Entity registry cleanup completed successfully!")
        print("\nNext steps:")
        print("1. Start Home Assistant")
        print("2. Check that your Roborock sensors now show proper translated names")
        print("3. If you need to restore, use: cp {BACKUP_PATH} {ENTITY_REGISTRY_PATH}")
    else:
        print("\n❌ Cleanup failed - restoring backup")
        try:
            shutil.copy2(BACKUP_PATH, ENTITY_REGISTRY_PATH)
            print("✅ Backup restored")
        except Exception as e:
            print(f"❌ Failed to restore backup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()