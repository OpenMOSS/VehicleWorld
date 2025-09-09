from module.environment import Environment
from utils import api
from enum import Enum

class OverheadScreen:
    """
    Entity class representing an overhead screen device in a vehicle.
    Controls screen state, brightness, language and time display format.
    """
    
    class BrightnessUnit(Enum):
        """Enumeration for brightness adjustment units"""
        GEAR = "gear"
        PERCENTAGE = "percentage"
        NIT = "nit"
    
    class BrightnessAdjustmentDegree(Enum):
        """Enumeration for brightness adjustment degrees"""
        LARGE = "large"
        LITTLE = "little"
        TINY = "tiny"
    
    class BrightnessLevel(Enum):
        """Enumeration for brightness levels"""
        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"
    
    class ScreenState(Enum):
        """Enumeration for overhead screen states"""
        OPEN = "open"
        CLOSED = "close"
      
    
    def __init__(self):
        # Screen state properties
        self._state = self.ScreenState.CLOSED
        
        # Brightness properties
        self._brightness_percentage = 50.0  # Default 50%
        self._brightness_gear = 3  # Default gear 3 (assuming 1-5 scale)
        self._brightness_nit = 250  # Default 250 nits
        self._current_brightness_unit = self.BrightnessUnit.PERCENTAGE
        
        # Brightness level mapping (percentage equivalents)
        self._brightness_level_mapping = {
            self.BrightnessLevel.MAX: 100.0,
            self.BrightnessLevel.HIGH: 75.0,
            self.BrightnessLevel.MEDIUM: 50.0,
            self.BrightnessLevel.LOW: 25.0,
            self.BrightnessLevel.MIN: 10.0
        }
        
        # Adjustment degree mapping (percentage increments)
        self._adjustment_degree_mapping = {
            self.BrightnessAdjustmentDegree.TINY: 5.0,
            self.BrightnessAdjustmentDegree.LITTLE: 10.0,
            self.BrightnessAdjustmentDegree.LARGE: 20.0
        }
        
        # Unit conversion rates
        self._max_gear = 5
        self._max_nit = 500
    
    # State property
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        if isinstance(value, self.ScreenState):
            self._state = value
        else:
            raise ValueError(f"State must be a ScreenState enum value, got {type(value)}")
    
    # Brightness percentage property
    @property
    def brightness_percentage(self):
        return self._brightness_percentage
    
    @brightness_percentage.setter
    def brightness_percentage(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f"Brightness percentage must be a number, got {type(value)}")
        
        # Clamp value between 0 and 100
        self._brightness_percentage = max(0.0, min(100.0, float(value)))
        
        # Update other brightness units
        self._sync_brightness_units()
    
    # Brightness gear property
    @property
    def brightness_gear(self):
        return self._brightness_gear
    
    @brightness_gear.setter
    def brightness_gear(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f"Brightness gear must be a number, got {type(value)}")
        
        # Clamp value between 0 and max gear
        self._brightness_gear = max(0, min(self._max_gear, int(value)))
        
        # Convert to percentage and update
        self._brightness_percentage = (self._brightness_gear / self._max_gear) * 100.0
        self._sync_brightness_units()
    
    # Brightness nit property
    @property
    def brightness_nit(self):
        return self._brightness_nit
    
    @brightness_nit.setter
    def brightness_nit(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f"Brightness nit must be a number, got {type(value)}")
        
        # Clamp value between 0 and max nit
        self._brightness_nit = max(0.0, min(self._max_nit, float(value)))
        
        # Convert to percentage and update
        self._brightness_percentage = (self._brightness_nit / self._max_nit) * 100.0
        self._sync_brightness_units()
    
    # Current brightness unit property
    @property
    def current_brightness_unit(self):
        return self._current_brightness_unit
    
    @current_brightness_unit.setter
    def current_brightness_unit(self, value):
        if isinstance(value, self.BrightnessUnit):
            self._current_brightness_unit = value
        else:
            raise ValueError(f"Current brightness unit must be a BrightnessUnit enum value, got {type(value)}")
    
    def _sync_brightness_units(self):
        """Synchronize all brightness units based on the percentage value"""
        self._brightness_gear = round((self._brightness_percentage / 100.0) * self._max_gear)
        self._brightness_nit = (self._brightness_percentage / 100.0) * self._max_nit
    
    def _get_brightness_value_by_unit(self, unit):
        """Get brightness value according to the specified unit"""
        if unit == self.BrightnessUnit.GEAR:
            return self._brightness_gear
        elif unit == self.BrightnessUnit.PERCENTAGE:
            return self._brightness_percentage
        elif unit == self.BrightnessUnit.NIT:
            return self._brightness_nit
        else:
            raise ValueError(f"Invalid brightness unit: {unit}")
    
    def _adjust_brightness_by_degree(self, degree, increase=True):
        """Adjust brightness by degree (tiny, little, large)"""
        if not isinstance(degree, self.BrightnessAdjustmentDegree):
            raise ValueError(f"Degree must be a BrightnessAdjustmentDegree enum value, got {type(degree)}")
        
        adjustment = self._adjustment_degree_mapping[degree]
        if not increase:
            adjustment = -adjustment
        
        self.brightness_percentage = self._brightness_percentage + adjustment
    
    def _set_brightness_by_level(self, level):
        """Set brightness by predefined level (max, high, medium, low, min)"""
        if not isinstance(level, self.BrightnessLevel):
            raise ValueError(f"Level must be a BrightnessLevel enum value, got {type(level)}")
        
        self.brightness_percentage = self._brightness_level_mapping[level]
    
    # API Methods
    @api("overheadScreen")
    def carcontrol_overheadScreen_timeDisplayFormat_set(self, mode):
        """
        Set the time display format on the overhead screen.
        
        Args:
            mode (str): Time display format options. Enum values: ["12-hour format", "24-hour format"]
            
        Returns:
            dict: Operation result and current state
        """
        if self.state != self.ScreenState.OPEN:
            return {
                "success": False,
                "error": "Operation failed: Overhead screen must be open to perform this action"
            }
            
        if mode not in ["12-hour format", "24-hour format"]:
            return {
                "success": False,
                "error": f"Invalid time display format: {mode}. Must be one of: '12-hour format', '24-hour format'"
            }
        
        # Update environment time display format
        Environment.set_time_display_format(mode)
        
        return {
            "success": True,
            "current_time_format": Environment.get_time_display_format()
        }
    
    @api("overheadScreen")
    def carcontrol_overheadScreen_language_set(self, mode):
        """
        Set the overhead screen language type.
        
        Args:
            mode (str): Language options. Enum values: ["Chinese", "English"]
            
        Returns:
            dict: Operation result and current state
        """
        if self.state != self.ScreenState.OPEN:
            return {
                "success": False,
                "error": "Operation failed: Overhead screen must be open to perform this action"
            }
            
        if mode not in ["Chinese", "English"]:
            return {
                "success": False,
                "error": f"Invalid language: {mode}. Must be one of: 'Chinese', 'English'"
            }
        
        # Update environment language
        Environment.set_language(mode)
        
        return {
            "success": True,
            "current_language": Environment.get_language()
        }
    
    @api("overheadScreen")
    def carcontrol_overheadScreen_switch(self, action):
        """
        Control overhead screen, can open, close
        
        Args:
            action (str): Overhead screen control method. Enum values: ["open", "close"]
            
        Returns:
            dict: Operation result and current state
        """
        if action not in ["open", "close"]:
            return {
                "success": False,
                "error": f"Invalid action: {action}. Must be one of: 'open', 'close'"
            }
        
        # Convert to enum and update state
        try:
            new_state = self.ScreenState(action)
            self.state = new_state
            
            return {
                "success": True,
                "current_state": self.state.value
            }
        except (ValueError, KeyError) as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("overheadScreen")
    def carcontrol_overheadScreen_brightness_increase(self, value=None, unit=None, degree=None):
        """
        Increase the overhead screen brightness.
        
        Args:
            value (float, optional): Numeric part of specific brightness adjustment.
            unit (str, optional): Unit part of specific brightness adjustment. Enum values: ["gear", "percentage", "nit"]
            degree (str, optional): Different levels of brightness adjustment. Enum values: ["large", "little", "tiny"]
            
        Returns:
            dict: Operation result and current brightness
        """
        # Check if we're already at maximum brightness
        if self.state != self.ScreenState.OPEN:
            return {
                "success": False,
                "error": "Operation failed: Overhead screen must be open to perform this action"
            }
            
        if self.brightness_percentage >= 100.0:
            return {
                "success": False,
                "error": "Brightness already at maximum",
                "current_brightness": {
                    "percentage": self.brightness_percentage,
                    "gear": self.brightness_gear,
                    "nit": self.brightness_nit
                }
            }
        
        # Case 1: Using degree
        if degree is not None:
            if value is not None or unit is not None:
                return {
                    "success": False,
                    "error": "Cannot specify both degree and value/unit"
                }
            
            try:
                degree_enum = self.BrightnessAdjustmentDegree(degree)
                self._adjust_brightness_by_degree(degree_enum, increase=True)
            except (ValueError, KeyError) as e:
                return {
                    "success": False,
                    "error": f"Invalid degree: {degree}. Must be one of: 'large', 'little', 'tiny'"
                }
        
        # Case 2: Using value and unit
        elif value is not None and unit is not None:
            if unit not in ["gear", "percentage", "nit"]:
                return {
                    "success": False,
                    "error": f"Invalid unit: {unit}. Must be one of: 'gear', 'percentage', 'nit'"
                }
            
            try:
                unit_enum = self.BrightnessUnit(unit)
                
                # Get current value based on unit
                current_value = self._get_brightness_value_by_unit(unit_enum)
                
                # Set new value based on unit
                if unit == "gear":
                    self.brightness_gear = current_value + value
                elif unit == "percentage":
                    self.brightness_percentage = current_value + value
                elif unit == "nit":
                    self.brightness_nit = current_value + value
            except (ValueError, KeyError) as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        # Case 3: Default increase (10%)
        else:
            self.brightness_percentage = self.brightness_percentage + 10.0
        
        return {
            "success": True,
            "current_brightness": {
                "percentage": self.brightness_percentage,
                "gear": self.brightness_gear,
                "nit": self.brightness_nit
            }
        }
    
    @api("overheadScreen")
    def carcontrol_overheadScreen_brightness_decrease(self, value=None, unit=None, degree=None):
        """
        Decrease the overhead screen brightness.
        
        Args:
            value (float, optional): Numeric part of specific brightness adjustment.
            unit (str, optional): Unit part of specific brightness adjustment. Enum values: ["gear", "percentage", "nit"]
            degree (str, optional): Different levels of brightness adjustment. Enum values: ["large", "little", "tiny"]
            
        Returns:
            dict: Operation result and current brightness
        """
        # Check if we're already at minimum brightness
        if self.state != self.ScreenState.OPEN:
            return {
                "success": False,
                "error": "Operation failed: Overhead screen must be open to perform this action"
            }
            
        if self.brightness_percentage <= 0.0:
            return {
                "success": False,
                "error": "Brightness already at minimum",
                "current_brightness": {
                    "percentage": self.brightness_percentage,
                    "gear": self.brightness_gear,
                    "nit": self.brightness_nit
                }
            }
        
        # Case 1: Using degree
        if degree is not None:
            if value is not None or unit is not None:
                return {
                    "success": False,
                    "error": "Cannot specify both degree and value/unit"
                }
            
            try:
                degree_enum = self.BrightnessAdjustmentDegree(degree)
                self._adjust_brightness_by_degree(degree_enum, increase=False)
            except (ValueError, KeyError) as e:
                return {
                    "success": False,
                    "error": f"Invalid degree: {degree}. Must be one of: 'large', 'little', 'tiny'"
                }
        
        # Case 2: Using value and unit
        elif value is not None and unit is not None:
            if unit not in ["gear", "percentage", "nit"]:
                return {
                    "success": False,
                    "error": f"Invalid unit: {unit}. Must be one of: 'gear', 'percentage', 'nit'"
                }
            
            try:
                unit_enum = self.BrightnessUnit(unit)
                
                # Get current value based on unit
                current_value = self._get_brightness_value_by_unit(unit_enum)
                
                # Set new value based on unit
                if unit == "gear":
                    self.brightness_gear = current_value - value
                elif unit == "percentage":
                    self.brightness_percentage = current_value - value
                elif unit == "nit":
                    self.brightness_nit = current_value - value
            except (ValueError, KeyError) as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        # Case 3: Default decrease (10%)
        else:
            self.brightness_percentage = self.brightness_percentage - 10.0
        
        return {
            "success": True,
            "current_brightness": {
                "percentage": self.brightness_percentage,
                "gear": self.brightness_gear,
                "nit": self.brightness_nit
            }
        }
    
    @api("overheadScreen")
    def carcontrol_overheadScreen_brightness_set(self, value=None, unit=None, degree=None):
        """
        Set the overhead screen brightness to a specified value.
        
        Args:
            value (float, optional): Numeric part of specific brightness adjustment.
            unit (str, optional): Unit part of specific brightness adjustment. Enum values: ["gear", "percentage", "nit"]
            degree (str, optional): Different levels of brightness adjustment. Enum values: ["max", "high", "medium", "low", "min"]
            
        Returns:
            dict: Operation result and current brightness
        """
        if self.state != self.ScreenState.OPEN:
            return {
                "success": False,
                "error": "Operation failed: Overhead screen must be open to perform this action"
            }
            
        # Validate arguments
        if degree is not None and (value is not None or unit is not None):
            return {
                "success": False,
                "error": "Cannot specify both degree and value/unit"
            }
        
        if degree is None and (value is None or unit is None):
            return {
                "success": False,
                "error": "Must specify either degree or both value and unit"
            }
        
        # Case 1: Using degree
        if degree is not None:
            if degree not in ["max", "high", "medium", "low", "min"]:
                return {
                    "success": False,
                    "error": f"Invalid degree: {degree}. Must be one of: 'max', 'high', 'medium', 'low', 'min'"
                }
            
            try:
                level_enum = self.BrightnessLevel(degree)
                self._set_brightness_by_level(level_enum)
            except (ValueError, KeyError) as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        # Case 2: Using value and unit
        else:
            if unit not in ["gear", "percentage", "nit"]:
                return {
                    "success": False,
                    "error": f"Invalid unit: {unit}. Must be one of: 'gear', 'percentage', 'nit'"
                }
            
            try:
                # Set value based on unit
                if unit == "gear":
                    self.brightness_gear = value
                elif unit == "percentage":
                    self.brightness_percentage = value
                elif unit == "nit":
                    self.brightness_nit = value
            except (ValueError, KeyError) as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        return {
            "success": True,
            "current_brightness": {
                "percentage": self.brightness_percentage,
                "gear": self.brightness_gear,
                "nit": self.brightness_nit
            }
        }
    


    def to_dict(self):
        """
        Convert the class instance to a dictionary with values, types, and descriptions.
        
        Returns:
            dict: Dictionary representation of the class
        """
        return {
            "state": {
                "value": self.state.value,
                "description": "Current state of the overhead screen (open, close)",
                "type": "ScreenState enum",
                "enum_values": [state.value for state in self.ScreenState]
            },
            "brightness_percentage": {
                "value": self.brightness_percentage,
                "description": "Current brightness as percentage (0-100),you can only change it when the state is open",
                "type": "float"
            },
            "brightness_gear": {
                "value": self.brightness_gear,
                "description": "Current brightness as gear level (0-5),you can only change it when the state is open",
                "type": "int"
            },
            "brightness_nit": {
                "value": self.brightness_nit,
                "description": "Current brightness in nits (0-500),you can only change it when the state is open",
                "type": "float"
            },
            "current_brightness_unit": {
                "value": self.current_brightness_unit.value,
                "description": "Currently used brightness unit for adjustments,you can only change it when the state is open",
                "type": "BrightnessUnit enum",
                "enum_values": [unit.value for unit in self.BrightnessUnit]
            },
            "language": {
                "value": Environment.get_language(),
                "description": "Current language setting (Chinese, English),you can only change it when the state is open",
                "type": "str",
                "enum_values": ["Chinese", "English"]
            },
            "time_display_format": {
                "value": Environment.get_time_display_format(),
                "description": "Current time display format (12-hour format, 24-hour format),you can only change it when the state is open",
                "type": "str",
                "enum_values": ["12-hour format", "24-hour format"]
            }
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a class instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing the class data
            
        Returns:
            OverheadScreen: Instance of the class
        """
        instance = cls()
        
        # Set state
        try:
            instance.state = cls.ScreenState(data["state"]["value"])
        except (KeyError, ValueError) as e:
            pass  # Use default if missing or invalid
        
        # Set brightness properties
        try:
            instance.brightness_percentage = data["brightness_percentage"]["value"]
        except (KeyError, ValueError) as e:
            pass  # Use default if missing or invalid
        
        # Set current brightness unit
        try:
            instance.current_brightness_unit = cls.BrightnessUnit(data["current_brightness_unit"]["value"])
        except (KeyError, ValueError) as e:
            pass  # Use default if missing or invalid
        
        # Set environment properties if they exist in the data
        try:
            Environment.set_language(data["language"]["value"])
        except (KeyError, ValueError) as e:
            pass  # Use default if missing or invalid
        
        try:
            Environment.set_time_display_format(data["time_display_format"]["value"])
        except (KeyError, ValueError) as e:
            pass  # Use default if missing or invalid
        
        return instance
    
    @classmethod
    def init1(cls):
        """
        First initialization method that creates an instance with default values.
        
        Returns:
            OverheadScreen: Instance with screen open, English language, 12-hour format, 
                        and medium brightness.
        """
        instance = cls()
        
        # Set screen to open state
        instance.state = cls.ScreenState.OPEN
        
        # Set brightness to medium level (50%)
        instance.brightness_percentage = 50.0
        
        # Set language to English
        Environment.set_language("English")
        
        # Set time display format to 12-hour
        Environment.set_time_display_format("12-hour format")
        
        # Set brightness unit to percentage
        instance.current_brightness_unit = cls.BrightnessUnit.PERCENTAGE
        
        return instance

    @classmethod
    def init2(cls):
        """
        Second initialization method that creates an instance with high brightness
        and Chinese language settings.
        
        Returns:
            OverheadScreen: Instance with screen closed, Chinese language, 24-hour format,
                        and high brightness using nit as the unit.
        """
        instance = cls()
        
        # Set screen to closed state
        instance.state = cls.ScreenState.CLOSED
        
        # Set brightness to high level (75%)
        instance._set_brightness_by_level(cls.BrightnessLevel.HIGH)
        
        # Set language to Chinese
        Environment.set_language("Chinese")
        
        # Set time display format to 24-hour
        Environment.set_time_display_format("24-hour format")
        
        # Set brightness unit to nit
        instance.current_brightness_unit = cls.BrightnessUnit.NIT
        
        return instance