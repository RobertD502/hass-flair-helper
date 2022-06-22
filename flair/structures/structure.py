import time
import collections
from ..resource_types import STRUCTURES

class Structure(object):
    def __init__(self, data, api):
        self.api = api
        self.structure_id = data.id_
        self.structure_name = data.attributes['name']
        self.refresh()

    def refresh(self):
        structure_state = self.api.refresh_attributes(STRUCTURES, self.structure_id)
        self.current_hvac_mode = structure_state.attributes['structure-heat-cool-mode']
        self.current_system_mode = structure_state.attributes['mode']
        self.is_home = structure_state.attributes['home']
        self.relationships = structure_state.relationships
        self.active_schedule = structure_state.attributes['active-schedule-id']
        try:
            structure_schedules = self.api.get_schedules(self.structure_id)

            """ Add No Schedule key in order to be able to set the structure schedule to No Schedule using the set_schedule function """

            self.schedules_dictionary = {
                "No Schedule": None,
            }

            """Combine all the schedules into a single dictionary"""

            for schedule in structure_schedules.resources:
                self.schedules_dictionary.update([(schedule.attributes['name'], schedule.id_)])

        except AttributeError:
            self.schedules_dictionary = {"No Schedule": None}
        except:
            print("Something went wrong while attempting to get Flair structure schedules")

    def set_schedule(self, schedule_id):
        attributes = {
        'active-schedule-id': schedule_id,
        }
        relationships = {}
        self.api.control_structure(self, STRUCTURES, attributes, relationships)
        self.refresh()

    def set_structure_mode(self, hvac_mode):
        """ Possible HVAC modes are heat, cool, auto, and float. Float means off """
        attributes = {
        'structure-heat-cool-mode': hvac_mode,
        }
        relationships = {}
        self.api.control_structure(self, STRUCTURES, attributes, relationships)
        self.refresh()

    def set_system_mode(self, system_mode):
        """ Possible System modes are auto and manual """
        attributes = {
        'mode': system_mode,
        }
        relationships = {}
        self.api.control_structure(self, STRUCTURES, attributes, relationships)
        self.refresh()

    def set_home_away_mode(self, home_mode):
        """ Home mode is True and Away mode is False """
        attributes = {
        'home': home_mode,
        }
        relationships = {}
        self.api.control_structure(self, STRUCTURES, attributes, relationships)
        self.refresh()
