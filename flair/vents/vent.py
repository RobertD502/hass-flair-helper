import time
import collections


class Vent(object):
    def __init__(self, data, api):
        self.api = api
        self.vent_id = data.id_
        self.vent_name = data.attributes['name']
        self.refresh()

    def refresh(self):
        vent_state = self.api.refresh_attributes('vents', self.vent_id)
        self.voltage = vent_state.attributes['voltage']
        self.is_vent_open = vent_state.attributes['percent-open'] == 100 or vent_state.attributes['percent-open'] == 50
        self.vent_percent = vent_state.attributes['percent-open']
        self.is_active = vent_state.attributes['inactive'] == False
        self.rssi = vent_state.attributes['current-rssi']

    def set_vent(self, open):
        self.is_vent_open = open
        self.resource_type = 'vents'
        self.attributes = {
        'percent-open': 100 if open else 0,
        }
        self.relationships = {}
        self.api.control(self, self.resource_type, self.vent_id, self.relationships)
        self.refresh()

    def set_vent_half(self):
        self.resource_type = 'vents'
        self.attributes = {
        'percent-open': 50,
        }
        self.relationships = {}
        self.api.control(self, self.resource_type, self.vent_id, self.relationships)
        self.refresh()

#Office-Right
#{'setup-lightstrip': 1, 'created-at': '2019-12-03T02:02:40.847808+00:00', 'voltage': 3.06, 'inactive': False, 'percent-open-reason': 'This room does not require heating. Vent will open when the room is below 67.0F.', 'updated-at': '2021-04-20T04:09:55.122649+00:00', 'percent-open': 0, 'name': 'Office-Right', 'has-buzzed': False, 'current-rssi': -87.0}
