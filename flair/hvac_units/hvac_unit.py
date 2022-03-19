from ..resource_types import HVAC_UNITS, PUCKS, ROOMS, STRUCTURES

class HvacUnit(object):
    def __init__(self, data, api):
        self.api = api
        self.hvac_id = data.id_
        self.hvac_model = data.attributes['make-name']
        self.hvac_name = data.attributes['name']
        self.room_id = data.relationships['room'].data['id']
        self.refresh()

    def refresh(self):
        hvac_state = self.api.refresh_attributes(HVAC_UNITS, self.hvac_id)
        puck_state = self.api.refresh_attributes(PUCKS, hvac_state.relationships['puck'].data['id'])
        structure_state = self.api.refresh_attributes(STRUCTURES, hvac_state.relationships['structure'].data['id'])
        self.puck_is_active = puck_state.attributes['inactive'] == False
        self.puck_temp = puck_state.attributes['current-temperature-c']
        self.puck_humidity = puck_state.attributes['current-humidity']
        ### Check to see if the structure is in auto or manual mode
        self.system_mode = structure_state.attributes['mode']
        self.is_powered_on = (hvac_state.attributes['power'] == "On")
        self.hvac_mode = hvac_state.attributes['mode']
        self.hvac_temp = hvac_state.attributes['temperature']

        ### Capabilities = Both, Heat, or Cool ###
        self.hvac_capabilities = hvac_state.attributes['capabilities']

        ### Create list of supported HVAC temps in different modes ###
        if self.hvac_capabilities == "Both":
            if "ON" in hvac_state.attributes['constraints']['ON']['HEAT'].keys():
                self.supported_heat_temps = next(iter(hvac_state.attributes['constraints']['ON']['HEAT']['ON'].values()))
            if "ON" not in hvac_state.attributes['constraints']['ON']['HEAT'].keys():
                self.supported_heat_temps = next(iter(hvac_state.attributes['constraints']['ON']['HEAT']['OFF'].values()))
            if "ON" in hvac_state.attributes['constraints']['ON']['COOL'].keys():
                self.supported_cool_temps = next(iter(hvac_state.attributes['constraints']['ON']['COOL']['ON'].values()))
            if "ON" not in hvac_state.attributes['constraints']['ON']['COOL'].keys():
                self.supported_cool_temps = next(iter(hvac_state.attributes['constraints']['ON']['COOL']['OFF'].values()))
        elif self.hvac_capabilities == "Heat":
            if "ON" in hvac_state.attributes['constraints']['ON']['HEAT'].keys():
                self.supported_heat_temps = next(iter(hvac_state.attributes['constraints']['ON']['HEAT']['ON'].values()))
            else:
                self.supported_heat_temps = next(iter(hvac_state.attributes['constraints']['ON']['HEAT']['OFF'].values()))
        else:
            if "ON" in hvac_state.attributes['constraints']['ON']['COOL'].keys():
                self.supported_cool_temps = next(iter(hvac_state.attributes['constraints']['ON']['COOL']['ON'].values()))
            else:
                self.supported_cool_temps = next(iter(hvac_state.attributes['constraints']['ON']['COOL']['OFF'].values()))

        ### Check to see if HVAC constraints has temperature-scale key, if not then determine scale from temp range ###
        if "temperature-scale" in hvac_state.attributes['constraints']:
            self.hvac_temp_scale = hvac_state.attributes['constraints']['temperature-scale']
        else:
            if self.hvac_capabilities == "Both":
                self.lower_end_temp = int(self.supported_heat_temps[0])
                if self.lower_end_temp < 55:
                    self.hvac_temp_scale = "C"
                else:
                    self.hvac_temp_scale = "F"
            elif self.hvac_capabilities == "Heat":
                self.lower_end_temp = int(self.supported_heat_temps[0])
                if self.lower_end_temp < 55:
                    self.hvac_temp_scale = "C"
                else:
                    self.hvac_temp_scale = "F"
            else:
                self.lower_end_temp = int(self.supported_cool_temps[0])
                if self.lower_end_temp < 55:
                    self.hvac_temp_scale = "C"
                else:
                    self.hvac_temp_scale = "F"

        ### Get current HVAC fan speed ###
        self.hvac_fan_speed = hvac_state.attributes['fan-speed']

        ### Check to See if HVAC Unit Supports Setting Swing On and Off ###
        if ('swing' in hvac_state.attributes and hvac_state.attributes['swing'] is not None):
            self.swing_state = hvac_state.attributes['swing']
            self.swing_available = True
        else:
            self.swing_available = False

        ### Create list of supported HVAC modes ###
        self.hvac_modes = []
        for key in hvac_state.attributes['constraints']['ON'].keys():
            self.hvac_modes.append(key)

        ### Create list of supported fan speeds ###
        self.hvac_fan_speeds = []
        if self.hvac_mode == "Heat":
            if "ON" in hvac_state.attributes['constraints']['ON']['HEAT'].keys():
                for key in hvac_state.attributes['constraints']['ON']['HEAT']['ON'].keys():
                    self.hvac_fan_speeds.append(key)
            else:
                for key in hvac_state.attributes['constraints']['ON']['HEAT']['OFF'].keys():
                    self.hvac_fan_speeds.append(key)
        if self.hvac_mode == "Cool":
            if "ON" in hvac_state.attributes['constraints']['ON']['COOL'].keys():
                for key in hvac_state.attributes['constraints']['ON']['COOL']['ON'].keys():
                    self.hvac_fan_speeds.append(key)
            else:
                for key in hvac_state.attributes['constraints']['ON']['COOL']['OFF'].keys():
                    self.hvac_fan_speeds.append(key)
        if self.hvac_mode == "Fan":
            if "ON" in hvac_state.attributes['constraints']['ON']['FAN'].keys():
                for key in hvac_state.attributes['constraints']['ON']['FAN']['ON'].keys():
                    self.hvac_fan_speeds.append(key)
            else:
                for key in hvac_state.attributes['constraints']['ON']['FAN']['OFF'].keys():
                    self.hvac_fan_speeds.append(key)
        if self.hvac_mode == "Dry":
            if "ON" in hvac_state.attributes['constraints']['ON']['DRY'].keys():
                for key in hvac_state.attributes['constraints']['ON']['DRY']['ON'].keys():
                    self.hvac_fan_speeds.append(key)
            else:
                for key in hvac_state.attributes['constraints']['ON']['DRY']['OFF'].keys():
                    self.hvac_fan_speeds.append(key)
        if self.hvac_mode == "Auto":
            if "ON" in hvac_state.attributes['constraints']['ON']['AUTO'].keys():
                for key in hvac_state.attributes['constraints']['ON']['AUTO']['ON'].keys():
                    self.hvac_fan_speeds.append(key)
            else:
                for key in hvac_state.attributes['constraints']['ON']['AUTO']['OFF'].keys():
                    self.hvac_fan_speeds.append(key)

    ### Power can be either On or Off ###
    def set_hvac_power(self, power):
        attributes = {
        "power": power,
        }
        relationships = {}
        self.api.control_hvac(self, HVAC_UNITS, attributes, relationships)
        self.refresh()

    ### Mode can be Dry, Heat, Cool, Fan, or Auto depending on unit's capabilities ###
    def set_hvac_mode(self, mode):
        attributes = {
        "mode": mode,
        }
        relationships = {}
        self.api.control_hvac(self, HVAC_UNITS, attributes, relationships)
        self.refresh()

    ### Swing can be On or Off if unit supports swing feature ###
    def set_hvac_swing(self, swing):
        attributes = {
        "swing": swing,
        }
        relationships = {}
        self.api.control_hvac(self, HVAC_UNITS, attributes, relationships)
        self.refresh()

    ### A Flair structure that is in Auto Mode needs a different method to change swing state. Valid swing inputs are True and False ###
    def set_auto_structure_hvac_swing(self, swing):
        attributes = {
        "swing-auto": swing,
        }
        relationships = {}
        self.api.control_hvac(self, HVAC_UNITS, attributes, relationships)
        self.refresh()

    ### Fan speed can be High, Medium, Low, or Auto depending on unit's capabilities ###
    def set_hvac_fan_speed(self, speed):
        attributes = {
        "fan-speed": speed,
        }
        relationships = {}
        self.api.control_hvac(self, HVAC_UNITS, attributes, relationships)
        self.refresh()

    ### A Flair structure that is in Auto Mode needs a different method to change fan speed. Valid speeds are AUTO, HIGH, MEDIUM, and LOW ###
    def set_auto_structure_hvac_fan_speed(self, speed):
        attributes = {
        "default-fan-speed": speed,
        }
        relationships = {}
        self.api.control_hvac(self, HVAC_UNITS, attributes, relationships)
        self.refresh()

    ### Temperature sent should fall in the range seen in self.supported_heat_temps if in heat mode and
    ### in the range seen in self.supported_cool_temps if in cool mode
    def set_hvac_temp(self, temp):
        attributes = {
        "temperature": temp,
        }
        relationships = {}
        self.api.control_hvac(self, HVAC_UNITS, attributes, relationships)
        self.refresh()

    ### The setpoint can only be changed when structure is in manual mode. When in auto mode, the room set-point needs to be changed ###
    def set_auto_hvac_temp(self, temp):
        attributes = {
        'set-point-c': temp,
        'active': True
        }
        relationships = {}
        self.api.control_room(self, ROOMS, attributes, relationships)
        self.refresh()
