import time
import collections

#Possible use in future
class Structure(object):
    def __init__(self, data, api):
        self.api = api
        self.structure_id = data.id_
        self.structure_name = data.attributes['name']
        self.refresh()

    def refresh(self):
        structure_state = self.api.refresh_attributes('structures', self.structure_id)
        self.current_hvac_mode = structure_state.attributes['structure-heat-cool-mode']
