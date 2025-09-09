from typing import Dict, Union, List, Optional, Any
from enum import Enum
from utils import api


class Sunshade:
    """
    Entity class representing the sunshade system in a vehicle.
    """
    class Position(Enum):
        """
        Enumeration for sunshade positions in the vehicle.
        """
        FRONT_ROW = "front row"
        REAR_ROW = "rear row"
        ALL = "all"

    class Action(Enum):
        """
        Enumeration for sunshade control actions.
        """
        OPEN = "open"
        CLOSE = "close"
        PAUSE = "pause"

    class Unit(Enum):
        """
        Enumeration for the unit of measurement for sunshade open degree.
        """
        GEAR = "gear"
        PERCENTAGE = "percentage"
        CENTIMETER = "centimeter"

    class DegreeTiny(Enum):
        """
        Enumeration for the incremental degree adjustment of sunshade.
        """
        LARGE = "large"
        LITTLE = "little"
        TINY = "tiny"

    class DegreeSet(Enum):
        """
        Enumeration for the preset degree values of sunshade.
        """
        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"

    class SunshadeStatus:
        """
        Class representing the status of a single sunshade.
        """
        def __init__(self, 
                    is_open: bool = False, 
                    is_paused: bool = False, 
                    open_degree_value: float = 0.0,
                    open_degree_unit: 'Sunshade.Unit' = None):
            self._is_open = is_open
            self._is_paused = is_paused
            self._open_degree_value = open_degree_value
            # Default to percentage if None is provided
            self._open_degree_unit = open_degree_unit if open_degree_unit is not None else Sunshade.Unit.PERCENTAGE

        @property
        def is_open(self) -> bool:
            return self._is_open

        @is_open.setter
        def is_open(self, value: bool):
            self._is_open = value

        @property
        def is_paused(self) -> bool:
            return self._is_paused

        @is_paused.setter
        def is_paused(self, value: bool):
            self._is_paused = value

        @property
        def open_degree_value(self) -> float:
            return self._open_degree_value

        @open_degree_value.setter
        def open_degree_value(self, value: float):
            # Normalize value based on unit
            if self._open_degree_unit == Sunshade.Unit.PERCENTAGE:
                # Percentage should be between 0 and 100
                self._open_degree_value = max(0.0, min(100.0, value))
            elif self._open_degree_unit == Sunshade.Unit.GEAR:
                # Gear can be between 0 and 10 (assuming 10 gears)
                self._open_degree_value = max(0.0, min(10.0, value))
            elif self._open_degree_unit == Sunshade.Unit.CENTIMETER:
                # Assuming max 30 cm opening
                self._open_degree_value = max(0.0, min(30.0, value))
            else:
                self._open_degree_value = value

        @property
        def open_degree_unit(self) -> 'Sunshade.Unit':
            return self._open_degree_unit

        @open_degree_unit.setter
        def open_degree_unit(self, value: 'Sunshade.Unit'):
            self._open_degree_unit = value

        def to_dict(self) -> Dict[str, Any]:
            """
            Convert the status to a dictionary representation.
            """
            return {
                "is_open": {
                    "value": self.is_open,
                    "description": "Whether the sunshade is open (True) or closed (False)",
                    "type": type(self.is_open).__name__
                },
                "is_paused": {
                    "value": self.is_paused,
                    "description": "Whether the sunshade movement is paused",
                    "type": type(self.is_paused).__name__
                },
                "open_degree_value": {
                    "value": self.open_degree_value,
                    "description": f"The numeric value of openness in {self.open_degree_unit.value}",
                    "type": type(self.open_degree_value).__name__
                },
                "open_degree_unit": {
                    "value": self.open_degree_unit.value,
                    "description": "The unit of measurement for the open degree, can be: gear, percentage, centimeter",
                    "type": "Sunshade.Unit(Enum)"
                }
            }

        @classmethod
        def from_dict(cls, data: Dict[str, Any]) -> 'Sunshade.SunshadeStatus':
            """
            Create a SunshadeStatus instance from a dictionary.
            """
            is_open = data["is_open"]["value"]
            is_paused = data["is_paused"]["value"]
            open_degree_value = data["open_degree_value"]["value"]
            open_degree_unit = Sunshade.Unit(data["open_degree_unit"]["value"])
            
            return cls(
                is_open=is_open,
                is_paused=is_paused,
                open_degree_value=open_degree_value,
                open_degree_unit=open_degree_unit
            )

    # Degree adjustment mappings
    TINY_DEGREE_MAPPING = {
        DegreeTiny.LARGE: 20.0,
        DegreeTiny.LITTLE: 10.0,
        DegreeTiny.TINY: 5.0
    }
    
    SET_DEGREE_MAPPING = {
        DegreeSet.MAX: 100.0,
        DegreeSet.HIGH: 75.0,
        DegreeSet.MEDIUM: 50.0,
        DegreeSet.LOW: 25.0,
        DegreeSet.MIN: 0.0
    }

    def __init__(self):
        # Initialize status for each position
        self._front_row_status = self.SunshadeStatus()
        self._rear_row_status = self.SunshadeStatus()
        self._leave_and_lock_auto_close_enabled = False

    @property
    def front_row_status(self) -> SunshadeStatus:
        return self._front_row_status

    @front_row_status.setter
    def front_row_status(self, value: SunshadeStatus):
        self._front_row_status = value

    @property
    def rear_row_status(self) -> SunshadeStatus:
        return self._rear_row_status

    @rear_row_status.setter
    def rear_row_status(self, value: SunshadeStatus):
        self._rear_row_status = value

    @property
    def leave_and_lock_auto_close_enabled(self) -> bool:
        return self._leave_and_lock_auto_close_enabled

    @leave_and_lock_auto_close_enabled.setter
    def leave_and_lock_auto_close_enabled(self, value: bool):
        self._leave_and_lock_auto_close_enabled = value

    def _get_status_by_position(self, position: Position) -> List[SunshadeStatus]:
        """
        Get sunshade status instances by position.
        
        Args:
            position: The position of the sunshade.
            
        Returns:
            List of SunshadeStatus objects.
        """
        if position == self.Position.FRONT_ROW:
            return [self.front_row_status]
        elif position == self.Position.REAR_ROW:
            return [self.rear_row_status]
        else:  # Position.ALL
            return [self.front_row_status, self.rear_row_status]

    @api("sunshade")
    def carcontrol_sunshade_switch(self, action: str, position: str = "all") -> Dict[str, Any]:
        """
        Turn on, off, or pause the sunshade.
        
        Args:
            action: Sunshade control mode. Must be one of ['open', 'close', 'pause'].
            position: Control the position of the sunshade. Must be one of ['front row', 'rear row', 'all'].
                     Default is 'all'.
                    
        Returns:
            A dictionary containing operation result and status information.
        
        Raises:
            ValueError: If the action is not recognized.
        """
        try:
            action_enum = self.Action(action)
            position_enum = self.Position(position)
            
            status_list = self._get_status_by_position(position_enum)
            
            for status in status_list:
                if action_enum == self.Action.OPEN:
                    status.is_open = True
                    status.is_paused = False
                elif action_enum == self.Action.CLOSE:
                    status.is_open = False
                    status.is_paused = False
                elif action_enum == self.Action.PAUSE:
                    status.is_paused = True
                else:
                    raise ValueError(f"Invalid action: {action}")
            
            return {
                "success": True,
                "message": f"Successfully {action} sunshade at {position}",
                "status": self.to_dict()
            }
            
        except (ValueError, TypeError) as e:
            return {
                "success": False,
                "message": str(e),
                "status": self.to_dict()
            }

    @api("sunshade")
    def carcontrol_sunshade_openDegree_increase(self, position: str = "all", 
                                               value: Optional[float] = None, 
                                               unit: Optional[str] = None, 
                                               degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Increase the sunshade's open degree.
        
        Args:
            position: Control the position of the sunshade. Must be one of ['front row', 'rear row', 'all'].
                     Default is 'all'.
            value: The numeric value part of the openDegree adjustment, mutually exclusive with degree.
            unit: The unit part of the openDegree adjustment, must be one of ['gear', 'percentage', 'centimeter'].
                  Mutually exclusive with degree.
            degree: The different degree of adjustment. Must be one of ['large', 'little', 'tiny'].
                    Mutually exclusive with value/unit.
                    
        Returns:
            A dictionary containing operation result and status information.
        """
        try:
            position_enum = self.Position(position)
            status_list = self._get_status_by_position(position_enum)
            
            for status in status_list:
                status.is_open = True
                status.is_paused = False
                if degree is not None:
                    # Use the degree mechanism
                    degree_enum = self.DegreeTiny(degree)
                    increase_amount = self.TINY_DEGREE_MAPPING[degree_enum]
                    status.open_degree_value = status.open_degree_value + increase_amount
                elif value is not None and unit is not None:
                    # Use the value/unit mechanism
                    unit_enum = self.Unit(unit)
                    # If the units are different, convert
                    if status.open_degree_unit != unit_enum:
                        status.open_degree_unit = unit_enum
                    status.open_degree_value = status.open_degree_value + value
                else:
                    # Default behavior if no specifics given - small increase
                    status.open_degree_value = status.open_degree_value + self.TINY_DEGREE_MAPPING[self.DegreeTiny.LITTLE]
            
            return {
                "success": True,
                "message": f"Successfully increased open degree for sunshade at {position}",
                "status": self.to_dict()
            }
            
        except (ValueError, TypeError) as e:
            return {
                "success": False,
                "message": str(e),
                "status": self.to_dict()
            }

    @api("sunshade")
    def carcontrol_sunshade_openDegree_decrease(self, position: str = "all", 
                                               value: Optional[float] = None, 
                                               unit: Optional[str] = None, 
                                               degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Decrease the sunshade's open degree.
        
        Args:
            position: Control the position of the sunshade. Must be one of ['front row', 'rear row', 'all'].
                     Default is 'all'.
            value: The numeric value part of the openDegree adjustment, mutually exclusive with degree.
            unit: The unit part of the openDegree adjustment, must be one of ['gear', 'percentage', 'centimeter'].
                  Mutually exclusive with degree.
            degree: The different degree of adjustment. Must be one of ['large', 'little', 'tiny'].
                    Mutually exclusive with value/unit.
                    
        Returns:
            A dictionary containing operation result and status information.
        """
        try:
            position_enum = self.Position(position)
            status_list = self._get_status_by_position(position_enum)
            
            for status in status_list:
                if degree is not None:
                    # Use the degree mechanism
                    degree_enum = self.DegreeTiny(degree)
                    decrease_amount = self.TINY_DEGREE_MAPPING[degree_enum]
                    status.open_degree_value = status.open_degree_value - decrease_amount
                elif value is not None and unit is not None:
                    # Use the value/unit mechanism
                    unit_enum = self.Unit(unit)
                    # If the units are different, convert
                    if status.open_degree_unit != unit_enum:
                        status.open_degree_unit = unit_enum
                    status.open_degree_value = status.open_degree_value - value
                else:
                    # Default behavior if no specifics given - small decrease
                    status.open_degree_value = status.open_degree_value - self.TINY_DEGREE_MAPPING[self.DegreeTiny.LITTLE]
                if status.open_degree_value == 0:
                    status.is_open = False
            return {
                "success": True,
                "message": f"Successfully decreased open degree for sunshade at {position}",
                "status": self.to_dict()
            }
            
        except (ValueError, TypeError) as e:
            return {
                "success": False,
                "message": str(e),
                "status": self.to_dict()
            }

    @api("sunshade")
    def carcontrol_sunshade_openDegree_set(self, position: str = "all", 
                                          value: Optional[float] = None, 
                                          unit: Optional[str] = None, 
                                          degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Set the sunshade's open degree to a specific value.
        
        Args:
            position: Control the position of the sunshade. Must be one of ['front row', 'rear row', 'all'].
                     Default is 'all'.
            value: The numeric value part of the openDegree adjustment, mutually exclusive with degree.
            unit: The unit part of the openDegree adjustment, must be one of ['gear', 'percentage', 'centimeter'].
                  Mutually exclusive with degree.
            degree: The different degree of the openDegree adjustment. Must be one of ['max', 'high', 'medium', 'low', 'min'].
                    Mutually exclusive with value/unit.
                    
        Returns:
            A dictionary containing operation result and status information.
            
        Raises:
            ValueError: If neither degree nor value+unit is provided.
        """
        try:
            position_enum = self.Position(position)
            status_list = self._get_status_by_position(position_enum)
            
            # Validate that we have either degree or value+unit
            if degree is None and (value is None or unit is None):
                raise ValueError("Either 'degree' or both 'value' and 'unit' must be provided")
            
            for status in status_list:
                status.is_open = True
                status.is_paused = False
                if degree is not None:
                    # Use the degree mechanism
                    degree_enum = self.DegreeSet(degree)
                    set_value = self.SET_DEGREE_MAPPING[degree_enum]
                    # When using degree presets, we use percentage as the unit
                    status.open_degree_unit = self.Unit.PERCENTAGE
                    status.open_degree_value = set_value
                elif value is not None and unit is not None:
                    # Use the value/unit mechanism
                    unit_enum = self.Unit(unit)
                    status.open_degree_unit = unit_enum
                    status.open_degree_value = value
            
            return {
                "success": True,
                "message": f"Successfully set open degree for sunshade at {position}",
                "status": self.to_dict()
            }
            
        except (ValueError, TypeError) as e:
            return {
                "success": False,
                "message": str(e),
                "status": self.to_dict()
            }

    @api("sunshade")
    def carcontrol_sunshade_mode_leaveAndLockAutoCloseCurtain(self, switch: bool) -> Dict[str, Any]:
        """
        Open/Close the 'Leave Car Lock Auto Close Sunshade' function.
        
        Args:
            switch: The switch for the 'Leave Car Lock Auto Close Sunshade' function. 
                   True means enable, False means disable.
                    
        Returns:
            A dictionary containing operation result and status information.
        """
        try:
            self.leave_and_lock_auto_close_enabled = switch
            
            return {
                "success": True,
                "message": f"Successfully {'enabled' if switch else 'disabled'} Leave Car Lock Auto Close Sunshade function",
                "status": {
                    "leave_and_lock_auto_close_enabled": {
                        "value": self.leave_and_lock_auto_close_enabled,
                        "description": "Whether the sunshade will automatically close when the car is locked and left",
                        "type": type(self.leave_and_lock_auto_close_enabled).__name__
                    }
                }
            }
            
        except (ValueError, TypeError) as e:
            return {
                "success": False,
                "message": str(e),
                "status": self.to_dict()
            }
    



    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the sunshade and its status to a dictionary representation.
        """
        return {
            "front_row_status": {
                "value": self.front_row_status.to_dict(),
                "description": "Status of the front row sunshade",
                "type": "Sunshade.SunshadeStatus"
            },
            "rear_row_status": {
                "value": self.rear_row_status.to_dict(),
                "description": "Status of the rear row sunshade",
                "type": "Sunshade.SunshadeStatus"
            },
            "leave_and_lock_auto_close_enabled": {
                "value": self.leave_and_lock_auto_close_enabled,
                "description": "Whether the sunshade will automatically close when the car is locked and left",
                "type": type(self.leave_and_lock_auto_close_enabled).__name__
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Sunshade':
        """
        Create a Sunshade instance from a dictionary.
        """
        instance = cls()
        
        # Restore front row status
        front_row_data = data["front_row_status"]["value"]
        instance.front_row_status = cls.SunshadeStatus.from_dict(front_row_data)
        
        # Restore rear row status
        rear_row_data = data["rear_row_status"]["value"]
        instance.rear_row_status = cls.SunshadeStatus.from_dict(rear_row_data)
        
        # Restore auto close setting
        auto_close_data = data["leave_and_lock_auto_close_enabled"]["value"]
        instance.leave_and_lock_auto_close_enabled = auto_close_data
        
        return instance

    @classmethod
    def init1(cls) -> 'Sunshade':
        """
        Initialize a Sunshade instance with default closed settings.
        
        In this configuration, all sunshades are closed (0% open) and the
        leave-and-lock auto-close feature is disabled.
        
        Returns:
            A new Sunshade instance with the specified configuration.
        """
        instance = cls()
        
        # Configure front row status - fully closed
        instance.front_row_status.is_open = False
        instance.front_row_status.is_paused = False
        instance.front_row_status.open_degree_value = 0.0
        instance.front_row_status.open_degree_unit = cls.Unit.PERCENTAGE
        
        # Configure rear row status - fully closed
        instance.rear_row_status.is_open = False
        instance.rear_row_status.is_paused = False
        instance.rear_row_status.open_degree_value = 0.0
        instance.rear_row_status.open_degree_unit = cls.Unit.PERCENTAGE
        
        # Disable leave-and-lock auto-close feature
        instance.leave_and_lock_auto_close_enabled = False
        
        return instance

    @classmethod
    def init2(cls) -> 'Sunshade':
        """
        Initialize a Sunshade instance with partially opened settings.
        
        In this configuration, the front row sunshade is partially open (50%),
        the rear row sunshade is fully open (100%), and the leave-and-lock
        auto-close feature is enabled.
        
        Returns:
            A new Sunshade instance with the specified configuration.
        """
        instance = cls()
        
        # Configure front row status - partially open (50%)
        instance.front_row_status.is_open = True
        instance.front_row_status.is_paused = False
        instance.front_row_status.open_degree_value = 50.0
        instance.front_row_status.open_degree_unit = cls.Unit.PERCENTAGE
        
        # Configure rear row status - fully open (100%)
        instance.rear_row_status.is_open = True
        instance.rear_row_status.is_paused = False
        instance.rear_row_status.open_degree_value = 100.0
        instance.rear_row_status.open_degree_unit = cls.Unit.PERCENTAGE
        
        # Enable leave-and-lock auto-close feature
        instance.leave_and_lock_auto_close_enabled = True
        
        return instance