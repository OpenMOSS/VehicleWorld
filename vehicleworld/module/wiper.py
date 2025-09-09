from typing import Dict, Union, Optional, Any, List
from enum import Enum
from utils import api


class Wiper:
    """
    Main Wiper entity class that manages the wipers system of a vehicle.
    Provides functionality to control the wipers on the front and rear windows.
    """
    class WiperPosition(Enum):
        """Enum for wiper positions"""
        FRONT = "front"
        REAR = "rear"
        ALL = "all"

    class SpeedUnit(Enum):
        """Enum for wiper speed units"""
        GEAR = "gear"
        PERCENTAGE = "percentage"

    class SpeedAdjustmentDegree(Enum):
        """Enum for degrees of wiper speed adjustment when increasing/decreasing"""
        LARGE = "large"
        LITTLE = "little"
        TINY = "tiny"

    class SpeedSettingDegree(Enum):
        """Enum for degrees of wiper speed when setting to a specific level"""
        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"

    class WiperSpeedSetting:
        """
        Internal class to manage wiper speed settings.
        This handles both numeric values (with units) and degree-based settings.
        """
        def __init__(self, value: float = 1.0, unit = None):
            if unit is None:
                unit = Wiper.SpeedUnit.GEAR
            self._value = value
            self._unit = unit
            # Default gear range: 1-5, percentage range: 0-100
            self._max_gear = 5
            self._min_gear = 1
            self._max_percentage = 100.0
            self._min_percentage = 0.0
            
            # Mapping of degree settings to numeric values
            self._degree_to_gear = {
                Wiper.SpeedSettingDegree.MIN: 1,
                Wiper.SpeedSettingDegree.LOW: 2,
                Wiper.SpeedSettingDegree.MEDIUM: 3,
                Wiper.SpeedSettingDegree.HIGH: 4,
                Wiper.SpeedSettingDegree.MAX: 5
            }
            
            self._degree_to_percentage = {
                Wiper.SpeedSettingDegree.MIN: 0.0,
                Wiper.SpeedSettingDegree.LOW: 25.0,
                Wiper.SpeedSettingDegree.MEDIUM: 50.0,
                Wiper.SpeedSettingDegree.HIGH: 75.0,
                Wiper.SpeedSettingDegree.MAX: 100.0
            }
            
            # Mapping for adjustment degrees
            self._adjustment_degree_value = {
                Wiper.SpeedAdjustmentDegree.TINY: 1,   # For gear: +1, for percentage: +10%
                Wiper.SpeedAdjustmentDegree.LITTLE: 2, # For gear: +2, for percentage: +25%
                Wiper.SpeedAdjustmentDegree.LARGE: 3   # For gear: +3, for percentage: +50%
            }

        @property
        def value(self) -> float:
            return self._value

        @value.setter
        def value(self, new_value: float):
            # Validate and set the value based on the current unit
            if self._unit == Wiper.SpeedUnit.GEAR:
                self._value = max(min(new_value, self._max_gear), self._min_gear)
            else:  # PERCENTAGE
                self._value = max(min(new_value, self._max_percentage), self._min_percentage)

        @property
        def unit(self):
            return self._unit

        @unit.setter
        def unit(self, new_unit):
            # Convert the value if the unit has changed
            old_unit = self._unit
            self._unit = new_unit
            
            if old_unit != new_unit:
                if old_unit == Wiper.SpeedUnit.GEAR and new_unit == Wiper.SpeedUnit.PERCENTAGE:
                    # Convert from gear to percentage
                    self._value = (self._value - self._min_gear) / (self._max_gear - self._min_gear) * 100
                elif old_unit == Wiper.SpeedUnit.PERCENTAGE and new_unit == Wiper.SpeedUnit.GEAR:
                    # Convert from percentage to gear
                    self._value = self._min_gear + (self._value / 100) * (self._max_gear - self._min_gear)
                    self._value = round(self._value)  # Round to nearest gear

        def set_by_degree(self, degree):
            """Set the speed according to a predefined degree level"""
            if self._unit == Wiper.SpeedUnit.GEAR:
                self._value = self._degree_to_gear[degree]
            else:  # PERCENTAGE
                self._value = self._degree_to_percentage[degree]

        def adjust_by_degree(self, degree, increase: bool = True):
            """
            Adjust the speed by a degree amount (tiny, little, large)
            :param degree: The degree of adjustment
            :param increase: True to increase, False to decrease
            """
            adjustment = self._adjustment_degree_value[degree]
            if self._unit == Wiper.SpeedUnit.GEAR:
                change = adjustment
            else:  # PERCENTAGE
                # Map tiny, little, large to percentage changes
                if degree == Wiper.SpeedAdjustmentDegree.TINY:
                    change = 10.0
                elif degree == Wiper.SpeedAdjustmentDegree.LITTLE:
                    change = 25.0
                else:  # LARGE
                    change = 50.0
            
            if not increase:
                change = -change
            
            self.value = self._value + change  # Use setter to apply validation

        def to_dict(self) -> Dict[str, Any]:
            return {
                "value": {
                    "value": self.value,
                    "description": "The numeric value of wiper speed",
                    "type": type(self.value).__name__
                },
                "unit": {
                    "value": self.unit.value,
                    "description": "The unit of wiper speed. Possible values: gear, percentage",
                    "type": "SpeedUnit enum"
                }
            }
        
        @classmethod
        def from_dict(cls, data: Dict[str, Any]):
            value = data["value"]["value"]
            unit_value = data["unit"]["value"]
            unit = Wiper.SpeedUnit(unit_value)
            instance = cls(value, unit)
            return instance

    class WiperState:
        """
        Internal class to manage the state of a wiper at a specific position.
        """
        def __init__(self, position):
            self._position = position
            self._is_on = False
            self._speed_setting = Wiper.WiperSpeedSetting()

        @property
        def position(self):
            return self._position

        @property
        def is_on(self) -> bool:
            return self._is_on

        @is_on.setter
        def is_on(self, value: bool):
            self._is_on = value

        @property
        def speed_setting(self):
            return self._speed_setting

        def to_dict(self) -> Dict[str, Any]:
            return {
                "position": {
                    "value": self.position.value,
                    "description": "Position of the wiper. Possible values: front, rear, all",
                    "type": "WiperPosition enum"
                },
                "is_on": {
                    "value": self.is_on,
                    "description": "Whether the wiper is turned on (true) or off (false)",
                    "type": type(self.is_on).__name__
                },
                "speed_setting": {
                    "value": self.speed_setting.to_dict(),
                    "description": "The speed setting of the wiper. Maps SpeedSettingDegree to gear values (MIN:1, LOW:2, MEDIUM:3, HIGH:4, MAX:5) and percentage values (MIN:0%, LOW:25%, MEDIUM:50%, HIGH:75%, MAX:100%). Speed adjustments are defined as: TINY (+1 gear/+10%), LITTLE (+2 gear/+25%), LARGE (+3 gear/+50%).",
                    "type": "WiperSpeedSetting"
                }
            }
        
        @classmethod
        def from_dict(cls, data: Dict[str, Any]):
            position_value = data["position"]["value"]
            position = Wiper.WiperPosition(position_value)
            instance = cls(position)
            instance.is_on = data["is_on"]["value"]
            speed_setting_data = data["speed_setting"]["value"]
            instance._speed_setting = Wiper.WiperSpeedSetting.from_dict(speed_setting_data)
            return instance

    def __init__(self):
        # Initialize wipers for different positions
        self._wipers = {
            self.WiperPosition.FRONT: self.WiperState(self.WiperPosition.FRONT),
            self.WiperPosition.REAR: self.WiperState(self.WiperPosition.REAR)
        }

    def _get_affected_wipers(self, position) -> List[WiperState]:
        """Helper method to get the wiper states affected by a position setting"""
        if position == self.WiperPosition.ALL:
            return [self._wipers[self.WiperPosition.FRONT], self._wipers[self.WiperPosition.REAR]]
        else:
            return [self._wipers[position]]

    @property
    def front_wiper(self):
        return self._wipers[self.WiperPosition.FRONT]

    @property
    def rear_wiper(self):
        return self._wipers[self.WiperPosition.REAR]

    @api("wiper")
    def carcontrol_wiperBlade_switch(self, switch: bool, position: str = "all") -> Dict[str, Any]:
        """
        Turn on or off the wiper at the specified position.
        
        :param switch: True to turn on, False to turn off
        :param position: Position of the wiper to control (front, rear, all). Default is 'all'.
                         Possible values: front, rear, all
        :return: A dictionary containing the operation result and updated states
        """
        try:
            wiper_position = self.WiperPosition(position)
            affected_wipers = self._get_affected_wipers(wiper_position)
            
            for wiper in affected_wipers:
                wiper.is_on = switch
            
            return {
                "success": True,
                "message": f"Wiper{'s' if wiper_position == self.WiperPosition.ALL else ''} at {position} position {'turned on' if switch else 'turned off'}",
                "affected_positions": [w.position.value for w in affected_wipers],
                "state": self.to_dict()
            }
        except ValueError as e:
            return {
                "success": False,
                "message": f"Invalid position value: {position}. Must be one of: front, rear, all",
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to switch wiper: {str(e)}",
                "error": str(e)
            }

    @api("wiper")
    def carcontrol_wiperBlade_speed_increase(self, 
                                            value: Optional[float] = None, 
                                            unit: Optional[str] = None, 
                                            degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Increase the wiper speed based on provided parameters.
        
        :param value: Numeric value for speed adjustment (optional)
        :param unit: Unit for speed adjustment (gear, percentage) (optional)
                     Possible values: gear, percentage
        :param degree: Degree of speed adjustment (large, little, tiny) (optional)
                       Possible values: large, little, tiny
        :return: A dictionary containing the operation result and updated states
        """
        try:
            # Check if any parameters were provided
            if value is None and unit is None and degree is None:
                # Default to tiny increase if no parameters specified
                degree = "tiny"
            
            # Process each active wiper
            updated_wipers = []
            for position, wiper in self._wipers.items():
                if wiper.is_on:
                    # Case 1: Using value and unit
                    if value is not None and unit is not None:
                        # Convert unit string to enum
                        speed_unit = self.SpeedUnit(unit)
                        
                        # Store original values to calculate the change
                        original_value = wiper.speed_setting.value
                        original_unit = wiper.speed_setting.unit
                        
                        # Temporarily set the unit to match the input unit
                        wiper.speed_setting.unit = speed_unit
                        
                        # Add the value
                        wiper.speed_setting.value += value
                        
                        # Restore original unit if needed
                        if original_unit != speed_unit:
                            wiper.speed_setting.unit = original_unit
                    
                    # Case 2: Using degree
                    elif degree is not None:
                        adjustment_degree = self.SpeedAdjustmentDegree(degree)
                        wiper.speed_setting.adjust_by_degree(adjustment_degree, increase=True)
                    
                    updated_wipers.append(position.value)
            
            if not updated_wipers:
                return {
                    "success": False,
                    "message": "No active wipers to adjust speed",
                }
            
            return {
                "success": True,
                "message": f"Wiper speed increased for positions: {', '.join(updated_wipers)}",
                "affected_positions": updated_wipers,
                "state": self.to_dict()
            }
        except ValueError as e:
            return {
                "success": False,
                "message": f"Invalid parameter value: {str(e)}",
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to increase wiper speed: {str(e)}",
                "error": str(e)
            }

    @api("wiper")
    def carcontrol_wiperBlade_speed_decrease(self, 
                                            value: Optional[float] = None, 
                                            unit: Optional[str] = None, 
                                            degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Decrease the wiper speed based on provided parameters.
        
        :param value: Numeric value for speed adjustment (optional)
        :param unit: Unit for speed adjustment (gear, percentage) (optional)
                     Possible values: gear, percentage
        :param degree: Degree of speed adjustment (large, little, tiny) (optional)
                       Possible values: large, little, tiny
        :return: A dictionary containing the operation result and updated states
        """
        try:
            # Check if any parameters were provided
            if value is None and unit is None and degree is None:
                # Default to tiny decrease if no parameters specified
                degree = "tiny"
            
            # Process each active wiper
            updated_wipers = []
            for position, wiper in self._wipers.items():
                if wiper.is_on:
                    # Case 1: Using value and unit
                    if value is not None and unit is not None:
                        # Convert unit string to enum
                        speed_unit = self.SpeedUnit(unit)
                        
                        # Store original values to calculate the change
                        original_value = wiper.speed_setting.value
                        original_unit = wiper.speed_setting.unit
                        
                        # Temporarily set the unit to match the input unit
                        wiper.speed_setting.unit = speed_unit
                        
                        # Subtract the value
                        wiper.speed_setting.value -= value
                        
                        # Restore original unit if needed
                        if original_unit != speed_unit:
                            wiper.speed_setting.unit = original_unit
                    
                    # Case 2: Using degree
                    elif degree is not None:
                        adjustment_degree = self.SpeedAdjustmentDegree(degree)
                        wiper.speed_setting.adjust_by_degree(adjustment_degree, increase=False)
                    
                    updated_wipers.append(position.value)
            
            if not updated_wipers:
                return {
                    "success": False,
                    "message": "No active wipers to adjust speed",
                }
            
            return {
                "success": True,
                "message": f"Wiper speed decreased for positions: {', '.join(updated_wipers)}",
                "affected_positions": updated_wipers,
                "state": self.to_dict()
            }
        except ValueError as e:
            return {
                "success": False,
                "message": f"Invalid parameter value: {str(e)}",
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to decrease wiper speed: {str(e)}",
                "error": str(e)
            }

    @api("wiper")
    def carcontrol_wiperBlade_speed_set(self, 
                                       value: Optional[float] = None, 
                                       unit: Optional[str] = None, 
                                       degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Set the wiper speed to a specific value.
        
        :param value: Numeric value for speed setting (required if degree not provided)
        :param unit: Unit for speed value (gear, percentage) (required if value is provided)
                     Possible values: gear, percentage
        :param degree: Predefined speed level (max, high, medium, low, min) (required if value not provided)
                       Possible values: max, high, medium, low, min
        :return: A dictionary containing the operation result and updated states
        """
        try:
            # Validate that either (value + unit) or degree is provided
            if (value is not None and unit is None) or (value is None and unit is not None):
                return {
                    "success": False,
                    "message": "Both value and unit must be provided together",
                }
            
            if value is None and unit is None and degree is None:
                return {
                    "success": False,
                    "message": "Must provide either (value + unit) or degree parameter",
                }
            
            # Process each active wiper
            updated_wipers = []
            for position, wiper in self._wipers.items():
                if wiper.is_on:
                    # Case 1: Using value and unit
                    if value is not None and unit is not None:
                        # Set unit first, then value
                        wiper.speed_setting.unit = self.SpeedUnit(unit)
                        wiper.speed_setting.value = value
                    
                    # Case 2: Using degree
                    elif degree is not None:
                        setting_degree = self.SpeedSettingDegree(degree)
                        wiper.speed_setting.set_by_degree(setting_degree)
                    
                    updated_wipers.append(position.value)
            
            if not updated_wipers:
                return {
                    "success": False,
                    "message": "No active wipers to set speed",
                }
            
            return {
                "success": True,
                "message": f"Wiper speed set for positions: {', '.join(updated_wipers)}",
                "affected_positions": updated_wipers,
                "state": self.to_dict()
            }
        except ValueError as e:
            return {
                "success": False,
                "message": f"Invalid parameter value: {str(e)}",
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to set wiper speed: {str(e)}",
                "error": str(e)
            }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Wiper object to a dictionary representation with all attributes, types, and descriptions.
        """
        return {
            "front_wiper": {
                "value": self.front_wiper.to_dict(),
                "description": "Front windshield wiper state",
                "type": "WiperState"
            },
            "rear_wiper": {
                "value": self.rear_wiper.to_dict(),
                "description": "Rear windshield wiper state",
                "type": "WiperState"
            }
        }
    

    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Create a Wiper instance from a dictionary representation.
        
        :param data: Dictionary with Wiper attributes
        :return: A new Wiper instance
        """
        instance = cls()
        
        # Restore front wiper
        front_wiper_data = data["front_wiper"]["value"]
        instance._wipers[cls.WiperPosition.FRONT] = cls.WiperState.from_dict(front_wiper_data)
        
        # Restore rear wiper
        rear_wiper_data = data["rear_wiper"]["value"]
        instance._wipers[cls.WiperPosition.REAR] = cls.WiperState.from_dict(rear_wiper_data)
        
        return instance
    
    @classmethod
    def init1(cls):
        """
        Initialize a Wiper instance with front wiper on at medium speed and rear wiper off.
        
        :return: A new Wiper instance with predefined state
        """
        instance = cls()
        
        # Configure front wiper: turned on, medium speed
        instance.front_wiper.is_on = True
        instance.front_wiper.speed_setting.set_by_degree(cls.SpeedSettingDegree.MEDIUM)
        
        # Configure rear wiper: turned off (default state)
        instance.rear_wiper.is_on = False
        
        return instance

    @classmethod
    def init2(cls):
        """
        Initialize a Wiper instance with both wipers on, front at high speed (percentage unit)
        and rear at low speed (gear unit).
        
        :return: A new Wiper instance with predefined state
        """
        instance = cls()
        
        # Configure front wiper: turned on, high speed with percentage unit
        instance.front_wiper.is_on = True
        instance.front_wiper.speed_setting.unit = cls.SpeedUnit.PERCENTAGE
        instance.front_wiper.speed_setting.set_by_degree(cls.SpeedSettingDegree.HIGH)
        
        # Configure rear wiper: turned on, low speed with gear unit
        instance.rear_wiper.is_on = True
        instance.rear_wiper.speed_setting.set_by_degree(cls.SpeedSettingDegree.LOW)
        
        return instance