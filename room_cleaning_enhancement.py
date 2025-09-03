"""
Room-Specific Cleaning Enhancement for Roborock Integration

This adds the missing room selection and cleaning functionality that allows users
to clean specific rooms by name or ID.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from roborock.containers import (
    RoborockErrorCode,
    RoborockStateCode,
)
from roborock.roborock_message import RoborockDataProtocol
from roborock.roborock_typing import DeviceProp, RoborockCommand

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

# This would be added to select.py

class RoborockRoomSelectEntity(RoborockCoordinatedEntityV1, SelectEntity):
    """A class to let you select a room for targeted cleaning on Roborock vacuum."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_translation_key = "room_selection"
    _attr_icon = "mdi:home-map-marker"

    def __init__(
        self,
        coordinator: RoborockDataUpdateCoordinator,
    ) -> None:
        """Create a room selection entity."""
        super().__init__(
            f"room_selection_{coordinator.duid_slug}",
            coordinator,
            None,
        )
        self._selected_room_id: int | None = None

    async def async_select_option(self, option: str) -> None:
        """Set the selected room (doesn't start cleaning yet)."""
        if (
            self.coordinator.current_map is not None
            and self.coordinator.current_map in self.coordinator.maps
        ):
            # Find room ID by name 
            room_map = self.coordinator.maps[self.coordinator.current_map].rooms
            for room_id, room_name in room_map.items():
                if room_name == option:
                    self._selected_room_id = room_id
                    break

    @property
    def options(self) -> list[str]:
        """Get all available room names for the current map."""
        if (
            self.coordinator.current_map is not None
            and self.coordinator.current_map in self.coordinator.maps
        ):
            return list(
                self.coordinator.maps[self.coordinator.current_map].rooms.values()
            )
        return []

    @property
    def current_option(self) -> str | None:
        """Get the currently selected room name."""
        if (
            self._selected_room_id is not None
            and self.coordinator.current_map is not None
            and self.coordinator.current_map in self.coordinator.maps
        ):
            room_map = self.coordinator.maps[self.coordinator.current_map].rooms
            return room_map.get(self._selected_room_id)
        return None

    @property
    def selected_room_id(self) -> int | None:
        """Get the currently selected room ID for other entities to use."""
        return self._selected_room_id


# This would be added to button.py

class RoborockCleanRoomButtonEntity(RoborockEntity, ButtonEntity):
    """A button to clean the selected room."""

    _attr_translation_key = "clean_selected_room"
    _attr_icon = "mdi:robot-vacuum"

    def __init__(
        self,
        coordinator: RoborockDataUpdateCoordinator,
        room_selector: RoborockRoomSelectEntity,
    ) -> None:
        """Create a clean room button entity."""
        super().__init__(
            f"clean_selected_room_{coordinator.duid_slug}",
            coordinator.device_info,
            coordinator.api,
        )
        self._coordinator = coordinator
        self._room_selector = room_selector

    async def async_press(self, **kwargs: Any) -> None:
        """Start cleaning the selected room."""
        if self._room_selector.selected_room_id is not None:
            # Use APP_SEGMENT_CLEAN command with room ID
            await self.send(
                RoborockCommand.APP_SEGMENT_CLEAN,
                [self._room_selector.selected_room_id]
            )
        else:
            raise HomeAssistantError("No room selected for cleaning")

    @property
    def available(self) -> bool:
        """Return if the button is available (room selected and vacuum ready)."""
        return (
            self._room_selector.selected_room_id is not None
            and self._coordinator.data.status.state in [
                RoborockStateCode.idle,
                RoborockStateCode.charging,
                RoborockStateCode.charging_complete,
            ]
        )


# Additional sensors for enhanced room information

@dataclass(frozen=True, kw_only=True)
class RoborockRoomSensorDescription(SensorEntityDescription):
    """Enhanced room sensor description."""
    
    value_fn: Callable[[DeviceProp, dict], str | int | None]


ROOM_SENSOR_DESCRIPTIONS = [
    RoborockRoomSensorDescription(
        key="total_rooms",
        translation_key="total_rooms",
        value_fn=lambda data, rooms: len(rooms) if rooms else 0,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:home-map-marker",
    ),
    RoborockRoomSensorDescription(
        key="room_cleaning_order",
        translation_key="room_cleaning_order",
        value_fn=lambda data, rooms: ", ".join(rooms.values()) if rooms else None,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:format-list-numbered",
    ),
]


class RoborockRoomInfoSensor(RoborockCoordinatedEntityV1, SensorEntity):
    """Sensor for room-related information."""

    entity_description: RoborockRoomSensorDescription

    def __init__(
        self,
        coordinator: RoborockDataUpdateCoordinator,
        description: RoborockRoomSensorDescription,
    ) -> None:
        """Initialize the room info sensor."""
        self.entity_description = description
        super().__init__(
            f"{description.key}_{coordinator.duid_slug}",
            coordinator,
            None,
        )

    @property
    def native_value(self) -> str | int | None:
        """Return the sensor value."""
        if (
            self.coordinator.current_map is not None
            and self.coordinator.current_map in self.coordinator.maps
        ):
            rooms = self.coordinator.maps[self.coordinator.current_map].rooms
            return self.entity_description.value_fn(self.coordinator.data, rooms)
        return None


# Service for advanced room operations
async def async_clean_rooms_service(
    hass: HomeAssistant, 
    call: ServiceCall
) -> None:
    """Service to clean multiple rooms at once."""
    entity_id = call.data["entity_id"]
    room_names = call.data["rooms"]
    
    # Implementation would resolve room names to IDs and call APP_SEGMENT_CLEAN
    # with multiple room IDs: [room_id1, room_id2, room_id3]