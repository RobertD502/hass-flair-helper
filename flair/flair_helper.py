import logging
import time
import requests
import json
import collections
from hass_flair_api import make_client, EmptyBodyException, ApiError

from flair.structures.structure import Structure
from flair.vents.vent import Vent
from flair.pucks.puck import Puck
from flair.rooms.room import Room
from flair.hvac_units.hvac_unit import HvacUnit

_LOGGER = logging.getLogger(__name__)

class FlairSession:

    client_id = ''
    client_secret = ''
    structures = []
    structure_ids = []
    vents = []
    pucks = []
    rooms = []
    hvac_units = []

SESSION = FlairSession()

class FlairHelper:
    def __init__(self, client_id, client_secret):
        SESSION.client_id = client_id
        SESSION.client_secret = client_secret
        if client_id is None or client_secret is None:
            return None
        else:
            self.client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
            self.discover_structures()
            self.discover_vents()
            self.discover_pucks()
            self.discover_rooms()
            self.discover_hvac_units()

    def structures(self):
        return SESSION.structures

    def vents(self):
        return SESSION.vents

    def pucks(self):
        return SESSION.pucks

    def rooms(self):
        return SESSION.rooms

    def hvac_units(self):
        return SESSION.hvac_units

    def discover_structures(self):
        structures = []
        structure_ids = []
        try:
            structures_list = self.client.get('structures')
            for structure in structures_list.resources:
                structures.append(Structure(structure, self))
                structure_ids.append(structure.id_)
        except EmptyBodyException:
            pass
        SESSION.structures = structures
        SESSION.structure_ids = structure_ids

    def refresh_structures(self):
        for structure in SESSION.structures:
            structure.refresh()

    def discover_vents(self):
        vents = []
        try:
            vents_list = self.client.get('vents')
            for vent in vents_list.resources:
                vents.append(Vent(vent, self))
        except EmptyBodyException:
            pass
        SESSION.vents = vents

    def refresh_vents(self):
        for vent in SESSION.vents:
            vent.refresh()

    def vent_current_reading(self, id):
        try:
            output = self.client.get('vents', id + '/current-reading')
            return output.attributes
        except ApiError as err:
            if err.status_code == 401:
                self.client.oauth_token()
                output = self.client.get('vents', id + '/current-reading')
                return output.attributes
            else:
                raise

    def puck_light_level(self, id):
        try:
            output = self.client.get('pucks', id + '/current-reading')
            return output.attributes
        except ApiError as err:
            if err.status_code == 401:
                self.client.oauth_token()
                output = self.client.get('pucks', id + '/current-reading')
                return output.attributes
            else:
                raise

    def discover_pucks(self):
        pucks = []
        try:
            pucks_list = self.client.get('pucks')
            for puck in pucks_list.resources:
                pucks.append(Puck(puck, self))
        except EmptyBodyException:
            pass
        SESSION.pucks = pucks

    def refresh_pucks(self):
        for puck in SESSION.pucks:
            puck.refresh()

    def discover_rooms(self):
        rooms = []
        try:
            rooms_list = self.client.get('rooms')
            for room in rooms_list.resources:
                if (room.relationships['structure'].data['id'] in SESSION.structure_ids):
                    rooms.append(Room(room, self))
        except EmptyBodyException:
            pass
        SESSION.rooms = rooms

    def refresh_rooms(self):
        for room in SESSION.rooms:
            room.refresh()

    def discover_hvac_units(self):
        hvac_units = []
        try:
            hvac_list = self.client.get('hvac-units')
            for hvac in hvac_list.resources:
                if hvac.attributes['model-id'] is not None:
                    hvac_units.append(HvacUnit(hvac, self))
        except EmptyBodyException:
            pass
        SESSION.hvac_units = hvac_units

    def refresh_hvac_units(self):
        for hvac_unit in SESSION.hvac_units:
            hvac_unit.refresh()

    def refresh_attributes(self, resource_type, id):
        try:
            return self.client.get(resource_type, id)
        except ApiError as err:
            if err.status_code == 401:
                self.client.oauth_token()
                return self.client.get(resource_type, id)
            else:
                raise



    def structure_related_to_room(self, resource_type, id):
        try:
            return self.client.get(resource_type, id)
        except ApiError as err:
            if err.status_code == 401:
                self.client.oauth_token()
                return self.client.get(resource_type, id)
            else:
                raise

    def get_schedules(self, id):
        try:
            current_structure = self.client.get('structures', id)
            return current_structure.get_rel('schedules')
        except ApiError as err:
            if err.status_code == 401:
                self.client.oauth_token()
                current_structure = self.client.get('structures', id)
                return current_structure.get_rel('schedules')
            else:
                raise
        except EmptyBodyException:
            pass


    def control_vent(self, vent, resource_type, attributes, relationships):
        id = vent.vent_id
        try:
            self.client.update(resource_type, id, attributes, relationships)
        except ApiError as err:
            if err.status_code == 401:
                self.client.oauth_token()
                self.client.update(resource_type, id, attributes, relationships)
            else:
                raise

    def control_structure(self, structure, resource_type, attributes, relationships):
        id = structure.structure_id
        try:
            self.client.update(resource_type, id, attributes, relationships)
        except ApiError as err:
            if err.status_code == 401:
                self.client.oauth_token()
                self.client.update(resource_type, id, attributes, relationships)
            else:
                raise

    def control_room(self, room, resource_type, attributes, relationships):
        id = room.room_id
        try:
            self.client.update(resource_type, id, attributes, relationships)
        except ApiError as err:
            if err.status_code == 401:
                self.client.oauth_token()
                self.client.update(resource_type, id, attributes, relationships)
            else:
                raise

    def control_hvac(self, hvac, resource_type, attributes, relationships):
        id = hvac.hvac_id
        try:
            self.client.update(resource_type, id, attributes, relationships)
        except ApiError as err:
            if err.status_code == 401:
                self.client.oauth_token()
                self.client.update(resource_type, id, attributes, relationships)
            else:
                raise

    def get_all_structures(self):
        return SESSION.structures

    def get_all_vents(self):
        return SESSION.vents

    def get_all_pucks(self):
        return SESSION.pucks

    def get_all_rooms(self):
        return SESSION.rooms
