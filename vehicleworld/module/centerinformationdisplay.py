from utils import api
from typing import Dict, Any, Optional, Union, List, Tuple
from module.environment import Environment

class CenterInformationDisplay:
    """
    Entity class representing the center information display of a vehicle,
    providing APIs to control display settings like brightness, language, and time format.
    """
    
    class BrightnessSettings:
        """
        Inner class for managing brightness-related settings and operations.
        """
        def __init__(self, 
                     brightness_level: float = 50.0, 
                     auto_brightness: bool = False, 
                     brightness_unit: str = "percentage", 
                     min_brightness: float = 0.0, 
                     max_brightness: float = 100.0):
            self._brightness_level = brightness_level
            self._auto_brightness = auto_brightness
            self._brightness_unit = brightness_unit
            self._min_brightness = min_brightness
            self._max_brightness = max_brightness
            
            # Mapping degree values to percentage values
            self._degree_mappings = {
                "min": 0.0,
                "low": 25.0,
                "medium": 50.0,
                "high": 75.0,
                "max": 100.0
            }
            
            # Adjustment increments for different degrees
            self._adjustment_increments = {
                "tiny": 5.0,
                "little": 10.0,
                "large": 20.0
            }
            
            # Conversion factors between different units
            self._unit_conversion = {
                "percentage": 1.0,  # Base unit
                "gear": 20.0,       # 5 gears correspond to 100%
                "nit": 5.0          # Assuming max nit is 500, so 100% = 500 nit
            }
        
        @property
        def brightness_level(self) -> float:
            return self._brightness_level
        
        @brightness_level.setter
        def brightness_level(self, value: float):
            if value < self._min_brightness:
                self._brightness_level = self._min_brightness
            elif value > self._max_brightness:
                self._brightness_level = self._max_brightness
            else:
                self._brightness_level = value
        
        @property
        def auto_brightness(self) -> bool:
            return self._auto_brightness
        
        @auto_brightness.setter
        def auto_brightness(self, value: bool):
            self._auto_brightness = value
        
        @property
        def brightness_unit(self) -> str:
            return self._brightness_unit
        
        @brightness_unit.setter
        def brightness_unit(self, value: str):
            if value in self._unit_conversion:
                self._brightness_unit = value
            else:
                raise ValueError(f"Unsupported brightness unit: {value}")
        
        @property
        def min_brightness(self) -> float:
            return self._min_brightness
        
        @property
        def max_brightness(self) -> float:
            return self._max_brightness
        
        def to_dict(self) -> Dict[str, Any]:
            return {
                "brightness_level": {
                    "value": self.brightness_level,
                    "description": "Current brightness level of the display",
                    "type": type(self.brightness_level).__name__
                },
                "auto_brightness": {
                    "value": self.auto_brightness,
                    "description": "Whether automatic brightness adjustment is enabled,if you want to change the brightness_level specifically,you need to set it to False",
                    "type": type(self.auto_brightness).__name__
                },
                "brightness_unit": {
                    "value": self.brightness_unit,
                    "description": "Unit for brightness measurement (percentage, gear, nit)",
                    "type": type(self.brightness_unit).__name__
                },
                "min_brightness": {
                    "value": self.min_brightness,
                    "description": "Minimum brightness level",
                    "type": type(self.min_brightness).__name__
                },
                "max_brightness": {
                    "value": self.max_brightness,
                    "description": "Maximum brightness level",
                    "type": type(self.max_brightness).__name__
                }
            }
        
        @classmethod
        def from_dict(cls, data: Dict[str, Any]) -> 'CenterInformationDisplay.BrightnessSettings':
            instance = cls(
                brightness_level=data["brightness_level"]["value"],
                auto_brightness=data["auto_brightness"]["value"],
                brightness_unit=data["brightness_unit"]["value"]
            )
            return instance
        
        def convert_to_percentage(self, value: float, unit: str) -> float:
            """Convert a value from any supported unit to percentage"""
            if unit not in self._unit_conversion:
                raise ValueError(f"Unsupported unit: {unit}")
            
            # Convert to percentage
            return value * self._unit_conversion[unit]
        
        def convert_from_percentage(self, percentage: float, unit: str) -> float:
            """Convert a percentage value to the specified unit"""
            if unit not in self._unit_conversion:
                raise ValueError(f"Unsupported unit: {unit}")
            
            # Convert from percentage to target unit
            return percentage / self._unit_conversion[unit]
        
        def get_value_from_degree(self, degree: str) -> float:
            """Convert a textual degree to a percentage value"""
            if degree not in self._degree_mappings:
                raise ValueError(f"Unsupported degree: {degree}")
            
            return self._degree_mappings[degree]
        
        def get_increment_from_degree(self, degree: str) -> float:
            """Get the increment value for a given adjustment degree"""
            if degree not in self._adjustment_increments:
                raise ValueError(f"Unsupported increment degree: {degree}")
            
            return self._adjustment_increments[degree]
    
    def __init__(self):
        # Initialize brightness settings
        self._brightness_settings = CenterInformationDisplay.BrightnessSettings()
    
    @property
    def brightness_settings(self) -> BrightnessSettings:
        return self._brightness_settings
    
    


    def to_dict(self) -> Dict[str, Any]:
        return {
            "brightness_settings": {
                "value": self.brightness_settings.to_dict(),
                "description": "Settings related to display brightness",
                "type": "BrightnessSettings"
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CenterInformationDisplay':
        instance = cls()
        instance._brightness_settings = CenterInformationDisplay.BrightnessSettings.from_dict(
            data["brightness_settings"]["value"]
        )
        return instance
    
    @api("centerInformationDisplay")
    def carcontrol_centerInformationDisplay_timeDisplayFormat_set(self, mode: str) -> Dict[str, Any]:
        """
        Set the time display format on the center information display.
        
        Args:
            mode (str): Time display format options. Options: ["12-hour format", "24-hour format"]
            
        Returns:
            Dict[str, Any]: Response containing operation result and updated state
        """
        # Validate input
        valid_modes = ["12-hour format", "24-hour format"]
        if mode not in valid_modes:
            return {
                "success": False,
                "error": f"Invalid mode. Expected one of {valid_modes}, got {mode}",
                "current_format": Environment.get_time_display_format()
            }
        
        # Update global environment setting
        Environment.set_time_display_format(mode)
        
        return {
            "success": True,
            "message": f"Time display format set to {mode}",
            "current_format": Environment.get_time_display_format()
        }
    
    @api("centerInformationDisplay")
    def carcontrol_centerInformationDisplay_language_set(self, mode: str) -> Dict[str, Any]:
        """
        Set the centerInformationDisplay language type.
        
        Args:
            mode (str): Language options. Options: ["Chinese", "English"]
            
        Returns:
            Dict[str, Any]: Response containing operation result and updated state
        """
        # Validate input
        valid_modes = ["Chinese", "English"]
        if mode not in valid_modes:
            return {
                "success": False,
                "error": f"Invalid language mode. Expected one of {valid_modes}, got {mode}",
                "current_language": Environment.get_language()
            }
        
        # Update global environment setting
        Environment.set_language(mode)
        
        return {
            "success": True,
            "message": f"Display language set to {mode}",
            "current_language": Environment.get_language()
        }
    
    @api("centerInformationDisplay")
    def carcontrol_centerInformationDisplay_mode_autoBrightness(self, switch: bool) -> Dict[str, Any]:
        """
        Turn on or off the automatic brightness adjustment feature.
        
        Args:
            switch (bool): True to turn on, False to turn off
            
        Returns:
            Dict[str, Any]: Response containing operation result and updated state
        """
        # Validate input
        if not isinstance(switch, bool):
            return {
                "success": False,
                "error": f"Invalid switch value. Expected boolean, got {type(switch).__name__}",
                "auto_brightness": self.brightness_settings.auto_brightness
            }
        
        # Update brightness settings
        self.brightness_settings.auto_brightness = switch
        
        return {
            "success": True,
            "message": f"Automatic brightness {'enabled' if switch else 'disabled'}",
            "auto_brightness": self.brightness_settings.auto_brightness
        }
    
    @api("centerInformationDisplay")
    def carcontrol_centerInformationDisplay_brightness_increase(
        self, 
        value: Optional[float] = None, 
        unit: Optional[str] = None, 
        degree: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Increase the center information display brightness.
        
        Args:
            value (Optional[float]): Numeric part of brightness adjustment
            unit (Optional[str]): Unit for brightness. Options: ["gear", "percentage", "nit"]
            degree (Optional[str]): Adjustment degree. Options: ["large", "little", "tiny"]
            
        Returns:
            Dict[str, Any]: Response containing operation result and updated state
        """
        # Cannot adjust brightness if auto mode is on
        self.brightness_settings.auto_brightness = False
        # Determine the increment value
        increment = 0.0
        
        # Case 1: Using specific value and unit
        if value is not None and unit is not None:
            # Validate unit
            valid_units = ["gear", "percentage", "nit"]
            if unit not in valid_units:
                return {
                    "success": False,
                    "error": f"Invalid unit. Expected one of {valid_units}, got {unit}",
                    "current_brightness": self.brightness_settings.brightness_level,
                    "unit": self.brightness_settings.brightness_unit
                }
            
            # Convert to percentage for internal calculations
            increment = self.brightness_settings.convert_to_percentage(value, unit)
        
        # Case 2: Using degree
        elif degree is not None:
            # Validate degree
            valid_degrees = ["large", "little", "tiny"]
            if degree not in valid_degrees:
                return {
                    "success": False,
                    "error": f"Invalid degree. Expected one of {valid_degrees}, got {degree}",
                    "current_brightness": self.brightness_settings.brightness_level,
                    "unit": self.brightness_settings.brightness_unit
                }
            
            increment = self.brightness_settings.get_increment_from_degree(degree)
        
        # Case 3: Default increment (medium level)
        else:
            increment = self.brightness_settings.get_increment_from_degree("little")
        
        # Apply the increment
        new_brightness = self.brightness_settings.brightness_level + increment
        self.brightness_settings.brightness_level = new_brightness
        
        # Prepare response
        return {
            "success": True,
            "message": f"Brightness increased by {increment} percentage points",
            "previous_brightness": self.brightness_settings.brightness_level - increment,
            "current_brightness": self.brightness_settings.brightness_level,
            "unit": self.brightness_settings.brightness_unit
        }
    
    @api("centerInformationDisplay")
    def carcontrol_centerInformationDisplay_brightness_decrease(
        self, 
        value: Optional[float] = None, 
        unit: Optional[str] = None, 
        degree: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Decrease the center information display brightness.
        
        Args:
            value (Optional[float]): Numeric part of brightness adjustment
            unit (Optional[str]): Unit for brightness. Options: ["gear", "percentage", "nit"]
            degree (Optional[str]): Adjustment degree. Options: ["large", "little", "tiny"]
            
        Returns:
            Dict[str, Any]: Response containing operation result and updated state
        """
        # Cannot adjust brightness if auto mode is on
        self.brightness_settings.auto_brightness = False
        # Determine the decrement value
        decrement = 0.0
        
        # Case 1: Using specific value and unit
        if value is not None and unit is not None:
            # Validate unit
            valid_units = ["gear", "percentage", "nit"]
            if unit not in valid_units:
                return {
                    "success": False,
                    "error": f"Invalid unit. Expected one of {valid_units}, got {unit}",
                    "current_brightness": self.brightness_settings.brightness_level,
                    "unit": self.brightness_settings.brightness_unit
                }
            
            # Convert to percentage for internal calculations
            decrement = self.brightness_settings.convert_to_percentage(value, unit)
        
        # Case 2: Using degree
        elif degree is not None:
            # Validate degree
            valid_degrees = ["large", "little", "tiny"]
            if degree not in valid_degrees:
                return {
                    "success": False,
                    "error": f"Invalid degree. Expected one of {valid_degrees}, got {degree}",
                    "current_brightness": self.brightness_settings.brightness_level,
                    "unit": self.brightness_settings.brightness_unit
                }
            
            decrement = self.brightness_settings.get_increment_from_degree(degree)
        
        # Case 3: Default decrement (medium level)
        else:
            decrement = self.brightness_settings.get_increment_from_degree("little")
        
        # Apply the decrement
        new_brightness = self.brightness_settings.brightness_level - decrement
        self.brightness_settings.brightness_level = new_brightness
        
        # Prepare response
        return {
            "success": True,
            "message": f"Brightness decreased by {decrement} percentage points",
            "previous_brightness": self.brightness_settings.brightness_level + decrement,
            "current_brightness": self.brightness_settings.brightness_level,
            "unit": self.brightness_settings.brightness_unit
        }
    
    @api("centerInformationDisplay")
    def carcontrol_centerInformationDisplay_brightness_set(
        self, 
        value: Optional[float] = None, 
        unit: Optional[str] = None, 
        degree: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Set the center information display brightness to a specified value.
        
        Args:
            value (Optional[float]): Numeric part of brightness setting
            unit (Optional[str]): Unit for brightness. Options: ["gear", "percentage", "nit"]
            degree (Optional[str]): Brightness level. Options: ["max", "high", "medium", "low", "min"]
            
        Returns:
            Dict[str, Any]: Response containing operation result and updated state
        """
        # Cannot set brightness if auto mode is on
        self.brightness_settings.auto_brightness = False
        
        # Store previous brightness for reporting
        previous_brightness = self.brightness_settings.brightness_level
        
        # Case 1: Using degree
        if degree is not None:
            # Validate degree
            valid_degrees = ["max", "high", "medium", "low", "min"]
            if degree not in valid_degrees:
                return {
                    "success": False,
                    "error": f"Invalid degree. Expected one of {valid_degrees}, got {degree}",
                    "current_brightness": self.brightness_settings.brightness_level,
                    "unit": self.brightness_settings.brightness_unit
                }
            
            # Get corresponding percentage value
            new_brightness = self.brightness_settings.get_value_from_degree(degree)
            self.brightness_settings.brightness_level = new_brightness
            
            return {
                "success": True,
                "message": f"Brightness set to {degree} ({new_brightness}%)",
                "previous_brightness": previous_brightness,
                "current_brightness": self.brightness_settings.brightness_level,
                "unit": self.brightness_settings.brightness_unit
            }
        
        # Case 2: Using value and unit
        elif value is not None and unit is not None:
            # Validate unit
            valid_units = ["gear", "percentage", "nit"]
            if unit not in valid_units:
                return {
                    "success": False,
                    "error": f"Invalid unit. Expected one of {valid_units}, got {unit}",
                    "current_brightness": self.brightness_settings.brightness_level,
                    "unit": self.brightness_settings.brightness_unit
                }
            
            # Convert to percentage and set
            new_brightness = self.brightness_settings.convert_to_percentage(value, unit)
            self.brightness_settings.brightness_level = new_brightness
            
            return {
                "success": True,
                "message": f"Brightness set to {value} {unit} ({new_brightness}%)",
                "previous_brightness": previous_brightness,
                "current_brightness": self.brightness_settings.brightness_level,
                "unit": self.brightness_settings.brightness_unit
            }
        
        # Neither case provided
        return {
            "success": False,
            "error": "Must provide either degree or both value and unit",
            "current_brightness": self.brightness_settings.brightness_level,
            "unit": self.brightness_settings.brightness_unit
        }
    @classmethod
    def init1(cls) -> 'CenterInformationDisplay':
        """
        Initialize a CenterInformationDisplay with default settings:
        - Auto brightness disabled
        - Brightness level at 50%
        - Brightness unit in percentage
        
        Returns:
            CenterInformationDisplay: A new instance with default settings
        """
        instance = cls()
        instance._brightness_settings = CenterInformationDisplay.BrightnessSettings(
            brightness_level=50.0,
            auto_brightness=False,
            brightness_unit="percentage",
            min_brightness=0.0,
            max_brightness=100.0
        )
        
        # Set default environment settings
        Environment.set_time_display_format("24-hour format")
        Environment.set_language("English")
        
        return instance

    @classmethod
    def init2(cls) -> 'CenterInformationDisplay':
        """
        Initialize a CenterInformationDisplay with night mode settings:
        - Auto brightness enabled
        - Brightness level at 25% (low)
        - Brightness unit in nit
        
        Returns:
            CenterInformationDisplay: A new instance with night mode settings
        """
        instance = cls()
        instance._brightness_settings = CenterInformationDisplay.BrightnessSettings(
            brightness_level=25.0,
            auto_brightness=True,
            brightness_unit="nit",
            min_brightness=0.0,
            max_brightness=100.0
        )
        
        # Set night mode environment settings
        Environment.set_time_display_format("12-hour format")
        Environment.set_language("English")
        
        return instance