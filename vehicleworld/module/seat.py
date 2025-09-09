from utils import api
import sys
from module.environment import Environment


class Seat:
    """
    A class representing a car seat with all its controllable functionalities.
    """

    class HeaterSystem:
        """
        Inner class representing the heating system of a car seat.
        """

        def __init__(self):
            self._is_on = False
            self._temperature_level = 1  # 1-5 (min-max)
            # Temperature can be specified in different units
            self._temperature_value = 20.0
            self._temperature_unit = "celsius"  # celsius, gear, percentage

        @property
        def is_on(self):
            return self._is_on

        @is_on.setter
        def is_on(self, value):
            self._is_on = value

        @property
        def temperature_level(self):
            return self._temperature_level

        @temperature_level.setter
        def temperature_level(self, value):
            if 1 <= value <= 5:
                self._temperature_level = value

        @property
        def temperature_value(self):
            return self._temperature_value

        @temperature_value.setter
        def temperature_value(self, value):
            self._temperature_value = value

        @property
        def temperature_unit(self):
            return self._temperature_unit

        @temperature_unit.setter
        def temperature_unit(self, value):
            self._temperature_unit = value

        def to_dict(self):
            return {
                "is_on": {
                    "value": self.is_on,
                    "description": "Whether the seat heater is turned on or off",
                    "type": type(self.is_on).__name__,
                },
                "temperature_level": {
                    "value": self.temperature_level,
                    "description": "The heating level from 1-5, where 1=min, 2=low, 3=medium, 4=high, 5=max",
                    "type": type(self.temperature_level).__name__,
                },
                "temperature_value": {
                    "value": self.temperature_value,
                    "description": "The specific temperature value",
                    "type": type(self.temperature_value).__name__,
                },
                "temperature_unit": {
                    "value": self.temperature_unit,
                    "description": "The unit for temperature measurement (celsius, gear, percentage)",
                    "type": type(self.temperature_unit).__name__,
                },
            }

        @classmethod
        def from_dict(cls, data):
            instance = cls()
            instance.is_on = data["is_on"]["value"]
            instance.temperature_level = data["temperature_level"]["value"]
            instance.temperature_value = data["temperature_value"]["value"]
            instance.temperature_unit = data["temperature_unit"]["value"]
            return instance

    class MassageSystem:
        """
        Inner class representing the massage system of a car seat.
        """

        def __init__(self):
            self._is_on = False
            self._intensity_level = 1  # 1-5 (min-max)
            self._intensity_value = 0.0
            self._intensity_unit = "gear"  # gear, percentage
            self._active_mode = None  # Current active massage mode

        @property
        def is_on(self):
            return self._is_on

        @is_on.setter
        def is_on(self, value):
            self._is_on = value

        @property
        def intensity_level(self):
            return self._intensity_level

        @intensity_level.setter
        def intensity_level(self, value):
            if 1 <= value <= 5:
                self._intensity_level = value

        @property
        def intensity_value(self):
            return self._intensity_value

        @intensity_value.setter
        def intensity_value(self, value):
            self._intensity_value = value

        @property
        def intensity_unit(self):
            return self._intensity_unit

        @intensity_unit.setter
        def intensity_unit(self, value):
            self._intensity_unit = value

        @property
        def active_mode(self):
            return self._active_mode

        @active_mode.setter
        def active_mode(self, value):
            valid_modes = [
                "wave",
                "cat step",
                "stretch",
                "snake",
                "butterfly",
                "shoulder",
                "upper back",
                "waist",
                "full back",
                "random",
            ]
            if value in valid_modes or value is None:
                self._active_mode = value

        def to_dict(self):
            return {
                "is_on": {
                    "value": self.is_on,
                    "description": "Whether the massage system is turned on or off",
                    "type": type(self.is_on).__name__,
                },
                "intensity_level": {
                    "value": self.intensity_level,
                    "description": "The massage intensity level from 1-5, where 1=min, 2=low, 3=medium, 4=high, 5=max",
                    "type": type(self.intensity_level).__name__,
                },
                "intensity_value": {
                    "value": self.intensity_value,
                    "description": "The specific massage intensity value",
                    "type": type(self.intensity_value).__name__,
                },
                "intensity_unit": {
                    "value": self.intensity_unit,
                    "description": "The unit for massage intensity (gear, percentage)",
                    "type": type(self.intensity_unit).__name__,
                },
                "active_mode": {
                    "value": self.active_mode,
                    "description": "The currently active massage mode (wave, cat step, stretch, snake, butterfly, shoulder, upper back, waist, full back, random)",
                    "type": str(type(self.active_mode).__name__),
                },
            }

        @classmethod
        def from_dict(cls, data):
            instance = cls()
            instance.is_on = data["is_on"]["value"]
            instance.intensity_level = data["intensity_level"]["value"]
            instance.intensity_value = data["intensity_value"]["value"]
            instance.intensity_unit = data["intensity_unit"]["value"]
            instance.active_mode = data["active_mode"]["value"]
            return instance

    class VentilationSystem:
        """
        Inner class representing the ventilation system of a car seat.
        """

        def __init__(self):
            self._is_on = False
            self._airflow_level = 1  # 1-5 (min-max)
            self._airflow_value = 0.0
            self._airflow_unit = "gear"  # gear, percentage

        @property
        def is_on(self):
            return self._is_on

        @is_on.setter
        def is_on(self, value):
            self._is_on = value

        @property
        def airflow_level(self):
            return self._airflow_level

        @airflow_level.setter
        def airflow_level(self, value):
            if 1 <= value <= 5:
                self._airflow_level = value

        @property
        def airflow_value(self):
            return self._airflow_value

        @airflow_value.setter
        def airflow_value(self, value):
            self._airflow_value = value

        @property
        def airflow_unit(self):
            return self._airflow_unit

        @airflow_unit.setter
        def airflow_unit(self, value):
            self._airflow_unit = value

        def to_dict(self):
            return {
                "is_on": {
                    "value": self.is_on,
                    "description": "Whether the seat ventilation system is turned on or off",
                    "type": type(self.is_on).__name__,
                },
                "airflow_level": {
                    "value": self.airflow_level,
                    "description": "The ventilation airflow level from 1-5, where 1=min, 2=low, 3=medium, 4=high, 5=max",
                    "type": type(self.airflow_level).__name__,
                },
                "airflow_value": {
                    "value": self.airflow_value,
                    "description": "The specific ventilation airflow value",
                    "type": type(self.airflow_value).__name__,
                },
                "airflow_unit": {
                    "value": self.airflow_unit,
                    "description": "The unit for ventilation airflow (gear, percentage)",
                    "type": type(self.airflow_unit).__name__,
                },
            }

        @classmethod
        def from_dict(cls, data):
            instance = cls()
            instance.is_on = data["is_on"]["value"]
            instance.airflow_level = data["airflow_level"]["value"]
            instance.airflow_value = data["airflow_value"]["value"]
            instance.airflow_unit = data["airflow_unit"]["value"]
            return instance

    class PositionSystem:
        """
        Inner class representing the positioning system of a car seat.
        """

        def __init__(self):
            # Basic positioning
            self._horizontal_position = 50  # 0-100%
            self._vertical_position = 50  # 0-100%
            self._is_folded = False
            self._cushion_length = 50  # 0-100%

            # New positioning attributes from additional APIs
            self._cushion_angle = 50  # 0-100%
            self._backrest_angle = 50  # 0-100%
            self._leg_rest_height = 0  # 0-100%
            self._feet_rest_height = 0  # 0-100%
            self._headrest_height = 50  # 0-100%
            self._guest_welcome_mode = False

        @property
        def horizontal_position(self):
            return self._horizontal_position

        @horizontal_position.setter
        def horizontal_position(self, value):
            if 0 <= value <= 100:
                self._horizontal_position = value

        @property
        def vertical_position(self):
            return self._vertical_position

        @vertical_position.setter
        def vertical_position(self, value):
            if 0 <= value <= 100:
                self._vertical_position = value

        @property
        def is_folded(self):
            return self._is_folded

        @is_folded.setter
        def is_folded(self, value):
            self._is_folded = value

        @property
        def cushion_length(self):
            return self._cushion_length

        @cushion_length.setter
        def cushion_length(self, value):
            if 0 <= value <= 100:
                self._cushion_length = value

        @property
        def cushion_angle(self):
            return self._cushion_angle

        @cushion_angle.setter
        def cushion_angle(self, value):
            if 0 <= value <= 100:
                self._cushion_angle = value

        @property
        def backrest_angle(self):
            return self._backrest_angle

        @backrest_angle.setter
        def backrest_angle(self, value):
            if 0 <= value <= 100:
                self._backrest_angle = value

        @property
        def leg_rest_height(self):
            return self._leg_rest_height

        @leg_rest_height.setter
        def leg_rest_height(self, value):
            if 0 <= value <= 100:
                self._leg_rest_height = value

        @property
        def feet_rest_height(self):
            return self._feet_rest_height

        @feet_rest_height.setter
        def feet_rest_height(self, value):
            if 0 <= value <= 100:
                self._feet_rest_height = value

        @property
        def headrest_height(self):
            return self._headrest_height

        @headrest_height.setter
        def headrest_height(self, value):
            if 0 <= value <= 100:
                self._headrest_height = value

        @property
        def guest_welcome_mode(self):
            return self._guest_welcome_mode

        @guest_welcome_mode.setter
        def guest_welcome_mode(self, value):
            self._guest_welcome_mode = value

        def to_dict(self):
            return {
                "horizontal_position": {
                    "value": self.horizontal_position,
                    "description": "The horizontal position of the seat (0-100%, where 0=furthest forward, 100=furthest back)",
                    "type": type(self.horizontal_position).__name__,
                },
                "vertical_position": {
                    "value": self.vertical_position,
                    "description": "The vertical position/height of the seat (0-100%, where 0=lowest, 100=highest)",
                    "type": type(self.vertical_position).__name__,
                },
                "is_folded": {
                    "value": self.is_folded,
                    "description": "Whether the seat is folded (closed) or unfolded (open)",
                    "type": type(self.is_folded).__name__,
                },
                "cushion_length": {
                    "value": self.cushion_length,
                    "description": "The length of the seat cushion (0-100%, where 0=shortest, 100=longest)",
                    "type": type(self.cushion_length).__name__,
                },
                "cushion_angle": {
                    "value": self.cushion_angle,
                    "description": "The inclination angle of the seat cushion (0-100%, where 0=flattest, 100=steepest)",
                    "type": type(self.cushion_angle).__name__,
                },
                "backrest_angle": {
                    "value": self.backrest_angle,
                    "description": "The inclination angle of the seat backrest (0-100%, where 0=most upright, 100=most reclined)",
                    "type": type(self.backrest_angle).__name__,
                },
                "leg_rest_height": {
                    "value": self.leg_rest_height,
                    "description": "The height of the leg rest (0-100%, where 0=lowest, 100=highest)",
                    "type": type(self.leg_rest_height).__name__,
                },
                "feet_rest_height": {
                    "value": self.feet_rest_height,
                    "description": "The height of the feet rest (0-100%, where 0=lowest, 100=highest)",
                    "type": type(self.feet_rest_height).__name__,
                },
                "headrest_height": {
                    "value": self.headrest_height,
                    "description": "The height of the headrest (0-100%, where 0=lowest, 100=highest)",
                    "type": type(self.headrest_height).__name__,
                },
                "guest_welcome_mode": {
                    "value": self.guest_welcome_mode,
                    "description": "Whether the guest welcome mode is turned on or off",
                    "type": type(self.guest_welcome_mode).__name__,
                },
            }

        @classmethod
        def from_dict(cls, data):
            instance = cls()
            instance.horizontal_position = data["horizontal_position"]["value"]
            instance.vertical_position = data["vertical_position"]["value"]
            instance.is_folded = data["is_folded"]["value"]
            instance.cushion_length = data["cushion_length"]["value"]
            instance.cushion_angle = data["cushion_angle"]["value"]
            instance.backrest_angle = data["backrest_angle"]["value"]
            instance.leg_rest_height = data["leg_rest_height"]["value"]
            instance.feet_rest_height = data["feet_rest_height"]["value"]
            instance.headrest_height = data["headrest_height"]["value"]
            instance.guest_welcome_mode = data["guest_welcome_mode"]["value"]
            return instance

    def __init__(self):
        # Initialize each seat position with its own systems
        self._seats = {
            "driver's seat": {
                "heater": Seat.HeaterSystem(),
                "massager": Seat.MassageSystem(),
                "position": Seat.PositionSystem(),
                "ventilation": Seat.VentilationSystem(),
            },
            "passenger seat": {
                "heater": Seat.HeaterSystem(),
                "massager": Seat.MassageSystem(),
                "position": Seat.PositionSystem(),
                "ventilation": Seat.VentilationSystem(),
            },
            "second row left": {
                "heater": Seat.HeaterSystem(),
                "massager": Seat.MassageSystem(),
                "position": Seat.PositionSystem(),
                "ventilation": Seat.VentilationSystem(),
            },
            "second row right": {
                "heater": Seat.HeaterSystem(),
                "massager": Seat.MassageSystem(),
                "position": Seat.PositionSystem(),
                "ventilation": Seat.VentilationSystem(),
            },
            "third row left": {
                "heater": Seat.HeaterSystem(),
                "massager": Seat.MassageSystem(),
                "position": Seat.PositionSystem(),
                "ventilation": Seat.VentilationSystem(),
            },
            "third row right": {
                "heater": Seat.HeaterSystem(),
                "massager": Seat.MassageSystem(),
                "position": Seat.PositionSystem(),
                "ventilation": Seat.VentilationSystem(),
            },
        }

        # Control view page state
        self._view_page_open = False

    @classmethod
    def init1(cls):
        """
        Initialize the Seat system with a comfort-oriented preset.
        All seats are configured with heated, ventilated, and massage functions
        optimized for maximum comfort.
        
        Returns:
            Seat: A new Seat instance with comfort-oriented settings
        """
        instance = cls()
        
        # Configure all seats with comfort settings
        for seat_pos in instance._seats:
            # Heater configuration - warm settings
            instance._seats[seat_pos]["heater"].is_on = False
            instance._seats[seat_pos]["heater"].temperature_level = 3
            instance._seats[seat_pos]["heater"].temperature_value = 25.0
            instance._seats[seat_pos]["heater"].temperature_unit = "celsius"
            
            # Massage configuration - gentle wave massage
            instance._seats[seat_pos]["massager"].is_on = False
            instance._seats[seat_pos]["massager"].intensity_level = 2
            instance._seats[seat_pos]["massager"].intensity_value = 40.0
            instance._seats[seat_pos]["massager"].intensity_unit = "percentage"
            instance._seats[seat_pos]["massager"].active_mode = "wave"
            
            # Ventilation configuration - light cooling
            instance._seats[seat_pos]["ventilation"].is_on = False
            instance._seats[seat_pos]["ventilation"].airflow_level = 2
            instance._seats[seat_pos]["ventilation"].airflow_value = 40.0
            instance._seats[seat_pos]["ventilation"].airflow_unit = "percentage"
            
            # Position configuration - relaxed position
            position = instance._seats[seat_pos]["position"]
            position.horizontal_position = 65  # More reclined
            position.vertical_position = 40    # Slightly lower
            position.is_folded = False
            position.cushion_length = 70      # Extended
            position.cushion_angle = 30       # Slightly angled
            position.backrest_angle = 70      # More reclined
            position.leg_rest_height = 40     # Partially raised
            position.feet_rest_height = 30    # Partially raised
            position.headrest_height = 60     # Properly positioned
            position.guest_welcome_mode = False
        
        # Set view page to closed
        instance._view_page_open = False
        
        return instance

    @classmethod
    def init2(cls):
        """
        Initialize the Seat system with a driving-focused preset.
        Front seats are configured for optimal driving position with moderate
        heating, while rear seats are configured for passenger comfort.
        
        Returns:
            Seat: A new Seat instance with driving-focused settings
        """
        instance = cls()
        
        # Configure front seats (driver and passenger) for driving
        for seat_pos in ["driver's seat", "passenger seat"]:
            # Heater configuration - mild warmth
            instance._seats[seat_pos]["heater"].is_on = True
            instance._seats[seat_pos]["heater"].temperature_level = 2
            instance._seats[seat_pos]["heater"].temperature_value = 22.0
            instance._seats[seat_pos]["heater"].temperature_unit = "celsius"
            
            # Massage configuration - off for driver, light for passenger
            instance._seats[seat_pos]["massager"].is_on = False if seat_pos == "driver's seat" else True
            instance._seats[seat_pos]["massager"].intensity_level = 1
            instance._seats[seat_pos]["massager"].intensity_value = 20.0
            instance._seats[seat_pos]["massager"].intensity_unit = "percentage"
            instance._seats[seat_pos]["massager"].active_mode = None if seat_pos == "driver's seat" else "shoulder"
            
            # Ventilation configuration - off
            instance._seats[seat_pos]["ventilation"].is_on = False
            instance._seats[seat_pos]["ventilation"].airflow_level = 1
            instance._seats[seat_pos]["ventilation"].airflow_value = 0.0
            instance._seats[seat_pos]["ventilation"].airflow_unit = "gear"
            
            # Position configuration - upright driving position
            position = instance._seats[seat_pos]["position"]
            position.horizontal_position = 40    # Forward for control
            position.vertical_position = 60      # Higher for visibility
            position.is_folded = False
            position.cushion_length = 50         # Standard
            position.cushion_angle = 20          # Slight angle
            position.backrest_angle = 30         # Upright
            position.leg_rest_height = 0         # Not raised
            position.feet_rest_height = 0        # Not raised
            position.headrest_height = 70        # Higher for safety
            position.guest_welcome_mode = False
        
        # Configure rear seats for passenger comfort
        for seat_pos in ["second row left", "second row right", "third row left", "third row right"]:
            # Heater configuration - cozy
            instance._seats[seat_pos]["heater"].is_on = True
            instance._seats[seat_pos]["heater"].temperature_level = 3
            instance._seats[seat_pos]["heater"].temperature_value = 24.0
            instance._seats[seat_pos]["heater"].temperature_unit = "celsius"
            
            # Massage configuration - comfort massage
            instance._seats[seat_pos]["massager"].is_on = True
            instance._seats[seat_pos]["massager"].intensity_level = 3
            instance._seats[seat_pos]["massager"].intensity_value = 60.0
            instance._seats[seat_pos]["massager"].intensity_unit = "percentage"
            instance._seats[seat_pos]["massager"].active_mode = "full back"
            
            # Ventilation configuration - gentle
            instance._seats[seat_pos]["ventilation"].is_on = True
            instance._seats[seat_pos]["ventilation"].airflow_level = 2
            instance._seats[seat_pos]["ventilation"].airflow_value = 40.0
            instance._seats[seat_pos]["ventilation"].airflow_unit = "percentage"
            
            # Position configuration - comfortable passenger position
            position = instance._seats[seat_pos]["position"]
            position.horizontal_position = 60    # More reclined
            position.vertical_position = 45      # Lower
            position.is_folded = False
            position.cushion_length = 65         # Extended
            position.cushion_angle = 25          # Comfortable angle
            position.backrest_angle = 60         # Reclined for comfort
            position.leg_rest_height = 30        # Partially raised
            position.feet_rest_height = 20       # Slightly raised
            position.headrest_height = 55        # Comfortable position
            position.guest_welcome_mode = True   # Welcome mode for passengers
        
        # Set view page to open
        instance._view_page_open = True
        
        return instance
    def _get_target_positions(self, position):
        """
        Determine which seat positions to target based on the position parameter.

        Args:
            position (list): List of seat positions to target, or ["all"] for all seats

        Returns:
            list: List of seat positions to adjust
        """
        if position is None:
            # Default to the current speaker's position
            speaker = Environment.get_current_speaker()
            return [speaker] if speaker in self._seats else ["driver's seat"]

        if "all" in position:
            return list(self._seats.keys())

        return [pos for pos in position if pos in self._seats]

    def _convert_degree_to_level(self, degree):
        """
        Convert a textual degree to a numeric level.

        Args:
            degree (str): The degree string ("min", "low", "medium", "high", "max",
                         or "tiny", "little", "large")

        Returns:
            int: The corresponding level (1-5) or adjustment value
        """
        if degree in ["min", "low", "medium", "high", "max"]:
            degree_map = {"min": 1, "low": 2, "medium": 3, "high": 4, "max": 5}
            return degree_map.get(degree, 3)  # Default to medium if not recognized
        elif degree in ["tiny", "little", "large"]:
            adjustment_map = {"tiny": 1, "little": 2, "large": 3}
            return adjustment_map.get(degree, 2)  # Default to little if not recognized
        return None

    def _adjust_value_by_degree(self, current_value, degree, min_val=0, max_val=100):
        """
        Adjust a current value by a degree of change.

        Args:
            current_value (float/int): The current value
            degree (str): The degree of adjustment ("tiny", "little", "large")
            min_val (float/int): Minimum allowable value
            max_val (float/int): Maximum allowable value

        Returns:
            float/int: The adjusted value
        """
        adjustment = self._convert_degree_to_level(degree)
        if adjustment:
            step = (max_val - min_val) / 10  # Divide range into 10 steps
            change = step * adjustment
            return max(min_val, min(max_val, current_value + change))
        return current_value

    def _adjust_value_by_inverse_degree(
        self, current_value, degree, min_val=0, max_val=100
    ):
        """
        Adjust a current value by a degree of change in the negative direction.

        Args:
            current_value (float/int): The current value
            degree (str): The degree of adjustment ("tiny", "little", "large")
            min_val (float/int): Minimum allowable value
            max_val (float/int): Maximum allowable value

        Returns:
            float/int: The adjusted value
        """
        adjustment = self._convert_degree_to_level(degree)
        if adjustment:
            step = (max_val - min_val) / 10  # Divide range into 10 steps
            change = step * adjustment
            return max(min_val, min(max_val, current_value - change))
        return current_value

    def get_module_status(self):
        print(self.to_dict())

    def to_dict(self):
        """Convert the entire Seat object to a dictionary."""
        result = {}
        for position, systems in self._seats.items():
            result[position] = {
                "heater": systems["heater"].to_dict(),
                "massager": systems["massager"].to_dict(),
                "position": systems["position"].to_dict(),
                "ventilation": systems["ventilation"].to_dict(),
            }

        result["view_page_open"] = {
            "value": self._view_page_open,
            "description": "Whether the seat control view page is open",
            "type": type(self._view_page_open).__name__,
        }

        return result

    @classmethod
    def from_dict(cls, data):
        """Restore a Seat object from a dictionary."""
        instance = cls()

        # Handle view page state if it exists in the data
        if "view_page_open" in data:
            instance._view_page_open = data["view_page_open"]["value"]

        # Process each seat position
        for position, systems in data.items():
            if position in instance._seats:
                instance._seats[position]["heater"] = Seat.HeaterSystem.from_dict(
                    systems["heater"]
                )
                instance._seats[position]["massager"] = Seat.MassageSystem.from_dict(
                    systems["massager"]
                )
                instance._seats[position]["position"] = Seat.PositionSystem.from_dict(
                    systems["position"]
                )
                instance._seats[position]["ventilation"] = (
                    Seat.VentilationSystem.from_dict(systems["ventilation"])
                )

        return instance

    # API Methods Implementation

    @api("seat")
    def carcontrol_carSeat_heater_switch(self, switch, position=None):
        """
        Turn on or off the car seat heating function.

        Args:
            switch (bool): True to turn heating on, False to turn it off
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            self._seats[pos]["heater"].is_on = switch
            results[pos] = {"heater_state": self._seats[pos]["heater"].is_on}

        return {
            "success": True,
            "action": "heater_switch_" + ("on" if switch else "off"),
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_heater_increase(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Increase car seat heating temperature.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "celsius"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            heater = self._seats[pos]["heater"]

            # Turn on heater if it's off
            if not heater.is_on:
                heater.is_on = True

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming gears are 1-5
                    heater.temperature_level = min(
                        5, heater.temperature_level + int(value)
                    )
                elif unit == "percentage":
                    # Adjust percentage and convert to level
                    current_pct = (
                        heater.temperature_level - 1
                    ) * 25  # Convert level to percentage (0-100)
                    new_pct = min(100, current_pct + value)
                    heater.temperature_level = min(5, max(1, int(new_pct / 25) + 1))
                elif unit == "celsius":
                    heater.temperature_value = heater.temperature_value + value
                    heater.temperature_unit = "celsius"
            elif degree is not None:
                # Handle degree-based adjustments
                adjustment = self._convert_degree_to_level(degree)
                if adjustment:
                    heater.temperature_level = min(
                        5, heater.temperature_level + adjustment
                    )
            else:
                # Default increase by 1 level if no specifics provided
                heater.temperature_level = min(5, heater.temperature_level + 1)

            results[pos] = {
                "heater_state": heater.is_on,
                "temperature_level": heater.temperature_level,
                "temperature_value": heater.temperature_value,
                "temperature_unit": heater.temperature_unit,
            }

        return {
            "success": True,
            "action": "heater_temperature_increased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_heater_decrease(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Decrease car seat heating temperature.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "celsius"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            heater = self._seats[pos]["heater"]

            # Skip if heater is already off
            if not heater.is_on:
                results[pos] = {"status": "heater already off"}
                continue

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming gears are 1-5
                    heater.temperature_level = max(
                        1, heater.temperature_level - int(value)
                    )
                    # Turn off if reduced to minimum
                    if heater.temperature_level == 1 and value >= 1:
                        heater.is_on = False
                elif unit == "percentage":
                    # Adjust percentage and convert to level
                    current_pct = (
                        heater.temperature_level - 1
                    ) * 25  # Convert level to percentage (0-100)
                    new_pct = max(0, current_pct - value)
                    heater.temperature_level = max(1, int(new_pct / 25) + 1)
                    # Turn off if reduced to 0%
                    if new_pct == 0:
                        heater.is_on = False
                elif unit == "celsius":
                    heater.temperature_value = max(0, heater.temperature_value - value)
                    heater.temperature_unit = "celsius"
            elif degree is not None:
                # Handle degree-based adjustments
                adjustment = self._convert_degree_to_level(degree)
                if adjustment:
                    heater.temperature_level = max(
                        1, heater.temperature_level - adjustment
                    )
                    # Turn off if reduced to minimum with large adjustment
                    if heater.temperature_level == 1 and degree == "large":
                        heater.is_on = False
            else:
                # Default decrease by 1 level if no specifics provided
                heater.temperature_level = max(1, heater.temperature_level - 1)
                # Turn off if reduced to minimum
                if heater.temperature_level == 1:
                    heater.is_on = False

            results[pos] = {
                "heater_state": heater.is_on,
                "temperature_level": heater.temperature_level,
                "temperature_value": heater.temperature_value,
                "temperature_unit": heater.temperature_unit,
            }

        return {
            "success": True,
            "action": "heater_temperature_decreased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_heater_set(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Set car seat heating temperature to a specified value.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value to set
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "celsius"]
            degree (str, optional): Predefined level if not using specific value
                                   Enum values: ["max", "high", "medium", "low", "min"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            heater = self._seats[pos]["heater"]

            # Turn on heater
            heater.is_on = True

            if value is not None and unit is not None:
                # Handle specific value settings
                if unit == "gear":
                    # Gears are typically 1-5
                    heater.temperature_level = max(1, min(5, int(value)))
                elif unit == "percentage":
                    # Convert percentage to level (1-5)
                    level = max(1, min(5, int(value / 25) + 1))
                    heater.temperature_level = level
                elif unit == "celsius":
                    heater.temperature_value = value
                    heater.temperature_unit = "celsius"
            elif degree is not None:
                # Handle predefined level settings
                level_map = {"min": 1, "low": 2, "medium": 3, "high": 4, "max": 5}
                heater.temperature_level = level_map.get(
                    degree, 3
                )  # Default to medium if not recognized

            results[pos] = {
                "heater_state": heater.is_on,
                "temperature_level": heater.temperature_level,
                "temperature_value": heater.temperature_value,
                "temperature_unit": heater.temperature_unit,
            }

        return {
            "success": True,
            "action": "heater_temperature_set",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_massager_switch(self, switch, position=None):
        """
        Turn on or off the car seat massage function.

        Args:
            switch (bool): True to turn massage on, False to turn it off
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            self._seats[pos]["massager"].is_on = switch
            results[pos] = {"massager_state": self._seats[pos]["massager"].is_on}

        return {
            "success": True,
            "action": "massager_switch_" + ("on" if switch else "off"),
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_massager_increase(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Increase car seat massage intensity.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            massager = self._seats[pos]["massager"]

            # Turn on massager if it's off
            if not massager.is_on:
                massager.is_on = True

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming gears are 1-5
                    massager.intensity_level = min(
                        5, massager.intensity_level + int(value)
                    )
                elif unit == "percentage":
                    # Adjust percentage and convert to level
                    current_pct = (
                        massager.intensity_level - 1
                    ) * 25  # Convert level to percentage (0-100)
                    new_pct = min(100, current_pct + value)
                    massager.intensity_level = min(5, max(1, int(new_pct / 25) + 1))
            elif degree is not None:
                # Handle degree-based adjustments
                adjustment = self._convert_degree_to_level(degree)
                if adjustment:
                    massager.intensity_level = min(
                        5, massager.intensity_level + adjustment
                    )
            else:
                # Default increase by 1 level if no specifics provided
                massager.intensity_level = min(5, massager.intensity_level + 1)

            results[pos] = {
                "massager_state": massager.is_on,
                "intensity_level": massager.intensity_level,
            }

        return {
            "success": True,
            "action": "massager_intensity_increased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_massager_decrease(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Decrease car seat massage intensity.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            massager = self._seats[pos]["massager"]

            # Skip if massager is already off
            if not massager.is_on:
                results[pos] = {"status": "massager already off"}
                continue

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming gears are 1-5
                    massager.intensity_level = max(
                        1, massager.intensity_level - int(value)
                    )
                    # Turn off if reduced to minimum
                    if massager.intensity_level == 1 and value >= 1:
                        massager.is_on = False
                elif unit == "percentage":
                    # Adjust percentage and convert to level
                    current_pct = (
                        massager.intensity_level - 1
                    ) * 25  # Convert level to percentage (0-100)
                    new_pct = max(0, current_pct - value)
                    massager.intensity_level = max(1, int(new_pct / 25) + 1)
                    # Turn off if reduced to 0%
                    if new_pct == 0:
                        massager.is_on = False
            elif degree is not None:
                # Handle degree-based adjustments
                adjustment = self._convert_degree_to_level(degree)
                if adjustment:
                    massager.intensity_level = max(
                        1, massager.intensity_level - adjustment
                    )
                    # Turn off if reduced to minimum with large adjustment
                    if massager.intensity_level == 1 and degree == "large":
                        massager.is_on = False
            else:
                # Default decrease by 1 level if no specifics provided
                massager.intensity_level = max(1, massager.intensity_level - 1)
                # Turn off if reduced to minimum
                if massager.intensity_level == 1:
                    massager.is_on = False

            results[pos] = {
                "massager_state": massager.is_on,
                "intensity_level": massager.intensity_level,
            }

        return {
            "success": True,
            "action": "massager_intensity_decreased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_massager_set(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Set car seat massage intensity to a specified value.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value to set
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage"]
            degree (str, optional): Predefined level if not using specific value
                                   Enum values: ["max", "high", "medium", "low", "min"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            massager = self._seats[pos]["massager"]

            # Turn on massager
            massager.is_on = True

            if value is not None and unit is not None:
                # Handle specific value settings
                if unit == "gear":
                    # Gears are typically 1-5
                    massager.intensity_level = max(1, min(5, int(value)))
                    massager.intensity_value = value
                    massager.intensity_unit = "gear"
                elif unit == "percentage":
                    # Convert percentage to level (1-5)
                    level = max(1, min(5, int(value / 25) + 1))
                    massager.intensity_level = level
                    massager.intensity_value = value
                    massager.intensity_unit = "percentage"
            elif degree is not None:
                # Handle predefined level settings
                level_map = {"min": 1, "low": 2, "medium": 3, "high": 4, "max": 5}
                massager.intensity_level = level_map.get(
                    degree, 3
                )  # Default to medium if not recognized

            results[pos] = {
                "massager_state": massager.is_on,
                "intensity_level": massager.intensity_level,
                "intensity_value": massager.intensity_value,
                "intensity_unit": massager.intensity_unit,
            }

        return {
            "success": True,
            "action": "massager_intensity_set",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_massager_mode(self, switch, mode, position=None):
        """
        Turn on or off a specific massage mode for the car seat massage function.

        Args:
            switch (bool): True to turn the mode on, False to turn it off
            mode (str): The massage mode to activate
                       Enum values: ["wave", "cat step", "stretch", "snake", "butterfly",
                                    "shoulder", "upper back", "waist", "full back", "random"]
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        valid_modes = [
            "wave",
            "cat step",
            "stretch",
            "snake",
            "butterfly",
            "shoulder",
            "upper back",
            "waist",
            "full back",
            "random",
        ]

        if mode not in valid_modes:
            return {
                "success": False,
                "error": f"Invalid massage mode: {mode}. Valid modes are: {', '.join(valid_modes)}",
            }

        for pos in targets:
            massager = self._seats[pos]["massager"]

            if switch:
                # Turn on the massager and set the mode
                massager.is_on = True
                massager.active_mode = mode
            else:
                # If turning off the specified mode
                if massager.active_mode == mode:
                    massager.active_mode = None
                    # Turn off massage system if no mode is active
                    if massager.active_mode is None:
                        massager.is_on = False

            results[pos] = {
                "massager_state": massager.is_on,
                "active_mode": massager.active_mode,
            }

        return {
            "success": True,
            "action": f"massager_mode_{mode}_"
            + ("activated" if switch else "deactivated"),
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_switch(self, action, position=None):
        """
        Open (unfold) or close (fold) the car seat.

        Args:
            action (str): Action to perform on the seat
                         Enum values: ["open", "close", "pause"]
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        valid_actions = ["open", "close", "pause"]

        if action not in valid_actions:
            return {
                "success": False,
                "error": f"Invalid seat action: {action}. Valid actions are: {', '.join(valid_actions)}",
            }

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if action == "open":
                position_system.is_folded = False
            elif action == "close":
                position_system.is_folded = True
            # For "pause", we don't change the folding state

            results[pos] = {"is_folded": position_system.is_folded}

        return {
            "success": True,
            "action": f"seat_{action}",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_horizontal_forward(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Move the car seat horizontal position forward.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.horizontal_position = max(
                        0, position_system.horizontal_position - adjustment
                    )
                elif unit == "percentage":
                    position_system.horizontal_position = max(
                        0, position_system.horizontal_position - value
                    )
                elif unit == "centimeter":
                    # Assuming 100% = 50cm, so 1cm = 2%
                    adjustment = value * 2
                    position_system.horizontal_position = max(
                        0, position_system.horizontal_position - adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (moving forward means decreasing the value)
                position_system.horizontal_position = (
                    self._adjust_value_by_inverse_degree(
                        position_system.horizontal_position, degree, 0, 100
                    )
                )
            else:
                # Default forward movement by 10%
                position_system.horizontal_position = max(
                    0, position_system.horizontal_position - 10
                )

            results[pos] = {"horizontal_position": position_system.horizontal_position}

        return {
            "success": True,
            "action": "seat_moved_forward",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_horizontal_backward(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Move the car seat horizontal position backward.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.horizontal_position = min(
                        100, position_system.horizontal_position + adjustment
                    )
                elif unit == "percentage":
                    position_system.horizontal_position = min(
                        100, position_system.horizontal_position + value
                    )
                elif unit == "centimeter":
                    # Assuming 100% = 50cm, so 1cm = 2%
                    adjustment = value * 2
                    position_system.horizontal_position = min(
                        100, position_system.horizontal_position + adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (moving backward means increasing the value)
                position_system.horizontal_position = self._adjust_value_by_degree(
                    position_system.horizontal_position, degree, 0, 100
                )
            else:
                # Default backward movement by 10%
                position_system.horizontal_position = min(
                    100, position_system.horizontal_position + 10
                )

            results[pos] = {"horizontal_position": position_system.horizontal_position}

        return {
            "success": True,
            "action": "seat_moved_backward",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_horizontal_set(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Set the car seat horizontal position to a specified value.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value to set
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Predefined position if not using specific value
                                   Enum values: ["max", "high", "medium", "low", "min"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value settings
                if unit == "gear":
                    # Convert gear (1-5) to percentage (0-100)
                    gear = max(1, min(5, int(value)))
                    position_system.horizontal_position = (gear - 1) * 25
                elif unit == "percentage":
                    position_system.horizontal_position = max(0, min(100, value))
                elif unit == "centimeter":
                    # Assuming 100% = 50cm, so 1cm = 2%
                    position_system.horizontal_position = max(0, min(100, value * 2))
            elif degree is not None:
                # Handle predefined position settings
                position_map = {
                    "min": 0,
                    "low": 25,
                    "medium": 50,
                    "high": 75,
                    "max": 100,
                }
                position_system.horizontal_position = position_map.get(
                    degree, 50
                )  # Default to medium if not recognized

            results[pos] = {"horizontal_position": position_system.horizontal_position}

        return {
            "success": True,
            "action": "seat_horizontal_position_set",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_height_increase(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Increase the car seat height.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.vertical_position = min(
                        100, position_system.vertical_position + adjustment
                    )
                elif unit == "percentage":
                    position_system.vertical_position = min(
                        100, position_system.vertical_position + value
                    )
                elif unit == "centimeter":
                    # Assuming 100% = 30cm, so 1cm = 3.33%
                    adjustment = value * 3.33
                    position_system.vertical_position = min(
                        100, position_system.vertical_position + adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (increasing height means increasing the value)
                position_system.vertical_position = self._adjust_value_by_degree(
                    position_system.vertical_position, degree, 0, 100
                )
            else:
                # Default height increase by 10%
                position_system.vertical_position = min(
                    100, position_system.vertical_position + 10
                )

            results[pos] = {"vertical_position": position_system.vertical_position}

        return {
            "success": True,
            "action": "seat_height_increased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_height_decrease(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Decrease the car seat height.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.vertical_position = max(
                        0, position_system.vertical_position - adjustment
                    )
                elif unit == "percentage":
                    position_system.vertical_position = max(
                        0, position_system.vertical_position - value
                    )
                elif unit == "centimeter":
                    # Assuming 100% = 30cm, so 1cm = 3.33%
                    adjustment = value * 3.33
                    position_system.vertical_position = max(
                        0, position_system.vertical_position - adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (decreasing height means decreasing the value)
                position_system.vertical_position = (
                    self._adjust_value_by_inverse_degree(
                        position_system.vertical_position, degree, 0, 100
                    )
                )
            else:
                # Default height decrease by 10%
                position_system.vertical_position = max(
                    0, position_system.vertical_position - 10
                )

            results[pos] = {"vertical_position": position_system.vertical_position}

        return {
            "success": True,
            "action": "seat_height_decreased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_height_set(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Set the car seat height to a specified value.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value to set
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Predefined height if not using specific value
                                   Enum values: ["max", "high", "medium", "low", "min"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value settings
                if unit == "gear":
                    # Convert gear (1-5) to percentage (0-100)
                    gear = max(1, min(5, int(value)))
                    position_system.vertical_position = (gear - 1) * 25
                elif unit == "percentage":
                    position_system.vertical_position = max(0, min(100, value))
                elif unit == "centimeter":
                    # Assuming 100% = 30cm, so 1cm = 3.33%
                    position_system.vertical_position = max(0, min(100, value * 3.33))
            elif degree is not None:
                # Handle predefined height settings
                height_map = {"min": 0, "low": 25, "medium": 50, "high": 75, "max": 100}
                position_system.vertical_position = height_map.get(
                    degree, 50
                )  # Default to medium if not recognized

            results[pos] = {"vertical_position": position_system.vertical_position}

        return {
            "success": True,
            "action": "seat_height_set",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatCushion_length_increase(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Increase the car seat cushion length.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.cushion_length = min(
                        100, position_system.cushion_length + adjustment
                    )
                elif unit == "percentage":
                    position_system.cushion_length = min(
                        100, position_system.cushion_length + value
                    )
                elif unit == "centimeter":
                    # Assuming 100% = 25cm, so 1cm = 4%
                    adjustment = value * 4
                    position_system.cushion_length = min(
                        100, position_system.cushion_length + adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (increasing length means increasing the value)
                position_system.cushion_length = self._adjust_value_by_degree(
                    position_system.cushion_length, degree, 0, 100
                )
            else:
                # Default length increase by 10%
                position_system.cushion_length = min(
                    100, position_system.cushion_length + 10
                )

            results[pos] = {"cushion_length": position_system.cushion_length}

        return {
            "success": True,
            "action": "seat_cushion_length_increased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatCushion_length_decrease(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Decrease the car seat cushion length.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.cushion_length = max(
                        0, position_system.cushion_length - adjustment
                    )
                elif unit == "percentage":
                    position_system.cushion_length = max(
                        0, position_system.cushion_length - value
                    )
                elif unit == "centimeter":
                    # Assuming 100% = 25cm, so 1cm = 4%
                    adjustment = value * 4
                    position_system.cushion_length = max(
                        0, position_system.cushion_length - adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (decreasing length means decreasing the value)
                position_system.cushion_length = self._adjust_value_by_inverse_degree(
                    position_system.cushion_length, degree, 0, 100
                )
            else:
                # Default length decrease by 10%
                position_system.cushion_length = max(
                    0, position_system.cushion_length - 10
                )

            results[pos] = {"cushion_length": position_system.cushion_length}

        return {
            "success": True,
            "action": "seat_cushion_length_decreased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatCushion_length_set(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Set the car seat cushion length to a specified value.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value to set
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Predefined length if not using specific value
                                   Enum values: ["max", "high", "medium", "low", "min"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value settings
                if unit == "gear":
                    # Convert gear (1-5) to percentage (0-100)
                    gear = max(1, min(5, int(value)))
                    position_system.cushion_length = (gear - 1) * 25
                elif unit == "percentage":
                    position_system.cushion_length = max(0, min(100, value))
                elif unit == "centimeter":
                    # Assuming 100% = 25cm, so 1cm = 4%
                    position_system.cushion_length = max(0, min(100, value * 4))
            elif degree is not None:
                # Handle predefined length settings
                length_map = {"min": 0, "low": 25, "medium": 50, "high": 75, "max": 100}
                position_system.cushion_length = length_map.get(
                    degree, 50
                )  # Default to medium if not recognized

            results[pos] = {"cushion_length": position_system.cushion_length}

        return {
            "success": True,
            "action": "seat_cushion_length_set",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatCushion_angle_increase(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Increase the car seat cushion inclination angle.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "degree"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.cushion_angle = min(
                        100, position_system.cushion_angle + adjustment
                    )
                elif unit == "percentage":
                    position_system.cushion_angle = min(
                        100, position_system.cushion_angle + value
                    )
                elif unit == "degree":
                    # Assuming 100% = 45°, so 1° = 2.22%
                    adjustment = value * 2.22
                    position_system.cushion_angle = min(
                        100, position_system.cushion_angle + adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (increasing angle means increasing the value)
                position_system.cushion_angle = self._adjust_value_by_degree(
                    position_system.cushion_angle, degree, 0, 100
                )
            else:
                # Default angle increase by 10%
                position_system.cushion_angle = min(
                    100, position_system.cushion_angle + 10
                )

            results[pos] = {"cushion_angle": position_system.cushion_angle}

        return {
            "success": True,
            "action": "seat_cushion_angle_increased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatCushion_angle_decrease(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Decrease the car seat cushion inclination angle.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "degree"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.cushion_angle = max(
                        0, position_system.cushion_angle - adjustment
                    )
                elif unit == "percentage":
                    position_system.cushion_angle = max(
                        0, position_system.cushion_angle - value
                    )
                elif unit == "degree":
                    # Assuming 100% = 45°, so 1° = 2.22%
                    adjustment = value * 2.22
                    position_system.cushion_angle = max(
                        0, position_system.cushion_angle - adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (decreasing angle means decreasing the value)
                position_system.cushion_angle = self._adjust_value_by_inverse_degree(
                    position_system.cushion_angle, degree, 0, 100
                )
            else:
                # Default angle decrease by 10%
                position_system.cushion_angle = max(
                    0, position_system.cushion_angle - 10
                )

            results[pos] = {"cushion_angle": position_system.cushion_angle}

        return {
            "success": True,
            "action": "seat_cushion_angle_decreased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatCushion_angle_set(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Set the car seat cushion inclination angle to a specified value.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value to set
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "degree"]
            degree (str, optional): Predefined angle if not using specific value
                                   Enum values: ["max", "high", "medium", "low", "min"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value settings
                if unit == "gear":
                    # Convert gear (1-5) to percentage (0-100)
                    gear = max(1, min(5, int(value)))
                    position_system.cushion_angle = (gear - 1) * 25
                elif unit == "percentage":
                    position_system.cushion_angle = max(0, min(100, value))
                elif unit == "degree":
                    # Assuming 100% = 45°, so 1° = 2.22%
                    position_system.cushion_angle = max(0, min(100, value * 2.22))
            elif degree is not None:
                # Handle predefined angle settings
                angle_map = {"min": 0, "low": 25, "medium": 50, "high": 75, "max": 100}
                position_system.cushion_angle = angle_map.get(
                    degree, 50
                )  # Default to medium if not recognized

            results[pos] = {"cushion_angle": position_system.cushion_angle}

        return {
            "success": True,
            "action": "seat_cushion_angle_set",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatBackrest_angle_increase(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Increase the car seat backrest inclination angle.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "degree"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.backrest_angle = min(
                        100, position_system.backrest_angle + adjustment
                    )
                elif unit == "percentage":
                    position_system.backrest_angle = min(
                        100, position_system.backrest_angle + value
                    )
                elif unit == "degree":
                    # Assuming 100% = 90°, so 1° = 1.11%
                    adjustment = value * 1.11
                    position_system.backrest_angle = min(
                        100, position_system.backrest_angle + adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (increasing angle means increasing the value)
                position_system.backrest_angle = self._adjust_value_by_degree(
                    position_system.backrest_angle, degree, 0, 100
                )
            else:
                # Default angle increase by 10%
                position_system.backrest_angle = min(
                    100, position_system.backrest_angle + 10
                )

            results[pos] = {"backrest_angle": position_system.backrest_angle}

        return {
            "success": True,
            "action": "seat_backrest_angle_increased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatBackrest_angle_decrease(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Decrease the car seat backrest inclination angle.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "degree"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.backrest_angle = max(
                        0, position_system.backrest_angle - adjustment
                    )
                elif unit == "percentage":
                    position_system.backrest_angle = max(
                        0, position_system.backrest_angle - value
                    )
                elif unit == "degree":
                    # Assuming 100% = 90°, so 1° = 1.11%
                    adjustment = value * 1.11
                    position_system.backrest_angle = max(
                        0, position_system.backrest_angle - adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (decreasing angle means decreasing the value)
                position_system.backrest_angle = self._adjust_value_by_inverse_degree(
                    position_system.backrest_angle, degree, 0, 100
                )
            else:
                # Default angle decrease by 10%
                position_system.backrest_angle = max(
                    0, position_system.backrest_angle - 10
                )

            results[pos] = {"backrest_angle": position_system.backrest_angle}

        return {
            "success": True,
            "action": "seat_backrest_angle_decreased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatBackrest_angle_set(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Set the car seat backrest inclination angle to a specified value.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value to set
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "degree"]
            degree (str, optional): Predefined angle if not using specific value
                                   Enum values: ["max", "high", "medium", "low", "min"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value settings
                if unit == "gear":
                    # Convert gear (1-5) to percentage (0-100)
                    gear = max(1, min(5, int(value)))
                    position_system.backrest_angle = (gear - 1) * 25
                elif unit == "percentage":
                    position_system.backrest_angle = max(0, min(100, value))
                elif unit == "degree":
                    # Assuming 100% = 90°, so 1° = 1.11%
                    position_system.backrest_angle = max(0, min(100, value * 1.11))
            elif degree is not None:
                # Handle predefined angle settings
                angle_map = {"min": 0, "low": 25, "medium": 50, "high": 75, "max": 100}
                position_system.backrest_angle = angle_map.get(
                    degree, 50
                )  # Default to medium if not recognized

            results[pos] = {"backrest_angle": position_system.backrest_angle}

        return {
            "success": True,
            "action": "seat_backrest_angle_set",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatLegRest_height_increase(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Increase the car seat leg rest height.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.leg_rest_height = min(
                        100, position_system.leg_rest_height + adjustment
                    )
                elif unit == "percentage":
                    position_system.leg_rest_height = min(
                        100, position_system.leg_rest_height + value
                    )
                elif unit == "centimeter":
                    # Assuming 100% = 30cm, so 1cm = 3.33%
                    adjustment = value * 3.33
                    position_system.leg_rest_height = min(
                        100, position_system.leg_rest_height + adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (increasing height means increasing the value)
                position_system.leg_rest_height = self._adjust_value_by_degree(
                    position_system.leg_rest_height, degree, 0, 100
                )
            else:
                # Default height increase by 10%
                position_system.leg_rest_height = min(
                    100, position_system.leg_rest_height + 10
                )

            results[pos] = {"leg_rest_height": position_system.leg_rest_height}

        return {
            "success": True,
            "action": "seat_leg_rest_height_increased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatLegRest_height_decrease(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Decrease the car seat leg rest height.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.leg_rest_height = max(
                        0, position_system.leg_rest_height - adjustment
                    )
                elif unit == "percentage":
                    position_system.leg_rest_height = max(
                        0, position_system.leg_rest_height - value
                    )
                elif unit == "centimeter":
                    # Assuming 100% = 30cm, so 1cm = 3.33%
                    adjustment = value * 3.33
                    position_system.leg_rest_height = max(
                        0, position_system.leg_rest_height - adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (decreasing height means decreasing the value)
                position_system.leg_rest_height = self._adjust_value_by_inverse_degree(
                    position_system.leg_rest_height, degree, 0, 100
                )
            else:
                # Default height decrease by 10%
                position_system.leg_rest_height = max(
                    0, position_system.leg_rest_height - 10
                )

            results[pos] = {"leg_rest_height": position_system.leg_rest_height}

        return {
            "success": True,
            "action": "seat_leg_rest_height_decreased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatLegRest_height_set(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Set the car seat leg rest height to a specified value.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value to set
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Predefined height if not using specific value
                                   Enum values: ["max", "high", "medium", "low", "min"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value settings
                if unit == "gear":
                    # Convert gear (1-5) to percentage (0-100)
                    gear = max(1, min(5, int(value)))
                    position_system.leg_rest_height = (gear - 1) * 25
                elif unit == "percentage":
                    position_system.leg_rest_height = max(0, min(100, value))
                elif unit == "centimeter":
                    # Assuming 100% = 30cm, so 1cm = 3.33%
                    position_system.leg_rest_height = max(0, min(100, value * 3.33))
            elif degree is not None:
                # Handle predefined height settings
                height_map = {"min": 0, "low": 25, "medium": 50, "high": 75, "max": 100}
                position_system.leg_rest_height = height_map.get(
                    degree, 50
                )  # Default to medium if not recognized

            results[pos] = {"leg_rest_height": position_system.leg_rest_height}

        return {
            "success": True,
            "action": "seat_leg_rest_height_set",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatFeetRest_height_increase(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Increase the car seat feet rest height.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.feet_rest_height = min(
                        100, position_system.feet_rest_height + adjustment
                    )
                elif unit == "percentage":
                    position_system.feet_rest_height = min(
                        100, position_system.feet_rest_height + value
                    )
                elif unit == "centimeter":
                    # Assuming 100% = 20cm, so 1cm = 5%
                    adjustment = value * 5
                    position_system.feet_rest_height = min(
                        100, position_system.feet_rest_height + adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (increasing height means increasing the value)
                position_system.feet_rest_height = self._adjust_value_by_degree(
                    position_system.feet_rest_height, degree, 0, 100
                )
            else:
                # Default height increase by 10%
                position_system.feet_rest_height = min(
                    100, position_system.feet_rest_height + 10
                )

            results[pos] = {"feet_rest_height": position_system.feet_rest_height}

        return {
            "success": True,
            "action": "seat_feet_rest_height_increased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatFeetRest_height_decrease(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Decrease the car seat feet rest height.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.feet_rest_height = max(
                        0, position_system.feet_rest_height - adjustment
                    )
                elif unit == "percentage":
                    position_system.feet_rest_height = max(
                        0, position_system.feet_rest_height - value
                    )
                elif unit == "centimeter":
                    # Assuming 100% = 20cm, so 1cm = 5%
                    adjustment = value * 5
                    position_system.feet_rest_height = max(
                        0, position_system.feet_rest_height - adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (decreasing height means decreasing the value)
                position_system.feet_rest_height = self._adjust_value_by_inverse_degree(
                    position_system.feet_rest_height, degree, 0, 100
                )
            else:
                # Default height decrease by 10%
                position_system.feet_rest_height = max(
                    0, position_system.feet_rest_height - 10
                )

            results[pos] = {"feet_rest_height": position_system.feet_rest_height}

        return {
            "success": True,
            "action": "seat_feet_rest_height_decreased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatFeetRest_height_set(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Set the car seat feet rest height to a specified value.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value to set
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Predefined height if not using specific value
                                   Enum values: ["max", "high", "medium", "low", "min"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value settings
                if unit == "gear":
                    # Convert gear (1-5) to percentage (0-100)
                    gear = max(1, min(5, int(value)))
                    position_system.feet_rest_height = (gear - 1) * 25
                elif unit == "percentage":
                    position_system.feet_rest_height = max(0, min(100, value))
                elif unit == "centimeter":
                    # Assuming 100% = 20cm, so 1cm = 5%
                    position_system.feet_rest_height = max(0, min(100, value * 5))
            elif degree is not None:
                # Handle predefined height settings
                height_map = {"min": 0, "low": 25, "medium": 50, "high": 75, "max": 100}
                position_system.feet_rest_height = height_map.get(
                    degree, 50
                )  # Default to medium if not recognized

            results[pos] = {"feet_rest_height": position_system.feet_rest_height}

        return {
            "success": True,
            "action": "seat_feet_rest_height_set",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatHeadRest_height_increase(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Increase the car seat headrest height.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.headrest_height = min(
                        100, position_system.headrest_height + adjustment
                    )
                elif unit == "percentage":
                    position_system.headrest_height = min(
                        100, position_system.headrest_height + value
                    )
                elif unit == "centimeter":
                    # Assuming 100% = 15cm, so 1cm = 6.67%
                    adjustment = value * 6.67
                    position_system.headrest_height = min(
                        100, position_system.headrest_height + adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (increasing height means increasing the value)
                position_system.headrest_height = self._adjust_value_by_degree(
                    position_system.headrest_height, degree, 0, 100
                )
            else:
                # Default height increase by 10%
                position_system.headrest_height = min(
                    100, position_system.headrest_height + 10
                )

            results[pos] = {"headrest_height": position_system.headrest_height}

        return {
            "success": True,
            "action": "seat_headrest_height_increased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatHeadRest_height_decrease(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Decrease the car seat headrest height.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming each gear is 20% of total range
                    adjustment = int(value) * 20
                    position_system.headrest_height = max(
                        0, position_system.headrest_height - adjustment
                    )
                elif unit == "percentage":
                    position_system.headrest_height = max(
                        0, position_system.headrest_height - value
                    )
                elif unit == "centimeter":
                    # Assuming 100% = 15cm, so 1cm = 6.67%
                    adjustment = value * 6.67
                    position_system.headrest_height = max(
                        0, position_system.headrest_height - adjustment
                    )
            elif degree is not None:
                # Handle degree-based adjustments (decreasing height means decreasing the value)
                position_system.headrest_height = self._adjust_value_by_inverse_degree(
                    position_system.headrest_height, degree, 0, 100
                )
            else:
                # Default height decrease by 10%
                position_system.headrest_height = max(
                    0, position_system.headrest_height - 10
                )

            results[pos] = {"headrest_height": position_system.headrest_height}

        return {
            "success": True,
            "action": "seat_headrest_height_decreased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeatHeadRest_height_set(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Set the car seat headrest height to a specified value.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value to set
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage", "centimeter"]
            degree (str, optional): Predefined height if not using specific value
                                   Enum values: ["max", "high", "medium", "low", "min"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]

            if value is not None and unit is not None:
                # Handle specific value settings
                if unit == "gear":
                    # Convert gear (1-5) to percentage (0-100)
                    gear = max(1, min(5, int(value)))
                    position_system.headrest_height = (gear - 1) * 25
                elif unit == "percentage":
                    position_system.headrest_height = max(0, min(100, value))
                elif unit == "centimeter":
                    # Assuming 100% = 15cm, so 1cm = 6.67%
                    position_system.headrest_height = max(0, min(100, value * 6.67))
            elif degree is not None:
                # Handle predefined height settings
                height_map = {"min": 0, "low": 25, "medium": 50, "high": 75, "max": 100}
                position_system.headrest_height = height_map.get(
                    degree, 50
                )  # Default to medium if not recognized

            results[pos] = {"headrest_height": position_system.headrest_height}

        return {
            "success": True,
            "action": "seat_headrest_height_set",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_greetGuestMode(self, switch, position=None):
        """
        Turn on or off the car seat guest welcome mode.

        Args:
            switch (bool): True to turn welcome mode on, False to turn it off
            position (list, optional): List of seat positions to adjust, defaults to all positions
                                      Enum values: ["driver's seat", "passenger seat", "second row left",
                                                    "second row right", "third row left", "third row right", "all"]

        Returns:
            dict: Operation result and updated states
        """
        # For guest welcome mode, default to all positions if none specified
        if position is None:
            position = ["all"]

        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            position_system = self._seats[pos]["position"]
            position_system.guest_welcome_mode = switch

            results[pos] = {"guest_welcome_mode": position_system.guest_welcome_mode}

        return {
            "success": True,
            "action": "seat_guest_welcome_mode_"
            + ("activated" if switch else "deactivated"),
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_ventilation_switch(self, switch, position=None):
        """
        Turn on or off the car seat ventilation function.

        Args:
            switch (bool): True to turn ventilation on, False to turn it off
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            self._seats[pos]["ventilation"].is_on = switch
            results[pos] = {"ventilation_state": self._seats[pos]["ventilation"].is_on}

        return {
            "success": True,
            "action": "ventilation_switch_" + ("on" if switch else "off"),
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_ventilation_increase(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Increase the car seat ventilation airflow.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            ventilation = self._seats[pos]["ventilation"]

            # Turn on ventilation if it's off
            if not ventilation.is_on:
                ventilation.is_on = True

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming gears are 1-5
                    ventilation.airflow_level = min(
                        5, ventilation.airflow_level + int(value)
                    )
                    ventilation.airflow_value = value
                    ventilation.airflow_unit = "gear"
                elif unit == "percentage":
                    # Adjust percentage and convert to level
                    current_pct = (
                        ventilation.airflow_level - 1
                    ) * 25  # Convert level to percentage (0-100)
                    new_pct = min(100, current_pct + value)
                    ventilation.airflow_level = min(5, max(1, int(new_pct / 25) + 1))
                    ventilation.airflow_value = value
                    ventilation.airflow_unit = "percentage"
            elif degree is not None:
                # Handle degree-based adjustments
                adjustment = self._convert_degree_to_level(degree)
                if adjustment:
                    ventilation.airflow_level = min(
                        5, ventilation.airflow_level + adjustment
                    )
            else:
                # Default increase by 1 level if no specifics provided
                ventilation.airflow_level = min(5, ventilation.airflow_level + 1)

            results[pos] = {
                "ventilation_state": ventilation.is_on,
                "airflow_level": ventilation.airflow_level,
            }

        return {
            "success": True,
            "action": "ventilation_airflow_increased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_ventilation_decrease(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Decrease the car seat ventilation airflow.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value for adjustment
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage"]
            degree (str, optional): Degree of adjustment if not using specific value
                                   Enum values: ["large", "little", "tiny"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            ventilation = self._seats[pos]["ventilation"]

            # Skip if ventilation is already off
            if not ventilation.is_on:
                results[pos] = {"status": "ventilation already off"}
                continue

            if value is not None and unit is not None:
                # Handle specific value adjustments
                if unit == "gear":
                    # Assuming gears are 1-5
                    ventilation.airflow_level = max(
                        1, ventilation.airflow_level - int(value)
                    )
                    ventilation.airflow_value = value
                    ventilation.airflow_unit = "gear"
                    # Turn off if reduced to minimum with substantial value
                    if ventilation.airflow_level == 1 and value >= 1:
                        ventilation.is_on = False
                elif unit == "percentage":
                    # Adjust percentage and convert to level
                    current_pct = (
                        ventilation.airflow_level - 1
                    ) * 25  # Convert level to percentage (0-100)
                    new_pct = max(0, current_pct - value)
                    ventilation.airflow_level = max(1, int(new_pct / 25) + 1)
                    ventilation.airflow_value = value
                    ventilation.airflow_unit = "percentage"
                    # Turn off if reduced to 0%
                    if new_pct == 0:
                        ventilation.is_on = False
            elif degree is not None:
                # Handle degree-based adjustments
                adjustment = self._convert_degree_to_level(degree)
                if adjustment:
                    ventilation.airflow_level = max(
                        1, ventilation.airflow_level - adjustment
                    )
                    # Turn off if reduced to minimum with large adjustment
                    if ventilation.airflow_level == 1 and degree == "large":
                        ventilation.is_on = False
            else:
                # Default decrease by 1 level if no specifics provided
                ventilation.airflow_level = max(1, ventilation.airflow_level - 1)
                # Turn off if reduced to minimum
                if ventilation.airflow_level == 1:
                    ventilation.is_on = False

            results[pos] = {
                "ventilation_state": ventilation.is_on,
                "airflow_level": ventilation.airflow_level,
            }

        return {
            "success": True,
            "action": "ventilation_airflow_decreased",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_ventilation_set(
        self, position=None, value=None, unit=None, degree=None
    ):
        """
        Set the car seat ventilation airflow to a specified value.

        Args:
            position (list): List of seat positions to adjust, defaults to current speaker position
                            Enum values: ["driver's seat", "passenger seat", "second row left",
                                          "second row right", "third row left", "third row right", "all"]
            value (float, optional): Specific numerical value to set
            unit (str, optional): Unit for the value
                                 Enum values: ["gear", "percentage"]
            degree (str, optional): Predefined level if not using specific value
                                   Enum values: ["max", "high", "medium", "low", "min"]

        Returns:
            dict: Operation result and updated states
        """
        targets = self._get_target_positions(position)
        results = {}

        for pos in targets:
            ventilation = self._seats[pos]["ventilation"]

            # Turn on ventilation (unless setting to minimum/0)
            ventilation.is_on = True

            if value is not None and unit is not None:
                # Handle specific value settings
                if unit == "gear":
                    # Gears are typically 1-5
                    level = max(1, min(5, int(value)))
                    ventilation.airflow_level = level
                    ventilation.airflow_value = value
                    ventilation.airflow_unit = "gear"
                    # Turn off if set to minimum
                    if level == 1 and value <= 1:
                        ventilation.is_on = False
                elif unit == "percentage":
                    # Convert percentage to level (1-5)
                    level = max(1, min(5, int(value / 25) + 1))
                    ventilation.airflow_level = level
                    ventilation.airflow_value = value
                    ventilation.airflow_unit = "percentage"
                    # Turn off if set to 0%
                    if value == 0:
                        ventilation.is_on = False
            elif degree is not None:
                # Handle predefined level settings
                level_map = {"min": 1, "low": 2, "medium": 3, "high": 4, "max": 5}
                ventilation.airflow_level = level_map.get(
                    degree, 3
                )  # Default to medium if not recognized
                # Turn off if set to minimum
                if degree == "min":
                    ventilation.is_on = False

            results[pos] = {
                "ventilation_state": ventilation.is_on,
                "airflow_level": ventilation.airflow_level,
            }

        return {
            "success": True,
            "action": "ventilation_airflow_set",
            "affected_positions": targets,
            "states": results,
        }

    @api("seat")
    def carcontrol_carSeat_view_switch(self, switch):
        """
        Open or close the car seat control page.

        Args:
            switch (bool): True to open the control page, False to close it

        Returns:
            dict: Operation result and updated state
        """
        self._view_page_open = switch

        return {
            "success": True,
            "action": "seat_control_page_" + ("opened" if switch else "closed"),
            "state": {"view_page_open": self._view_page_open},
        }
