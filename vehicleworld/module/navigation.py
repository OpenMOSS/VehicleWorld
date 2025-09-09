
from enum import Enum
from module.environment import Environment
import sys
from utils import api
class Navigation:
    class DistanceUnit(Enum):
        """
        Enumeration for distance units used in navigation.
        """
        KILOMETERS = "Kilometers"
        MILES = "Miles"
    
    class VolumeLevel(Enum):
        """
        Enumeration for predefined volume levels.
        """
        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"
    
    class MapView(Enum):
        """
        Enumeration for navigation map view types.
        """
        VIEW_2D = "2D view"
        VIEW_3D = "3D view"
        HEADING_UP = "Heading up"
        NORTH_UP = "North up"
    
    class BroadcastMode(Enum):
        """
        Enumeration for navigation broadcast detail levels.
        """
        CONCISE = "Concise"
        DETAILED = "Detailed"
        MUTE = "Mute"
    
    class ZoomDegree(Enum):
        """
        Enumeration for predefined zoom levels.
        """
        LARGE = "large"
        LITTLE = "little"
        TINY = "tiny"
    
    class ZoomMode(Enum):
        """
        Enumeration for zoom directions.
        """
        ZOOM_IN = "Zoom in"
        ZOOM_OUT = "Zoom out"
        
    class RouteInfo:
        """
        Inner class for storing route information between two points.
        """
        def __init__(self, departure="Current location", destination="", distance="", duration="", route_details=None):
            self._departure = departure
            self._destination = destination
            # self._distance = distance
            # self._duration = duration
            # self._route_details = route_details if route_details else ["默认路线详情"]
        
        @property
        def departure(self):
            return self._departure
            
        @departure.setter
        def departure(self, value):
            self._departure = value
            
        @property
        def destination(self):
            return self._destination
            
        @destination.setter
        def destination(self, value):
            self._destination = value
            
        # @property
        # def distance(self):
        #     return self._distance
            
        # @distance.setter
        # def distance(self, value):
        #     self._distance = value
            
        # @property
        # def duration(self):
        #     return self._duration
            
        # @duration.setter
        # def duration(self, value):
        #     self._duration = value
            
        # @property
        # def route_details(self):
        #     return self._route_details
            
        # @route_details.setter
        # def route_details(self, value):
        #     self._route_details = value
        
        def to_dict(self):
            return {
                "departure": {
                    "value": self.departure,
                    "description": "Starting point of the route",
                    "type": type(self.departure).__name__
                },
                "destination": {
                    "value": self.destination,
                    "description": "End point of the route",
                    "type": type(self.destination).__name__
                },
                # "distance": {
                #     "value": self.distance,
                #     "description": "Distance between departure and destination",
                #     "type": type(self.distance).__name__
                # },
                # "duration": {
                #     "value": self.duration,
                #     "description": "Estimated travel time",
                #     "type": type(self.duration).__name__
                # },
                # "route_details": {
                #     "value": self.route_details,
                #     "description": "Additional routing information",
                #     "type": type(self.route_details).__name__
                # }
            }
        
        @classmethod
        def from_dict(cls, data):
            return cls(
                departure=data["departure"]["value"],
                destination=data["destination"]["value"],
                # distance=data["distance"]["value"],
                # duration=data["duration"]["value"],
                # route_details=data["route_details"]["value"]
            )
    
    def __init__(self):
        # Base navigation state
        self._is_active = False
        
        
       
        
        # Route information
        self._current_route = self.RouteInfo()
        self._waypoints = ["Beijing"]
        
        # Map display settings
        self._map_zoom_level = 5  # Default zoom level (1-10)
        self._map_view = self.MapView.VIEW_2D
        
        # Feature toggles
        self._traffic_status_enabled = False
        self._speed_camera_enabled = False
        self._voice_notifications_enabled = True
        
        # Broadcast settings
        self._broadcast_mode = self.BroadcastMode.DETAILED
    
    # Property getters and setters
    @property
    def is_active(self):
        return self._is_active
    
    @is_active.setter
    def is_active(self, value):
        self._is_active = value
    
    @property
    def current_route(self):
        return self._current_route
    
    @current_route.setter
    def current_route(self, value):
        self._current_route = value
    
    @property
    def waypoints(self):
        return self._waypoints
    
    @waypoints.setter
    def waypoints(self, value):
        self._waypoints = value
    
    @property
    def map_zoom_level(self):
        return self._map_zoom_level
    
    @map_zoom_level.setter
    def map_zoom_level(self, value):
        if 1 <= value <= 10:
            self._map_zoom_level = value
        else:
            raise ValueError("Zoom level must be between 1 and 10")
    
    @property
    def map_view(self):
        return self._map_view
    
    @map_view.setter
    def map_view(self, value):
        if isinstance(value, self.MapView):
            self._map_view = value
        else:
            try:
                self._map_view = self.MapView(value)
            except ValueError:
                raise ValueError(f"Invalid map view: {value}. Must be one of {[e.value for e in self.MapView]}")
    
    @property
    def traffic_status_enabled(self):
        return self._traffic_status_enabled
    
    @traffic_status_enabled.setter
    def traffic_status_enabled(self, value):
        self._traffic_status_enabled = bool(value)
    
    @property
    def speed_camera_enabled(self):
        return self._speed_camera_enabled
    
    @speed_camera_enabled.setter
    def speed_camera_enabled(self, value):
        self._speed_camera_enabled = bool(value)
    
    @property
    def voice_notifications_enabled(self):
        return self._voice_notifications_enabled
    
    @voice_notifications_enabled.setter
    def voice_notifications_enabled(self, value):
        self._voice_notifications_enabled = bool(value)
    
    @property
    def broadcast_mode(self):
        return self._broadcast_mode
    
    @broadcast_mode.setter
    def broadcast_mode(self, value):
        if isinstance(value, self.BroadcastMode):
            self._broadcast_mode = value
        else:
            try:
                self._broadcast_mode = self.BroadcastMode(value)
            except ValueError:
                raise ValueError(f"Invalid broadcast mode: {value}. Must be one of {[e.value for e in self.BroadcastMode]}")
    
    # API Methods Implementation
    @api("navigation")
    def navigation_meter_unit(self, mode):
        """
        Set the unit of distance displayed on the navigation.
        
        Args:
            mode (str): Distance unit options. Valid values are "Kilometers" or "Miles".
        
        Returns:
            dict: Result of the operation with updated unit.
        """
        try:
           
            # Update the global environment unit system
            if mode == "Kilometers":
                Environment.set_unit_system("kilometer")
            else:
                Environment.set_unit_system("mile")
            
            return {
                "success": True,
                "unit": mode
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("navigation")
    def navigation_soundVolume_increase(self, value=None, degree=None):
        """
        Increase navigation volume.
        
        Args:
            value (int, optional): Specific numeric amount to increase volume.
            degree (str, optional): Categorical level of increase. 
                                    Valid values are "large", "little", "tiny",mutually exclusive with value.
        
        Returns:
            dict: Result of the operation with updated volume.
        """
        if value is not None and degree is not None:
            return {
                "success": False,
                "error": "Cannot specify both value and degree"
            }
        
        try:
            current_volume = Environment.get_volume()
            
            if value is not None:
                if not isinstance(value, int) or value < 0:
                    return {
                        "success": False,
                        "error": "Volume increase value must be a positive integer"
                    }
                new_volume = min(100, current_volume + value)
            elif degree is not None:
                # Map degree to volume increase amount
                degree_map = {
                    "large": 20,
                    "little": 10,
                    "tiny": 5
                }
                
                if degree not in degree_map:
                    return {
                        "success": False,
                        "error": f"Invalid volume increase degree: {degree}. Valid values are {list(degree_map.keys())}"
                    }
                
                new_volume = min(100, current_volume + degree_map[degree])
            else:
                # Default increase of 10%
                new_volume = min(100, current_volume + 10)
            
            
            
            # Set global environment volume and change sound channel to navigation
            Environment.set_volume(new_volume)
            Environment.set_sound_channel("navigation")
            
            return {
                "success": True,
                "old_volume": current_volume,
                "new_volume": new_volume,
                "sound_channel": Environment.get_sound_channel()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @api("navigation")
    def navigation_soundVolume_decrease(self, value=None, degree=None):
        """
        Decrease navigation volume.
        
        Args:
            value (int, optional): Specific numeric amount to decrease volume.
            degree (str, optional): Categorical level of decrease. 
                                    Valid values are "large", "little", "tiny",mutually exclusive with value.
        
        Returns:
            dict: Result of the operation with updated volume.
        """
        if value is not None and degree is not None:
            return {
                "success": False,
                "error": "Cannot specify both value and degree"
            }
        
        try:
            current_volume = Environment.get_volume()
            
            if value is not None:
                if not isinstance(value, int) or value < 0:
                    return {
                        "success": False,
                        "error": "Volume decrease value must be a positive integer"
                    }
                new_volume = max(0, current_volume - value)
            elif degree is not None:
                # Map degree to volume decrease amount
                degree_map = {
                    "large": 20,
                    "little": 10,
                    "tiny": 5
                }
                
                if degree not in degree_map:
                    return {
                        "success": False,
                        "error": f"Invalid volume decrease degree: {degree}. Valid values are {list(degree_map.keys())}"
                    }
                
                new_volume = max(0, current_volume - degree_map[degree])
            else:
                # Default decrease of 10%
                new_volume = max(0, current_volume - 10)
            
         
            
            # Set global environment volume and change sound channel to navigation
            Environment.set_volume(new_volume)
            Environment.set_sound_channel("navigation")
            
            return {
                "success": True,
                "old_volume": current_volume,
                "new_volume":  new_volume,
                "sound_channel": Environment.get_sound_channel()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        
    @api("navigation")
    def navigation_soundVolume_set(self, value=None, degree=None):
        """
        Set navigation volume adjustment.
        
        Args:
            value (int, optional): Numeric volume value (0-100).
            degree (str, optional): Categorical volume level. 
                                    Valid values are "max", "high", "medium", "low", "min",mutually exclusive with value.
        
        Returns:
            dict: Result of the operation with updated volume.
        """
        if value is not None and degree is not None:
            return {
                "success": False,
                "error": "Cannot specify both value and degree"
            }
        
        try:
            if value is not None:
                if not isinstance(value, int) or not (0 <= value <= 100):
                    return {
                        "success": False,
                        "error": "Volume value must be an integer between 0 and 100"
                    }
                Environment.set_volume(value)
            elif degree is not None:
                # Map degree to volume value
                degree_map = {
                    self.VolumeLevel.MAX.value: 100,
                    self.VolumeLevel.HIGH.value: 80,
                    self.VolumeLevel.MEDIUM.value: 50,
                    self.VolumeLevel.LOW.value: 20,
                    self.VolumeLevel.MIN.value: 0
                }
                
                if degree not in degree_map:
                    return {
                        "success": False,
                        "error": f"Invalid volume degree: {degree}. Valid values are {list(degree_map.keys())}"
                    }
                
                Environment.set_volume(degree_map[degree])
            else:
                return {
                    "success": False,
                    "error": "Either value or degree must be specified"
                }
            
            # Set global environment volume and change sound channel to navigation
            
            Environment.set_sound_channel("navigation")
            
            return {
                "success": True,
                "volume": Environment.get_volume(),
                "sound_channel": Environment.get_sound_channel()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    # @api("navigation")
    # def navigation_get_duration(self):
    #     """
    #     Get remaining time to destination in current navigation.
        
    #     Returns:
    #         dict: Information about the remaining time.
    #     """
    #     if not self.is_active or self.current_route is None:
    #         return {
    #             "success": False,
    #             "error": "No active navigation route"
    #         }
        
    #     return {
    #         "success": True,
    #         "duration": self.current_route.duration
    #     }
    
    # @api("navigation")
    # def navigation_get_distance(self):
    #     """
    #     Get remaining distance to destination in current navigation.
        
    #     Returns:
    #         dict: Information about the remaining distance.
    #     """
    #     if not self.is_active or self.current_route is None:
    #         return {
    #             "success": False,
    #             "error": "No active navigation route"
    #         }
        
    #     return {
    #         "success": True,
    #         "distance": self.current_route.distance
    #     }
    
    @api("navigation")
    def navigation_get_destination(self):
        """
        Get current navigation destination.
        
        Returns:
            dict: Information about the current destination.
        """
        if not self.is_active or self.current_route is None:
            return {
                "success": False,
                "error": "No active navigation route"
            }
        
        return {
            "success": True,
            "destinationInfo": self.current_route.destination
        }
    
    @api("navigation")
    def navigation_exit(self):
        """
        Exit navigation.
        
        Returns:
            dict: Result of the operation.
        """
        if not self.is_active:
            return {
                "success": False,
                "error": "Navigation is not active"
            }
        
        self.is_active = False
        self.current_route = None
        self.waypoints = []
        
        
        
        return {
            "success": True,
            "message": "Navigation exited successfully"
        }
    
    @api("navigation")
    def navigation_route_plan(self, address, placeOfDeparture="Current location"):
        """
        Route planning, specify destination to start navigation.
        
        Args:
            address (str): Destination name/address.
            placeOfDeparture(str): Departure name/address
        Returns:
            dict: Result of the operation with route details.
        """
        if not address:
            return {
                "success": False,
                "error": "Destination address is required"
            }
        
        # Create a new route with the specified destination
        self.current_route = self.RouteInfo(destination=address,departure=placeOfDeparture)
        
        # Simulate calculating distance and duration
        # unit_suffix = "km" if Environment.get_unit_system() == self.DistanceUnit.KILOMETERS else "miles"
        # self.current_route.distance = f"25 {unit_suffix}"  # Example distance
        # self.current_route.duration = "30 minutes"  # Example duration
        
        self.is_active = True
        self.waypoints = []
        
        # Set sound channel to navigation for voice guidance
        Environment.set_sound_channel("navigation")
        
        return {
            "success": True,
            "route": self.current_route.to_dict()
        }
    
    @api("navigation")
    def navigation_destination_change(self, address):
        """
        Change navigation destination.
        
        Args:
            address (str): New destination name/address.
        
        Returns:
            dict: Result of the operation with updated route details.
        """
        if not self.is_active:
            return {
                "success": False,
                "error": "Navigation is not active"
            }
        
        if not address:
            return {
                "success": False,
                "error": "New destination address is required"
            }
        
        # Update current route with new destination
        old_destination = self.current_route.destination
        self.current_route.destination = address
        self.waypoints = []
        
        # Simulate recalculating distance and duration
        # unit_suffix = "km" if Environment.get_unit_system() == self.DistanceUnit.KILOMETERS else "miles"
        # self.current_route.distance = f"30 {unit_suffix}"  # Example updated distance
        # self.current_route.duration = "35 minutes"  # Example updated duration
        
        # Set sound channel to navigation for voice guidance
        Environment.set_sound_channel("navigation")
        
        return {
            "success": True,
            "old_destination": old_destination,
            "new_destination": address,
            "route": self.current_route.to_dict()
        }
    
    @api("navigation")
    def navigation_midWay_add(self, midway):
        """
        Add waypoint to navigation, pick up someone mid-route.
        
        Args:
            midway (list): List of waypoint locations.
        
        Returns:
            dict: Result of the operation with updated waypoints.
        """
        if not self.is_active or self.current_route is None:
            return {
                "success": False,
                "error": "No active navigation route"
            }
        
        if not midway or not isinstance(midway, list):
            return {
                "success": False,
                "error": "Waypoints must be provided as a list"
            }
        
        # Add new waypoints
        self.waypoints.extend(midway)
        
        # Simulate recalculating route
        # unit_suffix = "km" if Environment.get_unit_system() == self.DistanceUnit.KILOMETERS else "miles"
        # self.current_route.distance = f"{25 + 5 * len(self.waypoints)} {unit_suffix}"  # Example updated distance
        # self.current_route.duration = f"{30 + 5 * len(self.waypoints)} minutes"  # Example updated duration
        
        # Set sound channel to navigation for voice guidance
        Environment.set_sound_channel("navigation")
        
        return {
            "success": True,
            "added_waypoints": midway,
            "all_waypoints": self.waypoints,
            "updated_route": self.current_route.to_dict()
        }
    
    @api("navigation")
    def navigation_midWay_delete(self, address=None, number=None):
        """
        Delete waypoint from navigation.
        
        Args:
            address (str, optional): Waypoint address to delete.
            number (int, optional): Index of waypoint to delete.
        
        Returns:
            dict: Result of the operation with updated waypoints.
        """
        if not self.is_active or self.current_route is None:
            return {
                "success": False,
                "error": "No active navigation route"
            }
        
        if not self.waypoints:
            return {
                "success": False,
                "error": "No waypoints to delete"
            }
        
        if address is not None and number is not None:
            return {
                "success": False,
                "error": "Cannot specify both address and number"
            }
        
        removed_waypoint = None
        
        try:
            if address is not None:
                if address in self.waypoints:
                    self.waypoints.remove(address)
                    removed_waypoint = address
                else:
                    return {
                        "success": False,
                        "error": f"Waypoint '{address}' not found"
                    }
            elif number is not None:
                if 0 <= number < len(self.waypoints):
                    removed_waypoint = self.waypoints.pop(number)
                else:
                    return {
                        "success": False,
                        "error": f"Waypoint number {number} is out of range"
                    }
            else:
                return {
                    "success": False,
                    "error": "Either address or number must be specified"
                }
            
            # Simulate recalculating route
            # unit_suffix = "km" if Environment.get_unit_system() == self.DistanceUnit.KILOMETERS else "miles"
            # self.current_route.distance = f"{25 + 5 * len(self.waypoints)} {unit_suffix}"  # Example updated distance
            # self.current_route.duration = f"{30 + 5 * len(self.waypoints)} minutes"  # Example updated duration
            
            # Set sound channel to navigation for voice guidance
            Environment.set_sound_channel("navigation")
            
            return {
                "success": True,
                "removed_waypoint": removed_waypoint,
                "remaining_waypoints": self.waypoints,
                "updated_route": self.current_route.to_dict()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    # @api("navigation")
    # def navigation_route_query(self, destination, placeOfDeparture="Current location"):
    #     """
    #     Query navigation route.
        
    #     Args:
    #         destination (str): Destination name/address.
    #         placeOfDeparture (str, optional): Departure location. Defaults to "Current location".
        
    #     Returns:
    #         dict: Information about available routes.
    #     """
    #     if not destination:
    #         return {
    #             "success": False,
    #             "error": "Destination is required"
    #         }
        
    #     # Simulate querying multiple route options
    #     routes = []
    #     unit_suffix = "km" if Environment.get_unit_system() == self.DistanceUnit.KILOMETERS else "miles"
        
    #     # Generate example routes
    #     routes.append({
    #         "route": "Fastest route via Highway 101",
    #         "distance": f"25 {unit_suffix}",
    #         "duration": "30 minutes"
    #     })
    #     routes.append({
    #         "route": "Shortest route via local roads",
    #         "distance": f"20 {unit_suffix}",
    #         "duration": "40 minutes"
    #     })
    #     routes.append({
    #         "route": "Alternative route avoiding tolls",
    #         "distance": f"28 {unit_suffix}",
    #         "duration": "35 minutes"
    #     })
        
    #     return {
    #         "success": True,
    #         "departure": placeOfDeparture,
    #         "destination": destination,
    #         "routeResult": routes
    #     }
    
    @api("navigation")
    def navigation_trafficStatus_switch(self, switch):
        """
        Turn on/off navigation traffic status.
        
        Args:
            switch (bool): True to turn on, False to turn off.
        
        Returns:
            dict: Result of the operation.
        """
        try:
            self.traffic_status_enabled = bool(switch)
            
            return {
                "success": True,
                "traffic_status_enabled": self.traffic_status_enabled
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    # @api("navigation")
    # def navigation_trafficStatus_query(self, destination=""):
    #     """
    #     Query navigation traffic status: congestion ahead/to destination.
        
    #     Args:
    #         destination (str, optional): Destination to check traffic to.
    #                                     If empty, checks traffic ahead.
        
    #     Returns:
    #         dict: Traffic status information.
    #     """
    #     if not self.traffic_status_enabled:
    #         return {
    #             "success": False,
    #             "error": "Traffic status is disabled"
    #         }
        
    #     # Simulate traffic status
    #     if destination:
    #         traffic_info = f"Light traffic to {destination}. Estimated arrival in 25 minutes."
    #     else:
    #         traffic_info = "Moderate traffic for the next 5 miles. Expect minor delays."
        
    #     return {
    #         "success": True,
    #         "trafficStatus": traffic_info
    #     }
    
    @api("navigation")
    def navigation_mapZoom(self, mode, value=None, unit=None, degree=None):
        """
        Zoom in/out navigation map.
        
        Args:
            mode (str): Zoom mode, either "Zoom in" or "Zoom out".
            value (int, optional): Numeric zoom value.
            unit (str, optional): Unit for zoom value.
            degree (str, optional): Categorical zoom level, one of "large", "little", "tiny".
        
        Returns:
            dict: Result of the operation with updated zoom level.
        """
        try:
            zoom_mode = self.ZoomMode(mode)
            
            if (value is not None and unit is not None) and degree is not None:
                return {
                    "success": False,
                    "error": "Cannot specify both value/unit and degree"
                }
            
            # Current zoom level (1-10 scale where 1 is most zoomed out, 10 is most zoomed in)
            current_level = self.map_zoom_level
            
            if degree is not None:
                # Apply zoom by degree
                degree_value = self.ZoomDegree(degree)
                
                if zoom_mode == self.ZoomMode.ZOOM_IN:
                    if degree_value == self.ZoomDegree.LARGE:
                        self.map_zoom_level = min(10, current_level + 3)
                    elif degree_value == self.ZoomDegree.LITTLE:
                        self.map_zoom_level = min(10, current_level + 2)
                    elif degree_value == self.ZoomDegree.TINY:
                        self.map_zoom_level = min(10, current_level + 1)
                else:  # ZOOM_OUT
                    if degree_value == self.ZoomDegree.LARGE:
                        self.map_zoom_level = max(1, current_level - 3)
                    elif degree_value == self.ZoomDegree.LITTLE:
                        self.map_zoom_level = max(1, current_level - 2)
                    elif degree_value == self.ZoomDegree.TINY:
                        self.map_zoom_level = max(1, current_level - 1)
            elif value is not None:
                # Apply zoom by precise value
                if zoom_mode == self.ZoomMode.ZOOM_IN:
                    self.map_zoom_level = min(10, current_level + value)
                else:  # ZOOM_OUT
                    self.map_zoom_level = max(1, current_level - value)
            else:
                # Default zoom adjustment
                if zoom_mode == self.ZoomMode.ZOOM_IN:
                    self.map_zoom_level = min(10, current_level + 1)
                else:  # ZOOM_OUT
                    self.map_zoom_level = max(1, current_level - 1)
            
            return {
                "success": True,
                "previous_zoom_level": current_level,
                "new_zoom_level": self.map_zoom_level,
                "zoom_mode": zoom_mode.value
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("navigation")
    def navigation_view_switch(self, type):
        """
        Switch navigation view.
        
        Args:
            type (str): View type. Valid values are "2D view", "3D view", "Heading up", "North up".
        
        Returns:
            dict: Result of the operation with updated view type.
        """
        try:
            previous_view = self.map_view
            self.map_view = self.MapView(type)
            
            return {
                "success": True,
                "previous_view": previous_view.value,
                "new_view": self.map_view.value
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("navigation")
    def navigation_broadCastMode_switch(self, type):
        """
        Switch navigation broadcast mode.
        
        Args:
            type (str): Broadcast mode type. Valid values are "Concise", "Detailed", "Mute".
        
        Returns:
            dict: Result of the operation with updated broadcast mode.
        """
        try:
            previous_mode = self.broadcast_mode
            self.broadcast_mode = self.BroadcastMode(type)
            
            # If changing to mute, disable voice notifications
            if self.broadcast_mode == self.BroadcastMode.MUTE:
                self.voice_notifications_enabled = False
            else:
                # Otherwise ensure voice notifications are enabled
                self.voice_notifications_enabled = True
                # And ensure sound channel is set to navigation
                Environment.set_sound_channel("navigation")
            
            return {
                "success": True,
                "previous_mode": previous_mode.value,
                "new_mode": self.broadcast_mode.value,
                "voice_notifications_enabled": self.voice_notifications_enabled
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("navigation")
    def navigation_eDog_switch(self, switch):
        """
        Turn on/off navigation speed camera mode.
        
        Args:
            switch (bool): True to turn on, False to turn off.
        
        Returns:
            dict: Result of the operation.
        """
        try:
            self.speed_camera_enabled = bool(switch)
            
            return {
                "success": True,
                "speed_camera_enabled": self.speed_camera_enabled
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("navigation")
    def navigation_voice_notify_switch(self, switch):
        """
        Turn on/off navigation voice prompts.
        
        Args:
            switch (bool): True to turn on, False to turn off.
        
        Returns:
            dict: Result of the operation.
        """
        try:
            self.voice_notifications_enabled = bool(switch)
            
            # If turning on voice notifications, ensure proper broadcast mode
            if self.voice_notifications_enabled:
                if self.broadcast_mode == self.BroadcastMode.MUTE:
                    self.broadcast_mode = self.BroadcastMode.DETAILED
                # Ensure sound channel is set to navigation
                Environment.set_sound_channel("navigation")
            
            return {
                "success": True,
                "voice_notifications_enabled": self.voice_notifications_enabled,
                "broadcast_mode": self.broadcast_mode.value
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    


    def to_dict(self):
        """
        Convert the Navigation object to a dictionary with metadata.
        
        Returns:
            dict: Dictionary representation of the Navigation object.
        """
        waypoints_info = []
        for i, waypoint in enumerate(self.waypoints):
            waypoints_info.append({
                "index": i,
                "location": waypoint
            })
        
        return {
            "is_active": {
                "value": self.is_active,
                "description": "Whether navigation is currently active,when you need to use navigation,you should set it to True.",
                "type": type(self.is_active).__name__
            },
            
            "current_route": {
                "value": self.current_route.to_dict() if self.current_route else None,
                "description": "Current active navigation route.Set it to None when exit navigation",
                "type": "RouteInfo or None"
            },
            "waypoints": {
                "value": waypoints_info,
                "description": "List of waypoints along the route. Clear this list (set to []) when changing destination or exit navigation.",
                "type": type(self.waypoints).__name__
            },
            "map_zoom_level": {
                "value": self.map_zoom_level,
                "description": "Current zoom level (1-10, where 10 is most zoomed in)",
                "type": type(self.map_zoom_level).__name__
            },
            "map_view": {
                "value": self.map_view.value,
                "description": "Current map view type",
                "type": "MapView enum",
                "enum_values": [e.value for e in self.MapView]
            },
            "traffic_status_enabled": {
                "value": self.traffic_status_enabled,
                "description": "Whether traffic status information is enabled",
                "type": type(self.traffic_status_enabled).__name__
            },
            "speed_camera_enabled": {
                "value": self.speed_camera_enabled,
                "description": "Whether speed camera alerts are enabled",
                "type": type(self.speed_camera_enabled).__name__
            },
            "voice_notifications_enabled": {
                "value": self.voice_notifications_enabled,
                "description": "Whether voice guidance is enabled",
                "type": type(self.voice_notifications_enabled).__name__
            },
            "broadcast_mode": {
                "value": self.broadcast_mode.value,
                "description": "Current navigation voice guidance detail level",
                "type": "BroadcastMode enum",
                "enum_values": [e.value for e in self.BroadcastMode]
            }
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Navigation object from dictionary data.
        
        Args:
            data (dict): Dictionary containing Navigation attributes.
        
        Returns:
            Navigation: Reconstructed Navigation object.
        """
        instance = cls()
        
        # Set basic properties
        instance.is_active = data["is_active"]["value"]
     
        # Reconstruct current route if it exists
        if data["current_route"]["value"]:
            instance.current_route = cls.RouteInfo.from_dict(data["current_route"]["value"])
        
        # Reconstruct waypoints
        instance.waypoints = [wp["location"] for wp in data["waypoints"]["value"]]
        
        # Set display settings
        instance.map_zoom_level = data["map_zoom_level"]["value"]
        instance.map_view = data["map_view"]["value"]
        
        # Set feature toggles
        instance.traffic_status_enabled = data["traffic_status_enabled"]["value"]
        instance.speed_camera_enabled = data["speed_camera_enabled"]["value"]
        instance.voice_notifications_enabled = data["voice_notifications_enabled"]["value"]
        
        # Set broadcast mode
        instance.broadcast_mode = data["broadcast_mode"]["value"]
        
        return instance


    @classmethod
    def init1(cls):
        """
        Initialize a Navigation instance with active navigation to a specified destination.
        
        Args:
            destination (str): Destination for the navigation. Defaults to "Shanghai".
            view_type (str): Map view type. Valid values are "2D view", "3D view", "Heading up", "North up".
                Defaults to "3D view".
        
        Returns:
            Navigation: An initialized Navigation instance with active navigation.
        """
        instance = cls()
        
        # Set navigation to active
        Environment.set_sound_channel("navigation")
        instance.is_active = True
        
        # Set up the current route
        instance.current_route = cls.RouteInfo(departure="Current location", destination="Shanghai")
        
        
        # Default to 3D view if invalid view type
        instance.map_view = cls.MapView.VIEW_3D
        
        # Enable voice notifications and set broadcast mode
        instance.voice_notifications_enabled = True
        instance.broadcast_mode = cls.BroadcastMode.DETAILED
        
      
        
        return instance

    @classmethod
    def init2(cls):
        """
        Initialize a Navigation instance with navigation not active.
        
        Returns:
            Navigation: An initialized Navigation instance with inactive navigation.
        """
        instance = cls()
        
        # Ensure navigation is inactive
        instance.is_active = False
        
        # Reset current route
        instance.current_route = cls.RouteInfo()
        
        # Set default map view
        instance.map_view = cls.MapView.VIEW_2D
        
        # Set default waypoints (empty list)
        instance.waypoints = []
        
        # Set default values for other properties
        instance.traffic_status_enabled = False
        instance.speed_camera_enabled = False
        instance.voice_notifications_enabled = False
        instance.broadcast_mode = cls.BroadcastMode.MUTE
        
        return instance