import time
import collections
from ..resource_types import PUCKS

class Puck(object):
    def __init__(self, data, api):
        self.api = api
        self.puck_id = data.id_
        self.puck_name = data.attributes['name']
        self.light_level_available = False
        self.refresh()

    def refresh(self):
        puck_state = self.api.refresh_attributes(PUCKS, self.puck_id)
        puck_light_level = self.api.puck_light_level(self.puck_id)
        self.current_temp = puck_state.attributes['current-temperature-c']
        self.rssi = puck_state.attributes['current-rssi']
        self.current_humidity = puck_state.attributes['current-humidity']
        self.is_gateway = puck_state.attributes['is-gateway']
        self.voltage = puck_state.attributes['voltage']
        self.is_active = puck_state.attributes['inactive'] == False
        try:
            self.light_level = puck_light_level['light']
        except TypeError as error:
            self.light_level_available = False
            print(f"Flair Servers returned empty light level value: {error}")
        else:
            self.light_level_available = True





#{'ignore-readings-for-room': False, 'ir-setup-enabled': None, 'setpoint-bound-high': 32.23, 'inactive': False, 'created-at': '2019-12-03T01:55:37.783018+00:00', 'current-temperature-c': 21.18, 'ir-download': False, 'humidity-offset': None, 'puck-display-color': 'white', 'name': 'Bedroom-Puck', 'demo-mode': 0, 'oauth-app-assigned-at': None, 'setpoint-bound-low': 10.0, 'orientation': 'standing', 'features': None, 'current-humidity': 53.0, 'locked': False, 'temperature-offset-c': -4.43, 'last-#reported-as-gateway': True, 'bluetooth-tx-power-mw': 500, 'beacon-interval-ms': 4095, 'reporting-interval-ds': 255, 'temperature-offset-override-c': -4.43, 'display-number': 'c530', 'voltage': 3.41, 'updated-at': '2021-04-20T04:06:36.203095+00:00', 'sub-ghz-radio-tx-power-mw': None, 'is-gateway': True, 'current-rssi': -62.0}
