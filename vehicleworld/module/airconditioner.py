from enum import Enum
from typing import List, Dict, Any, Union, Optional
from utils import api
import sys

sys.path.append("../")
from module.environment import Environment



class AirConditioner:
    """
    Main entity class representing the vehicle's air conditioning system.
    Manages multiple air conditioners across different positions in the car.
    """
    
    class Position(Enum):
        """Enum for air conditioner positions in the car."""
        DRIVER_SEAT = "driver's seat"
        PASSENGER_SEAT = "passenger seat"
        SECOND_ROW_LEFT = "second row left"
        SECOND_ROW_RIGHT = "second row right"
        THIRD_ROW_LEFT = "third row left"
        THIRD_ROW_RIGHT = "third row right"
        ALL = "all"

    class AirOutletMode(Enum):
        """Enum for air outlet modes that define where the air is directed."""
        FACE = "face"
        FEET = "feet"
        WINDOW = "window"
        FACE_AND_FEET = "face and feet"
        FACE_AND_WINDOW = "face and window"
        FEET_AND_WINDOW = "feet and window"
        RANDOM = "random"
        ALL = "all"
    
    class SweepingMode(Enum):
        """Enum for air sweeping modes that define how the air flow moves."""
        SWEEPING = "Sweeping"
        FREE_FLOW = "Free Flow"
        CUSTOM_FLOW = "Custom Flow"
        SMART_FLOW = "Smart Flow"
        AVOID_DIRECT_BLOW = "Avoid Direct Blow"
        AVOID_PEOPLE_BLOW = "Avoid People Blow"
        BLOW_TO_PEOPLE = "Blow to People"
        BLOW_TO_ME = "Blow to Me"
        BLOW_DIRECTLY = "Blow Directly"
    
    class CirculationMode(Enum):
        """Enum for air circulation modes."""
        INTERNAL = "internal circulation"
        EXTERNAL = "external circulation"
        AUTOMATIC = "automatic circulation"
        OFF = "off"
    
    class PurificationMode(Enum):
        """Enum for air purification modes."""
        AIR_PURIFICATION = "air purification"
        ION_PURIFICATION = "ion purification"
        OFF = "off"
    
    class OutletDirection(Enum):
        """Enum for air outlet direction."""
        UP = "up"
        DOWN = "down"
        LEFT = "left"
        RIGHT = "right"
    
    class TemperatureUnit(Enum):
        """Enum for temperature units."""
        LEVEL = "level"
        PERCENTAGE = "percentage"
        CELSIUS = "celsius"
    
    class WindSpeedUnit(Enum):
        """Enum for wind speed units."""
        LEVEL = "level"
        PERCENTAGE = "percentage"
    
    class AdjustmentDegree(Enum):
        """Enum for adjustment degrees in incremental changes."""
        LARGE = "large"
        LITTLE = "little"
        TINY = "tiny"
    
    class TemperatureDegree(Enum):
        """Enum for temperature preset levels."""
        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"
    
    class WindSpeedDegree(Enum):
        """Enum for wind speed preset levels."""
        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"
    
    class AirConditionerState:
        """
        Inner class representing the state of a single air conditioner unit at a specific position.
        Contains all settings and modes for the air conditioner.
        """
        
        def __init__(self, position: str, parent_system=None):
            """Initialize an air conditioner state for a specific position."""
            self._position = position
            self._is_on = False
            self._temperature = 25  # Default temperature in Celsius (range: 14-30)
            self._wind_speed = 3    # Default wind speed level (range: 1-7)
            self._child_safety_lock = False
            self._parent_system = parent_system 
            # Air flow states
            self._outlet_modes = {mode.value: False for mode in AirConditioner.AirOutletMode}
            self._sweeping_mode = None  # No default active sweeping mode
            
            # Direction
            self._outlet_direction = None  # No default direction
        
        # Position property
        @property
        def position(self) -> str:
            """Get the air conditioner position."""
            return self._position
            
        # Power state properties
        @property
        def is_on(self) -> bool:
            """Get the air conditioner power state."""
            return self._is_on
            
        @is_on.setter
        def is_on(self, value: bool):
            """Set the air conditioner power state."""
            self._is_on = value
            
        # Temperature properties
        @property
        def temperature(self) -> float:
            """Get the air conditioner temperature in Celsius."""
            return self._temperature
            
        @temperature.setter
        def temperature(self, value: float):
            """Set the air conditioner temperature in Celsius."""
            # Ensure temperature is within valid range (14-30)
            if 14 <= value <= 30:
                self._temperature = value
                # Update global environment temperature
                parent_system = self._parent_system
        
                # Update global environment temperature based on cooling/heating mode
                if parent_system:
                    if parent_system.cool_mode:
                        # Find the lowest temperature among all active air conditioners
                        min_temp = float('inf')
                        for pos, state in parent_system._ac_states.items():
                            if state.is_on:
                                min_temp = min(min_temp, state.temperature)
                        
                        # Set environment temperature to the lowest if any AC is on
                        if min_temp != float('inf'):
                            Environment.set_temperature(min_temp)
                    elif parent_system.heat_mode:
                        # Find the highest temperature among all active air conditioners
                        max_temp = float('-inf')
                        for pos, state in parent_system._ac_states.items():
                            if state.is_on:
                                max_temp = max(max_temp, state.temperature)
                        
                        # Set environment temperature to the highest if any AC is on
                        if max_temp != float('-inf'):
                            Environment.set_temperature(max_temp)
                    else:
                        # If neither cooling nor heating mode is active,
                        # just set environment temperature to this AC's temperature
                        Environment.set_temperature(value)
                
        # Wind speed properties
        @property
        def wind_speed(self) -> int:
            """Get the air conditioner wind speed level."""
            return self._wind_speed
            
        @wind_speed.setter
        def wind_speed(self, value: int):
            """Set the air conditioner wind speed level."""
            # Ensure wind speed is within valid range (1-7)
            if 1 <= value <= 7:
                self._wind_speed = value
                
        # Child safety lock properties
        @property
        def child_safety_lock(self) -> bool:
            """Get the child safety lock state."""
            return self._child_safety_lock
            
        @child_safety_lock.setter
        def child_safety_lock(self, value: bool):
            """Set the child safety lock state."""
            self._child_safety_lock = value
            
        # Outlet modes properties
        @property
        def outlet_modes(self) -> Dict[str, bool]:
            """Get all outlet modes states."""
            return self._outlet_modes.copy()
            
        def set_outlet_mode(self, mode: str, value: bool):
            """Set a specific outlet mode state."""
            if mode in self._outlet_modes:
                self._outlet_modes[mode] = value
                
        def get_outlet_mode(self, mode: str) -> bool:
            """Get a specific outlet mode state."""
            return self._outlet_modes.get(mode, False)
            
        # Sweeping mode properties
        @property
        def sweeping_mode(self) -> Optional[str]:
            """Get the current sweeping mode."""
            return self._sweeping_mode
            
        @sweeping_mode.setter
        def sweeping_mode(self, value: Optional[str]):
            """Set the sweeping mode."""
            self._sweeping_mode = value
            
        # Outlet direction properties
        @property
        def outlet_direction(self) -> Optional[str]:
            """Get the outlet direction."""
            return self._outlet_direction
            
        @outlet_direction.setter
        def outlet_direction(self, value: Optional[str]):
            """Set the outlet direction."""
            self._outlet_direction = value
            
        def to_dict(self) -> Dict[str, Any]:
            """Convert the AirConditionerState to a dictionary."""
            return {
                "position": {
                    "value": self._position,
                    "description": "Position of the air conditioner in the car",
                    "type": type(self._position).__name__
                },
                "is_on": {
                    "value": self._is_on,
                    "description": "Power state of the air conditioner",
                    "type": type(self._is_on).__name__
                },
                "temperature": {
                    "value": self._temperature,
                    "description": "Temperature setting in Celsius (range: 14-30): only change when user provides a specific numeric value or specific increment/decrement amount.  ",
                    "type": type(self._temperature).__name__
                },
                "wind_speed": {
                    "value": self._wind_speed,
                    "description": "Wind speed level (range: 1-7),: only change when user provides a specific numeric value or specific increment/decrement amount.",
                    "type": type(self._wind_speed).__name__
                },
                "child_safety_lock": {
                    "value": self._child_safety_lock,
                    "description": "Child safety lock state",
                    "type": type(self._child_safety_lock).__name__
                },
                "outlet_modes": {
                    "value": self._outlet_modes,
                    "description": f"Outlet modes states: {', '.join(AirConditioner.AirOutletMode.__members__.keys())}",
                    "type": "Dict[str, bool]"
                },
                "sweeping_mode": {
                    "value": self._sweeping_mode,
                    "description": f"Sweeping mode (options: {', '.join([mode.value for mode in AirConditioner.SweepingMode])})",
                    "type": "Optional[str]"
                },
                "outlet_direction": {
                    "value": self._outlet_direction,
                    "description": f"Outlet direction (options: {', '.join([direction.value for direction in AirConditioner.OutletDirection])})",
                    "type": "Optional[str]"
                }
            }
            
        @classmethod
        def from_dict(cls, data: Dict[str, Any],parent_system=None) -> 'AirConditioner.AirConditionerState':
            """Create an AirConditionerState instance from a dictionary."""
            state = cls(data["position"]["value"],parent_system)
            state.is_on = data["is_on"]["value"]
            state.temperature = data["temperature"]["value"]
            state.wind_speed = data["wind_speed"]["value"]
            state.child_safety_lock = data["child_safety_lock"]["value"]
            
            # Set outlet modes
            for mode, value in data["outlet_modes"]["value"].items():
                state.set_outlet_mode(mode, value)
                
            state.sweeping_mode = data["sweeping_mode"]["value"]
            state.outlet_direction = data["outlet_direction"]["value"]
            
            return state
    
    def __init__(self):
        """Initialize the air conditioner system with separate air conditioners for each position."""
        self._ac_view_open = False
        self._ac_states = {}
        
        # Mode states - moved from AirConditionerState to AirConditioner
        self._auto_mode = False
        self._ac_mode = False
        self._heat_mode = False
        self._cool_mode = False
        self._defrost_mode = False
        self._auto_defog_mode = False
        self._energy_saving_mode = False
        self._parking_ventilation_mode = False
        self._circulation_mode = AirConditioner.CirculationMode.OFF.value
        self._purification_mode = AirConditioner.PurificationMode.OFF.value
        
        # Initialize air conditioner state for each position
        for position in [pos.value for pos in self.Position if pos != self.Position.ALL]:
            self._ac_states[position] = self.AirConditionerState(position,self)
    
    @classmethod
    def init1(cls) -> 'AirConditioner':
        """
        Initialize an AirConditioner with default settings for all positions.
        All air conditioners are turned off initially.
        
        Returns:
            AirConditioner: A new air conditioner system instance with default settings.
        """
        system = cls()
        
        # Set default system-wide settings
        system.ac_view_open = False
        
        # Set default system-wide mode settings
        system._auto_mode = False
        system._ac_mode = False
        system._heat_mode = False
        system._cool_mode = True
        system._defrost_mode = False
        system._auto_defog_mode = False
        system._energy_saving_mode = False
        system._parking_ventilation_mode = False
        system._circulation_mode = cls.CirculationMode.OFF.value
        system._purification_mode = cls.PurificationMode.OFF.value
        
        # Configure each position with standard defaults
        for position in system.get_all_positions():
            ac_state = system.get_ac_state(position)
            
            # Power is off by default
            ac_state.is_on = False
            
            # Default temperature settings
            ac_state.temperature = 22.0  # Comfortable room temperature
            
            # Default wind settings
            ac_state.wind_speed = 3  # Medium-low wind speed
            
            # Safety settings
            ac_state.child_safety_lock = False
            
            # Air flow defaults
            # Reset all outlet modes to False
            for mode in [m.value for m in cls.AirOutletMode]:
                ac_state.set_outlet_mode(mode, False)
            
            # Default to face outlet
            ac_state.set_outlet_mode(cls.AirOutletMode.FACE.value, True)
            
            # Other air flow settings
            ac_state.sweeping_mode = None
            ac_state.outlet_direction = None
        
        return system

    @classmethod
    def init2(cls, auto_on: bool = True, default_temp: float = 24.0, 
            default_wind_speed: int = 4) -> 'AirConditioner':
        """
        Initialize an AirConditioner with customized settings where all air conditioners 
        are configured the same way but with specific parameters and automatically turned on.
        
        Args:
            auto_on (bool): Whether to automatically turn on all air conditioners. Default is True.
            default_temp (float): Default temperature in Celsius. Default is 24.0.
            default_wind_speed (int): Default wind speed level. Default is 4.
        
        Returns:
            AirConditioner: A new air conditioner system instance with custom settings.
        """
        system = cls()
        
        # Set UI state
        system.ac_view_open = True
        
        # Set system-wide mode settings
        system._auto_mode = True
        system._ac_mode = True
        system._heat_mode = True
        system._cool_mode = False
        system._defrost_mode = False
        system._auto_defog_mode = True
        system._energy_saving_mode = True
        system._parking_ventilation_mode = False
        system._circulation_mode = cls.CirculationMode.AUTOMATIC.value
        system._purification_mode = cls.PurificationMode.AIR_PURIFICATION.value
        
        # Configure each position with the same custom settings
        for position in system.get_all_positions():
            ac_state = system.get_ac_state(position)
            
            # Power state
            ac_state.is_on = auto_on
            
            # Temperature and wind settings
            ac_state.temperature = max(14, min(30, default_temp))  # Ensure within valid range
            ac_state.wind_speed = max(1, min(7, default_wind_speed))  # Ensure within valid range
            
            # Safety settings
            ac_state.child_safety_lock = False
            
            # Air flow settings
            # Reset all outlet modes to False first
            for mode in [m.value for m in cls.AirOutletMode]:
                ac_state.set_outlet_mode(mode, False)
            
            # Set default outlet mode
            ac_state.set_outlet_mode(cls.AirOutletMode.FACE_AND_FEET.value, True)
            
            # Other air flow settings
            ac_state.sweeping_mode = cls.SweepingMode.SMART_FLOW.value
            ac_state.outlet_direction = cls.OutletDirection.UP.value
        
        return system
    
    # Mode properties that have been moved from AirConditionerState to AirConditioner
    @property
    def auto_mode(self) -> bool:
        """Get the auto mode state."""
        return self._auto_mode
        
    @auto_mode.setter
    def auto_mode(self, value: bool):
        """Set the auto mode state."""
        self._auto_mode = value
        
    @property
    def ac_mode(self) -> bool:
        """Get the AC mode state."""
        return self._ac_mode
        
    @ac_mode.setter
    def ac_mode(self, value: bool):
        """Set the AC mode state."""
        self._ac_mode = value
        
    @property
    def heat_mode(self) -> bool:
        """Get the heat mode state."""
        return self._heat_mode
        
    @heat_mode.setter
    def heat_mode(self, value: bool):
        """Set the heat mode state."""
        self._heat_mode = value
        
    @property
    def cool_mode(self) -> bool:
        """Get the cool mode state."""
        return self._cool_mode
        
    @cool_mode.setter
    def cool_mode(self, value: bool):
        """Set the cool mode state."""
        self._cool_mode = value
        
    @property
    def defrost_mode(self) -> bool:
        """Get the defrost mode state."""
        return self._defrost_mode
        
    @defrost_mode.setter
    def defrost_mode(self, value: bool):
        """Set the defrost mode state."""
        self._defrost_mode = value
        
    @property
    def auto_defog_mode(self) -> bool:
        """Get the auto defog mode state."""
        return self._auto_defog_mode
        
    @auto_defog_mode.setter
    def auto_defog_mode(self, value: bool):
        """Set the auto defog mode state."""
        self._auto_defog_mode = value
        
    @property
    def energy_saving(self) -> bool:
        """Get the energy saving mode state."""
        return self._energy_saving_mode
        
    @energy_saving.setter
    def energy_saving(self, value: bool):
        """Set the energy saving mode state."""
        self._energy_saving_mode = value
        
    @property
    def parking_ventilation_mode(self) -> bool:
        """Get the parking ventilation mode state."""
        return self._parking_ventilation_mode
        
    @parking_ventilation_mode.setter
    def parking_ventilation_mode(self, value: bool):
        """Set the parking ventilation mode state."""
        self._parking_ventilation_mode = value
        
    @property
    def circulation_mode(self) -> str:
        """Get the circulation mode."""
        return self._circulation_mode
        
    @circulation_mode.setter
    def circulation_mode(self, value: str):
        """Set the circulation mode."""
        self._circulation_mode = value
        
    @property
    def purification_mode(self) -> str:
        """Get the purification mode."""
        return self._purification_mode
        
    @purification_mode.setter
    def purification_mode(self, value: str):
        """Set the purification mode."""
        self._purification_mode = value
        
    @property
    def ac_view_open(self) -> bool:
        """Get the state of the air conditioner control page."""
        return self._ac_view_open
        
    @ac_view_open.setter
    def ac_view_open(self, value: bool):
        """Set the state of the air conditioner control page."""
        self._ac_view_open = value
    
    def get_ac_state(self, position: str) -> 'AirConditioner.AirConditionerState':
        """Get the air conditioner state for a specific position."""
        return self._ac_states.get(position)
    
    def get_all_positions(self) -> List[str]:
        """Get all individual air conditioner positions."""
        return list(self._ac_states.keys())
    
    def resolve_positions(self, position_param: Optional[List[str]]) -> List[str]:
        """
        Resolve the positions to operate on based on input parameter.
        If 'all' is specified, returns all positions.
        If no position is specified, returns the current speaker's position.
        Otherwise, returns the specified positions.
        """
        if not position_param:
            # Default to current speaker's position
            return [Environment.get_current_speaker()]
        
        if "all" in position_param:
            # Return all individual positions
            return self.get_all_positions()
        
        # Return the specified positions
        return [pos for pos in position_param if pos in self._ac_states]
    
    def get_module_status(self):
        print(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        """Convert the AirConditioner to a dictionary."""
        return {
            "ac_view_open": {
                "value": self._ac_view_open,
                "description": "Whether the air conditioner control page is open",
                "type": type(self._ac_view_open).__name__
            },
            "ac_states": {
                "value": {position: state.to_dict() for position, state in self._ac_states.items()},
                "description": "Air conditioner states for each position",
                "type": "Dict[str, AirConditionerState]"
            },
            # Add the system-wide mode settings that were moved from AirConditionerState
            "auto_mode": {
                "value": self._auto_mode,
                "description": "Automatic mode state,you can only change the value of it when the airconditiner is open",
                "type": type(self._auto_mode).__name__
            },
            "ac_mode": {
                "value": self._ac_mode,
                "description": "AC mode state,you can only change the value of it when the airconditiner is open",
                "type": type(self._ac_mode).__name__
            },
            "heat_mode": {
                "value": self._heat_mode,
                "description": "Heat mode state,you can only change the value of it when the airconditiner is open",
                "type": type(self._heat_mode).__name__
            },
            "cool_mode": {
                "value": self._cool_mode,
                "description": "Cool mode state,you can only change the value of it when the airconditiner is open",
                "type": type(self._cool_mode).__name__
            },
            "defrost_mode": {
                "value": self._defrost_mode,
                "description": "Defrost mode state,you can only change the value of it when the airconditiner is open",
                "type": type(self._defrost_mode).__name__
            },
            "auto_defog_mode": {
                "value": self._auto_defog_mode,
                "description": "Auto defog mode state,you can only change the value of it when the airconditiner is open",
                "type": type(self._auto_defog_mode).__name__
            },
            "energy_saving_mode": {
                "value": self._energy_saving_mode,
                "description": "Energy saving mode state,you can only change the value of it when the airconditiner is open",
                "type": type(self._energy_saving_mode).__name__
            },
            "parking_ventilation_mode": {
                "value": self._parking_ventilation_mode,
                "description": "Parking ventilation mode state,you can only change the value of it when the airconditiner is open",
                "type": type(self._parking_ventilation_mode).__name__
            },
            "circulation_mode": {
                "value": self._circulation_mode,
                "description": f"Circulation mode (options: {', '.join([mode.value for mode in AirConditioner.CirculationMode])}),you can only change the value of it when the airconditiner is open",
                "type": "str"
            },
            "purification_mode": {
                "value": self._purification_mode,
                "description": f"Purification mode (options: {', '.join([mode.value for mode in AirConditioner.PurificationMode])},you can only change the value of it when the airconditiner is open)",
                "type": "str"
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AirConditioner':
        """Create an AirConditioner instance from a dictionary."""
        system = cls()
        system.ac_view_open = data["ac_view_open"]["value"]
        
        # Set system-wide mode settings
        system.auto_mode = data["auto_mode"]["value"]
        system.ac_mode = data["ac_mode"]["value"]
        system.heat_mode = data["heat_mode"]["value"]
        system.cool_mode = data["cool_mode"]["value"]
        system.defrost_mode = data["defrost_mode"]["value"]
        system.auto_defog_mode = data["auto_defog_mode"]["value"]
        system.energy_saving_mode = data["energy_saving_mode"]["value"]
        system.parking_ventilation_mode = data["parking_ventilation_mode"]["value"]
        system.circulation_mode = data["circulation_mode"]["value"]
        system.purification_mode = data["purification_mode"]["value"]
        
        # Restore states for each position
        for position, state_data in data["ac_states"]["value"].items():
            system._ac_states[position] = cls.AirConditionerState.from_dict(state_data,system)
        
        return system
    
    # API Methods Implementation
    
    @api("airConditioner")
    def child_safety_lock(self, switch: bool, position: List[str]) -> Dict[str, Any]:
        """
        Open or close the car air conditioner's child safety lock mode.
        
        Args:
            switch (bool): True to enable child safety lock, False to disable.
            position (List[str]): Positions to apply the setting. Options: 
                                  "driver's seat", "passenger seat", "second row left", 
                                  "second row right", "third row left", "third row right", "all",
                                  defaults to current speaker position.
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        positions = self.resolve_positions(position)
        results = {}
        
        for pos in positions:
            state = self.get_ac_state(pos)
            if state:
                state.child_safety_lock = switch
                results[pos] = {"success": True, "child_safety_lock": switch}
        
        return {
            "success": len(results) > 0,
            "message": f"Child safety lock {'enabled' if switch else 'disabled'} for {', '.join(positions)}",
            "results": results
        }
    
    @api("airConditioner")
    def view_switch(self, switch: bool) -> Dict[str, Any]:
        """
        Open or close the in-car air conditioner control page.
        
        Args:
            switch (bool): True to open the air conditioner page, False to close.
        
        Returns:
            Dict[str, Any]: Operation result and updated state.
        """
        self.ac_view_open = switch
        
        return {
            "success": True,
            "message": f"Air conditioner control page {'opened' if switch else 'closed'}",
            "ac_view_open": self.ac_view_open
        }
    
    @api("airConditioner")
    def switch(self, position: List[str], switch: bool) -> Dict[str, Any]:
        """
        Turn on or off the in-car air conditioner for specified positions.
        
        Args:
            position (List[str]): Positions to control. Options: 
                                 "driver's seat", "passenger seat", "second row left", 
                                 "second row right", "third row left", "third row right", "all",
                                 defaults to current speaker position
            switch (bool): True to turn on, False to turn off.
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        positions = self.resolve_positions(position)
        results = {}
        
        for pos in positions:
            state = self.get_ac_state(pos)
            if state:
                state.is_on = switch
                results[pos] = {"success": True, "is_on": switch}
        
        return {
            "success": len(results) > 0,
            "message": f"Air conditioner {'turned on' if switch else 'turned off'} for {', '.join(positions)}",
            "results": results
        }
    
    @api("airConditioner")
    def heat_mode_switch(self, switch: bool) -> Dict[str, Any]:
        """
        Turn on or off the air conditioner heating mode.
        
        Args:
            switch (bool): True to turn on heating mode, False to turn off.
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        # Check if any air conditioner is on
        any_on = False
        for pos, state in self._ac_states.items():
            if state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner is turned on, cannot adjust heating mode"}
        
        # If turning on heat mode, turn off cool mode
        if switch and self.cool_mode:
            self.cool_mode = False
        
        # Set the system-wide heat mode
        self.heat_mode = switch
        
        return {
            "success": True,
            "message": f"Heating mode {'turned on' if switch else 'turned off'} for all active air conditioners",
            "heat_mode": self.heat_mode
        }
    
    @api("airConditioner")
    def ac_mode_switch(self, switch: bool) -> Dict[str, Any]:
        """
        Turn on or off the air conditioner AC mode.
        
        Args:
            switch (bool): True to turn on AC mode, False to turn off.
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        # Check if any air conditioner is on
        any_on = False
        for pos, state in self._ac_states.items():
            if state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner is turned on, cannot adjust AC mode"}
        
        # Set the system-wide AC mode
        self.ac_mode = switch
        
        return {
            "success": True,
            "message": f"AC mode {'turned on' if switch else 'turned off'} for all active air conditioners",
            "ac_mode": self.ac_mode
        }
    
    @api("airConditioner")
    def cool_mode_switch(self, switch: bool) -> Dict[str, Any]:
        """
        Turn on or off the air conditioner cooling mode.
        
        Args:
            switch (bool): True to turn on cooling mode, False to turn off.
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        # Check if any air conditioner is on
        any_on = False
        for pos, state in self._ac_states.items():
            if state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner is turned on, cannot adjust cooling mode"}
        
        # If turning on cool mode, turn off heat mode
        if switch and self.heat_mode:
            self.heat_mode = False
        
        # Set the system-wide cool mode
        self.cool_mode = switch
        
        return {
            "success": True,
            "message": f"Cooling mode {'turned on' if switch else 'turned off'} for all active air conditioners",
            "cool_mode": self.cool_mode
        }
    
    @api("airConditioner")
    def outlet_mode(self, switch: bool, mode: str, position: List[str]) -> Dict[str, Any]:
        """
        Turn on or off specific air conditioner airflow outlet modes.
        
        Args:
            switch (bool): True to turn on the specified outlet mode, False to turn off.
            mode (str): Airflow direction. Options: "face", "feet", "window", "face and feet",
                        "face and window", "feet and window", "random", "all".
            position (List[str]): Positions to control. Options: 
                                 "driver's seat", "passenger seat", "second row left", 
                                 "second row right", "third row left", "third row right", "all",
                                 defaults to current speaker position
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        positions = self.resolve_positions(position)
        results = {}
        
        # Check if any air conditioner in the selected positions is on
        any_on = False
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner in the selected positions is turned on"}
        
        # Handle the "all" mode special case
        if mode == "all":
            modes = [m.value for m in self.AirOutletMode if m != self.AirOutletMode.ALL]
        else:
            modes = [mode]
        
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                for m in modes:
                    state.set_outlet_mode(m, switch)
                results[pos] = {"success": True, "modes": {m: switch for m in modes}}
        
        mode_str = "all outlet modes" if mode == "all" else f"'{mode}' outlet mode"
        return {
            "success": len(results) > 0,
            "message": f"{mode_str.capitalize()} {'turned on' if switch else 'turned off'} for {', '.join(positions)}",
            "results": results
        }
    
    @api("airConditioner")
    def sweeping_mode(self, switch: bool, mode: str, position: List[str]) -> Dict[str, Any]:
        """
        Turn on or off a specific air conditioner sweeping mode.
        
        Args:
            switch (bool): True to turn on the specified sweeping mode, False to turn off.
            mode (str): Sweeping mode. Options: "Sweeping", "Free Flow", "Custom Flow", 
                       "Smart Flow", "Avoid Direct Blow", "Avoid People Blow", 
                       "Blow to People", "Blow to Me", "Blow Directly".
            position (List[str]): Positions to control. Options: 
                                 "driver's seat", "passenger seat", "second row left", 
                                 "second row right", "third row left", "third row right", "all",
                                 defaults to current speaker position
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        positions = self.resolve_positions(position)
        results = {}
        
        # Check if any air conditioner in the selected positions is on
        any_on = False
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner in the selected positions is turned on"}
        
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                # If switch is True, set the mode; if False, clear it
                state.sweeping_mode = mode if switch else None
                results[pos] = {"success": True, "sweeping_mode": state.sweeping_mode}
        
        return {
            "success": len(results) > 0,
            "message": f"Sweeping mode '{mode}' {'activated' if switch else 'deactivated'} for {', '.join(positions)}",
            "results": results
        }
    
    @api("airConditioner")
    def energy_saving_mode(self, switch: bool) -> Dict[str, Any]:
        """
        Turn on or off the air conditioner energy-saving mode.
        
        Args:
            switch (bool): True to turn on energy-saving mode, False to turn off.
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        # Check if any air conditioner is on
        any_on = False
        for pos, state in self._ac_states.items():
            if state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner is turned on, cannot adjust energy-saving mode"}
        
        # Set the system-wide energy saving mode
        self.energy_saving = switch
        
        return {
            "success": True,
            "message": f"Energy-saving mode {'turned on' if switch else 'turned off'} for all active air conditioners",
            "energy_saving_mode": self.energy_saving
        }
    
    @api("airConditioner")
    def temperature_increase(self, position: List[str], value: Optional[float] = None, 
                           unit: Optional[str] = None, degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Increase the temperature of specified air conditioners.
        
        Args:
            position (List[str]): Positions to control. Options: 
                                 "driver's seat", "passenger seat", "second row left", 
                                 "second row right", "third row left", "third row right", "all",
                                 defaults to current speaker position
            value (Optional[float]): Numeric adjustment value (mutually exclusive with degree).
            unit (Optional[str]): Unit of adjustment. Options: "level", "percentage", "celsius".
            degree (Optional[str]): Degree of adjustment. Options: "large", "little", "tiny".
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        positions = self.resolve_positions(position)
        results = {}
        
        # Determine adjustment amount
        if degree:
            # Map degree to temperature change
            if degree == "large":
                temp_change = 3.0
            elif degree == "little":
                temp_change = 1.0
            else:  # tiny
                temp_change = 0.5
        elif value is not None and unit:
            if unit == "celsius":
                temp_change = value
            elif unit == "level":
                # Map level to temperature change (1 level = 1 degree)
                temp_change = value
            elif unit == "percentage":
                # Map percentage to temperature change (100% = 16 degrees range)
                temp_change = (value / 100) * 16
            else:
                temp_change = 1.0  # Default if unit is not recognized
        else:
            # Default change if neither degree nor value/unit is specified
            temp_change = 1.0
        
        # Check if any air conditioner in the selected positions is on
        any_on = False
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner in the selected positions is turned on"}
        
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                # Increase temperature but keep within valid range
                new_temp = min(30, state.temperature + temp_change)
                state.temperature = new_temp
                results[pos] = {"success": True, "temperature": new_temp}
        
        return {
            "success": len(results) > 0,
            "message": f"Temperature increased by {temp_change} degrees for {', '.join(positions)}",
            "results": results
        }
    
    @api("airConditioner")
    def temperature_decrease(self, position: List[str], value: Optional[float] = None, 
                            unit: Optional[str] = None, degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Decrease the temperature of specified air conditioners.
        
        Args:
            position (List[str]): Positions to control. Options: 
                                 "driver's seat", "passenger seat", "second row left", 
                                 "second row right", "third row left", "third row right", "all",
                                 defaults to current speaker position
            value (Optional[float]): Numeric adjustment value (mutually exclusive with degree).
            unit (Optional[str]): Unit of adjustment. Options: "level", "percentage", "celsius".
            degree (Optional[str]): Degree of adjustment. Options: "large", "little", "tiny".
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        positions = self.resolve_positions(position)
        results = {}
        
        # Determine adjustment amount
        if degree:
            # Map degree to temperature change
            if degree == "large":
                temp_change = 3.0
            elif degree == "little":
                temp_change = 1.0
            else:  # tiny
                temp_change = 0.5
        elif value is not None and unit:
            if unit == "celsius":
                temp_change = value
            elif unit == "level":
                # Map level to temperature change (1 level = 1 degree)
                temp_change = value
            elif unit == "percentage":
                # Map percentage to temperature change (100% = 16 degrees range)
                temp_change = (value / 100) * 16
            else:
                temp_change = 1.0  # Default if unit is not recognized
        else:
            # Default change if neither degree nor value/unit is specified
            temp_change = 1.0
        
        # Check if any air conditioner in the selected positions is on
        any_on = False
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner in the selected positions is turned on"}
        
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                # Decrease temperature but keep within valid range
                new_temp = max(14, state.temperature - temp_change)
                state.temperature = new_temp
                results[pos] = {"success": True, "temperature": new_temp}
        
        return {
            "success": len(results) > 0,
            "message": f"Temperature decreased by {temp_change} degrees for {', '.join(positions)}",
            "results": results
        }
    
    @api("airConditioner")
    def temperature_set(self, position: List[str], value: Optional[float] = None, 
                        unit: Optional[str] = None, degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Set the temperature of specified air conditioners to a specific value.
        
        Args:
            position (List[str]): Positions to control. Options: 
                                 "driver's seat", "passenger seat", "second row left", 
                                 "second row right", "third row left", "third row right", "all",
                                 defaults to current speaker position
            value (Optional[float]): Numeric temperature value (mutually exclusive with degree).
            unit (Optional[str]): Unit of temperature. Options: "level", "percentage", "celsius".
            degree (Optional[str]): Temperature level. Options: "max", "high", "medium", "low", "min".
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        positions = self.resolve_positions(position)
        results = {}
        
        # Determine target temperature
        if degree:
            # Map degree to temperature
            if degree == "max":
                target_temp = 30.0
            elif degree == "high":
                target_temp = 26.0
            elif degree == "medium":
                target_temp = 22.0
            elif degree == "low":
                target_temp = 18.0
            else:  # min
                target_temp = 14.0
        elif value is not None and unit:
            if unit == "celsius":
                # Ensure temperature is within valid range
                target_temp = max(14, min(30, value))
            elif unit == "level":
                # Map level to temperature (level 1-7 maps to 14-30)
                level_range = (30 - 14) / 6  # 6 steps for 7 levels
                target_temp = 14 + min(6, max(0, value - 1)) * level_range
            elif unit == "percentage":
                # Map percentage to temperature (0% = 14, 100% = 30)
                target_temp = 14 + (value / 100) * (30 - 14)
            else:
                target_temp = 22.0  # Default if unit is not recognized
        else:
            # Default temperature if neither degree nor value/unit is specified
            target_temp = 22.0
        
        # Ensure temperature is within valid range
        target_temp = max(14, min(30, target_temp))
        
        # Check if any air conditioner in the selected positions is on
        any_on = False
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner in the selected positions is turned on"}
        
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                state.temperature = target_temp
                results[pos] = {"success": True, "temperature": target_temp}
        
        return {
            "success": len(results) > 0,
            "message": f"Temperature set to {target_temp} degrees for {', '.join(positions)}",
            "results": results
        }
    
    @api("airConditioner")
    def wind_speed_increase(self, position: List[str], value: Optional[float] = None, 
                           unit: Optional[str] = None, degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Increase the wind speed of specified air conditioners.
        
        Args:
            position (List[str]): Positions to control. Options: 
                                 "driver's seat", "passenger seat", "second row left", 
                                 "second row right", "third row left", "third row right", "all",
                                 defaults to current speaker position
            value (Optional[float]): Numeric adjustment value (mutually exclusive with degree).
            unit (Optional[str]): Unit of adjustment. Options: "level", "percentage".
            degree (Optional[str]): Degree of adjustment. Options: "large", "little", "tiny".
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        positions = self.resolve_positions(position)
        results = {}
        
        # Determine adjustment amount
        if degree:
            # Map degree to wind speed change
            if degree == "large":
                speed_change = 3
            elif degree == "little":
                speed_change = 2
            else:  # tiny
                speed_change = 1
        elif value is not None and unit:
            if unit == "level":
                speed_change = int(value)
            elif unit == "percentage":
                # Map percentage to wind speed change (100% = 7 levels)
                speed_change = int((value / 100) * 7)
            else:
                speed_change = 1  # Default if unit is not recognized
        else:
            # Default change if neither degree nor value/unit is specified
            speed_change = 1
        
        # Check if any air conditioner in the selected positions is on
        any_on = False
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner in the selected positions is turned on"}
        
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                # Increase wind speed but keep within valid range
                new_speed = min(7, state.wind_speed + speed_change)
                state.wind_speed = new_speed
                results[pos] = {"success": True, "wind_speed": new_speed}
        
        return {
            "success": len(results) > 0,
            "message": f"Wind speed increased by {speed_change} levels for {', '.join(positions)}",
            "results": results
        }
    
    @api("airConditioner")
    def wind_speed_decrease(self, position: List[str], value: Optional[float] = None, 
                           unit: Optional[str] = None, degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Decrease the wind speed of specified air conditioners.
        
        Args:
            position (List[str]): Positions to control. Options: 
                                 "driver's seat", "passenger seat", "second row left", 
                                 "second row right", "third row left", "third row right", "all",
                                 defaults to current speaker position
            value (Optional[float]): Numeric adjustment value (mutually exclusive with degree).
            unit (Optional[str]): Unit of adjustment. Options: "level", "percentage".
            degree (Optional[str]): Degree of adjustment. Options: "large", "little", "tiny".
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        positions = self.resolve_positions(position)
        results = {}
        
        # Determine adjustment amount
        if degree:
            # Map degree to wind speed change
            if degree == "large":
                speed_change = 3
            elif degree == "little":
                speed_change = 2
            else:  # tiny
                speed_change = 1
        elif value is not None and unit:
            if unit == "level":
                speed_change = int(value)
            elif unit == "percentage":
                # Map percentage to wind speed change (100% = 7 levels)
                speed_change = int((value / 100) * 7)
            else:
                speed_change = 1  # Default if unit is not recognized
        else:
            # Default change if neither degree nor value/unit is specified
            speed_change = 1
        
        # Check if any air conditioner in the selected positions is on
        any_on = False
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner in the selected positions is turned on"}
        
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                # Decrease wind speed but keep within valid range
                new_speed = max(1, state.wind_speed - speed_change)
                state.wind_speed = new_speed
                results[pos] = {"success": True, "wind_speed": new_speed}
        
        return {
            "success": len(results) > 0,
            "message": f"Wind speed decreased by {speed_change} levels for {', '.join(positions)}",
            "results": results
        }
    
    @api("airConditioner")
    def wind_speed_set(self, position: List[str], value: Optional[float] = None, 
                      unit: Optional[str] = None, degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Set the wind speed of specified air conditioners to a specific value.
        
        Args:
            position (List[str]): Positions to control. Options: 
                                 "driver's seat", "passenger seat", "second row left", 
                                 "second row right", "third row left", "third row right", "all",
                                 defaults to current speaker position
            value (Optional[float]): Numeric wind speed value (mutually exclusive with degree).
            unit (Optional[str]): Unit of wind speed. Options: "level", "percentage".
            degree (Optional[str]): Wind speed level. Options: "max", "high", "medium", "low", "min".
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        positions = self.resolve_positions(position)
        results = {}
        
        # Determine target wind speed
        if degree:
            # Map degree to wind speed
            if degree == "max":
                target_speed = 7
            elif degree == "high":
                target_speed = 5
            elif degree == "medium":
                target_speed = 4
            elif degree == "low":
                target_speed = 2
            else:  # min
                target_speed = 1
        elif value is not None and unit:
            if unit == "level":
                # Ensure wind speed is within valid range
                target_speed = int(max(1, min(7, value)))
            elif unit == "percentage":
                # Map percentage to wind speed (0% = 1, 100% = 7)
                target_speed = int(1 + (value / 100) * 6)
            else:
                target_speed = 4  # Default if unit is not recognized
        else:
            # Default wind speed if neither degree nor value/unit is specified
            target_speed = 4
        
        # Ensure wind speed is within valid range
        target_speed = max(1, min(7, target_speed))
        
        # Check if any air conditioner in the selected positions is on
        any_on = False
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner in the selected positions is turned on"}
        
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                state.wind_speed = target_speed
                results[pos] = {"success": True, "wind_speed": target_speed}
        
        return {
            "success": len(results) > 0,
            "message": f"Wind speed set to level {target_speed} for {', '.join(positions)}",
            "results": results
        }
    
    @api("airConditioner")
    def auto_mode_switch(self, switch: bool) -> Dict[str, Any]:
        """
        Turn on or off the air conditioner auto mode.
        
        Args:
            switch (bool): True to turn on auto mode, False to turn off.
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        # Check if any air conditioner is on
        any_on = False
        for pos, state in self._ac_states.items():
            if state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner is turned on, cannot adjust auto mode"}
        
        # Set the system-wide auto mode
        self.auto_mode = switch
        
        return {
            "success": True,
            "message": f"Auto mode {'turned on' if switch else 'turned off'} for all active air conditioners",
            "auto_mode": self.auto_mode
        }
    
    @api("airConditioner")
    def defrost_mode_switch(self, switch: bool) -> Dict[str, Any]:
        """
        Turn on or off the defrost and dehumidifying function.
        
        Args:
            switch (bool): True to turn on defrost, False to turn off.
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        # Check if any air conditioner is on
        any_on = False
        for pos, state in self._ac_states.items():
            if state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner is turned on, cannot adjust defrost mode"}
        
        # Set the system-wide defrost mode
        self.defrost_mode = switch
        
        return {
            "success": True,
            "message": f"Defrost mode {'turned on' if switch else 'turned off'} for all active air conditioners",
            "defrost_mode": self.defrost_mode
        }
    
    @api("airConditioner")
    def recycle_mode_switch(self, mode: str) -> Dict[str, Any]:
        """
        Turn on or off specific air conditioning circulation modes.
        
        Args:
            mode (str): The circulation mode. Options: "internal circulation", 
                       "external circulation", "automatic circulation", "off".
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        # Check if any air conditioner is on
        any_on = False
        for pos, state in self._ac_states.items():
            if state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner is turned on, cannot adjust circulation mode"}
        
        # Set the system-wide circulation mode
        self.circulation_mode = mode
        
        mode_description = "disabled" if mode == "off" else f"set to '{mode}'"
        return {
            "success": True,
            "message": f"Circulation mode {mode_description} for all active air conditioners",
            "circulation_mode": self.circulation_mode
        }
    
    @api("airConditioner")
    def outlet_direction_switch(self, position: List[str], direction: str) -> Dict[str, Any]:
        """
        Adjust the direction of the air conditioning outlet.
        
        Args:
            position (List[str]): Positions to control. Options: 
                                 "driver's seat", "passenger seat", "second row left", 
                                 "second row right", "third row left", "third row right", "all",
                                 defaults to current speaker position
            direction (str): The direction of the air outlet. Options: "up", "down", "left", "right".
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        positions = self.resolve_positions(position)
        results = {}
        
        # Check if any air conditioner in the selected positions is on
        any_on = False
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner in the selected positions is turned on"}
        
        for pos in positions:
            state = self.get_ac_state(pos)
            if state and state.is_on:
                state.outlet_direction = direction
                results[pos] = {"success": True, "outlet_direction": direction}
        
        return {
            "success": len(results) > 0,
            "message": f"Outlet direction set to '{direction}' for {', '.join(positions)}",
            "results": results
        }
    
    @api("airConditioner")
    def parking_ventilation(self, switch: bool) -> Dict[str, Any]:
        """
        Turn on or off the air conditioner's parking ventilation mode.
        
        Args:
            switch (bool): True to turn on parking ventilation, False to turn off.
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        # Check if any air conditioner is on
        any_on = False
        for pos, state in self._ac_states.items():
            if state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner is turned on, cannot adjust parking ventilation mode"}
        
        # Set the system-wide parking ventilation mode
        self.parking_ventilation_mode = switch
        
        return {
            "success": True,
            "message": f"Parking ventilation mode {'turned on' if switch else 'turned off'} for all active air conditioners",
            "parking_ventilation_mode": self.parking_ventilation_mode
        }
    
    @api("airConditioner")
    def auto_defog_switch(self, switch: bool) -> Dict[str, Any]:
        """
        Turn on or off the air conditioner's automatic defog mode.
        
        Args:
            switch (bool): True to turn on automatic defog, False to turn off.
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        # Check if any air conditioner is on
        any_on = False
        for pos, state in self._ac_states.items():
            if state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner is turned on, cannot adjust auto defog mode"}
        
        # Set the system-wide auto defog mode
        self.auto_defog_mode = switch
        
        return {
            "success": True,
            "message": f"Automatic defog mode {'turned on' if switch else 'turned off'} for all active air conditioners",
            "auto_defog_mode": self.auto_defog_mode
        }
    
    @api("airConditioner")
    def purification_switch(self, mode: str) -> Dict[str, Any]:
        """
        Turn on or off the air conditioner's air purification mode.
        
        Args:
            mode (str): The air purification mode. Options: "air purification", 
                      "ion purification", "off".
        
        Returns:
            Dict[str, Any]: Operation result and updated states.
        """
        # Check if any air conditioner is on
        any_on = False
        for pos, state in self._ac_states.items():
            if state.is_on:
                any_on = True
                break
        
        if not any_on:
            return {"success": False, "message": "No air conditioner is turned on, cannot adjust purification mode"}
        
        # Set the system-wide purification mode
        self.purification_mode = mode
        
        mode_description = "disabled" if mode == "off" else f"set to '{mode}'"
        return {
            "success": True,
            "message": f"Purification mode {mode_description} for all active air conditioners",
            "purification_mode": self.purification_mode
        }