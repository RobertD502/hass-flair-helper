import time
import collections

class Room(object):
    def __init__(self, data, api):
        self.api = api
        self.room_id = data.id_
        self.room_name = data.attributes['name']
        self.refresh()

    def refresh(self):
        room_state = self.api.refresh_attributes('rooms', self.room_id)
        self.temp_set_point = room_state.attributes['set-point-c']
        self.current_temp = room_state.attributes['current-temperature-c']
        self.current_humidity = room_state.attributes['current-humidity']
        self.is_active = room_state.attributes['active'] == True



    def set_temperature(self, temp):
        self.temp = temp
        self.resource_type = 'rooms'
        self.attributes = {
        'set-point-c': temp,
        'active': True
        }
        self.relationships = {}
        self.api.control(self, self.resource_type, self.room_id, self.relationships)
        self.refresh()

#{'active': True, 'level': None, 'temp-away-max-c': 22.5, 'current-humidity': None, 'temp-away-min-c': 16.0, 'updated-at': '2021-04-20T03:49:16.417735+00:00', 'humidity-away-min': 10, 'room-type': None, 'frozen-pipe-pet-protect': True, 'created-at': '2019-12-03T02:04:43.105745+00:00', 'occupancy-mode': 'Flair Auto', 'current-temperature-c': 22.7778777777778, 'hold-until-schedule-event': False, 'pucks-inactive': 'Active', 'name': 'Guest Room', 'windows': None, 'set-point-c': 20.0, 'air-return': #False, 'preheat-precool': True, 'humidity-away-max': 80, 'hold-until': None, 'state-updated-at': '2021-04-20T03:33:52.004948+00:00', 'set-point-manual': False, 'room-away-mode': 'Smart Away', 'hold-reason': 'Set by Robert'}
