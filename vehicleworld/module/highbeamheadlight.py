from utils import api
from enum import Enum
from typing import Dict, Any, Union, Optional, List, Tuple

class HighBeamHeadlight:
    class DelayOffDurationDegree(Enum):
        """
        Enumeration representing the degree options for delay off duration.
        """
        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"
    
    class ExtensionDegree(Enum):
        """
        Enumeration representing the degree options for extending or shortening duration.
        """
        LARGE = "large"
        LITTLE = "little"
        TINY = "tiny"
    
    class TimeUnit(Enum):
        """
        Enumeration representing time units for duration.
        """
        HOUR = "hour"
        MINUTE = "minute"
        SECOND = "second"
    
    # Duration mapping in seconds for each degree
    _DEGREE_DURATION_MAPPING = {
        DelayOffDurationDegree.MAX: 300,  # 5 minutes
        DelayOffDurationDegree.HIGH: 180,  # 3 minutes
        DelayOffDurationDegree.MEDIUM: 120,  # 2 minutes
        DelayOffDurationDegree.LOW: 60,  # 1 minute
        DelayOffDurationDegree.MIN: 30,  # 30 seconds
    }
    
    # Extension mapping in seconds for each degree
    _EXTENSION_DURATION_MAPPING = {
        ExtensionDegree.LARGE: 60,  # 1 minute
        ExtensionDegree.LITTLE: 30,  # 30 seconds
        ExtensionDegree.TINY: 10,  # 10 seconds
    }
    
    # Conversion factors to seconds
    _TIME_UNIT_CONVERSION = {
        TimeUnit.HOUR: 3600,
        TimeUnit.MINUTE: 60,
        TimeUnit.SECOND: 1,
    }
    
    def __init__(self):
        # Initialize with default values
        self._high_beam_on = False
        self._delay_off_enabled = False
        self._delay_off_duration_seconds = 60  # Default: 1 minute
        
        # System constraints
        self._min_delay_duration = 5  # Minimum 5 seconds
        self._max_delay_duration = 300  # Maximum 5 minutes (300 seconds)
    
    # High beam on/off property
    @property
    def high_beam_on(self) -> bool:
        return self._high_beam_on
    
    @high_beam_on.setter
    def high_beam_on(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("High beam state must be a boolean")
        self._high_beam_on = value
    
    # Delay off enabled property
    @property
    def delay_off_enabled(self) -> bool:
        return self._delay_off_enabled
    
    @delay_off_enabled.setter
    def delay_off_enabled(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("Delay off enabled state must be a boolean")
        self._delay_off_enabled = value
    
    # Delay off duration property
    @property
    def delay_off_duration_seconds(self) -> int:
        return self._delay_off_duration_seconds
    
    @delay_off_duration_seconds.setter
    def delay_off_duration_seconds(self, value: int):
        if not isinstance(value, (int, float)):
            raise TypeError("Delay off duration must be a number")
        
        # Enforce min/max constraints
        value = max(self._min_delay_duration, min(self._max_delay_duration, int(value)))
        self._delay_off_duration_seconds = value
    
    # Helper method to convert time to seconds
    def _convert_to_seconds(self, value: float, unit: TimeUnit) -> int:
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be a number")
        if not isinstance(unit, self.TimeUnit):
            raise TypeError("Unit must be a valid TimeUnit enum")
        
        return int(value * self._TIME_UNIT_CONVERSION[unit])
    
    # API implementation methods
    @api("highBeamHeadlight")
    def switch(self, switch: bool) -> Dict[str, Any]:
        """
        Turn the vehicle's high beam headlights on or off.
        
        Args:
            switch (bool): True to turn on, False to turn off
            
        Returns:
            Dict: Operation result and current state
        """
        try:
            self.high_beam_on = switch
            return {
                "success": True,
                "status": "High beam headlight turned " + ("on" if switch else "off"),
                "current_state": {
                    "high_beam_on": self.high_beam_on
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("highBeamHeadlight")
    def delay_close(self, switch: bool) -> Dict[str, Any]:
        """
        Set the headlight delay off function.
        
        Args:
            switch (bool): True to enable, False to disable
            
        Returns:
            Dict: Operation result and current state
        """
        try:
            self.delay_off_enabled = switch
            return {
                "success": True,
                "status": "Headlight delay off function " + ("enabled" if switch else "disabled"),
                "current_state": {
                    "delay_off_enabled": self.delay_off_enabled,
                    "delay_off_duration_seconds": self.delay_off_duration_seconds
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("highBeamHeadlight")
    def set_delay_close_duration(self, 
                                 value: Optional[float] = None, 
                                 unit: Optional[str] = None, 
                                 degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Set the duration of headlight delay off.
        
        Args:
            value (float, optional): Numerical part of the duration value
            unit (str, optional): Unit of time ('hour', 'minute', 'second')
            degree (str, optional): Degree of duration ('max', 'high', 'medium', 'low', 'min')
                                  
        Note:
            Either (value + unit) OR degree must be provided, not both.
            If degree is provided, it must be one of: 'max', 'high', 'medium', 'low', 'min'
            If unit is provided, it must be one of: 'hour', 'minute', 'second'
            
        Returns:
            Dict: Operation result and current state
        """
        try:
            # Input validation
            if (value is not None and unit is not None) and degree is not None:
                raise ValueError("Cannot provide both numeric value and degree")
            
            if (value is None or unit is None) and degree is None:
                raise ValueError("Must provide either numeric value with unit or degree")
            
            # Set by degree
            if degree is not None:
                try:
                    degree_enum = self.DelayOffDurationDegree(degree)
                    new_duration = self._DEGREE_DURATION_MAPPING[degree_enum]
                    self.delay_off_duration_seconds = new_duration
                    status_msg = f"Set delay off duration to {degree} ({new_duration} seconds)"
                except ValueError:
                    valid_options = [e.value for e in self.DelayOffDurationDegree]
                    raise ValueError(f"Invalid degree value. Must be one of: {valid_options}")
            
            # Set by value and unit
            else:
                try:
                    unit_enum = self.TimeUnit(unit)
                    seconds = self._convert_to_seconds(value, unit_enum)
                    self.delay_off_duration_seconds = seconds
                    status_msg = f"Set delay off duration to {value} {unit} ({seconds} seconds)"
                except ValueError:
                    valid_units = [e.value for e in self.TimeUnit]
                    raise ValueError(f"Invalid unit value. Must be one of: {valid_units}")
            
            return {
                "success": True,
                "status": status_msg,
                "current_state": {
                    "delay_off_enabled": self.delay_off_enabled,
                    "delay_off_duration_seconds": self.delay_off_duration_seconds
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("highBeamHeadlight")
    def increase_delay_close_duration(self,
                                      value: Optional[float] = None,
                                      unit: Optional[str] = None,
                                      degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Extend the duration of headlight delay off.
        
        Args:
            value (float, optional): Numerical value to extend by
            unit (str, optional): Unit of time ('hour', 'minute', 'second')
            degree (str, optional): Degree of extension ('large', 'little', 'tiny')
            
        Note:
            If degree is provided, it must be one of: 'large', 'little', 'tiny'
            If unit is provided, it must be one of: 'hour', 'minute', 'second'
            
        Returns:
            Dict: Operation result and current state
        """
        try:
            # Default extension if no parameters provided
            if value is None and unit is None and degree is None:
                degree = "little"  # Default to little increase
            
            current_duration = self.delay_off_duration_seconds
            seconds_to_add = 0
            
            # Extend by degree
            if degree is not None:
                try:
                    degree_enum = self.ExtensionDegree(degree)
                    seconds_to_add = self._EXTENSION_DURATION_MAPPING[degree_enum]
                    status_detail = f"by {degree} increment ({seconds_to_add} seconds)"
                except ValueError:
                    valid_options = [e.value for e in self.ExtensionDegree]
                    raise ValueError(f"Invalid degree value. Must be one of: {valid_options}")
            
            # Extend by value and unit
            elif value is not None and unit is not None:
                try:
                    unit_enum = self.TimeUnit(unit)
                    seconds_to_add = self._convert_to_seconds(value, unit_enum)
                    status_detail = f"by {value} {unit}"
                except ValueError:
                    valid_units = [e.value for e in self.TimeUnit]
                    raise ValueError(f"Invalid unit value. Must be one of: {valid_units}")
            else:
                raise ValueError("Must provide either value and unit, or degree")
            
            # Apply the extension
            new_duration = current_duration + seconds_to_add
            self.delay_off_duration_seconds = new_duration
            
            return {
                "success": True,
                "status": f"Increased delay off duration {status_detail}",
                "current_state": {
                    "previous_duration_seconds": current_duration,
                    "current_duration_seconds": self.delay_off_duration_seconds,
                    "increase_amount_seconds": seconds_to_add
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("highBeamHeadlight")
    def decrease_delay_close_duration(self,
                                      value: Optional[float] = None,
                                      unit: Optional[str] = None,
                                      degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Shorten the duration of headlight delay off.
        
        Args:
            value (float, optional): Numerical value to shorten by
            unit (str, optional): Unit of time ('hour', 'minute', 'second')
            degree (str, optional): Degree of shortening ('large', 'little', 'tiny')
            
        Note:
            If degree is provided, it must be one of: 'large', 'little', 'tiny'
            If unit is provided, it must be one of: 'hour', 'minute', 'second'
            
        Returns:
            Dict: Operation result and current state
        """
        try:
            # Default decrease if no parameters provided
            if value is None and unit is None and degree is None:
                degree = "little"  # Default to little decrease
            
            current_duration = self.delay_off_duration_seconds
            seconds_to_subtract = 0
            
            # Decrease by degree
            if degree is not None:
                try:
                    degree_enum = self.ExtensionDegree(degree)
                    seconds_to_subtract = self._EXTENSION_DURATION_MAPPING[degree_enum]
                    status_detail = f"by {degree} increment ({seconds_to_subtract} seconds)"
                except ValueError:
                    valid_options = [e.value for e in self.ExtensionDegree]
                    raise ValueError(f"Invalid degree value. Must be one of: {valid_options}")
            
            # Decrease by value and unit
            elif value is not None and unit is not None:
                try:
                    unit_enum = self.TimeUnit(unit)
                    seconds_to_subtract = self._convert_to_seconds(value, unit_enum)
                    status_detail = f"by {value} {unit}"
                except ValueError:
                    valid_units = [e.value for e in self.TimeUnit]
                    raise ValueError(f"Invalid unit value. Must be one of: {valid_units}")
            else:
                raise ValueError("Must provide either value and unit, or degree")
            
            # Apply the decrease
            new_duration = max(self._min_delay_duration, current_duration - seconds_to_subtract)
            self.delay_off_duration_seconds = new_duration
            
            # Calculate actual amount decreased (might be limited by minimum constraint)
            actual_decrease = current_duration - new_duration
            
            return {
                "success": True,
                "status": f"Decreased delay off duration {status_detail}",
                "current_state": {
                    "previous_duration_seconds": current_duration,
                    "current_duration_seconds": self.delay_off_duration_seconds,
                    "decrease_amount_seconds": actual_decrease
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    


    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the class instance to a dictionary representation with values, types, and descriptions.
        
        Returns:
            Dict: Dictionary containing class attributes, types, and descriptions
        """
        return {
            "high_beam_on": {
                "value": self.high_beam_on,
                "description": "Current state of high beam headlights (on/off)",
                "type": type(self.high_beam_on).__name__
            },
            "delay_off_enabled": {
                "value": self.delay_off_enabled,
                "description": "Whether the headlight delay off function is enabled",
                "type": type(self.delay_off_enabled).__name__
            },
            "delay_off_duration_seconds": {
                "value": self.delay_off_duration_seconds,
                "description": "Duration in seconds for which headlights remain on after vehicle is turned off",
                "type": type(self.delay_off_duration_seconds).__name__
            },
            "system_constraints": {
                "value": {
                    "min_delay_duration": self._min_delay_duration,
                    "max_delay_duration": self._max_delay_duration
                },
                "description": "System constraints for delay off duration (seconds)",
                "type": "dict"
            },
            "delay_off_duration_degree_options": {
                "value": [degree.value for degree in self.DelayOffDurationDegree],
                "description": "Available degree options for setting delay off duration (max, high, medium, low, min)",
                "type": "list"
            },
            "extension_degree_options": {
                "value": [degree.value for degree in self.ExtensionDegree],
                "description": "Available degree options for extending/shortening duration (large, little, tiny)",
                "type": "list"
            },
            "time_unit_options": {
                "value": [unit.value for unit in self.TimeUnit],
                "description": "Available time units for specifying durations (hour, minute, second)",
                "type": "list"
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HighBeamHeadlight':
        """
        Create a class instance from a dictionary representation.
        
        Args:
            data (Dict): Dictionary containing class attributes
            
        Returns:
            HighBeamHeadlight: New instance with restored attributes
        """
        instance = cls()
        
        # Restore basic properties
        if "high_beam_on" in data:
            instance.high_beam_on = data["high_beam_on"]["value"]
        
        if "delay_off_enabled" in data:
            instance.delay_off_enabled = data["delay_off_enabled"]["value"]
        
        if "delay_off_duration_seconds" in data:
            instance.delay_off_duration_seconds = data["delay_off_duration_seconds"]["value"]
        
        # Restore system constraints if present
        if "system_constraints" in data and "value" in data["system_constraints"]:
            constraints = data["system_constraints"]["value"]
            if "min_delay_duration" in constraints:
                instance._min_delay_duration = constraints["min_delay_duration"]
            if "max_delay_duration" in constraints:
                instance._max_delay_duration = constraints["max_delay_duration"]
        
        return instance
    
    @classmethod
    def init1(cls) -> 'HighBeamHeadlight':
        """
        Initialize a HighBeamHeadlight instance with night driving configuration.
        
        This configuration sets high beam on, delay off enabled, and a medium
        delay duration of 2 minutes (120 seconds).
        
        Returns:
            HighBeamHeadlight: New instance with night driving configuration
        """
        instance = cls()
        instance.high_beam_on = True
        instance.delay_off_enabled = True
        instance.delay_off_duration_seconds = cls._DEGREE_DURATION_MAPPING[cls.DelayOffDurationDegree.MEDIUM]  # 120 seconds
        return instance

    @classmethod
    def init2(cls) -> 'HighBeamHeadlight':
        """
        Initialize a HighBeamHeadlight instance with daytime safety configuration.
        
        This configuration sets high beam off, delay off enabled, and a maximum
        delay duration of 5 minutes (300 seconds) for maximum visibility when needed.
        
        Returns:
            HighBeamHeadlight: New instance with daytime safety configuration
        """
        instance = cls()
        instance.high_beam_on = False
        instance.delay_off_enabled = True
        instance.delay_off_duration_seconds = cls._DEGREE_DURATION_MAPPING[cls.DelayOffDurationDegree.MAX]  # 300 seconds
        return instance