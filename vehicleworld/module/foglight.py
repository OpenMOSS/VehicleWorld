from enum import Enum
from utils import api

class FogLight:
    """
    Fog light entity class for managing the state and operations of vehicle fog lights.
    Fog lights are used in dense fog weather to improve visibility.
    """
    
    class Position(Enum):
        """
        Fog light position enumeration representing different position options for fog lights.
        """
        FRONT = "front"  # Front fog lights
        REAR = "rear"    # Rear fog lights
        ALL = "all"      # All fog lights
    
    class FogLightState:
        """
        Inner class for storing the state of fog lights at different positions.
        """
        def __init__(self, is_on=False):
            self._is_on = is_on
            
        @property
        def is_on(self):
            return self._is_on
            
        @is_on.setter
        def is_on(self, value):
            if not isinstance(value, bool):
                raise ValueError("Fog light state must be a boolean value")
            self._is_on = value
            
        def to_dict(self):
            return {
                "is_on": self.is_on,
                "description": "On/off state of fog lights",
                "type": type(self.is_on).__name__
            }
            
        @classmethod
        def from_dict(cls, data):
            instance = cls()
            instance.is_on = data["is_on"]
            return instance
    
    def __init__(self):
        # Initialize the state of fog lights at different positions
        self._front_light = FogLight.FogLightState()
        self._rear_light = FogLight.FogLightState()
        self._last_position = FogLight.Position.ALL  # Record the last operated position
        
    @property
    def front_light(self):
        return self._front_light
        
    @front_light.setter
    def front_light(self, value):
        if not isinstance(value, FogLight.FogLightState):
            raise ValueError("Front fog light state must be of FogLightState type")
        self._front_light = value
        
    @property
    def rear_light(self):
        return self._rear_light
        
    @rear_light.setter
    def rear_light(self, value):
        if not isinstance(value, FogLight.FogLightState):
            raise ValueError("Rear fog light state must be of FogLightState type")
        self._rear_light = value
        
    @property
    def last_position(self):
        return self._last_position
        
    @last_position.setter
    def last_position(self, value):
        if not isinstance(value, FogLight.Position):
            raise ValueError("Position must be of Position enum type")
        self._last_position = value
        
    @property
    def all_lights_on(self):
        """Get the state of whether all fog lights are on"""
        return self.front_light.is_on and self.rear_light.is_on
    
    @property
    def any_light_on(self):
        """Get the state of whether any fog light is on"""
        return self.front_light.is_on or self.rear_light.is_on
        


    def to_dict(self):
        return {
            "front_light": {
                "value": self.front_light.to_dict(),
                "description": "Front fog light status",
                "type": "FogLightState"
            },
            "rear_light": {
                "value": self.rear_light.to_dict(),
                "description": "Rear fog light status",
                "type": "FogLightState"
            },
            "last_position": {
                "value": self.last_position.value,
                "description": "The last operated fog light position, options: front, rear, all",
                "type": "Position"
            }
        }
        
    @classmethod
    def from_dict(cls, data):
        """
        Restore FogLight instance from dictionary data
        """
        instance = cls()
        
        # Restore front fog light state
        front_light_data = data.get("front_light", {}).get("value", {})
        if front_light_data:
            instance.front_light = FogLight.FogLightState.from_dict(front_light_data)
            
        # Restore rear fog light state
        rear_light_data = data.get("rear_light", {}).get("value", {})
        if rear_light_data:
            instance.rear_light = FogLight.FogLightState.from_dict(rear_light_data)
            
        # Restore last position
        last_position_value = data.get("last_position", {}).get("value", "all")
        for position in FogLight.Position:
            if position.value == last_position_value:
                instance.last_position = position
                break
                
        return instance
    
    @api("fogLight")
    def carcontrol_fogLight_switch(self, switch, position="all"):
        """
        Turn on or off fog lights, used in dense fog weather to improve visibility.
        
        Parameters:
        - switch (boolean): Fog light switch state
        - position (string): Fog light position, enum values: "front", "rear", "all", default is "all"
        
        Returns:
        - dict: Contains operation results and updated state information
        """
        # Parameter validation
        if not isinstance(switch, bool):
            raise ValueError("Switch parameter must be a boolean value")
            
        position_enum = None
        for pos in FogLight.Position:
            if pos.value == position:
                position_enum = pos
                break
                
        if position_enum is None:
            raise ValueError(f"Invalid position value: {position}. Must be 'front', 'rear', or 'all'")
            
        # Update fog light state
        self.last_position = position_enum
        
        changed_lights = []
        
        if position_enum in [FogLight.Position.FRONT, FogLight.Position.ALL]:
            if self.front_light.is_on != switch:
                self.front_light.is_on = switch
                changed_lights.append("front")
                
        if position_enum in [FogLight.Position.REAR, FogLight.Position.ALL]:
            if self.rear_light.is_on != switch:
                self.rear_light.is_on = switch
                changed_lights.append("rear")
        
        # Build response result
        result = {
            "success": True,
            "operation": "turn_on" if switch else "turn_off",
            "position": position,
            "changed_lights": changed_lights,
            "current_state": {
                "front_light_on": self.front_light.is_on,
                "rear_light_on": self.rear_light.is_on,
                "any_light_on": self.any_light_on,
                "all_lights_on": self.all_lights_on
            }
        }
        
        return result
    
    @classmethod
    def init1(cls):
        """
        Initialization method 1: Creates an instance with all fog lights off.
        
        Returns:
        - FogLight: A new FogLight instance with all fog lights in off state.
        """
        return cls()  # Use default initialization, all fog lights are off by default

    @classmethod
    def init2(cls):
        """
        Initialization method 2: Creates an instance with front fog lights on and rear fog lights off.
        
        Returns:
        - FogLight: A new FogLight instance with front fog lights on and rear fog lights off.
        """
        instance = cls()
        instance.front_light.is_on = True  # Front fog lights on
        instance.last_position = FogLight.Position.FRONT  # Record operation position as front fog lights
        return instance