class HvacUnit(object):
    def __init__(self, data, api):
        self.api = api
        self.hvac_id = data.id_
        self.hvac_model = data.attributes['make-name']
        self.hvac_name = data.attributes['name']
        self.refresh()

    def refresh(self):
        hvac_state = self.api.refresh_attributes('hvac-units', self.hvac_id)
        puck_state = self.api.refresh_attributes('pucks', hvac_state.relationships['puck'].data['id'])
        self.puck_is_active = puck_state.attributes['inactive'] == False
        self.puck_temp = puck_state.attributes['current-temperature-c']
        self.puck_humidity = puck_state.attributes['current-humidity']
        self.is_powered_on = (hvac_state.attributes['power'] == "On")
        self.hvac_mode = hvac_state.attributes['mode']
        self.hvac_temp = hvac_state.attributes['temperature']
        self.hvac_temp_scale = hvac_state.attributes['constraints']['temperature-scale']
        self.hvac_fan_speed = hvac_state.attributes['fan-speed']

        ### Check to See if HVAC Unit Supports Setting Swing On and Off ###
        if ('swing' in hvac_state.attributes and hvac_state.attributes['swing'] is not None):
            self.swing_state = hvac_state.attributes['swing']
            self.swing_available = True
        else:
            self.swing_available = False

        ### Capabilities = Both, Heat, or Cool ###
        self.hvac_capabilities = hvac_state.attributes['capabilities']

        ### Create list of supported HVAC modes ###
        self.hvac_modes = []
        for key in hvac_state.attributes['constraints']['ON'].keys():
            self.hvac_modes.append(key)

        ### Create list of supported fan speeds ###
        self.hvac_fan_speeds = []
        if self.hvac_mode == "Heat":
            for key in hvac_state.attributes['constraints']['ON']['HEAT']['ON'].keys():
                self.hvac_fan_speeds.append(key)
        if self.hvac_mode == "Cool":
            for key in hvac_state.attributes['constraints']['ON']['COOL']['ON'].keys():
                self.hvac_fan_speeds.append(key)
        if self.hvac_mode == "Fan":
            for key in hvac_state.attributes['constraints']['ON']['FAN']['ON'].keys():
                self.hvac_fan_speeds.append(key)
        if self.hvac_mode == "Dry":
            for key in hvac_state.attributes['constraints']['ON']['DRY']['ON'].keys():
                self.hvac_fan_speeds.append(key)
        if self.hvac_mode == "Auto":
            for key in hvac_state.attributes['constraints']['ON']['AUTO']['ON'].keys():
                self.hvac_fan_speeds.append(key)

        ### Create list of supported HVAC temps in different modes ###
        if self.hvac_capabilities == "Both":
            self.supported_heat_temps = next(iter(hvac_state.attributes['constraints']['ON']['HEAT']['ON'].values()))
            self.supported_cool_temps = next(iter(hvac_state.attributes['constraints']['ON']['COOL']['OFF'].values()))
        elif self.hvac_capabilities == "Heat":
            self.supported_heat_temps = next(iter(hvac_state.attributes['constraints']['ON']['HEAT']['ON'].values()))
        else:
            self.supported_cool_temps = next(iter(hvac_state.attributes['constraints']['ON']['COOL']['OFF'].values()))

    ### Power can be either On or Off ###
    def set_hvac_power(self, power):
        resource_type = 'hvac-units'
        attributes = {
        "power": power,
        }
        relationships = {}
        self.api.control_hvac(self, resource_type, attributes, relationships)
        self.refresh()

    ### Mode can be Dry, Heat, Cool, Fan, or Auto depending on unit's capabilities ###
    def set_hvac_mode(self, mode):
        resource_type = 'hvac-units'
        attributes = {
        "mode": mode,
        }
        relationships = {}
        self.api.control_hvac(self, resource_type, attributes, relationships)
        self.refresh()

    ### Swing can be On or Off if unit supports swing feature ###
    def set_hvac_swing(self, swing):
        resource_type = 'hvac-units'
        attributes = {
        "swing": swing,
        }
        relationships = {}
        self.api.control_hvac(self, resource_type, attributes, relationships)
        self.refresh()

    ### Fan speed can be High, Medium, Low, or Auto depending on unit's capabilities ###
    def set_hvac_fan_speed(self, speed):
        resource_type = 'hvac-units'
        attributes = {
        "fan-speed": speed,
        }
        relationships = {}
        self.api.control_hvac(self, resource_type, attributes, relationships)
        self.refresh()

    ### Temperature sent should fall in the range seen in self.supported_heat_temps if in heat mode and
    ### in the range seen in self.supported_cool_temps if in cool mode
    def set_hvac_temp(self, temp):
        resource_type = 'hvac-units'
        attributes = {
        "temperature": temp,
        }
        relationships = {}
        self.api.control_hvac(self, resource_type, attributes, relationships)
        self.refresh()
