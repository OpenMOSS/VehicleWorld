
from enum import Enum
from utils import api

class FrontTrunk:
    class OpenDegreeUnit(Enum):
        """
        Unit used for open degree measurement.
        """
        GEAR = "gear"
        PERCENTAGE = "percentage" 
        CENTIMETER = "centimeter"
    
    class OpenDegreeLevel(Enum):
        """
        Predefined levels for open degree adjustments.
        """
        # For increase/decrease operations
        LARGE = "large"
        LITTLE = "little"
        TINY = "tiny"
        # For set operations
        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"
    
    class TrunkAction(Enum):
        """
        Actions that can be performed on the front trunk.
        """
        OPEN = "open"
        CLOSE = "close"
       
    
    class TrunkState(Enum):
        """
        Possible states of the front trunk.
        """
        CLOSED = "closed"
        OPEN = "open"
        
    
    def __init__(self):
        # Current state of the trunk
        self._state = self.TrunkState.CLOSED
        
        # Open degree related attributes
        self._open_degree_value = 0.0  # Numeric value of open degree
        self._open_degree_unit = self.OpenDegreeUnit.PERCENTAGE  # Default unit
        
        # Max open degree values for different units
        self._max_open_degrees = {
            self.OpenDegreeUnit.GEAR: 5.0,  # Assuming 5 gears
            self.OpenDegreeUnit.PERCENTAGE: 100.0,  # 0-100%
            self.OpenDegreeUnit.CENTIMETER: 50.0,  # Assuming max height is 50cm
        }
        
        # Mapping of degree levels to percentage values
        self._degree_level_mapping = {
            # For increase/decrease
            self.OpenDegreeLevel.TINY: 5.0,
            self.OpenDegreeLevel.LITTLE: 15.0,
            self.OpenDegreeLevel.LARGE: 30.0,
            # For set operations
            self.OpenDegreeLevel.MIN: 10.0,
            self.OpenDegreeLevel.LOW: 25.0,
            self.OpenDegreeLevel.MEDIUM: 50.0,
            self.OpenDegreeLevel.HIGH: 75.0,
            self.OpenDegreeLevel.MAX: 100.0,
        }
        
        # Lock status
        self._is_locked = False
    
    # State property
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        if not isinstance(value, self.TrunkState):
            raise ValueError(f"State must be a TrunkState enum, got {type(value)}")
        self._state = value
    
    # Open degree value property
    @property
    def open_degree_value(self):
        return self._open_degree_value
    
    @open_degree_value.setter
    def open_degree_value(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f"Open degree value must be a number, got {type(value)}")
        # Ensure value is within valid range (0 to max for current unit)
        max_value = self._max_open_degrees[self.open_degree_unit]
        self._open_degree_value = max(0.0, min(value, max_value))
    
    # Open degree unit property
    @property
    def open_degree_unit(self):
        return self._open_degree_unit
    
    @open_degree_unit.setter
    def open_degree_unit(self, value):
        if not isinstance(value, self.OpenDegreeUnit):
            raise ValueError(f"Open degree unit must be an OpenDegreeUnit enum, got {type(value)}")
        
        # Convert current value to percentage for consistent storage
        if self._open_degree_unit != value:
            # First convert current value to percentage
            percentage = (self._open_degree_value / self._max_open_degrees[self._open_degree_unit]) * 100.0
            # Then convert percentage to new unit's value
            self._open_degree_value = (percentage / 100.0) * self._max_open_degrees[value]
            self._open_degree_unit = value
    
    # Is locked property
    @property
    def is_locked(self):
        return self._is_locked
    
    @is_locked.setter
    def is_locked(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"is_locked must be a boolean, got {type(value)}")
        self._is_locked = value
    
    # API implementations
    @api("frontTrunk")
    def carcontrol_frontTrunk_switch(self, action):
        """
        Open, close front trunk action.
        
        Args:
            action (str): Trunk action, must be one of ['open', 'close']
        
        Returns:
            dict: Operation result and current state information
        """
        # Parameter validation
        try:
            trunk_action = self.TrunkAction(action)
        except ValueError:
            return {
                "success": False,
                "error": f"Invalid action: {action}. Must be one of {[a.value for a in self.TrunkAction]}"
            }
        
        # Check if trunk is locked
        if self.is_locked and trunk_action == self.TrunkAction.OPEN:
            return {
                "success": False,
                "error": "Cannot open trunk when locked",
                "current_state": self.state.value,
                "is_locked": self.is_locked
            }
        
        # Process action based on current state
        if trunk_action == self.TrunkAction.OPEN:
            if self.state in [self.TrunkState.CLOSED]:
                self.state = self.TrunkState.OPEN
                # If fully closed, start opening
                if self.open_degree_value == 0.0:
                    self.open_degree_value = self._degree_level_mapping[self.OpenDegreeLevel.MIN]
            else:
                return {
                    "success": False, 
                    "error": f"Cannot open trunk in current state: {self.state.value}"
                }
        
        elif trunk_action == self.TrunkAction.CLOSE:
            if self.state in [self.TrunkState.OPEN]:
                self.state = self.TrunkState.CLOSED
                # If fully open, start closing
               
                self.open_degree_value = 0.0
            else:
                return {
                    "success": False, 
                    "error": f"Cannot close trunk in current state: {self.state.value}"
                }
        
        return {
            "success": True,
            "action": trunk_action.value,
            "current_state": self.state.value,
            "open_degree": {
                "value": self.open_degree_value,
                "unit": self.open_degree_unit.value
            },
            "is_locked": self.is_locked
        }
    
    @api("frontTrunk")
    def carcontrol_frontTrunk_openDegree_increase(self, value=None, unit=None, degree=None):
        """
        Control increase of front trunk's open degree.
        
        Args:
            value (float, optional): Numeric part of specific adjustment
            unit (str, optional): Unit part of adjustment ['gear', 'percentage', 'centimeter']
            degree (str, optional): Different levels of adjustment ['large', 'little', 'tiny']
        
        Returns:
            dict: Operation result and current state information
        """
        # Check if trunk is locked
        if self.is_locked:
            return {
                "success": False,
                "error": "Cannot adjust trunk when locked",
                "is_locked": self.is_locked
            }
        
        # Check if trunk is closed
        if self.state == self.TrunkState.CLOSED:
            return {
                "success": False,
                "error": "Cannot adjust trunk when closed",
                "current_state": self.state.value
            }
        
        # Parameter validation
        if degree is not None:
            try:
                degree_level = self.OpenDegreeLevel(degree)
                # Use the predefined increment for this level
                increment = self._degree_level_mapping[degree_level]
                # Convert to current unit
                unit_increment = (increment / 100.0) * self._max_open_degrees[self.open_degree_unit]
            except ValueError:
                return {
                    "success": False,
                    "error": f"Invalid degree: {degree}. Must be one of {[l.value for l in [self.OpenDegreeLevel.LARGE, self.OpenDegreeLevel.LITTLE, self.OpenDegreeLevel.TINY]]}"
                }
        
        elif value is not None and unit is not None:
            try:
                unit_enum = self.OpenDegreeUnit(unit)
                # Store current unit
                current_unit = self.open_degree_unit
                # Temporarily set unit to the provided unit
                self.open_degree_unit = unit_enum
                # Calculate increment in the new unit
                unit_increment = value
                # Restore original unit
                self.open_degree_unit = current_unit
            except ValueError:
                return {
                    "success": False,
                    "error": f"Invalid unit: {unit}. Must be one of {[u.value for u in self.OpenDegreeUnit]}"
                }
        
        else:
            # Default increment (10%)
            unit_increment = 0.1 * self._max_open_degrees[self.open_degree_unit]
        
        # Increase the open degree
        previous_value = self.open_degree_value
        self.open_degree_value += unit_increment
        
        # Update state based on new position
        
        self.state = self.TrunkState.OPEN
        
        return {
            "success": True,
            "previous_open_degree": {
                "value": previous_value,
                "unit": self.open_degree_unit.value
            },
            "current_open_degree": {
                "value": self.open_degree_value,
                "unit": self.open_degree_unit.value
            },
            "current_state": self.state.value,
            "is_locked": self.is_locked
        }
    
    @api("frontTrunk")
    def carcontrol_frontTrunk_openDegree_decrease(self, value=None, unit=None, degree=None):
        """
        Control decrease of front trunk's open degree.
        
        Args:
            value (float, optional): Numeric part of specific adjustment
            unit (str, optional): Unit part of adjustment ['gear', 'percentage', 'centimeter']
            degree (str, optional): Different levels of adjustment ['large', 'little', 'tiny']
        
        Returns:
            dict: Operation result and current state information
        """
        # Check if trunk is locked
        if self.is_locked:
            return {
                "success": False,
                "error": "Cannot adjust trunk when locked",
                "is_locked": self.is_locked
            }
        
        # Check if trunk is already closed
        if self.state == self.TrunkState.CLOSED:
            return {
                "success": False,
                "error": "Cannot decrease open degree when trunk is closed",
                "current_state": self.state.value
            }
        
        # Parameter validation
        if degree is not None:
            try:
                degree_level = self.OpenDegreeLevel(degree)
                # Use the predefined decrement for this level
                decrement = self._degree_level_mapping[degree_level]
                # Convert to current unit
                unit_decrement = (decrement / 100.0) * self._max_open_degrees[self.open_degree_unit]
            except ValueError:
                return {
                    "success": False,
                    "error": f"Invalid degree: {degree}. Must be one of {[l.value for l in [self.OpenDegreeLevel.LARGE, self.OpenDegreeLevel.LITTLE, self.OpenDegreeLevel.TINY]]}"
                }
        
        elif value is not None and unit is not None:
            try:
                unit_enum = self.OpenDegreeUnit(unit)
                # Store current unit
                current_unit = self.open_degree_unit
                # Temporarily set unit to the provided unit
                self.open_degree_unit = unit_enum
                # Calculate decrement in the new unit
                unit_decrement = value
                # Restore original unit
                self.open_degree_unit = current_unit
            except ValueError:
                return {
                    "success": False,
                    "error": f"Invalid unit: {unit}. Must be one of {[u.value for u in self.OpenDegreeUnit]}"
                }
        
        else:
            # Default decrement (10%)
            unit_decrement = 0.1 * self._max_open_degrees[self.open_degree_unit]
        
        # Decrease the open degree
        previous_value = self.open_degree_value
        self.open_degree_value -= unit_decrement
        
        # Update state based on new position
        if self.open_degree_value <= 0:
            self.open_degree_value = 0
            self.state = self.TrunkState.CLOSED
        
        return {
            "success": True,
            "previous_open_degree": {
                "value": previous_value,
                "unit": self.open_degree_unit.value
            },
            "current_open_degree": {
                "value": self.open_degree_value,
                "unit": self.open_degree_unit.value
            },
            "current_state": self.state.value,
            "is_locked": self.is_locked
        }
    
    @api("frontTrunk")
    def carcontrol_frontTrunk_openDegree_set(self, value=None, unit=None, degree=None):
        """
        Control front trunk open degree to a specific position.
        
        Args:
            value (float, optional): Numeric part of specific position
            unit (str, optional): Unit part of position ['gear', 'percentage', 'centimeter']
            degree (str, optional): Different levels of position ['max', 'high', 'medium', 'low', 'min']
        
        Returns:
            dict: Operation result and current state information
        """
        # Check if trunk is locked
        if self.is_locked:
            return {
                "success": False,
                "error": "Cannot adjust trunk when locked",
                "is_locked": self.is_locked
            }
        
        # Parameter validation
        if degree is not None:
            try:
                degree_level = self.OpenDegreeLevel(degree)
                # Only allow set operation levels
                if degree_level not in [self.OpenDegreeLevel.MAX, self.OpenDegreeLevel.HIGH, 
                                      self.OpenDegreeLevel.MEDIUM, self.OpenDegreeLevel.LOW, 
                                      self.OpenDegreeLevel.MIN]:
                    return {
                        "success": False,
                        "error": f"Invalid degree for set operation: {degree}. Must be one of {[l.value for l in [self.OpenDegreeLevel.MAX, self.OpenDegreeLevel.HIGH, self.OpenDegreeLevel.MEDIUM, self.OpenDegreeLevel.LOW, self.OpenDegreeLevel.MIN]]}"
                    }
                
                # Use the predefined position for this level
                percentage = self._degree_level_mapping[degree_level]
                # Convert to current unit
                target_value = (percentage / 100.0) * self._max_open_degrees[self.open_degree_unit]
            except ValueError:
                return {
                    "success": False,
                    "error": f"Invalid degree: {degree}. Must be one of {[l.value for l in [self.OpenDegreeLevel.MAX, self.OpenDegreeLevel.HIGH, self.OpenDegreeLevel.MEDIUM, self.OpenDegreeLevel.LOW, self.OpenDegreeLevel.MIN]]}"
                }
        
        elif value is not None and unit is not None:
            try:
                unit_enum = self.OpenDegreeUnit(unit)
                # Store current unit
                current_unit = self.open_degree_unit
                # Temporarily set unit to the provided unit
                self.open_degree_unit = unit_enum
                # Set the target value
                target_value = value
                # Validate the target value
                if target_value < 0 or target_value > self._max_open_degrees[unit_enum]:
                    return {
                        "success": False,
                        "error": f"Value {value} out of range for unit {unit}. Must be between 0 and {self._max_open_degrees[unit_enum]}"
                    }
                # Restore original unit
                self.open_degree_unit = current_unit
            except ValueError:
                return {
                    "success": False,
                    "error": f"Invalid unit: {unit}. Must be one of {[u.value for u in self.OpenDegreeUnit]}"
                }
        
        else:
            return {
                "success": False,
                "error": "Either degree or (value, unit) pair must be provided"
            }
        
        # Set the open degree
        previous_value = self.open_degree_value
        self.open_degree_value = target_value
        
        # Update state based on new position
        if self.open_degree_value <= 0:
            self.state = self.TrunkState.CLOSED
        elif self.open_degree_value >= self._max_open_degrees[self.open_degree_unit]:
            self.state = self.TrunkState.OPEN
        
            # If same value, maintain current state
        
        return {
            "success": True,
            "previous_open_degree": {
                "value": previous_value,
                "unit": self.open_degree_unit.value
            },
            "current_open_degree": {
                "value": self.open_degree_value,
                "unit": self.open_degree_unit.value
            },
            "current_state": self.state.value,
            "is_locked": self.is_locked
        }
    
    @api("frontTrunk")
    def carcontrol_frontTrunk_lock_switch(self, switch):
        """
        Open or close front trunk lock.
        
        Args:
            switch (bool): Front trunk lock mode switch, True for lock, False for unlock
        
        Returns:
            dict: Operation result and current state information
        """
        # Parameter validation
        if not isinstance(switch, bool):
            return {
                "success": False,
                "error": f"Switch must be a boolean, got {type(switch)}"
            }
        
        # Cannot lock when trunk is open
        if switch and self.state != self.TrunkState.CLOSED:
            return {
                "success": False,
                "error": "Cannot lock trunk when it is not fully closed",
                "current_state": self.state.value
            }
        
        # Change lock state
        previous_lock_state = self.is_locked
        self.is_locked = switch
        
        return {
            "success": True,
            "previous_lock_state": previous_lock_state,
            "current_lock_state": self.is_locked,
            "current_state": self.state.value
        }
    


    def to_dict(self):
        """
        Convert the FrontTrunk instance to a dictionary representation.
        
        Returns:
            dict: Dictionary with all properties, their values, types and descriptions
        """
        return {
            "state": {
                "value": self.state.value,
                "description": "Current state of the front trunk",
                "type": "TrunkState",
                "enum_values": [state.value for state in self.TrunkState]
            },
            "open_degree_value": {
                "value": self.open_degree_value,
                "description": f"Numeric value of front trunk open degree in {self.open_degree_unit.value}",
                "type": type(self.open_degree_value).__name__
            },
            "open_degree_unit": {
                "value": self.open_degree_unit.value,
                "description": "Unit used for open degree measurement",
                "type": "OpenDegreeUnit",
                "enum_values": [unit.value for unit in self.OpenDegreeUnit]
            },
            "is_locked": {
                "value": self.is_locked,
                "description": "Whether the front trunk is locked,it can only be locked when it's closed",
                "type": type(self.is_locked).__name__
            },
            "max_open_degrees": {
                "value": {unit.value: value for unit, value in self._max_open_degrees.items()},
                "description": "Maximum open degree values for different units",
                "type": "dict"
            },
            "degree_level_mapping": {
                "value": {level.value: value for level, value in self._degree_level_mapping.items()},
                "description": "Mapping of degree levels to percentage values",
                "type": "dict"
            }
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a FrontTrunk instance from a dictionary.
        
        Args:
            data (dict): Dictionary with property values
        
        Returns:
            FrontTrunk: New FrontTrunk instance
        """
        instance = cls()
        
        # Set state
        if "state" in data:
            instance.state = cls.TrunkState(data["state"]["value"])
        
        # Set open degree value
        if "open_degree_value" in data:
            instance.open_degree_value = data["open_degree_value"]["value"]
        
        # Set open degree unit
        if "open_degree_unit" in data:
            instance.open_degree_unit = cls.OpenDegreeUnit(data["open_degree_unit"]["value"])
        
        # Set lock state
        if "is_locked" in data:
            instance.is_locked = data["is_locked"]["value"]
        
        # Set max open degrees if provided
        if "max_open_degrees" in data:
            value_dict = data["max_open_degrees"]["value"]
            instance._max_open_degrees = {
                cls.OpenDegreeUnit(unit): value 
                for unit, value in value_dict.items()
            }
        
        # Set degree level mapping if provided
        if "degree_level_mapping" in data:
            value_dict = data["degree_level_mapping"]["value"]
            instance._degree_level_mapping = {
                cls.OpenDegreeLevel(level): value 
                for level, value in value_dict.items()
            }
        
        return instance
    
    @classmethod
    def init1(cls):
        """
        Creates a FrontTrunk instance initialized in closed state with default settings.
        
        Returns:
            FrontTrunk: New FrontTrunk instance in closed state
        """
        instance = cls()
        # Default state is already closed
        # Default is_locked is already False
        # Default open_degree_value is already 0.0
        # Default open_degree_unit is already percentage
        return instance

    @classmethod
    def init2(cls):
        """
        Creates a FrontTrunk instance initialized in open state with 
        custom settings - partially open and using gear unit.
        
        Returns:
            FrontTrunk: New FrontTrunk instance in open state
        """
        instance = cls()
        # Change state to open
        instance.state = cls.TrunkState.OPEN
        # Change unit to gear
        instance.open_degree_unit = cls.OpenDegreeUnit.GEAR
        # Set to medium opening level
        instance.open_degree_value = instance._degree_level_mapping[cls.OpenDegreeLevel.MEDIUM] / 100.0 * instance._max_open_degrees[instance.open_degree_unit]
        # is_locked remains False since trunk is open
        return instance