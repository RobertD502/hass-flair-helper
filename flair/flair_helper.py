import logging
import time
import collections
from flair_api import make_client

from flair.structures.structure import Structure
from flair.vents.vent import Vent
from flair.pucks.puck import Puck
from flair.rooms.room import Room

_LOGGER = logging.getLogger(__name__)

class FlairSession:

    client_id = ''
    client_secret = ''
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
            self.discover_structures()
            self.discover_vents()
            self.discover_pucks()
            self.discover_rooms()

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
        structures_list = client.get('structures')
        structures = []
        for structure in structures_list.resources:
            structures.append(Structure(structure, self))
        SESSION.structures = structures

    def refresh_structures(self):
        for structure in SESSION.structures:
            structure.refresh()

    def discover_vents(self):
        client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
        vents_list = client.get('vents')
        vents = []
        for vent in vents_list.resources:
            vents.append(Vent(vent, self))
        SESSION.vents = vents

    def refresh_vents(self):
        for vent in SESSION.vents:
            vent.refresh()

    def discover_pucks(self):
        client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
        pucks_list = client.get('pucks')
        pucks = []
        for puck in pucks_list.resources:
            pucks.append(Puck(puck, self))
        SESSION.pucks = pucks

    def refresh_pucks(self):
        for puck in SESSION.pucks:
            puck.refresh()

    def discover_rooms(self):
        client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
        rooms_list = client.get('rooms')
        rooms = []
        for room in rooms_list.resources:
            rooms.append(Room(room, self))
        SESSION.rooms = rooms

    def refresh_rooms(self):
        for room in SESSION.rooms:
            room.refresh()

    def refresh_attributes(self, resource_type, id):
        client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
        return client.get(resource_type, id)


    def control(self, resource_type, id, attributes, relationships):
        client = make_client(SESSION.client_id, SESSION.client_secret, 'https://api.flair.co/')
        client.update(resource_type, id, attributes, relationships)

    def get_all_structures(self):
        return SESSION.structures

    def get_all_vents(self):
        return SESSION.vents

    def get_all_pucks(self):
        return SESSION.pucks

    def get_all_rooms(self):
        return SESSION.rooms
