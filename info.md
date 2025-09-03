# Roborock Integration

## What's New in This Version

This HACS version includes the latest updates from Home Assistant Core:

### Version 1.0.0
- ✅ **Updated Dependencies**: python-roborock upgraded to 2.39.0
- ✅ **New Device Support**: Added support for B01, A01, QRevo, and Zeo models  
- ✅ **Dynamic Clean Modes**: Automatic detection of device-specific cleaning modes
- ✅ **Enhanced API Coverage**: Expanded API functionality with better error handling
- ✅ **Improved MQTT Handling**: Better communication reliability with Roborock services
- ✅ **Map Initialization**: Enhanced map handling during device setup
- ✅ **Better Error Handling**: Improved stability and error recovery

## Installation

1. Install via HACS (Home Assistant Community Store)
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration
4. Search for "Roborock" and follow the setup wizard

## Configuration

The integration will automatically discover Roborock devices on your network. You can also manually add devices using their IP addresses if needed.

## Support

This integration is based on the official Home Assistant Core integration with the latest updates and improvements. For issues, please report them on the GitHub repository.

## Dependencies

- Home Assistant 2024.1.0 or newer
- python-roborock 2.39.0
- vacuum-map-parser-roborock 0.1.4