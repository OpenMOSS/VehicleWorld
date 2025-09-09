from enum import Enum
from typing import Dict, Any, Optional, Union, List
from utils import api
from module.environment import Environment


class FootPedal:
    """
    Entity class representing a foot pedal in a vehicle.
    """
    class Position(Enum):
        """
        Enumeration of possible foot pedal positions in the vehicle.
        """

        DRIVER = "driver's seat"
        PASSENGER = "passenger seat"
        ALL = "all"


    class PedalState(Enum):
        """
        Enumeration representing the possible states of a foot pedal.
        """

        ON = True
        OFF = False

    class PedalInfo:
        """
        Inner class to store detailed information about each pedal.
        """

        def __init__(self, position: str, state: bool = False):
            self._position = position
            self._state = state

        @property
        def position(self) -> str:
            return self._position

        @position.setter
        def position(self, value: str) -> None:
            self._position = value

        @property
        def state(self) -> bool:
            return self._state

        @state.setter
        def state(self, value: bool) -> None:
            self._state = value

        def to_dict(self) -> Dict[str, Any]:
            return {
                "position": {
                    "value": self.position,
                    "description": "Position of the pedal in the vehicle (driver's seat, passenger seat)",
                    "type": type(self.position).__name__,
                },
                "state": {
                    "value": self.state,
                    "description": "Current state of the pedal (True for ON, False for OFF)",
                    "type": type(self.state).__name__,
                },
            }

        @classmethod
        def from_dict(cls, data: Dict[str, Any]):
            """
            Create a PedalInfo instance from dictionary data.
            """
            position = data["position"]["value"]
            state = data["state"]["value"]
            return cls(position, state)

    def __init__(self):
        """
        Initialize the FootPedal entity with default values.
        """
        # Create pedal information for each available position
        self._pedals = {
            FootPedal.Position.DRIVER.value: FootPedal.PedalInfo(FootPedal.Position.DRIVER.value),
            FootPedal.Position.PASSENGER.value: FootPedal.PedalInfo(FootPedal.Position.PASSENGER.value),
        }
    @classmethod
    def init1(cls, driver_state: bool = False, passenger_state: bool = False):
        """
        Initialize a FootPedal instance with specified states for both positions.
        
        Args:
            driver_state (bool, optional): Initial state for driver's pedal. Defaults to False.
            passenger_state (bool, optional): Initial state for passenger's pedal. Defaults to False.
            
        Returns:
            FootPedal: A new FootPedal instance with the specified states
        """
        instance = cls()
        instance.set_pedal_state(FootPedal.Position.DRIVER.value, driver_state)
        instance.set_pedal_state(FootPedal.Position.PASSENGER.value, passenger_state)
        return instance
    @classmethod
    def init2(cls, driver_state: bool = True, passenger_state: bool = False):
        """
        Initialize a FootPedal instance with specified states for both positions.
        
        Args:
            driver_state (bool, optional): Initial state for driver's pedal. Defaults to False.
            passenger_state (bool, optional): Initial state for passenger's pedal. Defaults to False.
            
        Returns:
            FootPedal: A new FootPedal instance with the specified states
        """
        instance = cls()
        instance.set_pedal_state(FootPedal.Position.DRIVER.value, driver_state)
        instance.set_pedal_state(FootPedal.Position.PASSENGER.value, passenger_state)
        return instance
    @property
    def pedals(self) -> Dict[str, PedalInfo]:
        """
        Get all pedals information.
        """
        return self._pedals

    def get_pedal_state(self, position: str) -> bool:
        """
        Get the state of a specific pedal.

        Args:
            position (str): The position of the pedal to check

        Returns:
            bool: The current state of the pedal (True for ON, False for OFF)

        Raises:
            ValueError: If the position is invalid
        """
        if position not in self._pedals:
            raise ValueError(f"Invalid position: {position}")
        return self._pedals[position].state

    def set_pedal_state(self, position: str, state: bool) -> None:
        """
        Set the state of a specific pedal.

        Args:
            position (str): The position of the pedal to set
            state (bool): The state to set (True for ON, False for OFF)

        Raises:
            ValueError: If the position is invalid
        """
        if position not in self._pedals:
            raise ValueError(f"Invalid position: {position}")
        self._pedals[position].state = state

    @api("footPedal")
    def carcontrol_pedals_switch(
        self, switch: bool, position: List[str] = None
    ) -> Dict[str, Any]:
        """
        Turn on/off the foot pedal or footrest.

        Args:
            switch (bool): The foot pedal switch, true to turn on, false to turn off.
            position (List[str], optional): The positions of the foot pedal.
                                          Possible values in list: ["driver's seat", "passenger seat", "all"]
                                          If None or empty list, defaults to current speaker position.
                                          If contains "all", all positions will be affected.
                                          defaults to current speaker position.

        Returns:
            Dict[str, Any]: A dictionary containing operation result and updated states.

        Raises:
            ValueError: If any position in the list is invalid
        """
        result = {
            "success": True,
            "message": "Foot pedals operation completed",
            "updated_states": {},
        }

        # Handle default case - if position is None or empty list
        if position is None or len(position) == 0:
            speaker_position = Environment.get_current_speaker()
            position = [speaker_position] if speaker_position in self._pedals else [FootPedal.Position.DRIVER.value]
        
        # Check if "all" is in the list
        if FootPedal.Position.ALL.value in position:
            position = list(self._pedals.keys())
        
        try:
            # Process each position in the list
            for pos in position:
                if pos in self._pedals:
                    self.set_pedal_state(pos, switch)
                    result["updated_states"][pos] = switch
                else:
                    raise ValueError(f"Invalid position: {pos}")
            
            # Update message based on results
            positions_text = ", ".join(result["updated_states"].keys())
            action_text = "turned on" if switch else "turned off"
            result["message"] = f"Foot pedal{'s' if len(result['updated_states']) > 1 else ''} at {positions_text} {action_text}"

        except Exception as e:
            result["success"] = False
            result["message"] = str(e)

        return result

    def get_module_status(self):
        print(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the FootPedal entity to a dictionary representation.

        Returns:
            Dict[str, Any]: Dictionary containing all the FootPedal properties.
        """
        pedals_dict = {}
        for pos, pedal_info in self._pedals.items():
            pedals_dict[pos] = pedal_info.to_dict()

        return {
            "pedals": {
                "value": pedals_dict,
                "description": "Dictionary of all foot pedals, keyed by position",
                "type": "Dict[str, PedalInfo]",
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Create a FootPedal instance from dictionary data.

        Args:
            data (Dict[str, Any]): Dictionary containing FootPedal data

        Returns:
            FootPedal: A new FootPedal instance with the specified data
        """
        instance = cls()

        pedals_data = data["pedals"]["value"]
        for pos, pedal_data in pedals_data.items():
            pedal_info = FootPedal.PedalInfo.from_dict(pedal_data)
            instance._pedals[pos] = pedal_info

        return instance