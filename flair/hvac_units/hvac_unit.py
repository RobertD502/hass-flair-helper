class HvacUnit(object):
    def __init__(self, data, api):
        self.api = api
        self.hvac_id = data.id_
        self.hvac_name = data.attributes['name']
        self.refresh()

    def turn_on(self):
        self.api.control_hvac(self.hvac_id, "On")

    def turn_off(self):
        self.api.control_hvac(self.hvac_id, "Off")

    def refresh(self):
        hvac_state = self.api.refresh_attributes('hvac-units', self.hvac_id)
        self.is_powered_on = (hvac_state.attributes['power'] == "On")

