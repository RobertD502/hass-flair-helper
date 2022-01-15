import time
import collections
from ..resource_types import ROOMS, STRUCTURES

class Room(object):
    def __init__(self, data, api):
        self.api = api
        self.room_id = data.id_
        self.room_name = data.attributes['name']
        self.refresh()

    def refresh(self):
        room_state = self.api.refresh_attributes(ROOMS, self.room_id)
        self.temp_set_point = room_state.attributes['set-point-c']
        self.current_temp = room_state.attributes['current-temperature-c']
        self.current_humidity = room_state.attributes['current-humidity']
        self.is_active = room_state.attributes['active'] == True
        self.related_structure_id = room_state.relationships['structure'].data['id']
        room_related = self.api.structure_related_to_room(STRUCTURES, self.related_structure_id)
        self.current_hvac_mode = room_related.attributes['structure-heat-cool-mode']
        self.hold_duration = room_related.attributes['default-hold-duration']


    def set_temperature(self, temp):
        attributes = {
        'set-point-c': temp,
        'active': True
        }
        relationships = {}
        self.api.control_room(self, ROOMS, attributes, relationships)
        self.refresh()

    def set_activity(self, active_inactive):
        attributes = {
        'active': active_inactive
        }
        relationships = {}
        self.api.control_room(self, ROOMS, attributes, relationships)
        self.refresh()

        #Room attributes
#{'active': True, 'level': None, 'temp-away-max-c': 22.5, 'current-humidity': None, 'temp-away-min-c': 16.0, 'updated-at': '2021-04-20T03:49:16.417735+00:00', 'humidity-away-min': 10, 'room-type': None, 'frozen-pipe-pet-protect': True, 'created-at': '2019-12-03T02:04:43.105745+00:00', 'occupancy-mode': 'Flair Auto', 'current-temperature-c': 22.7778777777778, 'hold-until-schedule-event': False, 'pucks-inactive': 'Active', 'name': 'Guest Room', 'windows': None, 'set-point-c': 20.0, 'air-return': #False, 'preheat-precool': True, 'humidity-away-max': 80, 'hold-until': None, 'state-updated-at': '2021-04-20T03:33:52.004948+00:00', 'set-point-manual': False, 'room-away-mode': 'Smart Away', 'hold-reason': 'Set by Robert'}


#Structure attributes
#{'temp-away-max-c': 25.0, 'time-zone': 'America/New_York', 'temp-away-min-c': 18.88, 'structure-away-mode': 'Smart Away', 'updated-at': '2021-04-21T21:23:25.640687+00:00', 'set-point-mode': 'Home Evenness For Active Rooms Follow Third Party', 'setup-mode-first-time': True, 'dr-start-time': None, 'is-active': False, 'setup-mode': False, 'hold-until-schedule-event': False, 'dr-end-time': None, 'hold-reason': 'thermostat', 'puck-client-secret': '', 'structure-heat-cool-mode': 'heat', 'structure-#heat-cool-mode-popup-resolved-at': None, 'puck-client-id': '', 'hvac-unit-group-lock': False, 'zip-code': None, 'country': 'US', 'reporting-gateway': True, 'hysteresis-a': 50, 'current-dr-state': None, 'setup-complete': True, 'structure-heat-cool-mode-calculated': None, 'set-point-temperature-c': 22.22, 'hysteresis-b': 100, 'location-type': None, 'longitude': None, 'home': True, 'location': None, 'setup-step': 'structure/config', 'humidity-away-max': 80, 'hold-until': None, 'latitude': None, #'default-hold-duration': 'Until', 'release-channel': 'production', 'structure-type': None, 'temperature-scale': 'F', 'use-remote-sensor-occupancy': None, 'active-schedule-id': None, 'city': None, 'humidity-away-min': 10, 'mode': 'auto', 'hysteresis-heat-cool-mode': 111, 'frozen-pipe-pet-protect': True, 'created-at': '2019-12-#03T01:59:34.190576+00:00', 'dr-event-string': None, 'state': None, 'name': '', 'licensed-features': [], 'home-away-mode': 'Third Party Home Away', 'preheat-precool': #True, 'state-updated-at': '2021-04-21T20:34:57.024260+00:00'}
