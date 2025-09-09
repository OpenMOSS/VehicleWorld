from module.environment import Environment

from enum import Enum
from utils import api
from typing import Dict, Any, Union, List, Optional, Tuple


class Trunk:
    class OpenDegreeUnit(Enum):
        """
        Enumeration for trunk open degree units.
        """
        GEAR = "gear"
        PERCENTAGE = "percentage"
        CENTIMETER = "centimeter"
        
        @classmethod
        def to_dict(cls) -> List[str]:
            return [e.value for e in cls]
    
    class OpenDegreeLevelAdjustment(Enum):
        """
        Enumeration for relative trunk open degree adjustments.
        """
        LARGE = "large"
        LITTLE = "little"
        TINY = "tiny"
        
        @classmethod
        def to_dict(cls) -> List[str]:
            return [e.value for e in cls]
    
    class OpenDegreeLevel(Enum):
        """
        Enumeration for absolute trunk open degree levels.
        """
        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"
        
        @classmethod
        def to_dict(cls) -> List[str]:
            return [e.value for e in cls]
    
    class TrunkAction(Enum):
        """
        Enumeration for trunk actions.
        """
        OPEN = "open"
        CLOSE = "close"
        PAUSE = "pause"
        
        @classmethod
        def to_dict(cls) -> List[str]:
            return [e.value for e in cls]
    
    class TrunkState(Enum):
        """
        Enumeration for trunk states.
        """
        CLOSED = "closed"
        OPENING = "opening"
        OPEN = "open"
        CLOSING = "closing"
        PAUSED = "paused"
        
        @classmethod
        def to_dict(cls) -> List[str]:
            return [e.value for e in cls]
    
    def __init__(self):
        # Trunk state
        self._state = Trunk.TrunkState.CLOSED
        
        # Open degree attributes
        self._current_open_degree_percentage = 0.0  # 0-100%
        self._current_open_degree_gear = 0  # Discrete gears (0-10)
        self._current_open_degree_cm = 0.0  # Open height in centimeters
        self._max_open_height_cm = 100.0  # Maximum opening height in cm
        
        # Level presets (as percentage of full opening)
        self._level_presets = {
            Trunk.OpenDegreeLevel.MIN: 10.0,
            Trunk.OpenDegreeLevel.LOW: 25.0,
            Trunk.OpenDegreeLevel.MEDIUM: 50.0,
            Trunk.OpenDegreeLevel.HIGH: 75.0,
            Trunk.OpenDegreeLevel.MAX: 100.0
        }
        
        # Adjustment presets (as percentage change)
        self._adjustment_presets = {
            Trunk.OpenDegreeLevelAdjustment.TINY: 5.0,
            Trunk.OpenDegreeLevelAdjustment.LITTLE: 10.0,
            Trunk.OpenDegreeLevelAdjustment.LARGE: 20.0
        }
        
        # Security
        self._is_locked = True
        
        # Motion parameters
        self._is_in_motion = False
    
    # Property getters and setters
    @property
    def state(self) -> TrunkState:
        return self._state
    
    @state.setter
    def state(self, value: TrunkState):
        self._state = value
    
    @property
    def current_open_degree_percentage(self) -> float:
        return self._current_open_degree_percentage
    
    @current_open_degree_percentage.setter
    def current_open_degree_percentage(self, value: float):
        if 0.0 <= value <= 100.0:
            self._current_open_degree_percentage = value
            # Update other representations
            self._current_open_degree_gear = int(value / 10)  # 0-10 gears
            self._current_open_degree_cm = (value / 100.0) * self._max_open_height_cm
    
    @property
    def current_open_degree_gear(self) -> int:
        return self._current_open_degree_gear
    
    @current_open_degree_gear.setter
    def current_open_degree_gear(self, value: int):
        if 0 <= value <= 10:
            self._current_open_degree_gear = value
            # Update other representations
            self._current_open_degree_percentage = value * 10.0
            self._current_open_degree_cm = (value / 10.0) * self._max_open_height_cm
    
    @property
    def current_open_degree_cm(self) -> float:
        return self._current_open_degree_cm
    
    @current_open_degree_cm.setter
    def current_open_degree_cm(self, value: float):
        if 0.0 <= value <= self._max_open_height_cm:
            self._current_open_degree_cm = value
            # Update other representations
            self._current_open_degree_percentage = (value / self._max_open_height_cm) * 100.0
            self._current_open_degree_gear = int(self._current_open_degree_percentage / 10)
    
    @property
    def max_open_height_cm(self) -> float:
        return self._max_open_height_cm
    
    @max_open_height_cm.setter
    def max_open_height_cm(self, value: float):
        if value > 0:
            self._max_open_height_cm = value
            # Recalculate current cm based on percentage
            self._current_open_degree_cm = (self._current_open_degree_percentage / 100.0) * value
    
    @property
    def level_presets(self) -> Dict[OpenDegreeLevel, float]:
        return self._level_presets
    
    @level_presets.setter
    def level_presets(self, value: Dict[OpenDegreeLevel, float]):
        self._level_presets = value
    
    @property
    def adjustment_presets(self) -> Dict[OpenDegreeLevelAdjustment, float]:
        return self._adjustment_presets
    
    @adjustment_presets.setter
    def adjustment_presets(self, value: Dict[OpenDegreeLevelAdjustment, float]):
        self._adjustment_presets = value
    
    @property
    def is_locked(self) -> bool:
        return self._is_locked
    
    @is_locked.setter
    def is_locked(self, value: bool):
        self._is_locked = value
    
    @property
    def is_in_motion(self) -> bool:
        return self._is_in_motion
    
    @is_in_motion.setter
    def is_in_motion(self, value: bool):
        self._is_in_motion = value
    
    # API Methods Implementation
    @api("trunk")
    def carcontrol_trunk_switch(self, action: str) -> Dict[str, Any]:
        """
        Control vehicle trunk opening, closing, or pausing
        
        Args:
            action (str): Trunk action, options: ["open", "close", "pause"]
        
        Returns:
            Dict containing operation result and current state
        """
        try:
            # Convert string to enum
            trunk_action = Trunk.TrunkAction(action)
            
            # Check if trunk is locked
            if self.is_locked and trunk_action != Trunk.TrunkAction.CLOSE:
                return {
                    "success": False,
                    "message": "Trunk is locked. Please unlock the trunk first.",
                    "current_state": self.state.value
                }
            
            # Process the action
            if trunk_action == Trunk.TrunkAction.OPEN:
                if self.state == Trunk.TrunkState.CLOSED or self.state == Trunk.TrunkState.PAUSED:
                    self.state = Trunk.TrunkState.OPENING
                    self.is_in_motion = True
                    # Simulate finished opening
                    if self.current_open_degree_percentage < 100:
                        self.current_open_degree_percentage = 20
                        self.state = Trunk.TrunkState.OPEN
                        self.is_in_motion = False
                elif self.state == Trunk.TrunkState.CLOSING:
                    # Change direction
                    self.state = Trunk.TrunkState.OPENING
                elif self.state == Trunk.TrunkState.OPEN:
                    return {
                        "success": False,
                        "message": "Trunk is already fully open.",
                        "current_state": self.state.value
                    }
            
            elif trunk_action == Trunk.TrunkAction.CLOSE:
                if self.state == Trunk.TrunkState.OPEN or self.state == Trunk.TrunkState.PAUSED:
                    self.state = Trunk.TrunkState.CLOSING
                    self.is_in_motion = True
                    # Simulate finished closing
                    if self.current_open_degree_percentage > 0:
                        self.current_open_degree_percentage = 0
                        self.state = Trunk.TrunkState.CLOSED
                        self.is_in_motion = False
                elif self.state == Trunk.TrunkState.OPENING:
                    # Change direction
                    self.state = Trunk.TrunkState.CLOSING
                elif self.state == Trunk.TrunkState.CLOSED:
                    return {
                        "success": False,
                        "message": "Trunk is already closed.",
                        "current_state": self.state.value
                    }
            
            elif trunk_action == Trunk.TrunkAction.PAUSE:
                if self.state == Trunk.TrunkState.OPENING or self.state == Trunk.TrunkState.CLOSING:
                    self.state = Trunk.TrunkState.PAUSED
                    self.is_in_motion = False
                else:
                    return {
                        "success": False,
                        "message": f"Cannot pause trunk in {self.state.value} state.",
                        "current_state": self.state.value
                    }
            
            return {
                "success": True,
                "message": f"Trunk {trunk_action.value} operation successful.",
                "current_state": self.state.value,
                "open_degree": {
                    "percentage": self.current_open_degree_percentage,
                    "gear": self.current_open_degree_gear,
                    "centimeter": self.current_open_degree_cm
                }
            }
            
        except ValueError:
            return {
                "success": False,
                "message": f"Invalid action: {action}. Valid options are: {Trunk.TrunkAction.to_dict()}",
                "current_state": self.state.value
            }
    
    @api("trunk")
    def carcontrol_trunk_openDegree_increase(self, 
                                            value: Optional[float] = None, 
                                            unit: Optional[str] = None, 
                                            degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Control increase of trunk's open degree
        
        Args:
            value (float, optional): Numeric value for adjustment
            unit (str, optional): Unit for adjustment, options: ["gear", "percentage", "centimeter"]
            degree (str, optional): Preset adjustment level, options: ["large", "little", "tiny"]
            
        Note: Either (value, unit) or degree should be provided, not both.
        
        Returns:
            Dict containing operation result and current state
        """
        try:
            # Validate trunk state
            if self.state not in [Trunk.TrunkState.OPEN, Trunk.TrunkState.PAUSED, Trunk.TrunkState.OPENING]:
                return {
                    "success": False,
                    "message": f"Cannot increase open degree when trunk is {self.state.value}.",
                    "current_state": self.state.value
                }
            
            # Check if trunk is locked
            if self.is_locked:
                return {
                    "success": False,
                    "message": "Trunk is locked. Please unlock the trunk first.",
                    "current_state": self.state.value
                }
            
            # Case 1: Using preset degree
            if degree is not None:
                try:
                    adjustment_level = Trunk.OpenDegreeLevelAdjustment(degree)
                    adjustment_value = self.adjustment_presets[adjustment_level]
                    
                    # Apply the adjustment to percentage
                    new_percentage = min(100, self.current_open_degree_percentage + adjustment_value)
                    self.current_open_degree_percentage = new_percentage
                    
                    # Update state if needed
                    if new_percentage == 100:
                        self.state = Trunk.TrunkState.OPEN
                        self.is_in_motion = False
                    else:
                        self.state = Trunk.TrunkState.PAUSED
                
                except ValueError:
                    return {
                        "success": False,
                        "message": f"Invalid degree: {degree}. Valid options are: {Trunk.OpenDegreeLevelAdjustment.to_dict()}",
                        "current_state": self.state.value
                    }
            
            # Case 2: Using value and unit
            elif value is not None and unit is not None:
                try:
                    degree_unit = Trunk.OpenDegreeUnit(unit)
                    
                    if degree_unit == Trunk.OpenDegreeUnit.PERCENTAGE:
                        new_percentage = min(100, self.current_open_degree_percentage + value)
                        self.current_open_degree_percentage = new_percentage
                    
                    elif degree_unit == Trunk.OpenDegreeUnit.GEAR:
                        new_gear = min(10, self.current_open_degree_gear + int(value))
                        self.current_open_degree_gear = new_gear
                    
                    elif degree_unit == Trunk.OpenDegreeUnit.CENTIMETER:
                        new_cm = min(self.max_open_height_cm, self.current_open_degree_cm + value)
                        self.current_open_degree_cm = new_cm
                    
                    # Update state if needed
                    if self.current_open_degree_percentage == 100:
                        self.state = Trunk.TrunkState.OPEN
                        self.is_in_motion = False
                    else:
                        self.state = Trunk.TrunkState.PAUSED
                
                except ValueError:
                    return {
                        "success": False,
                        "message": f"Invalid unit: {unit}. Valid options are: {Trunk.OpenDegreeUnit.to_dict()}",
                        "current_state": self.state.value
                    }
            
            # Case 3: No parameters, use default
            else:
                # Default to a small increment
                adjustment_value = self.adjustment_presets[Trunk.OpenDegreeLevelAdjustment.LITTLE]
                new_percentage = min(100, self.current_open_degree_percentage + adjustment_value)
                self.current_open_degree_percentage = new_percentage
                
                # Update state if needed
                if new_percentage == 100:
                    self.state = Trunk.TrunkState.OPEN
                    self.is_in_motion = False
                else:
                    self.state = Trunk.TrunkState.PAUSED
            
            return {
                "success": True,
                "message": "Trunk open degree increased successfully.",
                "current_state": self.state.value,
                "open_degree": {
                    "percentage": self.current_open_degree_percentage,
                    "gear": self.current_open_degree_gear,
                    "centimeter": self.current_open_degree_cm
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error increasing trunk open degree: {str(e)}",
                "current_state": self.state.value
            }
    
    @api("trunk")
    def carcontrol_trunk_openDegree_decrease(self, 
                                            value: Optional[float] = None, 
                                            unit: Optional[str] = None, 
                                            degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Control decrease of trunk's open degree
        
        Args:
            value (float, optional): Numeric value for adjustment
            unit (str, optional): Unit for adjustment, options: ["gear", "percentage", "centimeter"]
            degree (str, optional): Preset adjustment level, options: ["large", "little", "tiny"]
            
        Note: Either (value, unit) or degree should be provided, not both.
        
        Returns:
            Dict containing operation result and current state
        """
        try:
            # Validate trunk state
            if self.state not in [Trunk.TrunkState.OPEN, Trunk.TrunkState.PAUSED, Trunk.TrunkState.CLOSING]:
                return {
                    "success": False,
                    "message": f"Cannot decrease open degree when trunk is {self.state.value}.",
                    "current_state": self.state.value
                }
            
            # Check if trunk is locked
            if self.is_locked:
                return {
                    "success": False,
                    "message": "Trunk is locked. Please unlock the trunk first.",
                    "current_state": self.state.value
                }
            
            # Case 1: Using preset degree
            if degree is not None:
                try:
                    adjustment_level = Trunk.OpenDegreeLevelAdjustment(degree)
                    adjustment_value = self.adjustment_presets[adjustment_level]
                    
                    # Apply the adjustment to percentage
                    new_percentage = max(0, self.current_open_degree_percentage - adjustment_value)
                    self.current_open_degree_percentage = new_percentage
                    
                    # Update state if needed
                    if new_percentage == 0:
                        self.state = Trunk.TrunkState.CLOSED
                        self.is_in_motion = False
                    else:
                        self.state = Trunk.TrunkState.PAUSED
                
                except ValueError:
                    return {
                        "success": False,
                        "message": f"Invalid degree: {degree}. Valid options are: {Trunk.OpenDegreeLevelAdjustment.to_dict()}",
                        "current_state": self.state.value
                    }
            
            # Case 2: Using value and unit
            elif value is not None and unit is not None:
                try:
                    degree_unit = Trunk.OpenDegreeUnit(unit)
                    
                    if degree_unit == Trunk.OpenDegreeUnit.PERCENTAGE:
                        new_percentage = max(0, self.current_open_degree_percentage - value)
                        self.current_open_degree_percentage = new_percentage
                    
                    elif degree_unit == Trunk.OpenDegreeUnit.GEAR:
                        new_gear = max(0, self.current_open_degree_gear - int(value))
                        self.current_open_degree_gear = new_gear
                    
                    elif degree_unit == Trunk.OpenDegreeUnit.CENTIMETER:
                        new_cm = max(0, self.current_open_degree_cm - value)
                        self.current_open_degree_cm = new_cm
                    
                    # Update state if needed
                    if self.current_open_degree_percentage == 0:
                        self.state = Trunk.TrunkState.CLOSED
                        self.is_in_motion = False
                    else:
                        self.state = Trunk.TrunkState.PAUSED
                
                except ValueError:
                    return {
                        "success": False,
                        "message": f"Invalid unit: {unit}. Valid options are: {Trunk.OpenDegreeUnit.to_dict()}",
                        "current_state": self.state.value
                    }
            
            # Case 3: No parameters, use default
            else:
                # Default to a small decrement
                adjustment_value = self.adjustment_presets[Trunk.OpenDegreeLevelAdjustment.LITTLE]
                new_percentage = max(0, self.current_open_degree_percentage - adjustment_value)
                self.current_open_degree_percentage = new_percentage
                
                # Update state if needed
                if new_percentage == 0:
                    self.state = Trunk.TrunkState.CLOSED
                    self.is_in_motion = False
                else:
                    self.state = Trunk.TrunkState.PAUSED
            
            return {
                "success": True,
                "message": "Trunk open degree decreased successfully.",
                "current_state": self.state.value,
                "open_degree": {
                    "percentage": self.current_open_degree_percentage,
                    "gear": self.current_open_degree_gear,
                    "centimeter": self.current_open_degree_cm
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error decreasing trunk open degree: {str(e)}",
                "current_state": self.state.value
            }
    
    @api("trunk")
    def carcontrol_trunk_openDegree_set(self, 
                                       value: Optional[float] = None, 
                                       unit: Optional[str] = None, 
                                       degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Control trunk open degree to a specific position
        
        Args:
            value (float, optional): Numeric value for position
            unit (str, optional): Unit for position, options: ["gear", "percentage", "centimeter"]
            degree (str, optional): Preset position level, options: ["max", "high", "medium", "low", "min"]
            
        Note: Either (value, unit) or degree must be provided.
        
        Returns:
            Dict containing operation result and current state
        """
        try:
            # Validate trunk state
            if self.state == Trunk.TrunkState.CLOSED:
                # First need to open the trunk
                self.carcontrol_trunk_switch("open")
            
            # Check if trunk is locked
            if self.is_locked:
                return {
                    "success": False,
                    "message": "Trunk is locked. Please unlock the trunk first.",
                    "current_state": self.state.value
                }
            
            # Case 1: Using preset degree
            if degree is not None:
                try:
                    level = Trunk.OpenDegreeLevel(degree)
                    new_percentage = self.level_presets[level]
                    self.current_open_degree_percentage = new_percentage
                    
                    # Update state
                    if new_percentage == 0:
                        self.state = Trunk.TrunkState.CLOSED
                        self.is_in_motion = False
                    elif new_percentage == 100:
                        self.state = Trunk.TrunkState.OPEN
                        self.is_in_motion = False
                    else:
                        self.state = Trunk.TrunkState.PAUSED
                        self.is_in_motion = False
                
                except ValueError:
                    return {
                        "success": False,
                        "message": f"Invalid degree: {degree}. Valid options are: {Trunk.OpenDegreeLevel.to_dict()}",
                        "current_state": self.state.value
                    }
            
            # Case 2: Using value and unit
            elif value is not None and unit is not None:
                try:
                    degree_unit = Trunk.OpenDegreeUnit(unit)
                    
                    if degree_unit == Trunk.OpenDegreeUnit.PERCENTAGE:
                        if 0 <= value <= 100:
                            self.current_open_degree_percentage = value
                        else:
                            return {
                                "success": False,
                                "message": f"Percentage value must be between 0 and 100.",
                                "current_state": self.state.value
                            }
                    
                    elif degree_unit == Trunk.OpenDegreeUnit.GEAR:
                        if 0 <= value <= 10:
                            self.current_open_degree_gear = int(value)
                        else:
                            return {
                                "success": False,
                                "message": f"Gear value must be between 0 and 10.",
                                "current_state": self.state.value
                            }
                    
                    elif degree_unit == Trunk.OpenDegreeUnit.CENTIMETER:
                        if 0 <= value <= self.max_open_height_cm:
                            self.current_open_degree_cm = value
                        else:
                            return {
                                "success": False,
                                "message": f"Centimeter value must be between 0 and {self.max_open_height_cm}.",
                                "current_state": self.state.value
                            }
                    
                    # Update state
                    if self.current_open_degree_percentage == 0:
                        self.state = Trunk.TrunkState.CLOSED
                        self.is_in_motion = False
                    elif self.current_open_degree_percentage == 100:
                        self.state = Trunk.TrunkState.OPEN
                        self.is_in_motion = False
                    else:
                        self.state = Trunk.TrunkState.PAUSED
                        self.is_in_motion = False
                
                except ValueError:
                    return {
                        "success": False,
                        "message": f"Invalid unit: {unit}. Valid options are: {Trunk.OpenDegreeUnit.to_dict()}",
                        "current_state": self.state.value
                    }
            
            # Case 3: No parameters
            else:
                return {
                    "success": False,
                    "message": "Either degree or (value, unit) must be provided.",
                    "current_state": self.state.value
                }
            
            return {
                "success": True,
                "message": "Trunk open degree set successfully.",
                "current_state": self.state.value,
                "open_degree": {
                    "percentage": self.current_open_degree_percentage,
                    "gear": self.current_open_degree_gear,
                    "centimeter": self.current_open_degree_cm
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error setting trunk open degree: {str(e)}",
                "current_state": self.state.value
            }
    
    @api("trunk")
    def carcontrol_trunk_lock_switch(self, switch: bool) -> Dict[str, Any]:
        """
        Lock or unlock trunk
        
        Args:
            switch (bool): True to lock, False to unlock
        
        Returns:
            Dict containing operation result and current state
        """
        try:
            # Don't allow locking if trunk is open
            if switch and self.state != Trunk.TrunkState.CLOSED:
                return {
                    "success": False,
                    "message": "Cannot lock trunk when it is not fully closed.",
                    "current_state": self.state.value,
                    "locked": self.is_locked
                }
            
            self.is_locked = switch
            
            return {
                "success": True,
                "message": f"Trunk {'locked' if switch else 'unlocked'} successfully.",
                "current_state": self.state.value,
                "locked": self.is_locked
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error {'locking' if switch else 'unlocking'} trunk: {str(e)}",
                "current_state": self.state.value,
                "locked": self.is_locked
            }
    


    def to_dict(self) -> Dict[str, Any]:
        """
        Convert trunk instance to dictionary representation
        
        Returns:
            Dict containing all attributes and their descriptions
        """
        return {
            "state": {
                "value": self.state.value,
                "description": "Current state of the trunk (closed, opening, open, closing, paused)",
                "type": "TrunkState",
                "possible_values": Trunk.TrunkState.to_dict()
            },
            "current_open_degree_percentage": {
                "value": self.current_open_degree_percentage,
                "description": "Current trunk open degree as percentage (0-100%), increases/decreases in sync with current_open_degree_gear and current_open_degree_cm",
                "type": "float"
            },
            "current_open_degree_gear": {
                "value": self.current_open_degree_gear,
                "description": "Current trunk open degree as gear level (0-10), increases/decreases in sync with current_open_degree_percentage and current_open_degree_cm",
                "type": "int"
            },
            "current_open_degree_cm": {
                "value": self.current_open_degree_cm,
                "description": f"Current trunk open height in centimeters (0-{self.max_open_height_cm}), increases/decreases in sync with current_open_degree_percentage and current_open_degree_gear",
                "type": "float"
            },
            "max_open_height_cm": {
                "value": self.max_open_height_cm,
                "description": "Maximum trunk open height in centimeters",
                "type": "float"
            },
            "level_presets": {
                "value": {k.value: v for k, v in self.level_presets.items()},
                "description": "Predefined trunk open degree levels as percentages",
                "type": "Dict[OpenDegreeLevel, float]",
                "possible_values": Trunk.OpenDegreeLevel.to_dict()
            },
            "adjustment_presets": {
                "value": {k.value: v for k, v in self.adjustment_presets.items()},
                "description": "Predefined trunk open degree adjustment increments as percentages",
                "type": "Dict[OpenDegreeLevelAdjustment, float]",
                "possible_values": Trunk.OpenDegreeLevelAdjustment.to_dict()
            },
            "is_locked": {
                "value": self.is_locked,
                "description": "Whether the trunk is locked (true) or unlocked (false)",
                "type": "bool"
            },
            "is_in_motion": {
                "value": self.is_in_motion,
                "description": "Whether the trunk is currently in motion",
                "type": "bool"
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Trunk':
        """
        Create a Trunk instance from dictionary data
        
        Args:
            data: Dictionary containing trunk attributes
            
        Returns:
            New Trunk instance
        """
        trunk = cls()
        
        # Set basic properties
        if "state" in data:
            state_value = data["state"]["value"]
            trunk.state = Trunk.TrunkState(state_value)
        
        if "current_open_degree_percentage" in data:
            trunk.current_open_degree_percentage = data["current_open_degree_percentage"]["value"]
        
        # No need to set gear and cm explicitly as they're derived from percentage
        
        if "max_open_height_cm" in data:
            trunk.max_open_height_cm = data["max_open_height_cm"]["value"]
        
        if "level_presets" in data:
            level_dict = data["level_presets"]["value"]
            trunk.level_presets = {Trunk.OpenDegreeLevel(k): v for k, v in level_dict.items()}
        
        if "adjustment_presets" in data:
            adj_dict = data["adjustment_presets"]["value"]
            trunk.adjustment_presets = {Trunk.OpenDegreeLevelAdjustment(k): v for k, v in adj_dict.items()}
        
        if "is_locked" in data:
            trunk.is_locked = data["is_locked"]["value"]
        
        if "is_in_motion" in data:
            trunk.is_in_motion = data["is_in_motion"]["value"]
        
        return trunk
    
    @classmethod
    def init1(cls) -> 'Trunk':
        """
        Initialize a Trunk instance with default closed state.
        This is the standard initialization with trunk locked and closed.
        
        Returns:
            New Trunk instance with default closed configuration
        """
        trunk = cls()
        # Default initialization is already closed and locked
        return trunk

    @classmethod
    def init2(cls) -> 'Trunk':
        """
        Initialize a Trunk instance in open state.
        This creates a trunk that is already open and unlocked.
        
        Returns:
            New Trunk instance with open configuration
        """
        trunk = cls()
        # Set to open state
        trunk.state = Trunk.TrunkState.OPEN
        trunk.is_locked = False
        trunk.is_in_motion = False
        trunk.current_open_degree_percentage = 100.0  # Fully open
        # The other properties (gear and cm) will be updated automatically
        return trunk