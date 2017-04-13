"""
    Location utility functions
    FSU = (30.441878, -84.298489)
"""

from api.models import Player
from geopy.distance import distance
from copy import deepcopy


def distance_in_meters(p1: Player, p2: Player) -> float:
    """
        Estimates the exact distance between two players, in meters
    """
    p1_loc = (p1.location_lat, p1.location_lng)
    p2_loc = (p2.location_lat, p2.location_lng)
    return distance(p1_loc, p2_loc).m


class Location(object):
    def __init__(self, lat: float, lng: float):
        self.lat = lat
        self.lng = lng

    def to_tuple(self):
        return self.lat, self.lng


class CardinalSpread(object):
    def __init__(self, origin: Location, north: Location, east: Location, south: Location, west: Location):
        self.origin = origin
        self.north = north
        self.east = east
        self.south = south
        self.west = west


def converge_on_distance(
        origin: Location, step: float, do_step: callable, desired_distance: float, error_meters=1.0
):
    """
        Attempt to get the distance by calling the modifier function until the distances is within acceptable error
    """
    result = deepcopy(origin)
    while True:
        do_step(result, step)

        dist = distance(origin.to_tuple(), result.to_tuple()).m
        error = desired_distance - dist
        if abs(error) < error_meters:
            # Close enough
            break

        if error < 0:
            # Overshot it, go back and reduce the step
            do_step(result, (-1.0)*step)
            step /= 2.0

    return result


def get_cardinal_spread(lat, lng, distance) -> CardinalSpread:
    # TODO get converge distance for each cardinal direction
    pass
