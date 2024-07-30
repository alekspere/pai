from paradox.config import config as cfg
from paradox.interfaces.mqtt.entities.abstract_entity import AbstractEntity
from paradox.lib.utils import sanitize_key


class AbstractStatusBinarySensor(AbstractEntity):
    def __init__(self, entity, property: str, device, availability_topic: str):
        super().__init__(device, availability_topic)

        self.label = entity.get("label", entity["key"].replace("_", " "))
        self.property = property

        self.key = sanitize_key(entity["key"])

        self.hass_entity_type = "binary_sensor"

    def serialize(self):
        config = super().serialize()
        config.update(dict(
            payload_on="True",
            payload_off="False",
        ))
        return config


class PartitionBinarySensor(AbstractStatusBinarySensor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pai_entity_type = "partition"


class ZoneStatusBinarySensor(AbstractStatusBinarySensor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pai_entity_type = "zone"
        self.hass_entity_class = cfg.HOMEASSISTANT_ZONE_CLASSES.get(self.label)

    def serialize(self):
        config = super().serialize()

        if self.property == 'open':
            if self.hass_entity_class:
                config['device_class'] = self.hass_entity_class
            else:
                config['device_class'] = 'motion'
        elif self.property == 'tamper':
            config['device_class'] = 'tamper'
        elif self.property == 'fire':
            config['device_class'] = 'smoke'
        elif self.property == 'rf_supervision_trouble':
            config['device_class'] = 'problem'
        elif self.property == 'rf_low_battery_trouble':
            config['device_class'] = 'battery'

        return config


class SystemBinarySensor(AbstractStatusBinarySensor):
    def __init__(self, key: str, property: str, device, availability_topic: str):
        super().__init__({"key": key}, property, device, availability_topic)

        self.pai_entity_type = "system"
