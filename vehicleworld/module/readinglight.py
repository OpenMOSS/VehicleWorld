from utils import api
from typing import Dict, List, Union, Optional, Any
from enum import Enum
from module.environment import Environment


class ReadingLight:
    """Reading light entity class, manages reading lights at various positions in the vehicle"""

    class Position(Enum):
        """Position enumeration class, used to represent the location of reading lights"""

        DRIVER_SEAT = "driver's seat"
        PASSENGER_SEAT = "passenger seat"
        SECOND_ROW_LEFT = "second row left"
        SECOND_ROW_RIGHT = "second row right"
        THIRD_ROW_LEFT = "third row left"
        THIRD_ROW_RIGHT = "third row right"
        ALL = "all"

    class BrightnessUnit(Enum):
        """Brightness unit enumeration class"""

        GEAR = "gear"
        PERCENTAGE = "percentage"
        NITS = "Nits"

    class BrightnessDegree(Enum):
        """Brightness degree enumeration class, used for setting brightness"""

        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"

    class BrightnessChangeDegree(Enum):
        """Brightness change degree enumeration class, used for increasing or decreasing brightness"""

        LARGE = "large"
        LITTLE = "little"
        TINY = "tiny"

    class LightState:
        """
        Inner class used to represent the state of an individual reading light
        """

        def __init__(
            self,
            is_on: bool = False,
            brightness_value: float = 50.0,
            brightness_unit = None,
        ):
            if brightness_unit is None:
                brightness_unit = ReadingLight.BrightnessUnit.PERCENTAGE
                
            self._is_on = is_on
            self._brightness_value = brightness_value
            self._brightness_unit = brightness_unit

            # Min, max values and default step size for different units
            self._unit_ranges = {
                ReadingLight.BrightnessUnit.GEAR: {"min": 0, "max": 5, "step": 1},
                ReadingLight.BrightnessUnit.PERCENTAGE: {"min": 0, "max": 100, "step": 10},
                ReadingLight.BrightnessUnit.NITS: {"min": 0, "max": 500, "step": 50},
            }

            # Mapping from degree to percentage
            self._degree_mapping = {
                ReadingLight.BrightnessDegree.MAX: 100,
                ReadingLight.BrightnessDegree.HIGH: 80,
                ReadingLight.BrightnessDegree.MEDIUM: 60,
                ReadingLight.BrightnessDegree.LOW: 40,
                ReadingLight.BrightnessDegree.MIN: 20,
            }

            # Mapping from change degree to percentage
            self._change_degree_mapping = {
                ReadingLight.BrightnessChangeDegree.LARGE: 30,
                ReadingLight.BrightnessChangeDegree.LITTLE: 15,
                ReadingLight.BrightnessChangeDegree.TINY: 5,
            }

        @property
        def is_on(self) -> bool:
            return self._is_on

        @is_on.setter
        def is_on(self, value: bool):
            self._is_on = value
            # # When turning off the reading light, automatically set brightness to 0
            if not value:  # If set to off
                # Save current unit
                current_unit = self._brightness_unit
                
                # Set brightness to minimum value for current unit
                min_val = self._unit_ranges[current_unit]["min"]
                self._brightness_value = min_val
            else:
                current_unit = self._brightness_unit
                if self.brightness_value == self._unit_ranges[current_unit]["min"]:
                    self.brightness_value = self._unit_ranges[current_unit]["step"]*4



        @property
        def brightness_value(self) -> float:
            return self._brightness_value

        @brightness_value.setter
        def brightness_value(self, value: float):
            min_val = self._unit_ranges[self._brightness_unit]["min"]
            max_val = self._unit_ranges[self._brightness_unit]["max"]
            self._brightness_value = max(min_val, min(value, max_val))

        @property
        def brightness_unit(self):
            return self._brightness_unit

        @brightness_unit.setter
        def brightness_unit(self, unit):
            # Convert brightness value to accommodate the new unit
            if self._brightness_unit != unit:
                # First convert current value to percentage
                percentage = self._convert_to_percentage(
                    self._brightness_value, self._brightness_unit
                )
                # Then convert percentage to new unit value
                self._brightness_value = self._convert_from_percentage(percentage, unit)
                self._brightness_unit = unit

        def _convert_to_percentage(self, value: float, unit) -> float:
            """Convert value of given unit to percentage"""
            min_val = self._unit_ranges[unit]["min"]
            max_val = self._unit_ranges[unit]["max"]
            return ((value - min_val) / (max_val - min_val)) * 100

        def _convert_from_percentage(
            self, percentage: float, unit
        ) -> float:
            """Convert percentage to value of given unit"""
            min_val = self._unit_ranges[unit]["min"]
            max_val = self._unit_ranges[unit]["max"]
            return min_val + (percentage / 100) * (max_val - min_val)

        def set_brightness_by_degree(self, degree) -> None:
            """Set brightness by degree"""
            percentage = self._degree_mapping[degree]
            self._brightness_value = self._convert_from_percentage(
                percentage, self._brightness_unit
            )

        def increase_brightness(
            self,
            value: Optional[float] = None,
            unit = None,
            degree = None,
        ) -> None:
            """Increase brightness"""
            if value is not None and unit is not None:
                # If units are different, conversion is needed
                if unit != self._brightness_unit:
                    value_in_current_unit = self._convert_unit(
                        value, unit, self._brightness_unit
                    )
                    self._brightness_value += value_in_current_unit
                else:
                    self._brightness_value += value
            elif degree is not None:
                # Use degree to increase brightness
                percentage_increase = self._change_degree_mapping[degree]
                current_percentage = self._convert_to_percentage(
                    self._brightness_value, self._brightness_unit
                )
                new_percentage = min(100, current_percentage + percentage_increase)
                self._brightness_value = self._convert_from_percentage(
                    new_percentage, self._brightness_unit
                )
            else:
                # Default increase by one step
                step = self._unit_ranges[self._brightness_unit]["step"]
                self._brightness_value = min(
                    self._unit_ranges[self._brightness_unit]["max"],
                    self._brightness_value + step,
                )

            # Ensure brightness is within valid range
            self.brightness_value = self._brightness_value

        def decrease_brightness(
            self,
            value: Optional[float] = None,
            unit = None,
            degree = None,
        ) -> None:
            """Decrease brightness"""
            if value is not None and unit is not None:
                # If units are different, conversion is needed
                if unit != self._brightness_unit:
                    value_in_current_unit = self._convert_unit(
                        value, unit, self._brightness_unit
                    )
                    self._brightness_value -= value_in_current_unit
                else:
                    self._brightness_value -= value
            elif degree is not None:
                # Use degree to decrease brightness
                percentage_decrease = self._change_degree_mapping[degree]
                current_percentage = self._convert_to_percentage(
                    self._brightness_value, self._brightness_unit
                )
                new_percentage = max(0, current_percentage - percentage_decrease)
                self._brightness_value = self._convert_from_percentage(
                    new_percentage, self._brightness_unit
                )
            else:
                # Default decrease by one step
                step = self._unit_ranges[self._brightness_unit]["step"]
                self._brightness_value = max(
                    self._unit_ranges[self._brightness_unit]["min"],
                    self._brightness_value - step,
                )

            # Ensure brightness is within valid range
            self.brightness_value = self._brightness_value

        def _convert_unit(
            self, value: float, from_unit, to_unit
        ) -> float:
            """Convert values between different units"""
            # First convert to percentage
            percentage = self._convert_to_percentage(value, from_unit)
            # Then convert from percentage to target unit
            return self._convert_from_percentage(percentage, to_unit)

        def to_dict(self) -> Dict:
            """Return dictionary representation of the inner class state"""
            return {
                "is_on": {
                    "value": self.is_on,
                    "description": "Whether the reading light is on",
                    "type": type(self.is_on).__name__,
                },
                "brightness_value": {
                    "value": self.brightness_value,
                    "description": "Reading light brightness value, can only be adjusted when the light is on. When is_on is set to True, if this value is 0, you should set it to 40. Values are converted between units using linear scaling: percentage = ((value - min_val) / (max_val - min_val)) * 100, and unit_value = min_val + (percentage / 100) * (max_val - min_val)",
                    "type": type(self.brightness_value).__name__,
                },
                "brightness_unit": {
                    "value": self.brightness_unit.value,
                    "description": "Reading light brightness unit, possible values include: gear, percentage, Nits, can only be adjusted when the light is on",
                    "type": "BrightnessUnit",
                },
            }

        @classmethod
        def from_dict(cls, data: Dict) -> "ReadingLight.LightState":
            """Restore inner class instance from dictionary"""
            instance = cls()
            instance.is_on = data["is_on"]["value"]
            instance.brightness_value = data["brightness_value"]["value"]
            # Convert string back to enum type
            for unit in ReadingLight.BrightnessUnit:
                if unit.value == data["brightness_unit"]["value"]:
                    instance.brightness_unit = unit
                    break
            return instance

    def __init__(self):
        # Initialize reading light states for each position
        self._lights = {
            ReadingLight.Position.DRIVER_SEAT: ReadingLight.LightState(),
            ReadingLight.Position.PASSENGER_SEAT: ReadingLight.LightState(),
            ReadingLight.Position.SECOND_ROW_LEFT: ReadingLight.LightState(),
            ReadingLight.Position.SECOND_ROW_RIGHT: ReadingLight.LightState(),
            ReadingLight.Position.THIRD_ROW_LEFT: ReadingLight.LightState(),
            ReadingLight.Position.THIRD_ROW_RIGHT: ReadingLight.LightState(),
        }

        # Auto mode status
        self._auto_mode = False

    @classmethod
    def init1(cls):
        """
        Initialize reading light system - Standard configuration
        
        All reading lights are off by default, brightness set to 0%, using percentage unit
        Auto mode is off by default
        """
        # Initialize reading light states for each position
        instance = cls()
        instance._lights = {
            ReadingLight.Position.DRIVER_SEAT: ReadingLight.LightState(is_on=False, brightness_value=0, brightness_unit=ReadingLight.BrightnessUnit.PERCENTAGE),
            ReadingLight.Position.PASSENGER_SEAT: ReadingLight.LightState(is_on=False, brightness_value=0, brightness_unit=ReadingLight.BrightnessUnit.PERCENTAGE),
            ReadingLight.Position.SECOND_ROW_LEFT: ReadingLight.LightState(is_on=False, brightness_value=0, brightness_unit=ReadingLight.BrightnessUnit.PERCENTAGE),
            ReadingLight.Position.SECOND_ROW_RIGHT: ReadingLight.LightState(is_on=False, brightness_value=0, brightness_unit=ReadingLight.BrightnessUnit.PERCENTAGE),
            ReadingLight.Position.THIRD_ROW_LEFT: ReadingLight.LightState(is_on=False, brightness_value=0, brightness_unit=ReadingLight.BrightnessUnit.PERCENTAGE),
            ReadingLight.Position.THIRD_ROW_RIGHT: ReadingLight.LightState(is_on=False, brightness_value=0, brightness_unit=ReadingLight.BrightnessUnit.PERCENTAGE),
        }
        
        # Auto mode status
        instance._auto_mode = False
        return instance
    
    @classmethod
    def init2(cls):
        """
        Initialize reading light system - Night mode configuration
        
        Front row reading lights are on with low brightness, rear row reading lights are off
        All lights use gear brightness unit
        Auto mode is on
        """
        # Initialize reading light states for each position
        instance = cls()
        instance._lights = {
            # Front row reading lights on, low brightness (level 2, range 1-5)
            ReadingLight.Position.DRIVER_SEAT: ReadingLight.LightState(is_on=True, brightness_value=2.0, brightness_unit=ReadingLight.BrightnessUnit.GEAR),
            ReadingLight.Position.PASSENGER_SEAT: ReadingLight.LightState(is_on=True, brightness_value=2.0, brightness_unit=ReadingLight.BrightnessUnit.GEAR),
            
            # Rear row reading lights off by default, but preset to medium brightness (level 3, range 1-5)
            ReadingLight.Position.SECOND_ROW_LEFT: ReadingLight.LightState(is_on=False, brightness_value=0, brightness_unit=ReadingLight.BrightnessUnit.GEAR),
            ReadingLight.Position.SECOND_ROW_RIGHT: ReadingLight.LightState(is_on=False, brightness_value=0, brightness_unit=ReadingLight.BrightnessUnit.GEAR),
            ReadingLight.Position.THIRD_ROW_LEFT: ReadingLight.LightState(is_on=False, brightness_value=0, brightness_unit=ReadingLight.BrightnessUnit.GEAR),
            ReadingLight.Position.THIRD_ROW_RIGHT: ReadingLight.LightState(is_on=False, brightness_value=0, brightness_unit=ReadingLight.BrightnessUnit.GEAR),
        }
        
        # Enable auto mode
        instance._auto_mode = True
        return instance
        
    @property
    def auto_mode(self) -> bool:
        """Get auto mode status"""
        return self._auto_mode

    @auto_mode.setter
    def auto_mode(self, value: bool):
        """Set auto mode status"""
        self._auto_mode = value

    def _get_position_from_input(
        self, positions: Optional[List[str]] = None
    ) -> List[str]:
        """
        Get a list of position strings based on input
        If not specified, return the current speaker's position
        If position is "all", return a list of all positions
        """
        if positions is None or len(positions) == 0:
            # Get current speaker position
            speaker_position = Environment.get_current_speaker()
            for pos in ReadingLight.Position:
                if pos.value == speaker_position:
                    return [pos.value]
            # If no matching position is found, return driver's seat position by default
            return [ReadingLight.Position.DRIVER_SEAT.value]

        result_positions = []
        for position in positions:
            for pos in ReadingLight.Position:
                if pos.value == position:
                    if pos == ReadingLight.Position.ALL:
                        # If "all", return list of all positions (except ALL itself)
                        return [p.value for p in ReadingLight.Position if p != ReadingLight.Position.ALL]
                    result_positions.append(pos.value)
                    break
            else:
                # If no matching position is found, raise an exception
                raise ValueError(f"Invalid position value: {position}")
        
        return result_positions

    def _validate_and_get_position(
        self, positions: Optional[List[str]] = None
    ) -> List[str]:
        """Validate and get position string list"""
        try:
            return self._get_position_from_input(positions)
        except ValueError as e:
            raise ValueError(f"Position validation failed: {str(e)}")

    def _apply_to_positions(
        self, positions: List[str], func, *args, **kwargs
    ) -> Dict:
        """
        Apply function to specified positions and return operation results
        """
        results = {}

        for pos_str in positions:
            # Convert string to corresponding enum value to get light status
            pos_enum = None
            for p in ReadingLight.Position:
                if p.value == pos_str:
                    pos_enum = p
                    break
            
            if pos_enum is None:
                continue  # If no matching enum value is found, skip this position
                
            result = func(pos_enum, *args, **kwargs)
            results[pos_str] = result

        return results

    @api("readingLight")
    def carcontrol_readingLight_switch(
        self, position: List[str], switch: bool = False
    ) -> Dict:
        """
        Switch reading light on/off

        Args:
            position: List of reading light positions, possible values: "driver's seat", "passenger seat",
                     "second row left", "second row right", "third row left",
                     "third row right", "all". If not specified, use current speaker's position.
            switch: Switch status, True means on, False means off

        Returns:
            Dictionary containing operation results and status information
        """
        try:
            positions = self._validate_and_get_position(position)

            def switch_light(pos: ReadingLight.Position, state: bool) -> Dict:
                light = self._lights[pos]
                light.is_on = state
                return {
                    "success": True,
                    "message": f"{'Turned on' if state else 'Turned off'} the {pos.value} reading light",
                    "state": light.to_dict(),
                }

            results = self._apply_to_positions(positions, switch_light, switch)

            return {"success": True, "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @api("readingLight")
    def carcontrol_readingLight_mode_auto(self, switch: bool) -> Dict:
        """
        Set reading light auto mode

        Args:
            switch: Auto mode switch status, True means on, False means off

        Returns:
            Dictionary containing operation results and status information
        """
        try:
            self.auto_mode = switch

            return {
                "success": True,
                "message": f"{'Enabled' if switch else 'Disabled'} reading light auto mode",
                "auto_mode": self.auto_mode,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @api("readingLight")
    def carcontrol_readingLight_brightness_set(
        self,
        position: List[str],
        value: Optional[float] = None,
        unit: Optional[str] = None,
        degree: Optional[str] = None,
    ) -> Dict:
        """
        Set reading light brightness

        Args:
            position: List of reading light positions, possible values: "driver's seat", "passenger seat",
                     "second row left", "second row right", "third row left",
                     "third row right", "all". If not specified, use current speaker's position.
            value: Brightness value, used with unit
            unit: Brightness unit, possible values: "gear", "percentage", "Nits"
            degree: Brightness degree, possible values: "max", "high", "medium", "low", "min"
                   Mutually exclusive with value/unit

        Returns:
            Dictionary containing operation results and status information
        """
        try:
            # Validate mutually exclusive parameters
            if (value is not None and unit is not None) and degree is not None:
                raise ValueError("Parameter error: value/unit and degree are mutually exclusive")

            if (value is not None and unit is None) or (
                value is None and unit is not None
            ):
                raise ValueError("Parameter error: value and unit must be provided together")

            positions = self._validate_and_get_position(position)

            # If unit is provided, validate and convert to enum type
            unit_enum = None
            if unit is not None:
                unit_enum = next((u for u in ReadingLight.BrightnessUnit if u.value == unit), None)
                if unit_enum is None:
                    raise ValueError(f"Invalid brightness unit: {unit}")

            # If degree is provided, validate and convert to enum type
            degree_enum = None
            if degree is not None:
                degree_enum = next(
                    (d for d in ReadingLight.BrightnessDegree if d.value == degree), None
                )
                if degree_enum is None:
                    raise ValueError(f"Invalid brightness degree: {degree}")

            def set_brightness(
                pos: ReadingLight.Position,
                val: Optional[float],
                unit_e,
                deg,
            ) -> Dict:
                light = self._lights[pos]

                # Ensure light is on
                if not light.is_on:
                    light.is_on = True
                    # return {"success": False, "message":  f"{pos.value} reading light is off, cannot adjust brightness", "state": light.to_dict()}

                if deg is not None:
                    # Set brightness using degree
                    light.set_brightness_by_degree(deg)
                    message = f"Set {pos.value} reading light brightness to {deg.value}"
                elif val is not None and unit_e is not None:
                    # Set brightness using specific value and unit
                    if unit_e != light.brightness_unit:
                        light.brightness_unit = unit_e
                    light.brightness_value = val
                    message = f"Set {pos.value} reading light brightness to {val} {unit_e.value}"
                else:
                    raise ValueError("Parameter error: must provide value/unit or degree")

                return {"success": True, "message": message, "state": light.to_dict()}

            results = self._apply_to_positions(
                positions, set_brightness, value, unit_enum, degree_enum
            )

            return {"success": True, "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @api("readingLight")
    def carcontrol_readingLight_brightness_increase(
        self,
        position: List[str],
        value: Optional[float] = None,
        unit: Optional[str] = None,
        degree: Optional[str] = None,
    ) -> Dict:
        """
        Increase reading light brightness

        Args:
            position: List of reading light positions, possible values: "driver's seat", "passenger seat",
                     "second row left", "second row right", "third row left",
                     "third row right", "all". If not specified, use current speaker's position.
            value: Brightness value to increase, used with unit
            unit: Brightness unit, possible values: "gear", "percentage", "Nits"
            degree: Degree of brightness increase, possible values: "large", "little", "tiny"
                   Mutually exclusive with value/unit

        Returns:
            Dictionary containing operation results and status information
        """
        try:
            # Validate mutually exclusive parameters
            if (value is not None and unit is not None) and degree is not None:
                raise ValueError("Parameter error: value/unit and degree are mutually exclusive")

            if (value is not None and unit is None) or (
                value is None and unit is not None
            ):
                raise ValueError("Parameter error: value and unit must be provided together")

            positions = self._validate_and_get_position(position)

            # If unit is provided, validate and convert to enum type
            unit_enum = None
            if unit is not None:
                unit_enum = next((u for u in ReadingLight.BrightnessUnit if u.value == unit), None)
                if unit_enum is None:
                    raise ValueError(f"Invalid brightness unit: {unit}")

            # If degree is provided, validate and convert to enum type
            degree_enum = None
            if degree is not None:
                degree_enum = next(
                    (d for d in ReadingLight.BrightnessChangeDegree if d.value == degree), None
                )
                if degree_enum is None:
                    raise ValueError(f"Invalid brightness increase degree: {degree}")

            def increase_brightness(
                pos: ReadingLight.Position,
                val: Optional[float],
                unit_e,
                deg,
            ) -> Dict:
                light = self._lights[pos]

                # Ensure light is on
                if not light.is_on:
                    light.is_on = True
                    # return {"success": False, "message":  f"{pos.value} reading light is off, cannot adjust brightness", "state": light.to_dict()}

                # Increase brightness
                old_value = light.brightness_value
                light.increase_brightness(val, unit_e, deg)

                # Construct message
                if deg is not None:
                    message = f"Increased {pos.value} reading light brightness by {deg.value} degree"
                elif val is not None and unit_e is not None:
                    message = f"Increased {pos.value} reading light brightness by {val} {unit_e.value}"
                else:
                    message = f"Increased {pos.value} reading light brightness"

                message += f", from {old_value} to {light.brightness_value}"

                return {"success": True, "message": message, "state": light.to_dict()}

            results = self._apply_to_positions(
                positions, increase_brightness, value, unit_enum, degree_enum
            )

            return {"success": True, "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @api("readingLight")
    def carcontrol_readingLight_brightness_decrease(
        self,
        position: List[str],
        value: Optional[float] = None,
        unit: Optional[str] = None,
        degree: Optional[str] = None,
    ) -> Dict:
        """
        Decrease reading light brightness

        Args:
            position: List of reading light positions, possible values: "driver's seat", "passenger seat",
                     "second row left", "second row right", "third row left",
                     "third row right", "all". If not specified, use current speaker's position.
            value: Brightness value to decrease, used with unit
            unit: Brightness unit, possible values: "gear", "percentage", "Nits"
            degree: Degree of brightness decrease, possible values: "large", "little", "tiny"
                   Mutually exclusive with value/unit

        Returns:
            Dictionary containing operation results and status information
        """
        try:
            # Validate mutually exclusive parameters
            if (value is not None and unit is not None) and degree is not None:
                raise ValueError("Parameter error: value/unit and degree are mutually exclusive")

            if (value is not None and unit is None) or (
                value is None and unit is not None
            ):
                raise ValueError("Parameter error: value and unit must be provided together")

            positions = self._validate_and_get_position(position)

            # If unit is provided, validate and convert to enum type
            unit_enum = None
            if unit is not None:
                unit_enum = next((u for u in ReadingLight.BrightnessUnit if u.value == unit), None)
                if unit_enum is None:
                    raise ValueError(f"Invalid brightness unit: {unit}")

            # If degree is provided, validate and convert to enum type
            degree_enum = None
            if degree is not None:
                degree_enum = next(
                    (d for d in ReadingLight.BrightnessChangeDegree if d.value == degree), None
                )
                if degree_enum is None:
                    raise ValueError(f"Invalid brightness decrease degree: {degree}")

            def decrease_brightness(
                pos: ReadingLight.Position,
                val: Optional[float],
                unit_e,
                deg,
            ) -> Dict:
                light = self._lights[pos]

                # If light is off, no operation needed
                if not light.is_on:
                    return {
                        "success": False,
                        "message": f"{pos.value} reading light is off, cannot adjust brightness",
                        "state": light.to_dict(),
                    }

                # Decrease brightness
                old_value = light.brightness_value
                light.decrease_brightness(val, unit_e, deg)

                # Construct message
                if deg is not None:
                    message = f"Decreased {pos.value} reading light brightness by {deg.value} degree"
                elif val is not None and unit_e is not None:
                    message = f"Decreased {pos.value} reading light brightness by {val} {unit_e.value}"
                else:
                    message = f"Decreased {pos.value} reading light brightness"

                message += f", from {old_value} to {light.brightness_value}"

                return {"success": True, "message": message, "state": light.to_dict()}

            results = self._apply_to_positions(
                positions, decrease_brightness, value, unit_enum, degree_enum
            )

            return {"success": True, "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    
    def get_module_status(self):
        print(self.to_dict())

    def to_dict(self) -> Dict[str, Dict]:
        """Return status of reading lights at all positions
        
        Returns:
            Dict[str, Dict]: Dictionary with position strings as keys and corresponding light states as values
        """
        light_states = {}
        for pos, light in self._lights.items():
            light_states[pos.value] = light.to_dict()
        
        return light_states