import time
import collections


class Structure(object):
    def __init__(self, data, api):
        self.api = api
        self.structure_id = data.id_
        self.structure_name = data.attributes['name']
        self.refresh()

    def refresh(self):
        structure_state = self.api.refresh_attributes('structures', self.structure_id)
        self.current_hvac_mode = structure_state.attributes['structure-heat-cool-mode']
        self.relationships = structure_state.relationships
        self.active_schedule = structure_state.attributes['active-schedule-id']
        try:
            structure_schedules = self.api.get_schedules(self.structure_id)
            """Get all schedules as dictionaries and place in a list"""
            sl = []
            for schedule in structure_schedules.resources:
                sl.append({
                    schedule.attributes['name']: schedule.id_,
                })
            self.schedules_list = sl
            """Combine all the schedule dictionaries into a single dictionary"""
            cs = {}
            for dictc in sl:
                cs.update(dictc)
            self.combined_schedules = cs
        except AttributeError:
            print("This structure doesn't have any attributes")
        except:
            print("Something went wrong")
    
    def set_schedule(self, schedule_id):
        resource_type = 'structures'
        attributes = {
        'active-schedule-id': schedule_id,
        }
        relationships = {}
        self.api.control_schedule(self, resource_type, attributes, relationships)
        self.refresh()
