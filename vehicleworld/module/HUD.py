from utils import api
from enum import Enum
from typing import Dict, Any, Union, Optional, List, Tuple

class HUD:
    """
    Head-Up Display (HUD) entity class that manages the state and operations
    of a vehicle's windshield projection system displaying driving information.
    """
    
    class BrightnessUnitEnum(Enum):
        """Enumeration for brightness adjustment units"""
        LEVEL = "level"
        PERCENTAGE = "percentage"
        NITS = "Nits"
    
    class HeightUnitEnum(Enum):
        """Enumeration for height adjustment units"""
        LEVEL = "level"
        PERCENTAGE = "percentage"
        CENTIMETER = "centimeter"
    
    class AdjustmentDegreeEnum(Enum):
        """Enumeration for small incremental adjustments"""
        TINY = "tiny"
        LITTLE = "little"
        LARGE = "large"
    
    class SettingDegreeEnum(Enum):
        """Enumeration for absolute setting levels"""
        MIN = "min"
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
        MAX = "max"
    
    # Constants for minimum and maximum values
    MIN_BRIGHTNESS_PERCENTAGE = 0
    MAX_BRIGHTNESS_PERCENTAGE = 100
    MIN_BRIGHTNESS_LEVEL = 1
    MAX_BRIGHTNESS_LEVEL = 10
    MIN_BRIGHTNESS_NITS = 0
    MAX_BRIGHTNESS_NITS = 1000
    
    MIN_HEIGHT_PERCENTAGE = 0
    MAX_HEIGHT_PERCENTAGE = 100
    MIN_HEIGHT_LEVEL = 1
    MAX_HEIGHT_LEVEL = 10
    MIN_HEIGHT_CENTIMETER = 0
    MAX_HEIGHT_CENTIMETER = 20
    
    # Adjustment increments for degree-based changes
    BRIGHTNESS_INCREMENTS = {
        AdjustmentDegreeEnum.TINY: {"level": 1, "percentage": 5, "Nits": 50},
        AdjustmentDegreeEnum.LITTLE: {"level": 2, "percentage": 10, "Nits": 100},
        AdjustmentDegreeEnum.LARGE: {"level": 3, "percentage": 20, "Nits": 200}
    }
    
    HEIGHT_INCREMENTS = {
        AdjustmentDegreeEnum.TINY: {"level": 1, "percentage": 5, "centimeter": 1},
        AdjustmentDegreeEnum.LITTLE: {"level": 2, "percentage": 10, "centimeter": 2},
        AdjustmentDegreeEnum.LARGE: {"level": 3, "percentage": 20, "centimeter": 3}
    }
    
    # Absolute values for degree-based settings
    BRIGHTNESS_SETTINGS = {
        SettingDegreeEnum.MIN: {"level": 1, "percentage": 0, "Nits": 0},
        SettingDegreeEnum.LOW: {"level": 3, "percentage": 25, "Nits": 250},
        SettingDegreeEnum.MEDIUM: {"level": 5, "percentage": 50, "Nits": 500},
        SettingDegreeEnum.HIGH: {"level": 8, "percentage": 75, "Nits": 750},
        SettingDegreeEnum.MAX: {"level": 10, "percentage": 100, "Nits": 1000}
    }
    
    HEIGHT_SETTINGS = {
        SettingDegreeEnum.MIN: {"level": 1, "percentage": 0, "centimeter": 0},
        SettingDegreeEnum.LOW: {"level": 3, "percentage": 25, "centimeter": 5},
        SettingDegreeEnum.MEDIUM: {"level": 5, "percentage": 50, "centimeter": 10},
        SettingDegreeEnum.HIGH: {"level": 8, "percentage": 75, "centimeter": 15},
        SettingDegreeEnum.MAX: {"level": 10, "percentage": 100, "centimeter": 20}
    }
    
    def __init__(self):
        """Initialize the HUD with default values"""
        # Primary state
        self._is_on = False
        
        # Brightness state
        self._brightness_level = 5  # Default mid-level (1-10)
        self._brightness_percentage = 50  # Default 50%
        self._brightness_nits = 500  # Default 500 nits
        self._current_brightness_unit = self.BrightnessUnitEnum.PERCENTAGE
        
        # Height state
        self._height_level = 5  # Default mid-level (1-10)
        self._height_percentage = 50  # Default 50%
        self._height_centimeter = 10  # Default 10cm
        self._current_height_unit = self.HeightUnitEnum.PERCENTAGE
    
    # === SWITCH STATE ===
    @property
    def is_on(self) -> bool:
        """Get the current HUD power state"""
        return self._is_on
    
    @is_on.setter
    def is_on(self, value: bool):
        """Set the HUD power state"""
        self._is_on = value
    
    # === BRIGHTNESS PROPERTIES ===
    @property
    def brightness_level(self) -> int:
        """Get the current brightness level (1-10)"""
        return self._brightness_level
    
    @brightness_level.setter
    def brightness_level(self, value: int):
        """Set the brightness level (1-10)"""
        if value < self.MIN_BRIGHTNESS_LEVEL:
            self._brightness_level = self.MIN_BRIGHTNESS_LEVEL
        elif value > self.MAX_BRIGHTNESS_LEVEL:
            self._brightness_level = self.MAX_BRIGHTNESS_LEVEL
        else:
            self._brightness_level = value
        
        # Sync other brightness units
        self._sync_brightness_units(self.BrightnessUnitEnum.LEVEL)
    
    @property
    def brightness_percentage(self) -> float:
        """Get the current brightness percentage (0-100)"""
        return self._brightness_percentage
    
    @brightness_percentage.setter
    def brightness_percentage(self, value: float):
        """Set the brightness percentage (0-100)"""
        if value < self.MIN_BRIGHTNESS_PERCENTAGE:
            self._brightness_percentage = self.MIN_BRIGHTNESS_PERCENTAGE
        elif value > self.MAX_BRIGHTNESS_PERCENTAGE:
            self._brightness_percentage = self.MAX_BRIGHTNESS_PERCENTAGE
        else:
            self._brightness_percentage = value
        
        # Sync other brightness units
        self._sync_brightness_units(self.BrightnessUnitEnum.PERCENTAGE)
    
    @property
    def brightness_nits(self) -> float:
        """Get the current brightness in nits (0-1000)"""
        return self._brightness_nits
    
    @brightness_nits.setter
    def brightness_nits(self, value: float):
        """Set the brightness in nits (0-1000)"""
        if value < self.MIN_BRIGHTNESS_NITS:
            self._brightness_nits = self.MIN_BRIGHTNESS_NITS
        elif value > self.MAX_BRIGHTNESS_NITS:
            self._brightness_nits = self.MAX_BRIGHTNESS_NITS
        else:
            self._brightness_nits = value
        
        # Sync other brightness units
        self._sync_brightness_units(self.BrightnessUnitEnum.NITS)
    
    @property
    def current_brightness_unit(self) -> BrightnessUnitEnum:
        """Get the current brightness unit being used"""
        return self._current_brightness_unit
    
    @current_brightness_unit.setter
    def current_brightness_unit(self, value: BrightnessUnitEnum):
        """Set the current brightness unit"""
        self._current_brightness_unit = value
    
    # === HEIGHT PROPERTIES ===
    @property
    def height_level(self) -> int:
        """Get the current height level (1-10)"""
        return self._height_level
    
    @height_level.setter
    def height_level(self, value: int):
        """Set the height level (1-10)"""
        if value < self.MIN_HEIGHT_LEVEL:
            self._height_level = self.MIN_HEIGHT_LEVEL
        elif value > self.MAX_HEIGHT_LEVEL:
            self._height_level = self.MAX_HEIGHT_LEVEL
        else:
            self._height_level = value
        
        # Sync other height units
        self._sync_height_units(self.HeightUnitEnum.LEVEL)
    
    @property
    def height_percentage(self) -> float:
        """Get the current height percentage (0-100)"""
        return self._height_percentage
    
    @height_percentage.setter
    def height_percentage(self, value: float):
        """Set the height percentage (0-100)"""
        if value < self.MIN_HEIGHT_PERCENTAGE:
            self._height_percentage = self.MIN_HEIGHT_PERCENTAGE
        elif value > self.MAX_HEIGHT_PERCENTAGE:
            self._height_percentage = self.MAX_HEIGHT_PERCENTAGE
        else:
            self._height_percentage = value
        
        # Sync other height units
        self._sync_height_units(self.HeightUnitEnum.PERCENTAGE)
    
    @property
    def height_centimeter(self) -> float:
        """Get the current height in centimeters (0-20)"""
        return self._height_centimeter
    
    @height_centimeter.setter
    def height_centimeter(self, value: float):
        """Set the height in centimeters (0-20)"""
        if value < self.MIN_HEIGHT_CENTIMETER:
            self._height_centimeter = self.MIN_HEIGHT_CENTIMETER
        elif value > self.MAX_HEIGHT_CENTIMETER:
            self._height_centimeter = self.MAX_HEIGHT_CENTIMETER
        else:
            self._height_centimeter = value
        
        # Sync other height units
        self._sync_height_units(self.HeightUnitEnum.CENTIMETER)
    
    @property
    def current_height_unit(self) -> HeightUnitEnum:
        """Get the current height unit being used"""
        return self._current_height_unit
    
    @current_height_unit.setter
    def current_height_unit(self, value: HeightUnitEnum):
        """Set the current height unit"""
        self._current_height_unit = value
    
    # === HELPER METHODS ===
    def _sync_brightness_units(self, changed_unit: BrightnessUnitEnum):
        """
        Synchronize all brightness units after one has been changed
        
        Args:
            changed_unit: The unit that was changed and caused this sync
        """
        if changed_unit == self.BrightnessUnitEnum.LEVEL:
            # Convert level to percentage and nits
            ratio = (self._brightness_level - self.MIN_BRIGHTNESS_LEVEL) / (self.MAX_BRIGHTNESS_LEVEL - self.MIN_BRIGHTNESS_LEVEL)
            self._brightness_percentage = ratio * (self.MAX_BRIGHTNESS_PERCENTAGE - self.MIN_BRIGHTNESS_PERCENTAGE) + self.MIN_BRIGHTNESS_PERCENTAGE
            self._brightness_nits = ratio * (self.MAX_BRIGHTNESS_NITS - self.MIN_BRIGHTNESS_NITS) + self.MIN_BRIGHTNESS_NITS
        
        elif changed_unit == self.BrightnessUnitEnum.PERCENTAGE:
            # Convert percentage to level and nits
            ratio = (self._brightness_percentage - self.MIN_BRIGHTNESS_PERCENTAGE) / (self.MAX_BRIGHTNESS_PERCENTAGE - self.MIN_BRIGHTNESS_PERCENTAGE)
            self._brightness_level = int(ratio * (self.MAX_BRIGHTNESS_LEVEL - self.MIN_BRIGHTNESS_LEVEL) + self.MIN_BRIGHTNESS_LEVEL)
            self._brightness_nits = ratio * (self.MAX_BRIGHTNESS_NITS - self.MIN_BRIGHTNESS_NITS) + self.MIN_BRIGHTNESS_NITS
        
        elif changed_unit == self.BrightnessUnitEnum.NITS:
            # Convert nits to level and percentage
            ratio = (self._brightness_nits - self.MIN_BRIGHTNESS_NITS) / (self.MAX_BRIGHTNESS_NITS - self.MIN_BRIGHTNESS_NITS)
            self._brightness_level = int(ratio * (self.MAX_BRIGHTNESS_LEVEL - self.MIN_BRIGHTNESS_LEVEL) + self.MIN_BRIGHTNESS_LEVEL)
            self._brightness_percentage = ratio * (self.MAX_BRIGHTNESS_PERCENTAGE - self.MIN_BRIGHTNESS_PERCENTAGE) + self.MIN_BRIGHTNESS_PERCENTAGE
    
    def _sync_height_units(self, changed_unit: HeightUnitEnum):
        """
        Synchronize all height units after one has been changed
        
        Args:
            changed_unit: The unit that was changed and caused this sync
        """
        if changed_unit == self.HeightUnitEnum.LEVEL:
            # Convert level to percentage and centimeter
            ratio = (self._height_level - self.MIN_HEIGHT_LEVEL) / (self.MAX_HEIGHT_LEVEL - self.MIN_HEIGHT_LEVEL)
            self._height_percentage = ratio * (self.MAX_HEIGHT_PERCENTAGE - self.MIN_HEIGHT_PERCENTAGE) + self.MIN_HEIGHT_PERCENTAGE
            self._height_centimeter = ratio * (self.MAX_HEIGHT_CENTIMETER - self.MIN_HEIGHT_CENTIMETER) + self.MIN_HEIGHT_CENTIMETER
        
        elif changed_unit == self.HeightUnitEnum.PERCENTAGE:
            # Convert percentage to level and centimeter
            ratio = (self._height_percentage - self.MIN_HEIGHT_PERCENTAGE) / (self.MAX_HEIGHT_PERCENTAGE - self.MIN_HEIGHT_PERCENTAGE)
            self._height_level = int(ratio * (self.MAX_HEIGHT_LEVEL - self.MIN_HEIGHT_LEVEL) + self.MIN_HEIGHT_LEVEL)
            self._height_centimeter = ratio * (self.MAX_HEIGHT_CENTIMETER - self.MIN_HEIGHT_CENTIMETER) + self.MIN_HEIGHT_CENTIMETER
        
        elif changed_unit == self.HeightUnitEnum.CENTIMETER:
            # Convert centimeter to level and percentage
            ratio = (self._height_centimeter - self.MIN_HEIGHT_CENTIMETER) / (self.MAX_HEIGHT_CENTIMETER - self.MIN_HEIGHT_CENTIMETER)
            self._height_level = int(ratio * (self.MAX_HEIGHT_LEVEL - self.MIN_HEIGHT_LEVEL) + self.MIN_HEIGHT_LEVEL)
            self._height_percentage = ratio * (self.MAX_HEIGHT_PERCENTAGE - self.MIN_HEIGHT_PERCENTAGE) + self.MIN_HEIGHT_PERCENTAGE
    
    # === API IMPLEMENTATION METHODS ===
    @api("HUD")
    def carcontrol_HUD_switch(self, switch: bool) -> Dict[str, Any]:
        """
        Turn the head-up display HUD on or off.
        The HUD is a projection device that displays driving-related information 
        on the windshield in real-time.
        
        Args:
            switch (bool): HUD switch, true means on, false means off
            
        Returns:
            Dict[str, Any]: Operation result and current HUD state
        """
        self.is_on = switch
        
        result = {
            "success": True,
            "message": f"HUD {'activated' if switch else 'deactivated'} successfully",
            "current_state": {
                "is_on": self.is_on
            }
        }
        
        return result
    
    @api("HUD")
    def carcontrol_HUD_brightness_increase(self, 
                                          value: Optional[float] = None,
                                          unit: Optional[str] = None,
                                          degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Increase the brightness of the HUD.
        
        Args:
            value (Optional[float]): The numeric value to adjust the HUD brightness. 
                                     Mutually exclusive with 'degree'.
            unit (Optional[str]): The unit for adjusting the HUD brightness. 
                                  Possible values: 'level', 'percentage', 'Nits'.
                                  Mutually exclusive with 'degree'.
            degree (Optional[str]): The degree to adjust the HUD brightness.
                                    Possible values: 'large', 'little', 'tiny'.
                                    Mutually exclusive with 'value' and 'unit'.
                                    
        Returns:
            Dict[str, Any]: Operation result and updated brightness information
        """
        # Validate state
        if not self.is_on:
            return {
                "success": False,
                "message": "Cannot adjust brightness: HUD is turned off",
                "current_state": {"is_on": self.is_on}
            }
        
        # Track original values for reporting changes
        original_brightness = {
            "level": self.brightness_level,
            "percentage": self.brightness_percentage,
            "nits": self.brightness_nits
        }
        
        # Process degree-based adjustments
        if degree is not None:
            try:
                degree_enum = self.AdjustmentDegreeEnum(degree)
                current_unit = self.current_brightness_unit.value
                increment = self.BRIGHTNESS_INCREMENTS[degree_enum][current_unit]
                
                # Apply increment based on current unit
                if current_unit == self.BrightnessUnitEnum.LEVEL.value:
                    self.brightness_level += increment
                elif current_unit == self.BrightnessUnitEnum.PERCENTAGE.value:
                    self.brightness_percentage += increment
                elif current_unit == self.BrightnessUnitEnum.NITS.value:
                    self.brightness_nits += increment
            except (ValueError, KeyError):
                return {
                    "success": False,
                    "message": f"Invalid degree value: {degree}. Expected one of: 'large', 'little', 'tiny'",
                    "current_state": {
                        "brightness_level": self.brightness_level,
                        "brightness_percentage": self.brightness_percentage,
                        "brightness_nits": self.brightness_nits
                    }
                }
        
        # Process value-based adjustments
        elif value is not None and unit is not None:
            try:
                unit_enum = self.BrightnessUnitEnum(unit)
                
                # Apply value based on unit
                if unit_enum == self.BrightnessUnitEnum.LEVEL:
                    self.brightness_level += value
                    self.current_brightness_unit = self.BrightnessUnitEnum.LEVEL
                elif unit_enum == self.BrightnessUnitEnum.PERCENTAGE:
                    self.brightness_percentage += value
                    self.current_brightness_unit = self.BrightnessUnitEnum.PERCENTAGE
                elif unit_enum == self.BrightnessUnitEnum.NITS:
                    self.brightness_nits += value
                    self.current_brightness_unit = self.BrightnessUnitEnum.NITS
            except ValueError:
                return {
                    "success": False,
                    "message": f"Invalid unit value: {unit}. Expected one of: 'level', 'percentage', 'Nits'",
                    "current_state": {
                        "brightness_level": self.brightness_level,
                        "brightness_percentage": self.brightness_percentage,
                        "brightness_nits": self.brightness_nits
                    }
                }
        
        # Default increment (when no parameters provided)
        else:
            # Increase by a small default amount
            current_unit = self.current_brightness_unit.value
            increment = self.BRIGHTNESS_INCREMENTS[self.AdjustmentDegreeEnum.LITTLE][current_unit]
            
            if current_unit == self.BrightnessUnitEnum.LEVEL.value:
                self.brightness_level += increment
            elif current_unit == self.BrightnessUnitEnum.PERCENTAGE.value:
                self.brightness_percentage += increment
            elif current_unit == self.BrightnessUnitEnum.NITS.value:
                self.brightness_nits += increment
        
        # Calculate changes
        brightness_change = {
            "level": self.brightness_level - original_brightness["level"],
            "percentage": self.brightness_percentage - original_brightness["percentage"],
            "nits": self.brightness_nits - original_brightness["nits"]
        }
        
        return {
            "success": True,
            "message": "HUD brightness increased successfully",
            "brightness_change": brightness_change,
            "current_state": {
                "brightness_level": self.brightness_level,
                "brightness_percentage": self.brightness_percentage,
                "brightness_nits": self.brightness_nits,
                "current_unit": self.current_brightness_unit.value
            }
        }
    
    @api("HUD")
    def carcontrol_HUD_brightness_decrease(self, 
                                          value: Optional[float] = None,
                                          unit: Optional[str] = None,
                                          degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Decrease the brightness of the HUD.
        
        Args:
            value (Optional[float]): The numeric value to adjust the HUD brightness. 
                                     Mutually exclusive with 'degree'.
            unit (Optional[str]): The unit for adjusting the HUD brightness. 
                                  Possible values: 'level', 'percentage', 'Nits'.
                                  Mutually exclusive with 'degree'.
            degree (Optional[str]): The degree to adjust the HUD brightness.
                                    Possible values: 'large', 'little', 'tiny'.
                                    Mutually exclusive with 'value' and 'unit'.
                                    
        Returns:
            Dict[str, Any]: Operation result and updated brightness information
        """
        # Validate state
        if not self.is_on:
            return {
                "success": False,
                "message": "Cannot adjust brightness: HUD is turned off",
                "current_state": {"is_on": self.is_on}
            }
        
        # Track original values for reporting changes
        original_brightness = {
            "level": self.brightness_level,
            "percentage": self.brightness_percentage,
            "nits": self.brightness_nits
        }
        
        # Process degree-based adjustments
        if degree is not None:
            try:
                degree_enum = self.AdjustmentDegreeEnum(degree)
                current_unit = self.current_brightness_unit.value
                decrement = self.BRIGHTNESS_INCREMENTS[degree_enum][current_unit]
                
                # Apply decrement based on current unit
                if current_unit == self.BrightnessUnitEnum.LEVEL.value:
                    self.brightness_level -= decrement
                elif current_unit == self.BrightnessUnitEnum.PERCENTAGE.value:
                    self.brightness_percentage -= decrement
                elif current_unit == self.BrightnessUnitEnum.NITS.value:
                    self.brightness_nits -= decrement
            except (ValueError, KeyError):
                return {
                    "success": False,
                    "message": f"Invalid degree value: {degree}. Expected one of: 'large', 'little', 'tiny'",
                    "current_state": {
                        "brightness_level": self.brightness_level,
                        "brightness_percentage": self.brightness_percentage,
                        "brightness_nits": self.brightness_nits
                    }
                }
        
        # Process value-based adjustments
        elif value is not None and unit is not None:
            try:
                unit_enum = self.BrightnessUnitEnum(unit)
                
                # Apply value based on unit
                if unit_enum == self.BrightnessUnitEnum.LEVEL:
                    self.brightness_level -= value
                    self.current_brightness_unit = self.BrightnessUnitEnum.LEVEL
                elif unit_enum == self.BrightnessUnitEnum.PERCENTAGE:
                    self.brightness_percentage -= value
                    self.current_brightness_unit = self.BrightnessUnitEnum.PERCENTAGE
                elif unit_enum == self.BrightnessUnitEnum.NITS:
                    self.brightness_nits -= value
                    self.current_brightness_unit = self.BrightnessUnitEnum.NITS
            except ValueError:
                return {
                    "success": False,
                    "message": f"Invalid unit value: {unit}. Expected one of: 'level', 'percentage', 'Nits'",
                    "current_state": {
                        "brightness_level": self.brightness_level,
                        "brightness_percentage": self.brightness_percentage,
                        "brightness_nits": self.brightness_nits
                    }
                }
        
        # Default decrement (when no parameters provided)
        else:
            # Decrease by a small default amount
            current_unit = self.current_brightness_unit.value
            decrement = self.BRIGHTNESS_INCREMENTS[self.AdjustmentDegreeEnum.LITTLE][current_unit]
            
            if current_unit == self.BrightnessUnitEnum.LEVEL.value:
                self.brightness_level -= decrement
            elif current_unit == self.BrightnessUnitEnum.PERCENTAGE.value:
                self.brightness_percentage -= decrement
            elif current_unit == self.BrightnessUnitEnum.NITS.value:
                self.brightness_nits -= decrement
        
        # Calculate changes
        brightness_change = {
            "level": self.brightness_level - original_brightness["level"],
            "percentage": self.brightness_percentage - original_brightness["percentage"],
            "nits": self.brightness_nits - original_brightness["nits"]
        }
        
        return {
            "success": True,
            "message": "HUD brightness decreased successfully",
            "brightness_change": brightness_change,
            "current_state": {
                "brightness_level": self.brightness_level,
                "brightness_percentage": self.brightness_percentage,
                "brightness_nits": self.brightness_nits,
                "current_unit": self.current_brightness_unit.value
            }
        }
    
    @api("HUD")
    def carcontrol_HUD_brightness_set(self, 
                                     value: Optional[float] = None,
                                     unit: Optional[str] = None,
                                     degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Set the brightness of the HUD to a specific value.
        
        Args:
            value (Optional[float]): The numeric value to set the HUD brightness. 
                                     Mutually exclusive with 'degree'.
            unit (Optional[str]): The unit for setting the HUD brightness. 
                                  Possible values: 'level', 'percentage', 'Nits'.
                                  Mutually exclusive with 'degree'.
            degree (Optional[str]): The absolute degree for the HUD brightness.
                                    Possible values: 'max', 'high', 'medium', 'low', 'min'.
                                    Mutually exclusive with 'value' and 'unit'.
                                    
        Returns:
            Dict[str, Any]: Operation result and updated brightness information
        """
        # Validate state
        if not self.is_on:
            return {
                "success": False,
                "message": "Cannot set brightness: HUD is turned off",
                "current_state": {"is_on": self.is_on}
            }
        
        # Validate input: either degree OR (value AND unit) must be provided
        if degree is None and (value is None or unit is None):
            return {
                "success": False,
                "message": "Invalid arguments: Either 'degree' OR both 'value' and 'unit' must be provided",
                "current_state": {
                    "brightness_level": self.brightness_level,
                    "brightness_percentage": self.brightness_percentage,
                    "brightness_nits": self.brightness_nits
                }
            }
        
        # Track original values for reporting changes
        original_brightness = {
            "level": self.brightness_level,
            "percentage": self.brightness_percentage,
            "nits": self.brightness_nits
        }
        
        # Process degree-based settings
        if degree is not None:
            try:
                degree_enum = self.SettingDegreeEnum(degree)
                
                # Set brightness for all units based on degree
                level_value = self.BRIGHTNESS_SETTINGS[degree_enum]["level"]
                percentage_value = self.BRIGHTNESS_SETTINGS[degree_enum]["percentage"]
                nits_value = self.BRIGHTNESS_SETTINGS[degree_enum]["Nits"]
                
                # Set all brightness values directly to avoid multiple sync operations
                self._brightness_level = level_value
                self._brightness_percentage = percentage_value
                self._brightness_nits = nits_value
                
            except ValueError:
                return {
                    "success": False,
                    "message": f"Invalid degree value: {degree}. Expected one of: 'max', 'high', 'medium', 'low', 'min'",
                    "current_state": {
                        "brightness_level": self.brightness_level,
                        "brightness_percentage": self.brightness_percentage,
                        "brightness_nits": self.brightness_nits
                    }
                }
        
        # Process value-based settings
        elif value is not None and unit is not None:
            try:
                unit_enum = self.BrightnessUnitEnum(unit)
                
                # Set value based on unit
                if unit_enum == self.BrightnessUnitEnum.LEVEL:
                    self.brightness_level = int(value)
                    self.current_brightness_unit = self.BrightnessUnitEnum.LEVEL
                elif unit_enum == self.BrightnessUnitEnum.PERCENTAGE:
                    self.brightness_percentage = float(value)
                    self.current_brightness_unit = self.BrightnessUnitEnum.PERCENTAGE
                elif unit_enum == self.BrightnessUnitEnum.NITS:
                    self.brightness_nits = float(value)
                    self.current_brightness_unit = self.BrightnessUnitEnum.NITS
            except ValueError:
                return {
                    "success": False,
                    "message": f"Invalid unit value: {unit}. Expected one of: 'level', 'percentage', 'Nits'",
                    "current_state": {
                        "brightness_level": self.brightness_level,
                        "brightness_percentage": self.brightness_percentage,
                        "brightness_nits": self.brightness_nits
                    }
                }
        
        # Calculate changes
        brightness_change = {
            "level": self.brightness_level - original_brightness["level"],
            "percentage": self.brightness_percentage - original_brightness["percentage"],
            "nits": self.brightness_nits - original_brightness["nits"]
        }
        
        return {
            "success": True,
            "message": "HUD brightness set successfully",
            "brightness_change": brightness_change,
            "current_state": {
                "brightness_level": self.brightness_level,
                "brightness_percentage": self.brightness_percentage,
                "brightness_nits": self.brightness_nits,
                "current_unit": self.current_brightness_unit.value
            }
        }
    
    @api("HUD")
    def carcontrol_HUD_height_increase(self, 
                                      value: Optional[float] = None,
                                      unit: Optional[str] = None,
                                      degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Increase the display height of the HUD.
        
        Args:
            value (Optional[float]): The numeric value to adjust the HUD height. 
                                     Mutually exclusive with 'degree'.
            unit (Optional[str]): The unit for adjusting the HUD height. 
                                  Possible values: 'level', 'percentage', 'centimeter'.
                                  Mutually exclusive with 'degree'.
            degree (Optional[str]): The degree to adjust the HUD height.
                                    Possible values: 'large', 'little', 'tiny'.
                                    Mutually exclusive with 'value' and 'unit'.
                                    
        Returns:
            Dict[str, Any]: Operation result and updated height information
        """
        # Validate state
        if not self.is_on:
            return {
                "success": False,
                "message": "Cannot adjust height: HUD is turned off",
                "current_state": {"is_on": self.is_on}
            }
        
        # Track original values for reporting changes
        original_height = {
            "level": self.height_level,
            "percentage": self.height_percentage,
            "centimeter": self.height_centimeter
        }
        
        # Process degree-based adjustments
        if degree is not None:
            try:
                degree_enum = self.AdjustmentDegreeEnum(degree)
                current_unit = self.current_height_unit.value
                increment = self.HEIGHT_INCREMENTS[degree_enum][current_unit]
                
                # Apply increment based on current unit
                if current_unit == self.HeightUnitEnum.LEVEL.value:
                    self.height_level += increment
                elif current_unit == self.HeightUnitEnum.PERCENTAGE.value:
                    self.height_percentage += increment
                elif current_unit == self.HeightUnitEnum.CENTIMETER.value:
                    self.height_centimeter += increment
            except (ValueError, KeyError):
                return {
                    "success": False,
                    "message": f"Invalid degree value: {degree}. Expected one of: 'large', 'little', 'tiny'",
                    "current_state": {
                        "height_level": self.height_level,
                        "height_percentage": self.height_percentage,
                        "height_centimeter": self.height_centimeter
                    }
                }
        
        # Process value-based adjustments
        elif value is not None and unit is not None:
            try:
                unit_enum = self.HeightUnitEnum(unit)
                
                # Apply value based on unit
                if unit_enum == self.HeightUnitEnum.LEVEL:
                    self.height_level += value
                    self.current_height_unit = self.HeightUnitEnum.LEVEL
                elif unit_enum == self.HeightUnitEnum.PERCENTAGE:
                    self.height_percentage += value
                    self.current_height_unit = self.HeightUnitEnum.PERCENTAGE
                elif unit_enum == self.HeightUnitEnum.CENTIMETER:
                    self.height_centimeter += value
                    self.current_height_unit = self.HeightUnitEnum.CENTIMETER
            except ValueError:
                return {
                    "success": False,
                    "message": f"Invalid unit value: {unit}. Expected one of: 'level', 'percentage', 'centimeter'",
                    "current_state": {
                        "height_level": self.height_level,
                        "height_percentage": self.height_percentage,
                        "height_centimeter": self.height_centimeter
                    }
                }
        
        # Default increment (when no parameters provided)
        else:
            # Increase by a small default amount
            current_unit = self.current_height_unit.value
            increment = self.HEIGHT_INCREMENTS[self.AdjustmentDegreeEnum.LITTLE][current_unit]
            
            if current_unit == self.HeightUnitEnum.LEVEL.value:
                self.height_level += increment
            elif current_unit == self.HeightUnitEnum.PERCENTAGE.value:
                self.height_percentage += increment
            elif current_unit == self.HeightUnitEnum.CENTIMETER.value:
                self.height_centimeter += increment
        
        # Calculate changes
        height_change = {
            "level": self.height_level - original_height["level"],
            "percentage": self.height_percentage - original_height["percentage"],
            "centimeter": self.height_centimeter - original_height["centimeter"]
        }
        
        return {
            "success": True,
            "message": "HUD height increased successfully",
            "height_change": height_change,
            "current_state": {
                "height_level": self.height_level,
                "height_percentage": self.height_percentage,
                "height_centimeter": self.height_centimeter,
                "current_unit": self.current_height_unit.value
            }
        }
    
    @api("HUD")
    def carcontrol_HUD_height_decrease(self, 
                                      value: Optional[float] = None,
                                      unit: Optional[str] = None,
                                      degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Decrease the display height of the HUD.
        
        Args:
            value (Optional[float]): The numeric value to adjust the HUD height. 
                                     Mutually exclusive with 'degree'.
            unit (Optional[str]): The unit for adjusting the HUD height. 
                                  Possible values: 'level', 'percentage', 'centimeter'.
                                  Mutually exclusive with 'degree'.
            degree (Optional[str]): The degree to adjust the HUD height.
                                    Possible values: 'large', 'little', 'tiny'.
                                    Mutually exclusive with 'value' and 'unit'.
                                    
        Returns:
            Dict[str, Any]: Operation result and updated height information
        """
        # Validate state
        if not self.is_on:
            return {
                "success": False,
                "message": "Cannot adjust height: HUD is turned off",
                "current_state": {"is_on": self.is_on}
            }
        
        # Track original values for reporting changes
        original_height = {
            "level": self.height_level,
            "percentage": self.height_percentage,
            "centimeter": self.height_centimeter
        }
        
        # Process degree-based adjustments
        if degree is not None:
            try:
                degree_enum = self.AdjustmentDegreeEnum(degree)
                current_unit = self.current_height_unit.value
                decrement = self.HEIGHT_INCREMENTS[degree_enum][current_unit]
                
                # Apply decrement based on current unit
                if current_unit == self.HeightUnitEnum.LEVEL.value:
                    self.height_level -= decrement
                elif current_unit == self.HeightUnitEnum.PERCENTAGE.value:
                    self.height_percentage -= decrement
                elif current_unit == self.HeightUnitEnum.CENTIMETER.value:
                    self.height_centimeter -= decrement
            except (ValueError, KeyError):
                return {
                    "success": False,
                    "message": f"Invalid degree value: {degree}. Expected one of: 'large', 'little', 'tiny'",
                    "current_state": {
                        "height_level": self.height_level,
                        "height_percentage": self.height_percentage,
                        "height_centimeter": self.height_centimeter
                    }
                }
        
        # Process value-based adjustments
        elif value is not None and unit is not None:
            try:
                unit_enum = self.HeightUnitEnum(unit)
                
                # Apply value based on unit
                if unit_enum == self.HeightUnitEnum.LEVEL:
                    self.height_level -= value
                    self.current_height_unit = self.HeightUnitEnum.LEVEL
                elif unit_enum == self.HeightUnitEnum.PERCENTAGE:
                    self.height_percentage -= value
                    self.current_height_unit = self.HeightUnitEnum.PERCENTAGE
                elif unit_enum == self.HeightUnitEnum.CENTIMETER:
                    self.height_centimeter -= value
                    self.current_height_unit = self.HeightUnitEnum.CENTIMETER
            except ValueError:
                return {
                    "success": False,
                    "message": f"Invalid unit value: {unit}. Expected one of: 'level', 'percentage', 'centimeter'",
                    "current_state": {
                        "height_level": self.height_level,
                        "height_percentage": self.height_percentage,
                        "height_centimeter": self.height_centimeter
                    }
                }
        
        # Default decrement (when no parameters provided)
        else:
            # Decrease by a small default amount
            current_unit = self.current_height_unit.value
            decrement = self.HEIGHT_INCREMENTS[self.AdjustmentDegreeEnum.LITTLE][current_unit]
            
            if current_unit == self.HeightUnitEnum.LEVEL.value:
                self.height_level -= decrement
            elif current_unit == self.HeightUnitEnum.PERCENTAGE.value:
                self.height_percentage -= decrement
            elif current_unit == self.HeightUnitEnum.CENTIMETER.value:
                self.height_centimeter -= decrement
        
        # Calculate changes
        height_change = {
            "level": self.height_level - original_height["level"],
            "percentage": self.height_percentage - original_height["percentage"],
            "centimeter": self.height_centimeter - original_height["centimeter"]
        }
        
        return {
            "success": True,
            "message": "HUD height decreased successfully",
            "height_change": height_change,
            "current_state": {
                "height_level": self.height_level,
                "height_percentage": self.height_percentage,
                "height_centimeter": self.height_centimeter,
                "current_unit": self.current_height_unit.value
            }
        }
    
    @api("HUD")
    def carcontrol_HUD_height_set(self, 
                                 value: Optional[float] = None,
                                 unit: Optional[str] = None,
                                 degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Set the HUD display height to a specific value.
        
        Args:
            value (Optional[float]): The numeric value to set the HUD height. 
                                     Mutually exclusive with 'degree'.
            unit (Optional[str]): The unit for setting the HUD height. 
                                  Possible values: 'level', 'percentage', 'centimeter'.
                                  Mutually exclusive with 'degree'.
            degree (Optional[str]): The absolute degree for the HUD height.
                                    Possible values: 'max', 'high', 'medium', 'low', 'min'.
                                    Mutually exclusive with 'value' and 'unit'.
                                    
        Returns:
            Dict[str, Any]: Operation result and updated height information
        """
        # Validate state
        if not self.is_on:
            return {
                "success": False,
                "message": "Cannot set height: HUD is turned off",
                "current_state": {"is_on": self.is_on}
            }
        
        # Validate input: either degree OR (value AND unit) must be provided
        if degree is None and (value is None or unit is None):
            return {
                "success": False,
                "message": "Invalid arguments: Either 'degree' OR both 'value' and 'unit' must be provided",
                "current_state": {
                    "height_level": self.height_level,
                    "height_percentage": self.height_percentage,
                    "height_centimeter": self.height_centimeter
                }
            }
        
        # Track original values for reporting changes
        original_height = {
            "level": self.height_level,
            "percentage": self.height_percentage,
            "centimeter": self.height_centimeter
        }
        
        # Process degree-based settings
        if degree is not None:
            try:
                degree_enum = self.SettingDegreeEnum(degree)
                
                # Set height for all units based on degree
                level_value = self.HEIGHT_SETTINGS[degree_enum]["level"]
                percentage_value = self.HEIGHT_SETTINGS[degree_enum]["percentage"]
                centimeter_value = self.HEIGHT_SETTINGS[degree_enum]["centimeter"]
                
                # Set all height values directly to avoid multiple sync operations
                self._height_level = level_value
                self._height_percentage = percentage_value
                self._height_centimeter = centimeter_value
                
            except ValueError:
                return {
                    "success": False,
                    "message": f"Invalid degree value: {degree}. Expected one of: 'max', 'high', 'medium', 'low', 'min'",
                    "current_state": {
                        "height_level": self.height_level,
                        "height_percentage": self.height_percentage,
                        "height_centimeter": self.height_centimeter
                    }
                }
        
        # Process value-based settings
        elif value is not None and unit is not None:
            try:
                unit_enum = self.HeightUnitEnum(unit)
                
                # Set value based on unit
                if unit_enum == self.HeightUnitEnum.LEVEL:
                    self.height_level = int(value)
                    self.current_height_unit = self.HeightUnitEnum.LEVEL
                elif unit_enum == self.HeightUnitEnum.PERCENTAGE:
                    self.height_percentage = float(value)
                    self.current_height_unit = self.HeightUnitEnum.PERCENTAGE
                elif unit_enum == self.HeightUnitEnum.CENTIMETER:
                    self.height_centimeter = float(value)
                    self.current_height_unit = self.HeightUnitEnum.CENTIMETER
            except ValueError:
                return {
                    "success": False,
                    "message": f"Invalid unit value: {unit}. Expected one of: 'level', 'percentage', 'centimeter'",
                    "current_state": {
                        "height_level": self.height_level,
                        "height_percentage": self.height_percentage,
                        "height_centimeter": self.height_centimeter
                    }
                }
        
        # Calculate changes
        height_change = {
            "level": self.height_level - original_height["level"],
            "percentage": self.height_percentage - original_height["percentage"],
            "centimeter": self.height_centimeter - original_height["centimeter"]
        }
        
        return {
            "success": True,
            "message": "HUD height set successfully",
            "height_change": height_change,
            "current_state": {
                "height_level": self.height_level,
                "height_percentage": self.height_percentage,
                "height_centimeter": self.height_centimeter,
                "current_unit": self.current_height_unit.value
            }
        }
    


    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the HUD entity to a dictionary with value descriptions and types.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the HUD entity
        """
        return {
            "is_on": {
                "value": self.is_on,
                "description": "Whether the HUD is turned on or off",
                "type": type(self.is_on).__name__
            },
            "brightness": {
                "level": {
                    "value": self.brightness_level,
                    "description": "HUD brightness level (1-10)",
                    "type": type(self.brightness_level).__name__
                },
                "percentage": {
                    "value": self.brightness_percentage,
                    "description": "HUD brightness percentage (0-100)",
                    "type": type(self.brightness_percentage).__name__
                },
                "nits": {
                    "value": self.brightness_nits,
                    "description": "HUD brightness in nits (0-1000)",
                    "type": type(self.brightness_nits).__name__
                },
                "current_unit": {
                    "value": self.current_brightness_unit.value,
                    "description": "Current unit used for brightness adjustments. Possible values: 'level', 'percentage', 'Nits'",
                    "type": "BrightnessUnitEnum"
                }
            },
            "height": {
                "level": {
                    "value": self.height_level,
                    "description": "HUD height level (1-10)",
                    "type": type(self.height_level).__name__
                },
                "percentage": {
                    "value": self.height_percentage,
                    "description": "HUD height percentage (0-100)",
                    "type": type(self.height_percentage).__name__
                },
                "centimeter": {
                    "value": self.height_centimeter,
                    "description": "HUD height in centimeters (0-20)",
                    "type": type(self.height_centimeter).__name__
                },
                "current_unit": {
                    "value": self.current_height_unit.value,
                    "description": "Current unit used for height adjustments. Possible values: 'level', 'percentage', 'centimeter'",
                    "type": "HeightUnitEnum"
                }
            },
            "adjustment_increments": {
                "brightness": {
                    "value": {
                        "tiny": self.BRIGHTNESS_INCREMENTS[self.AdjustmentDegreeEnum.TINY],
                        "little": self.BRIGHTNESS_INCREMENTS[self.AdjustmentDegreeEnum.LITTLE],
                        "large": self.BRIGHTNESS_INCREMENTS[self.AdjustmentDegreeEnum.LARGE]
                    },
                    "description": "Increment values for different degrees of brightness adjustment",
                    "type": "Dict"
                },
                "height": {
                    "value": {
                        "tiny": self.HEIGHT_INCREMENTS[self.AdjustmentDegreeEnum.TINY],
                        "little": self.HEIGHT_INCREMENTS[self.AdjustmentDegreeEnum.LITTLE],
                        "large": self.HEIGHT_INCREMENTS[self.AdjustmentDegreeEnum.LARGE]
                    },
                    "description": "Increment values for different degrees of height adjustment",
                    "type": "Dict"
                }
            },
            "preset_settings": {
                "brightness": {
                    "value": {
                        "min": self.BRIGHTNESS_SETTINGS[self.SettingDegreeEnum.MIN],
                        "low": self.BRIGHTNESS_SETTINGS[self.SettingDegreeEnum.LOW],
                        "medium": self.BRIGHTNESS_SETTINGS[self.SettingDegreeEnum.MEDIUM],
                        "high": self.BRIGHTNESS_SETTINGS[self.SettingDegreeEnum.HIGH],
                        "max": self.BRIGHTNESS_SETTINGS[self.SettingDegreeEnum.MAX]
                    },
                    "description": "Predefined brightness values for different setting degrees",
                    "type": "Dict"
                },
                "height": {
                    "value": {
                        "min": self.HEIGHT_SETTINGS[self.SettingDegreeEnum.MIN],
                        "low": self.HEIGHT_SETTINGS[self.SettingDegreeEnum.LOW],
                        "medium": self.HEIGHT_SETTINGS[self.SettingDegreeEnum.MEDIUM],
                        "high": self.HEIGHT_SETTINGS[self.SettingDegreeEnum.HIGH],
                        "max": self.HEIGHT_SETTINGS[self.SettingDegreeEnum.MAX]
                    },
                    "description": "Predefined height values for different setting degrees",
                    "type": "Dict"
                }
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HUD':
        """
        Create a HUD instance from a dictionary representation.
        
        Args:
            data (Dict[str, Any]): Dictionary containing HUD configuration
            
        Returns:
            HUD: New HUD instance with the configuration from the dictionary
        """
        instance = cls()
        
        # Set power state
        instance.is_on = data["is_on"]["value"]
        
        # Set brightness values
        instance._brightness_level = data["brightness"]["level"]["value"]
        instance._brightness_percentage = data["brightness"]["percentage"]["value"]
        instance._brightness_nits = data["brightness"]["nits"]["value"]
        
        # Set current brightness unit
        unit_value = data["brightness"]["current_unit"]["value"]
        instance._current_brightness_unit = instance.BrightnessUnitEnum(unit_value)
        
        # Set height values
        instance._height_level = data["height"]["level"]["value"]
        instance._height_percentage = data["height"]["percentage"]["value"]
        instance._height_centimeter = data["height"]["centimeter"]["value"]
        
        # Set current height unit
        unit_value = data["height"]["current_unit"]["value"]
        instance._current_height_unit = instance.HeightUnitEnum(unit_value)
        
        return instance

    
    @classmethod
    def init1(cls) -> 'HUD':
        """
        Initialize a HUD instance with low brightness and high position settings.
        This configuration is suitable for nighttime driving.
        
        Returns:
            HUD: New HUD instance with low brightness and high position
        """
        instance = cls()
        
        # Set power state to on
        instance.is_on = True
        
        # Set brightness to low level
        instance._brightness_level = 3
        instance._brightness_percentage = 25
        instance._brightness_nits = 250
        instance._current_brightness_unit = cls.BrightnessUnitEnum.PERCENTAGE
        
        # Set height to high position
        instance._height_level = 8
        instance._height_percentage = 75
        instance._height_centimeter = 15
        instance._current_height_unit = cls.HeightUnitEnum.PERCENTAGE
        
        return instance

    @classmethod
    def init2(cls) -> 'HUD':
        """
        Initialize a HUD instance with high brightness and low position settings.
        This configuration is suitable for daytime driving.
        
        Returns:
            HUD: New HUD instance with high brightness and low position
        """
        instance = cls()
        
        # Set power state to on
        instance.is_on = True
        
        # Set brightness to high level
        instance._brightness_level = 8
        instance._brightness_percentage = 75
        instance._brightness_nits = 750
        instance._current_brightness_unit = cls.BrightnessUnitEnum.NITS
        
        # Set height to low position
        instance._height_level = 3
        instance._height_percentage = 25
        instance._height_centimeter = 5
        instance._current_height_unit = cls.HeightUnitEnum.CENTIMETER
        
        return instance