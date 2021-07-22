import logging
import time
import requests
import json
import collections
from flair_api import make_client, EmptyBodyException

from flair.structures.structure import Structure
from flair.vents.vent import Vent
from flair.pucks.puck import Puck
from flair.rooms.room import Room

_LOGGER = logging.getLogger(__name__)

class FlairSession:

    client_id = ''
    client_secret = ''
    bearer_token = ''
    structures = []
    vents = []
    pucks = []
    rooms = []

SESSION = FlairSession()

class FlairHelper:
    def __init__(self, client_id, client_secret):
        SESSION.client_id = client_id
        SESSION.client_secret = client_secret
        if client_id is None or client_secret is None:
            return None
        else:
            self._authorize()
            self.discover_structures()
            self.discover_vents()
            self.discover_pucks()
            self.discover_rooms()

    def _authorize(self):
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post('https://api.flair.co/oauth/token?client_id=' + SESSION.client_id + '&client_secret=' + SESSION.client_secret +
        '&scope=thermostats.view+vents.view+vents.edit+pucks.view+pucks.edit+structures.view+structures.edit&grant_type=client_credentials', headers=headers)
        output = response.json()
        SESSION.bearer_token = output['access_token']

    def structures(self):
        return SESSION.structures

    def vents(self):
        return SESSION.vents

    def pucks(self):
        return SESSION.pucks

    def rooms(self):
        return SESSION.rooms

    def discover_structures(self):
        client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
        structures = []
        try:
            structures_list = client.get('structures')
            for structure in structures_list.resources:
                structures.append(Structure(structure, self))
        except EmptyBodyException:
            pass
        SESSION.structures = structures

    def refresh_structures(self):
        for structure in SESSION.structures:
            structure.refresh()

    def discover_vents(self):
        client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
        vents = []
        try:
            vents_list = client.get('vents')
            for vent in vents_list.resources:
                vents.append(Vent(vent, self))
        except EmptyBodyException:
            pass
        SESSION.vents = vents

    def refresh_vents(self):
        for vent in SESSION.vents:
            vent.refresh()

    def vent_current_reading(self, id):
        headers = {
        'Authorization': 'Bearer ' + SESSION.bearer_token
        }
        response = requests.get('https://api.flair.co/api/vents/' + id + '/current-reading', headers=headers)
        output = response.json()
        try:
            error = output['errors'][0]['title']
            if error == 'invalid_token':
                self._authorize()
                self.vent_current_reading(id)
            else:
                return None
        except:
            return output

    def discover_pucks(self):
        client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
        pucks = []
        try:
            pucks_list = client.get('pucks')
            for puck in pucks_list.resources:
                pucks.append(Puck(puck, self))
        except EmptyBodyException:
            pass
        SESSION.pucks = pucks

    def refresh_pucks(self):
        for puck in SESSION.pucks:
            puck.refresh()

    def discover_rooms(self):
        client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
        rooms = []
        try:
            rooms_list = client.get('rooms')
            for room in rooms_list.resources:
                rooms.append(Room(room, self))
        except EmptyBodyException:
            pass
        SESSION.rooms = rooms

    def refresh_rooms(self):
        for room in SESSION.rooms:
            room.refresh()

    def refresh_attributes(self, resource_type, id):
        client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
        return client.get(resource_type, id)

    def structure_related_to_room(self, resource_type, id):
        client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
        return client.get(resource_type, id)

    def get_schedules(self, id):
        try:
            client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
            current_structure = client.get('structures', id)
            return current_structure.get_rel('schedules')
        except:
            return None

    def control_vent(self, vent, resource_type, attributes, relationships):
        client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
        id = vent.vent_id
        client.update(resource_type, id, attributes, relationships)

    def control_schedule(self, structure, resource_type, attributes, relationships):
        client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
        id = structure.structure_id
        client.update(resource_type, id, attributes, relationships)

    def control_room(self, room, resource_type, attributes, relationships):
        client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
        id = room.room_id
        client.update(resource_type, id, attributes, relationships)

    def get_all_structures(self):
        return SESSION.structures

    def get_all_vents(self):
        return SESSION.vents

    def get_all_pucks(self):
        return SESSION.pucks

    def get_all_rooms(self):
        return SESSION.rooms
