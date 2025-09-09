from enum import Enum
from utils import api

class SteeringWheel:
    class HeaterDegree(Enum):
        """
        Enum class representing preset steering wheel heating levels.
        """
        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"
        
        @classmethod
        def get_all_values(cls):
            return [e.value for e in cls]
    
    class HeaterUnit(Enum):
        """
        Enum class representing the units of measurement for steering wheel heating levels.
        """
        CELSIUS = "celsius"
        LEVEL = "level"
        PERCENTAGE = "percentage"
        
        @classmethod
        def get_all_values(cls):
            return [e.value for e in cls]
    
    class IncreaseDegree(Enum):
        """
        Enum class representing the degree of increase/decrease for steering wheel heating.
        """
        LARGE = "large"
        LITTLE = "little"
        TINY = "tiny"
        
        @classmethod
        def get_all_values(cls):
            return [e.value for e in cls]

    def __init__(self):
        # View display status
        self._is_view_open = False
        
        # Heating function status
        self._is_heater_on = False
        
        # Heating level related properties
        self._heater_level = 0  # Range: 0-10, represents heating level
        self._heater_celsius = 20.0  # Temperature value, unit: Celsius
        self._heater_percentage = 0.0  # Percentage value, range: 0.0-100.0
        
        # Currently used unit
        self._current_unit = self.HeaterUnit.LEVEL
        
        # Level mapping relationship
        self._degree_to_level = {
            self.HeaterDegree.MIN: 0,
            self.HeaterDegree.LOW: 2,
            self.HeaterDegree.MEDIUM: 5,
            self.HeaterDegree.HIGH: 8,
            self.HeaterDegree.MAX: 10
        }
        
        # Conversion relationships between level, temperature, and percentage
        self._level_to_celsius = lambda level: 20.0 + level * 3.0  # 20°C - 50°C
        self._level_to_percentage = lambda level: level * 10.0  # 0% - 100%
        
        # Increment mapping
        self._increase_degree_map = {
            self.IncreaseDegree.TINY: 1,
            self.IncreaseDegree.LITTLE: 2,
            self.IncreaseDegree.LARGE: 3
        }

    # Getter and setter for view status
    @property
    def is_view_open(self):
        return self._is_view_open

    @is_view_open.setter
    def is_view_open(self, value):
        if not isinstance(value, bool):
            raise TypeError("is_view_open must be a boolean value")
        self._is_view_open = value

    # Getter and setter for heating status
    @property
    def is_heater_on(self):
        return self._is_heater_on

    @is_heater_on.setter
    def is_heater_on(self, value):
        if not isinstance(value, bool):
            raise TypeError("is_heater_on must be a boolean value")
        self._is_heater_on = value

    # Getter and setter for heating level
    @property
    def heater_level(self):
        return self._heater_level

    @heater_level.setter
    def heater_level(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("heater_level must be a numeric value")
        
        # Ensure value is within valid range
        self._heater_level = max(0, min(10, value))
        
        # Update values for other units
        self._update_unit_values()

    # Getter and setter for Celsius temperature
    @property
    def heater_celsius(self):
        return self._heater_celsius

    @heater_celsius.setter
    def heater_celsius(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("heater_celsius must be a numeric value")
        
        # Ensure value is within valid range: 20°C - 50°C
        self._heater_celsius = max(20.0, min(50.0, value))
        
        # # Update level
        level = (self._heater_celsius - 20.0) / 3.0
        self._heater_level = max(0, min(10, level))
        
        # Update percentage
        self._heater_percentage = self._level_to_percentage(self._heater_level)

    # Getter and setter for percentage
    @property
    def heater_percentage(self):
        return self._heater_percentage

    @heater_percentage.setter
    def heater_percentage(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("heater_percentage must be a numeric value")
        
        # Ensure value is within valid range: 0.0% - 100.0%
        self._heater_percentage = max(0.0, min(100.0, value))
        
        # Update level
        level = self._heater_percentage / 10.0
        self._heater_level = max(0, min(10, level))
        
        # Update temperature
        self._heater_celsius = self._level_to_celsius(self._heater_level)

    # Getter and setter for current unit
    @property
    def current_unit(self):
        return self._current_unit

    @current_unit.setter
    def current_unit(self, value):
        if not isinstance(value, self.HeaterUnit):
            raise TypeError("current_unit must be a HeaterUnit enum value")
        self._current_unit = value

    # Helper method: update other unit values based on current level
    def _update_unit_values(self):
        self._heater_celsius = self._level_to_celsius(self._heater_level)
        self._heater_percentage = self._level_to_percentage(self._heater_level)

    # Helper method: get value for current unit
    def _get_current_unit_value(self):
        if self._current_unit == self.HeaterUnit.CELSIUS:
            return self._heater_celsius
        elif self._current_unit == self.HeaterUnit.PERCENTAGE:
            return self._heater_percentage
        else:  # LEVEL
            return self._heater_level

    # Helper method: set value for current unit
    def _set_current_unit_value(self, value):
        if self._current_unit == self.HeaterUnit.CELSIUS:
            self.heater_celsius = value
        elif self._current_unit == self.HeaterUnit.PERCENTAGE:
            self.heater_percentage = value
        else:  # LEVEL
            self.heater_level = value

    # Helper method: convert string to enum type
    def _str_to_enum(self, enum_cls, value):
        if isinstance(value, str):
            try:
                return enum_cls(value)
            except ValueError:
                valid_values = enum_cls.get_all_values()
                raise ValueError(f"Invalid value: {value}. Valid values are: {valid_values}")
        return value

    # API implementation
    @api("steeringWheel")
    def carcontrol_steeringWheel_view_switch(self, switch):
        """
        Open or close the steering wheel page.
        
        Parameters:
            switch (bool): Steering wheel page switch, True to open, False to close
            
        Returns:
            dict: Contains operation result and current status
        """
        if not isinstance(switch, bool):
            raise TypeError("switch must be a boolean value")
        
        self.is_view_open = switch
        
        return {
            "success": True,
            "is_view_open": self.is_view_open
        }

    @api("steeringWheel")
    def carcontrol_steeringWheel_heater_switch(self, switch):
        """
        Turn on or off the steering wheel heating function.
        
        Parameters:
            switch (bool): Steering wheel heating switch, True to turn on, False to turn off
            
        Returns:
            dict: Contains operation result and current status
        """
        if not isinstance(switch, bool):
            raise TypeError("switch must be a boolean value")
        
        self.is_heater_on = switch
        
        return {
            "success": True,
            "is_heater_on": self.is_heater_on,
            "current_level": self.heater_level,
            "current_celsius": self.heater_celsius,
            "current_percentage": self.heater_percentage
        }

    @api("steeringWheel")
    def carcontrol_steeringWheel_heater_increase(self, value=None, unit=None, degree=None):
        """
        Increase the steering wheel heating level.
        
        Parameters:
            value (float, optional): Value to increase by, used with unit, mutually exclusive with degree
            unit (str, optional): Unit of the increase value, used with value, mutually exclusive with degree
                                 Enum values: ['celsius', 'level', 'percentage']
            degree (str, optional): Degree of increase, from 'tiny' (smallest) to 'large' (largest), 
                                   mutually exclusive with value and unit
                                   Enum values: ['large', 'little', 'tiny']
            
        Returns:
            dict: Contains operation result and current status
        """
        # Input validation
        if value is not None and degree is not None:
            raise ValueError("value and degree are mutually exclusive")
        
        if value is not None and unit is None:
            raise ValueError("unit must be provided when using value")
        
        # Ensure heating function is on
        if not self.is_heater_on:
            return {
                "success": False,
                "message": "Heater is not turned on",
                "is_heater_on": self.is_heater_on
            }
        
        # Increase temperature based on degree or value
        if degree is not None:
            # Convert string to enum type
            degree_enum = self._str_to_enum(self.IncreaseDegree, degree)
            
            # Get the amount to increase
            increase_amount = self._increase_degree_map.get(degree_enum, 1)
            self.heater_level = self.heater_level + increase_amount
        elif value is not None and unit is not None:
            # Convert string to enum type
            unit_enum = self._str_to_enum(self.HeaterUnit, unit)
            
            # Set current unit
            old_unit = self.current_unit
            self.current_unit = unit_enum
            
            # Get current value and increase
            current_value = self._get_current_unit_value()
            self._set_current_unit_value(current_value + value)
            
            # Restore original unit
            self.current_unit = old_unit
        else:
            # Default increase by one small unit
            self.heater_level = self.heater_level + 1
        
        return {
            "success": True,
            "is_heater_on": self.is_heater_on,
            "current_level": self.heater_level,
            "current_celsius": self.heater_celsius,
            "current_percentage": self.heater_percentage
        }

    @api("steeringWheel")
    def carcontrol_steeringWheel_heater_decrease(self, value=None, unit=None, degree=None):
        """
        Decrease the steering wheel heating level.
        
        Parameters:
            value (float, optional): Value to decrease by, used with unit, mutually exclusive with degree
            unit (str, optional): Unit of the decrease value, used with value, mutually exclusive with degree
                                 Enum values: ['celsius', 'level', 'percentage']
            degree (str, optional): Degree of decrease, from 'tiny' (smallest) to 'large' (largest),
                                   mutually exclusive with value and unit
                                   Enum values: ['large', 'little', 'tiny']
            
        Returns:
            dict: Contains operation result and current status
        """
        # Input validation
        if value is not None and degree is not None:
            raise ValueError("value and degree are mutually exclusive")
        
        if value is not None and unit is None:
            raise ValueError("unit must be provided when using value")
        
        # Ensure heating function is on
        if not self.is_heater_on:
            return {
                "success": False,
                "message": "Heater is not turned on",
                "is_heater_on": self.is_heater_on
            }
        
        # Decrease temperature based on degree or value
        if degree is not None:
            # Convert string to enum type
            degree_enum = self._str_to_enum(self.IncreaseDegree, degree)
            
            # Get the amount to decrease
            decrease_amount = self._increase_degree_map.get(degree_enum, 1)
            self.heater_level = self.heater_level - decrease_amount
        elif value is not None and unit is not None:
            # Convert string to enum type
            unit_enum = self._str_to_enum(self.HeaterUnit, unit)
            
            # Set current unit
            old_unit = self.current_unit
            self.current_unit = unit_enum
            
            # Get current value and decrease
            current_value = self._get_current_unit_value()
            self._set_current_unit_value(current_value - value)
            
            # Restore original unit
            self.current_unit = old_unit
        else:
            # Default decrease by one small unit
            self.heater_level = self.heater_level - 1
        
        return {
            "success": True,
            "is_heater_on": self.is_heater_on,
            "current_level": self.heater_level,
            "current_celsius": self.heater_celsius,
            "current_percentage": self.heater_percentage
        }

    @api("steeringWheel")
    def carcontrol_steeringWheel_heater_set(self, value=None, unit=None, degree=None):
        """
        Set the steering wheel heating level to a specific level.
        
        Parameters:
            value (float, optional): Value to set, used with unit, mutually exclusive with degree
            unit (str, optional): Unit of the set value, used with value, mutually exclusive with degree
                                 Enum values: ['celsius', 'level', 'percentage']
            degree (str, optional): Specific heating level, mutually exclusive with value and unit
                                   Enum values: ['max', 'high', 'medium', 'low', 'min']
            
        Returns:
            dict: Contains operation result and current status
        """
        # Input validation
        if value is not None and degree is not None:
            raise ValueError("value and degree are mutually exclusive")
        
        if value is not None and unit is None:
            raise ValueError("unit must be provided when using value")
        
        if value is None and unit is None and degree is None:
            raise ValueError("Either degree or (value with unit) must be provided")
        
        # Ensure heating function is on
        if not self.is_heater_on:
            return {
                "success": False,
                "message": "Heater is not turned on",
                "is_heater_on": self.is_heater_on
            }
        
        # Set temperature based on degree or value
        if degree is not None:
            # Convert string to enum type
            degree_enum = self._str_to_enum(self.HeaterDegree, degree)
            
            # Set corresponding level
            self.heater_level = self._degree_to_level.get(degree_enum, 5)  # Default to medium level
        elif value is not None and unit is not None:
            # Convert string to enum type
            unit_enum = self._str_to_enum(self.HeaterUnit, unit)
            
            # Set current unit
            old_unit = self.current_unit
            self.current_unit = unit_enum
            
            # Set new value
            self._set_current_unit_value(value)
            
            # Restore original unit
            self.current_unit = old_unit
        
        return {
            "success": True,
            "is_heater_on": self.is_heater_on,
            "current_level": self.heater_level,
            "current_celsius": self.heater_celsius,
            "current_percentage": self.heater_percentage
        }



    def to_dict(self):
        """
        Convert the SteeringWheel instance to a dictionary, including properties, value types, and property descriptions.
        
        Returns:
            dict: Dictionary containing all properties of the SteeringWheel instance
        """
        return {
            "is_view_open": {
                "value": self.is_view_open,
                "description": "Whether the steering wheel page is open, True means open, False means closed",
                "type": type(self.is_view_open).__name__
            },
            "is_heater_on": {
                "value": self.is_heater_on,
                "description": "Whether the steering wheel heating function is on, True means on, False means off",
                "type": type(self.is_heater_on).__name__
            },
            "heater_level": {
                "value": self.heater_level,
                "description": "Steering wheel heating level, range: 0-10, increases/decreases in sync with heater_celsius and heater_percentage",
                "type": type(self.heater_level).__name__
            },
            "heater_celsius": {
                "value": self.heater_celsius,
                "description": "Steering wheel heating temperature, unit: Celsius, range: 20.0-50.0, increases/decreases in sync with heater_level and heater_percentage",
                "type": type(self.heater_celsius).__name__
            },
            "heater_percentage": {
                "value": self.heater_percentage,
                "description": "Steering wheel heating percentage, range: 0.0-100.0, increases/decreases in sync with heater_level and heater_celsius",
                "type": type(self.heater_percentage).__name__
            },
            "current_unit": {
                "value": self.current_unit.value,
                "description": f"Currently used unit, enum values: {self.HeaterUnit.get_all_values()}",
                "type": "HeaterUnit(Enum)"
            },
            "degree_to_level": {
                "value": {k.value: v for k, v in self._degree_to_level.items()},
                "description": f"Mapping between preset heating levels and values, enum values: {self.HeaterDegree.get_all_values()}",
                "type": "dict"
            },
            "increase_degree_map": {
                "value": {k.value: v for k, v in self._increase_degree_map.items()},
                "description": f"Increment mapping relationship, enum values: {self.IncreaseDegree.get_all_values()}",
                "type": "dict"
            }
        }

    @classmethod
    def from_dict(cls, data):
        """
        Restore a SteeringWheel instance from dictionary data.
        
        Parameters:
            data (dict): Dictionary containing SteeringWheel instance properties
            
        Returns:
            SteeringWheel: Restored SteeringWheel instance
        """
        instance = cls()
        
        # Restore basic properties
        instance.is_view_open = data["is_view_open"]["value"]
        instance.is_heater_on = data["is_heater_on"]["value"]
        instance.heater_level = data["heater_level"]["value"]
        
        # Restore current unit
        unit_value = data["current_unit"]["value"]
        instance.current_unit = instance._str_to_enum(instance.HeaterUnit, unit_value)
        
        # Restore mapping relationships (if customization needed)
        degree_to_level = data["degree_to_level"]["value"]
        for key, value in degree_to_level.items():
            degree_enum = instance._str_to_enum(instance.HeaterDegree, key)
            instance._degree_to_level[degree_enum] = value
        
        increase_degree_map = data["increase_degree_map"]["value"]
        for key, value in increase_degree_map.items():
            degree_enum = instance._str_to_enum(instance.IncreaseDegree, key)
            instance._increase_degree_map[degree_enum] = value
        
        # Update values for other units
        instance._update_unit_values()
        
        return instance
    
    @classmethod
    def init1(cls):
        """
        Initialize steering wheel to comfort mode:
        - Page open
        - Heating function on
        - Heating level at medium
        - Celsius as the unit
        
        Returns:
            SteeringWheel: Initialized SteeringWheel instance
        """
        instance = cls()
        
        # Set page status to open
        instance.is_view_open = True
        
        # Set heating function to on
        instance.is_heater_on = True
        
        # Set heating level to medium
        instance.heater_level = instance._degree_to_level[cls.HeaterDegree.MEDIUM]
        
        # Set unit to Celsius
        instance.current_unit = cls.HeaterUnit.CELSIUS
        
        # Update values for other units
        instance._update_unit_values()
        
        return instance

    @classmethod
    def init2(cls):
        """
        Initialize steering wheel to sport mode:
        - Page open
        - Heating function on
        - Heating level at high
        - Percentage as the unit
        
        Returns:
            SteeringWheel: Initialized SteeringWheel instance
        """
        instance = cls()
        
        # Set page status to open
        instance.is_view_open = True
        
        # Set heating function to on
        instance.is_heater_on = True
        
        # Set heating level to high
        instance.heater_level = instance._degree_to_level[cls.HeaterDegree.HIGH]
        
        # Set unit to percentage
        instance.current_unit = cls.HeaterUnit.PERCENTAGE
        
        # Update values for other units
        instance._update_unit_values()
        
        return instance