# Roborock HACS Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

A Home Assistant Custom Component for Roborock vacuum cleaners, extracted from Home Assistant Core with the latest updates.

## Description

This integration provides comprehensive support for Roborock vacuum cleaners in Home Assistant, including:

- Vacuum control (start, stop, pause, return to dock)
- Real-time status monitoring
- Map visualization and room-specific cleaning
- Sensor data (battery, cleaning time, area cleaned, etc.)
- Switch controls for various features
- Scheduling and timer controls
- Support for multiple Roborock device models

## Features

- **Latest Updates**: Includes support for new device models (B01, A01, QRevo, Zeo)
- **Dynamic Clean Modes**: Automatically detects and supports device-specific cleaning modes
- **Enhanced API Coverage**: Full API feature support with improved error handling
- **Improved MQTT Handling**: Better communication with Roborock cloud services
- **Map Support**: Visual map display with room-specific cleaning capabilities

## Installation

### HACS Installation (Recommended)

1. Ensure you have [HACS](https://hacs.xyz/) installed
2. Add this repository as a custom repository in HACS:
   - Go to HACS → Integrations
   - Click the three dots in the top right corner
   - Select "Custom repositories"
   - Add this repository URL and select "Integration" as the category
3. Install the integration through HACS
4. Restart Home Assistant
5. Add the integration through the UI (Configuration → Integrations → Add Integration → Roborock)

### Manual Installation

1. Download the latest release from this repository
2. Extract the contents to your `custom_components` directory
3. Restart Home Assistant
4. Add the integration through the UI

## Configuration

The integration supports automatic discovery of Roborock devices on your network. You can also configure devices manually using their IP addresses.

## Supported Devices

This integration supports all Roborock vacuum models that are compatible with the python-roborock library, including:

- S Series (S4, S5, S6, S7, etc.)
- Q Series (Q5, Q7, QRevo)
- Other models (check python-roborock compatibility)

## Dependencies

- `python-roborock==2.39.0`
- `vacuum-map-parser-roborock==0.1.4`

## Credits

This integration is based on the official Home Assistant Roborock integration from the Home Assistant Core repository, with additional enhancements and updates.

## License

This project follows the same license as Home Assistant Core (Apache License 2.0).