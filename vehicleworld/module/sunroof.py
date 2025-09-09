from enum import Enum
from typing import Dict, Union, Optional, Any, List, Tuple
from utils import api

class Sunroof:
    class SunroofState(Enum):
        """
        Enum representing the different states of the sunroof.
        """
        CLOSED = "closed"
        OPENING = "opening"
        CLOSING = "closing"
        PAUSED = "paused"
        OPEN = "open"
        TILTED = "tilted"
    
    class SunroofAction(Enum):
        """
        Enum representing the different actions that can be performed on the sunroof.
        """
        OPEN = "open"
        CLOSE = "close"
        PAUSE = "pause"
        TILT = "Tilt"
    
    class OpenDegreeUnit(Enum):
        """
        Enum representing the different units for specifying the sunroof's open degree.
        """
        GEAR = "gear"
        PERCENTAGE = "percentage"
        CENTIMETER = "centimeter"
    
    class AdjustmentDegree(Enum):
        """
        Enum representing the different levels of adjustment for the sunroof's open degree.
        """
        LARGE = "large"
        LITTLE = "little"
        TINY = "tiny"
    
    class OpenDegreeLevel(Enum):
        """
        Enum representing the predefined levels for the sunroof's open degree.
        """
        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"
    
    def __init__(self):
        # Initialize the sunroof state
        self._state = Sunroof.SunroofState.CLOSED
        
        # Open degree properties
        self._open_degree_percentage = 0.0
        self._open_degree_gear = 0
        self._open_degree_centimeter = 0.0
        
        # Configuration properties
        self._max_gear = 10
        self._max_centimeter = 50.0
        self._gear_to_percentage_ratio = 10.0  # 1 gear = 10%
        self._centimeter_to_percentage_ratio = 2.0  # 1 cm = 2%
        
        # Adjustment increments for each degree level
        self._adjustment_values = {
            Sunroof.AdjustmentDegree.TINY: {
                Sunroof.OpenDegreeUnit.GEAR: 1,
                Sunroof.OpenDegreeUnit.PERCENTAGE: 10.0,
                Sunroof.OpenDegreeUnit.CENTIMETER: 5.0
            },
            Sunroof.AdjustmentDegree.LITTLE: {
                Sunroof.OpenDegreeUnit.GEAR: 2,
                Sunroof.OpenDegreeUnit.PERCENTAGE: 20.0,
                Sunroof.OpenDegreeUnit.CENTIMETER: 10.0
            },
            Sunroof.AdjustmentDegree.LARGE: {
                Sunroof.OpenDegreeUnit.GEAR: 5,
                Sunroof.OpenDegreeUnit.PERCENTAGE: 50.0,
                Sunroof.OpenDegreeUnit.CENTIMETER: 25.0
            }
        }
        
        # Predefined levels for open degree
        self._open_degree_levels = {
            Sunroof.OpenDegreeLevel.MIN: 0.0,
            Sunroof.OpenDegreeLevel.LOW: 25.0,
            Sunroof.OpenDegreeLevel.MEDIUM: 50.0,
            Sunroof.OpenDegreeLevel.HIGH: 75.0,
            Sunroof.OpenDegreeLevel.MAX: 100.0
        }
    
    # State property
    @property
    def state(self) -> SunroofState:
        return self._state
    
    @state.setter
    def state(self, value: SunroofState):
        if not isinstance(value, Sunroof.SunroofState):
            raise TypeError("State must be a SunroofState enum value")
        self._state = value
    
    # Open degree percentage property
    @property
    def open_degree_percentage(self) -> float:
        return self._open_degree_percentage
    
    @open_degree_percentage.setter
    def open_degree_percentage(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Open degree percentage must be a number")
        
        # Clamp the value between 0 and 100
        self._open_degree_percentage = max(0.0, min(100.0, float(value)))
        
        # Update other units accordingly
        self._update_other_units_from_percentage()
        
        # Update state based on open degree
        self._update_state_from_open_degree()
    
    # Open degree gear property
    @property
    def open_degree_gear(self) -> int:
        return self._open_degree_gear
    
    @open_degree_gear.setter
    def open_degree_gear(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Open degree gear must be an integer")
        
        # Clamp the value between 0 and max_gear
        self._open_degree_gear = max(0, min(self._max_gear, value))
        
        # Convert to percentage and update other units
        self._open_degree_percentage = (self._open_degree_gear / self._max_gear) * 100.0
        self._update_other_units_from_percentage()
        
        # Update state based on open degree
        self._update_state_from_open_degree()
    
    # Open degree centimeter property
    @property
    def open_degree_centimeter(self) -> float:
        return self._open_degree_centimeter
    
    @open_degree_centimeter.setter
    def open_degree_centimeter(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Open degree centimeter must be a number")
        
        # Clamp the value between 0 and max_centimeter
        self._open_degree_centimeter = max(0.0, min(self._max_centimeter, float(value)))
        
        # Convert to percentage and update other units
        self._open_degree_percentage = (self._open_degree_centimeter / self._max_centimeter) * 100.0
        self._update_other_units_from_percentage()
        
        # Update state based on open degree
        self._update_state_from_open_degree()
    
    # Helper methods for internal state updates
    def _update_other_units_from_percentage(self):
        """
        Update gear and centimeter values based on the current percentage.
        """
        self._open_degree_gear = int((self._open_degree_percentage / 100.0) * self._max_gear)
        self._open_degree_centimeter = (self._open_degree_percentage / 100.0) * self._max_centimeter
    
    def _update_state_from_open_degree(self):
        """
        Update the state based on the current open degree.
        """
        if self._open_degree_percentage == 0:
            self._state = Sunroof.SunroofState.CLOSED
        elif self._open_degree_percentage == 100:
            self._state = Sunroof.SunroofState.OPEN
        elif self._state == Sunroof.SunroofState.TILTED:
            # If it was tilted, keep it tilted
            pass
        elif self._state not in [Sunroof.SunroofState.PAUSED, Sunroof.SunroofState.OPENING, Sunroof.SunroofState.CLOSING]:
            # If not in a transitional state, set to open
            self._state = Sunroof.SunroofState.OPEN
    
    # API methods
    @api("sunroof")
    def carcontrol_sunroof_switch(self, action: str) -> Dict[str, Any]:
        """
        Open, close, pause, or tilt vehicle sunroof.
        
        Args:
            action (str): Sunroof control mode. 
                          Enum values: ['open', 'close', 'pause', 'Tilt']
        
        Returns:
            Dict[str, Any]: Operation result and current sunroof state
        """
        try:
            # Validate action parameter
            if not action:
                return {"success": False, "error": "Action parameter is required", "state": self.state.value}
            
            # Convert to enum if provided as string
            if isinstance(action, str):
                try:
                    action = Sunroof.SunroofAction(action)
                except ValueError:
                    return {
                        "success": False, 
                        "error": f"Invalid action: {action}. Must be one of {[a.value for a in Sunroof.SunroofAction]}", 
                        "state": self.state.value
                    }
            
            # Process the action
            if action == Sunroof.SunroofAction.OPEN:
                self.state = Sunroof.SunroofState.OPENING
                self.open_degree_percentage = 100.0
                self.state = Sunroof.SunroofState.OPEN
            elif action == Sunroof.SunroofAction.CLOSE:
                self.state = Sunroof.SunroofState.CLOSING
                self.open_degree_percentage = 0.0
                self.state = Sunroof.SunroofState.CLOSED
            elif action == Sunroof.SunroofAction.PAUSE:
                if self.state in [Sunroof.SunroofState.OPENING, Sunroof.SunroofState.CLOSING]:
                    self.state = Sunroof.SunroofState.PAUSED
            elif action == Sunroof.SunroofAction.TILT:
                self.state = Sunroof.SunroofState.TILTED
                # Assuming tilt is a special state with a fixed opening degree
                self.open_degree_percentage = 15.0
            
            return {
                "success": True,
                "action": action.value,
                "state": self.state.value,
                "open_degree_percentage": self.open_degree_percentage,
                "open_degree_gear": self.open_degree_gear,
                "open_degree_centimeter": self.open_degree_centimeter
            }
        
        except Exception as e:
            return {"success": False, "error": str(e), "state": self.state.value}
    
    @api("sunroof")
    def carcontrol_sunroof_openDegree_increase(
        self, 
        value: Optional[float] = None, 
        unit: Optional[str] = None, 
        degree: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        When called, the sunroof's open degree will increase.
        
        Args:
            value (Optional[float]): Numeric part of specific sunroof open degree adjustment, 
                                    unit reference from unit field, mutually exclusive with degree.
            unit (Optional[str]): Unit part of specific sunroof open degree adjustment, 
                                 mutually exclusive with degree.
                                 Enum values: ['gear', 'percentage', 'centimeter']
            degree (Optional[str]): Different levels of sunroof open degree adjustment, 
                                   tiny is the smallest, large is the largest, 
                                   mutually exclusive with value/unit.
                                   Enum values: ['large', 'little', 'tiny']
        
        Returns:
            Dict[str, Any]: Operation result and updated sunroof state
        """
        try:
            # Use default adjustment if no parameters provided
            if value is None and unit is None and degree is None:
                degree = Sunroof.AdjustmentDegree.LITTLE.value
            
            # Process based on provided parameters
            if degree is not None:
                # Validate and convert degree
                try:
                    adjustment_degree = Sunroof.AdjustmentDegree(degree)
                except ValueError:
                    return {
                        "success": False, 
                        "error": f"Invalid degree: {degree}. Must be one of {[d.value for d in Sunroof.AdjustmentDegree]}", 
                        "state": self.state.value
                    }
                
                # Apply the percentage adjustment
                adjustment = self._adjustment_values[adjustment_degree][Sunroof.OpenDegreeUnit.PERCENTAGE]
                new_percentage = self.open_degree_percentage + adjustment
                
            elif value is not None and unit is not None:
                # Validate and convert unit
                try:
                    adjustment_unit = Sunroof.OpenDegreeUnit(unit)
                except ValueError:
                    return {
                        "success": False, 
                        "error": f"Invalid unit: {unit}. Must be one of {[u.value for u in Sunroof.OpenDegreeUnit]}", 
                        "state": self.state.value
                    }
                
                # Apply the adjustment based on the unit
                if adjustment_unit == Sunroof.OpenDegreeUnit.PERCENTAGE:
                    new_percentage = self.open_degree_percentage + value
                elif adjustment_unit == Sunroof.OpenDegreeUnit.GEAR:
                    new_gear = self.open_degree_gear + int(value)
                    new_percentage = (new_gear / self._max_gear) * 100.0
                elif adjustment_unit == Sunroof.OpenDegreeUnit.CENTIMETER:
                    new_centimeter = self.open_degree_centimeter + value
                    new_percentage = (new_centimeter / self._max_centimeter) * 100.0
            else:
                return {
                    "success": False, 
                    "error": "Invalid parameters. Either provide degree or both value and unit", 
                    "state": self.state.value
                }
            
            # Update the state based on current operation
            if self.state == Sunroof.SunroofState.CLOSED:
                self.state = Sunroof.SunroofState.OPENING
            elif self.state == Sunroof.SunroofState.PAUSED:
                self.state = Sunroof.SunroofState.OPENING
            
            # Apply the new percentage
            old_percentage = self.open_degree_percentage
            self.open_degree_percentage = new_percentage
            
            # If fully open, update state
            if self.open_degree_percentage >= 100.0:
                self.state = Sunroof.SunroofState.OPEN
            
            return {
                "success": True,
                "previous_open_degree_percentage": old_percentage,
                "open_degree_percentage": self.open_degree_percentage,
                "open_degree_gear": self.open_degree_gear,
                "open_degree_centimeter": self.open_degree_centimeter,
                "state": self.state.value
            }
        
        except Exception as e:
            return {"success": False, "error": str(e), "state": self.state.value}
    
    @api("sunroof")
    def carcontrol_sunroof_openDegree_decrease(
        self, 
        value: Optional[float] = None, 
        unit: Optional[str] = None, 
        degree: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        When called, the sunroof's open degree will decrease.
        
        Args:
            value (Optional[float]): Numeric part of specific sunroof open degree adjustment, 
                                    unit reference from unit field, mutually exclusive with degree.
            unit (Optional[str]): Unit part of specific sunroof open degree adjustment, 
                                 mutually exclusive with degree.
                                 Enum values: ['gear', 'percentage', 'centimeter']
            degree (Optional[str]): Different levels of sunroof open degree adjustment, 
                                   tiny is the smallest, large is the largest, 
                                   mutually exclusive with value/unit.
                                   Enum values: ['large', 'little', 'tiny']
        
        Returns:
            Dict[str, Any]: Operation result and updated sunroof state
        """
        try:
            # Use default adjustment if no parameters provided
            if value is None and unit is None and degree is None:
                degree = Sunroof.AdjustmentDegree.LITTLE.value
            
            # Process based on provided parameters
            if degree is not None:
                # Validate and convert degree
                try:
                    adjustment_degree = Sunroof.AdjustmentDegree(degree)
                except ValueError:
                    return {
                        "success": False, 
                        "error": f"Invalid degree: {degree}. Must be one of {[d.value for d in Sunroof.AdjustmentDegree]}", 
                        "state": self.state.value
                    }
                
                # Apply the percentage adjustment (decrease)
                adjustment = self._adjustment_values[adjustment_degree][Sunroof.OpenDegreeUnit.PERCENTAGE]
                new_percentage = self.open_degree_percentage - adjustment
                
            elif value is not None and unit is not None:
                # Validate and convert unit
                try:
                    adjustment_unit = Sunroof.OpenDegreeUnit(unit)
                except ValueError:
                    return {
                        "success": False, 
                        "error": f"Invalid unit: {unit}. Must be one of {[u.value for u in Sunroof.OpenDegreeUnit]}", 
                        "state": self.state.value
                    }
                
                # Apply the adjustment based on the unit (decrease)
                if adjustment_unit == Sunroof.OpenDegreeUnit.PERCENTAGE:
                    new_percentage = self.open_degree_percentage - value
                elif adjustment_unit == Sunroof.OpenDegreeUnit.GEAR:
                    new_gear = self.open_degree_gear - int(value)
                    new_percentage = (new_gear / self._max_gear) * 100.0
                elif adjustment_unit == Sunroof.OpenDegreeUnit.CENTIMETER:
                    new_centimeter = self.open_degree_centimeter - value
                    new_percentage = (new_centimeter / self._max_centimeter) * 100.0
            else:
                return {
                    "success": False, 
                    "error": "Invalid parameters. Either provide degree or both value and unit", 
                    "state": self.state.value
                }
            
            # Update the state based on current operation
            if self.state == Sunroof.SunroofState.OPEN:
                self.state = Sunroof.SunroofState.CLOSING
            elif self.state == Sunroof.SunroofState.PAUSED:
                self.state = Sunroof.SunroofState.CLOSING
            
            # Apply the new percentage
            old_percentage = self.open_degree_percentage
            self.open_degree_percentage = new_percentage
            
            # If fully closed, update state
            if self.open_degree_percentage <= 0.0:
                self.state = Sunroof.SunroofState.CLOSED
            
            return {
                "success": True,
                "previous_open_degree_percentage": old_percentage,
                "open_degree_percentage": self.open_degree_percentage,
                "open_degree_gear": self.open_degree_gear,
                "open_degree_centimeter": self.open_degree_centimeter,
                "state": self.state.value
            }
        
        except Exception as e:
            return {"success": False, "error": str(e), "state": self.state.value}
    
    @api("sunroof")
    def carcontrol_sunroof_openDegree_set(
        self, 
        value: Optional[float] = None, 
        unit: Optional[str] = None, 
        degree: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        When called, the sunroof's open degree will be set to a specific value.
        
        Args:
            value (Optional[float]): Numeric part of specific sunroof open degree adjustment, 
                                    unit reference from unit field, mutually exclusive with degree.
            unit (Optional[str]): Unit part of specific sunroof open degree adjustment, 
                                 mutually exclusive with degree.
                                 Enum values: ['gear', 'percentage', 'centimeter']
            degree (Optional[str]): Different levels of sunroof open degree adjustment, 
                                   mutually exclusive with value/unit.
                                   Enum values: ['max', 'high', 'medium', 'low', 'min']
        
        Returns:
            Dict[str, Any]: Operation result and updated sunroof state
        """
        try:
            if degree is not None:
                # Validate and convert degree
                try:
                    open_level = Sunroof.OpenDegreeLevel(degree)
                except ValueError:
                    return {
                        "success": False, 
                        "error": f"Invalid degree: {degree}. Must be one of {[l.value for l in Sunroof.OpenDegreeLevel]}", 
                        "state": self.state.value
                    }
                
                # Get the percentage for the specified level
                new_percentage = self._open_degree_levels[open_level]
                
            elif value is not None and unit is not None:
                # Validate and convert unit
                try:
                    set_unit = Sunroof.OpenDegreeUnit(unit)
                except ValueError:
                    return {
                        "success": False, 
                        "error": f"Invalid unit: {unit}. Must be one of {[u.value for u in Sunroof.OpenDegreeUnit]}", 
                        "state": self.state.value
                    }
                
                # Calculate the new percentage based on the unit
                if set_unit == Sunroof.OpenDegreeUnit.PERCENTAGE:
                    new_percentage = value
                elif set_unit == Sunroof.OpenDegreeUnit.GEAR:
                    # Ensure the gear value is an integer and within bounds
                    gear_value = min(max(0, int(value)), self._max_gear)
                    new_percentage = (gear_value / self._max_gear) * 100.0
                elif set_unit == Sunroof.OpenDegreeUnit.CENTIMETER:
                    # Ensure the centimeter value is within bounds
                    cm_value = min(max(0.0, float(value)), self._max_centimeter)
                    new_percentage = (cm_value / self._max_centimeter) * 100.0
            else:
                return {
                    "success": False, 
                    "error": "Invalid parameters. Either provide degree or both value and unit", 
                    "state": self.state.value
                }
            
            # Determine the direction of movement
            if new_percentage > self.open_degree_percentage:
                self.state = Sunroof.SunroofState.OPENING
            elif new_percentage < self.open_degree_percentage:
                self.state = Sunroof.SunroofState.CLOSING
            
            # Store the old percentage for reporting
            old_percentage = self.open_degree_percentage
            
            # Apply the new percentage
            self.open_degree_percentage = new_percentage
            
            # Update the final state
            if self.open_degree_percentage >= 100.0:
                self.state = Sunroof.SunroofState.OPEN
            elif self.open_degree_percentage <= 0.0:
                self.state = Sunroof.SunroofState.CLOSED
            else:
                self.state = Sunroof.SunroofState.OPEN
            
            return {
                "success": True,
                "previous_open_degree_percentage": old_percentage,
                "open_degree_percentage": self.open_degree_percentage,
                "open_degree_gear": self.open_degree_gear,
                "open_degree_centimeter": self.open_degree_centimeter,
                "state": self.state.value
            }
        
        except Exception as e:
            return {"success": False, "error": str(e), "state": self.state.value}
    


    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary representation of the Sunroof entity with attributes, types, and descriptions.
        
        Returns:
            Dict[str, Any]: Dictionary representation
        """
        return {
            "state": {
                "value": self.state.value,
                "description": "Current state of the sunroof. Possible values: " + 
                               ", ".join([state.value for state in Sunroof.SunroofState]),
                "type": "SunroofState (Enum)"
            },
            "open_degree_percentage": {
                "value": self.open_degree_percentage,
                "description": "The open degree of the sunroof expressed as a percentage (0-100%), increases/decreases in sync with open_degree_gear and open_degree_centimeter",
                "type": "float"
            },
            "open_degree_gear": {
                "value": self.open_degree_gear,
                "description": f"The open degree of the sunroof expressed in gears (0-{self._max_gear}), increases/decreases in sync with open_degree_percentage and open_degree_centimeter",
                "type": "int"
            },
            "open_degree_centimeter": {
                "value": self.open_degree_centimeter,
                "description": f"The open degree of the sunroof expressed in centimeters (0-{self._max_centimeter}cm), increases/decreases in sync with open_degree_percentage and open_degree_gear",
                "type": "float"
            },
            "configuration": {
                "max_gear": {
                    "value": self._max_gear,
                    "description": "Maximum number of gears for the sunroof",
                    "type": "int"
                },
                "max_centimeter": {
                    "value": self._max_centimeter,
                    "description": "Maximum opening in centimeters for the sunroof",
                    "type": "float"
                },
                "gear_to_percentage_ratio": {
                    "value": self._gear_to_percentage_ratio,
                    "description": "Conversion ratio from gear to percentage",
                    "type": "float"
                },
                "centimeter_to_percentage_ratio": {
                    "value": self._centimeter_to_percentage_ratio,
                    "description": "Conversion ratio from centimeter to percentage",
                    "type": "float"
                }
            },
            "adjustment_values": {
                "value": {degree.value: {unit.value: value for unit, value in units.items()} 
                          for degree, units in self._adjustment_values.items()},
                "description": "Adjustment increments for each degree level and unit",
                "type": "Dict[str, Dict[str, Union[int, float]]]"
            },
            "open_degree_levels": {
                "value": {level.value: value for level, value in self._open_degree_levels.items()},
                "description": "Predefined percentage values for each open degree level",
                "type": "Dict[str, float]"
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Sunroof':
        """
        Creates a Sunroof instance from a dictionary representation.
        
        Args:
            data (Dict[str, Any]): Dictionary representation of a Sunroof entity
        
        Returns:
            Sunroof: A new Sunroof instance
        """
        instance = cls()
        
        # Set the state
        if "state" in data:
            state_value = data["state"]["value"]
            instance.state = Sunroof.SunroofState(state_value)
        
        # Set the open degree (percentage is the primary representation)
        if "open_degree_percentage" in data:
            instance.open_degree_percentage = data["open_degree_percentage"]["value"]
        
        # Set configuration values if present
        if "configuration" in data:
            config = data["configuration"]
            if "max_gear" in config:
                instance._max_gear = config["max_gear"]["value"]
            if "max_centimeter" in config:
                instance._max_centimeter = config["max_centimeter"]["value"]
            if "gear_to_percentage_ratio" in config:
                instance._gear_to_percentage_ratio = config["gear_to_percentage_ratio"]["value"]
            if "centimeter_to_percentage_ratio" in config:
                instance._centimeter_to_percentage_ratio = config["centimeter_to_percentage_ratio"]["value"]
        
        # Update dependent values
        instance._update_other_units_from_percentage()
        
        return instance
    

    @classmethod
    def init1(cls) -> 'Sunroof':
        """
        Initialize a Sunroof instance in a partially open state.
        
        Returns:
            Sunroof: A new Sunroof instance with 50% open degree (medium setting)
        """
        instance = cls()
        # Set to medium open degree (50%)
        instance.open_degree_percentage = 50.0
        instance.state = Sunroof.SunroofState.OPEN
        return instance

    @classmethod
    def init2(cls) -> 'Sunroof':
        """
        Initialize a Sunroof instance in a tilted state.
        
        Returns:
            Sunroof: A new Sunroof instance in tilted state with 15% open degree
        """
        instance = cls()
        instance.state = Sunroof.SunroofState.TILTED
        instance.open_degree_percentage = 15.0
        return instance