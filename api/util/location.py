"""
    Location utility functions
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

    def __str__(self):
        return '{},{}'.format(self.lat, self.lng)

    def to_dict(self):
        return {
            'lat': self.lat,
            'lng': self.lng
        }


class CardinalSpread(object):
    def __init__(self, origin_lat: float, origin_lng: float, radius_in_meters: float):
        self.origin = Location(origin_lat, origin_lng)
        self.north = self.converge_on_distance(0.00001, self.do_step_north, radius_in_meters)
        self.east = self.converge_on_distance(0.00001, self.do_step_east, radius_in_meters)
        self.south = self.converge_on_distance(0.00001, self.do_step_south, radius_in_meters)
        self.west = self.converge_on_distance(0.00001, self.do_step_west, radius_in_meters)

        # Infer corners
        self.north_west = Location(self.north.lat, self.west.lng)
        self.north_east = Location(self.north.lat, self.east.lng)
        self.south_west = Location(self.south.lat, self.west.lng)
        self.south_east = Location(self.south.lat, self.west.lat)

    @staticmethod
    def do_step_north(loc: Location, step: float):
        loc.lat += step

    @staticmethod
    def do_step_east(loc: Location, step: float):
        loc.lng += step

    @staticmethod
    def do_step_south(loc: Location, step: float):
        loc.lat -= step

    @staticmethod
    def do_step_west(loc: Location, step: float):
        loc.lng -= step

    def converge_on_distance(
            self, step: float, do_step: callable, desired_distance: float, error_meters=0.25
    ) -> Location:
        """
            Attempt to get the distance by calling the modifier function until the distances is within acceptable error
        """
        result = deepcopy(self.origin)
        while True:
            do_step(result, step)

            dist = distance(self.origin.to_tuple(), result.to_tuple()).m
            error = desired_distance - dist
            if abs(error) < error_meters:
                # Close enough
                break

            if error < 0:
                # Overshot it, go back and reduce the step
                do_step(result, (-1.0)*step)
                step /= 2.0
            elif error > step * 3.0:
                # Under shot it by 3x, increase step
                step *= 2.0

        return result

    def __str__(self):
        return '{}\n\n{}\n{}\n{}\n{}'.format(
            self.origin, self.north, self.east, self.south, self.west
        )

    def to_dict(self):
        return {
            'north': self.north.to_dict(),
            'west': self.west.to_dict(),
            'south': self.south.to_dict(),
            'east': self.east.to_dict(),
            'north_west': self.north_west.to_dict(),
            'north_east': self.north_east.to_dict(),
            'south_east': self.south_east.to_dict(),
            'south_west': self.south_west.to_dict()
        }

