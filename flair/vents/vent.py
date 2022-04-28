import time
import collections
from ..resource_types import VENTS

class Vent(object):
    def __init__(self, data, api):
        self.api = api
        self.vent_id = data.id_
        self.vent_name = data.attributes['name']
        self.refresh()

    def refresh(self):
        vent_state = self.api.refresh_attributes(VENTS, self.vent_id)
        self.voltage = vent_state.attributes['voltage']
        self.is_vent_open = vent_state.attributes['percent-open'] == 100 or vent_state.attributes['percent-open'] == 50
        self.vent_percent = vent_state.attributes['percent-open']
        self.is_active = vent_state.attributes['inactive'] == False
        self.rssi = vent_state.attributes['current-rssi']
        try:
            vent_current_reading = self.api.vent_current_reading(self.vent_id)
            self.duct_temp = vent_current_reading['duct-temperature-c']
            self.duct_pressure = vent_current_reading['duct-pressure']
        except:
            return None

    def set_vent_percentage(self, percent):
        attributes = {
        'percent-open': percent,
        }
        relationships = {}
        self.api.control_vent(self, VENTS, attributes, relationships)
        self.refresh()

#Vent available attributes
#Office-Right
#{'setup-lightstrip': 1, 'created-at': '2019-12-03T02:02:40.847808+00:00', 'voltage': 3.06, 'inactive': False, 'percent-open-reason': 'This room does not require heating. Vent will open when the room is below 67.0F.', 'updated-at': '2021-04-20T04:09:55.122649+00:00', 'percent-open': 0, 'name': 'Office-Right', 'has-buzzed': False, 'current-rssi': -87.0}
