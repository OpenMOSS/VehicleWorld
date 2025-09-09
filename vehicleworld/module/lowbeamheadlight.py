from enum import Enum
from utils import api

class LowBeamHeadlight:
    """
    Low beam headlight entity class, used to control the state and height of vehicle's low beam headlights.
    """
    
    class Mode(Enum):
        """
        Working mode enumeration for low beam headlights
        """
        ON = "on"
        OFF = "off"
        AUTO = "auto"
    
    class HeightUnit(Enum):
        """
        Unit enumeration for low beam headlight height adjustment
        """
        LEVEL = "level"
        PERCENTAGE = "percentage"
        CENTIMETER = "centimeter"
    
    class AdjustmentDegree(Enum):
        """
        Degree enumeration for low beam headlight height adjustment, used for increase and decrease operations
        """
        LARGE = "large"
        LITTLE = "little"
        TINY = "tiny"
    
    class HeightDegree(Enum):
        """
        Preset level enumeration for low beam headlight height, used for direct setting
        """
        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"
    
    # Default height configuration
    MAX_HEIGHT_LEVEL = 10
    MIN_HEIGHT_LEVEL = 0
    MAX_HEIGHT_PERCENTAGE = 100.0
    MIN_HEIGHT_PERCENTAGE = 0.0
    MAX_HEIGHT_CENTIMETER = 15.0
    MIN_HEIGHT_CENTIMETER = 0.0
    
    # Adjustment increment configuration
    ADJUSTMENT_LARGE = {"level": 3, "percentage": 30.0, "centimeter": 4.5}
    ADJUSTMENT_LITTLE = {"level": 1, "percentage": 10.0, "centimeter": 1.5}
    ADJUSTMENT_TINY = {"level": 0.5, "percentage": 5.0, "centimeter": 0.75}
    
    # Preset level configuration
    HEIGHT_DEGREE_VALUES = {
        "max": {"level": 10, "percentage": 100.0, "centimeter": 15.0},
        "high": {"level": 7.5, "percentage": 75.0, "centimeter": 11.25},
        "medium": {"level": 5, "percentage": 50.0, "centimeter": 7.5},
        "low": {"level": 2.5, "percentage": 25.0, "centimeter": 3.75},
        "min": {"level": 0, "percentage": 0.0, "centimeter": 0.0}
    }
    
    def __init__(self):
        """
        Initialize low beam headlight, set default properties
        """
        self._mode = self.Mode.OFF  # Default off
        self._height_level = 5  # Default medium height (range 0-10)
        self._height_percentage = 50.0  # Default medium height (range 0-100%)
        self._height_centimeter = 7.5  # Default medium height (range 0-15cm)
        self._current_unit = self.HeightUnit.LEVEL  # Default using level unit
    
    # Getter and setter for Mode property
    @property
    def mode(self):
        """Get the current working mode of low beam headlight"""
        return self._mode
    
    @mode.setter
    def mode(self, value):
        """Set the working mode of low beam headlight"""
        if isinstance(value, self.Mode):
            self._mode = value
        elif isinstance(value, str) and value in [mode.value for mode in self.Mode]:
            self._mode = self.Mode(value)
        else:
            raise ValueError(f"Invalid mode: {value}. Must be one of {[mode.value for mode in self.Mode]}")
    
    # Getter and setter for Height properties
    @property
    def height_level(self):
        """Get the low beam headlight height (level)"""
        return self._height_level
    
    @height_level.setter
    def height_level(self, value):
        """Set the low beam headlight height (level)"""
        if not isinstance(value, (int, float)):
            raise ValueError("Height level must be a number")
        
        # Ensure value is within valid range
        value = max(self.MIN_HEIGHT_LEVEL, min(value, self.MAX_HEIGHT_LEVEL))
        self._height_level = value
        
        # Synchronize values in other units
        percentage = (value / self.MAX_HEIGHT_LEVEL) * self.MAX_HEIGHT_PERCENTAGE
        self._height_percentage = percentage
        
        centimeter = (value / self.MAX_HEIGHT_LEVEL) * self.MAX_HEIGHT_CENTIMETER
        self._height_centimeter = centimeter
    
    @property
    def height_percentage(self):
        """Get the low beam headlight height (percentage)"""
        return self._height_percentage
    
    @height_percentage.setter
    def height_percentage(self, value):
        """Set the low beam headlight height (percentage)"""
        if not isinstance(value, (int, float)):
            raise ValueError("Height percentage must be a number")
        
        # Ensure value is within valid range
        value = max(self.MIN_HEIGHT_PERCENTAGE, min(value, self.MAX_HEIGHT_PERCENTAGE))
        self._height_percentage = value
        
        # Synchronize values in other units
        level = (value / self.MAX_HEIGHT_PERCENTAGE) * self.MAX_HEIGHT_LEVEL
        self._height_level = level
        
        centimeter = (value / self.MAX_HEIGHT_PERCENTAGE) * self.MAX_HEIGHT_CENTIMETER
        self._height_centimeter = centimeter
    
    @property
    def height_centimeter(self):
        """Get the low beam headlight height (centimeter)"""
        return self._height_centimeter
    
    @height_centimeter.setter
    def height_centimeter(self, value):
        """Set the low beam headlight height (centimeter)"""
        if not isinstance(value, (int, float)):
            raise ValueError("Height centimeter must be a number")
        
        # Ensure value is within valid range
        value = max(self.MIN_HEIGHT_CENTIMETER, min(value, self.MAX_HEIGHT_CENTIMETER))
        self._height_centimeter = value
        
        # Synchronize values in other units
        level = (value / self.MAX_HEIGHT_CENTIMETER) * self.MAX_HEIGHT_LEVEL
        self._height_level = level
        
        percentage = (value / self.MAX_HEIGHT_CENTIMETER) * self.MAX_HEIGHT_PERCENTAGE
        self._height_percentage = percentage
    
    @property
    def current_unit(self):
        """Get the currently used height unit"""
        return self._current_unit
    
    @current_unit.setter
    def current_unit(self, value):
        """Set the currently used height unit"""
        if isinstance(value, self.HeightUnit):
            self._current_unit = value
        elif isinstance(value, str) and value in [unit.value for unit in self.HeightUnit]:
            self._current_unit = self.HeightUnit(value)
        else:
            raise ValueError(f"Invalid unit: {value}. Must be one of {[unit.value for unit in self.HeightUnit]}")
    
    def get_height_by_unit(self, unit=None):
        """
        Get height value according to specified unit
        
        Args:
            unit: The specified unit, if None, use current unit
            
        Returns:
            Height value in corresponding unit
        """
        if unit is None:
            unit = self.current_unit
            
        if isinstance(unit, str):
            unit = self.HeightUnit(unit)
            
        if unit == self.HeightUnit.LEVEL:
            return self.height_level
        elif unit == self.HeightUnit.PERCENTAGE:
            return self.height_percentage
        elif unit == self.HeightUnit.CENTIMETER:
            return self.height_centimeter
        else:
            raise ValueError(f"Invalid unit: {unit}")
    
    def set_height_by_unit(self, value, unit=None):
        """
        Set height value according to specified unit
        
        Args:
            value: Height value
            unit: The specified unit, if None, use current unit
            
        Returns:
            None
        """
        if unit is None:
            unit = self.current_unit
            
        if isinstance(unit, str):
            unit = self.HeightUnit(unit)
            
        if unit == self.HeightUnit.LEVEL:
            self.height_level = value
        elif unit == self.HeightUnit.PERCENTAGE:
            self.height_percentage = value
        elif unit == self.HeightUnit.CENTIMETER:
            self.height_centimeter = value
        else:
            raise ValueError(f"Invalid unit: {unit}")
    



    def to_dict(self):
        """
        Convert entity class to dictionary form, including properties, types and descriptions
        
        Returns:
            Dictionary containing entity class information
        """
        return {
            "mode": {
                "value": self.mode.value,
                "description": "Working mode of low beam headlight, possible values: on (on), off (off), auto (automatic)",
                "type": "Mode(Enum)"
            },
            "height_level": {
                "value": self.height_level,
                "description": f"Low beam headlight height (level), range: {self.MIN_HEIGHT_LEVEL}-{self.MAX_HEIGHT_LEVEL}",
                "type": type(self.height_level).__name__
            },
            "height_percentage": {
                "value": self.height_percentage,
                "description": f"Low beam headlight height (percentage), range: {self.MIN_HEIGHT_PERCENTAGE}-{self.MAX_HEIGHT_PERCENTAGE}%",
                "type": type(self.height_percentage).__name__
            },
            "height_centimeter": {
                "value": self.height_centimeter,
                "description": f"Low beam headlight height (centimeter), range: {self.MIN_HEIGHT_CENTIMETER}-{self.MAX_HEIGHT_CENTIMETER}cm",
                "type": type(self.height_centimeter).__name__
            },
            "current_unit": {
                "value": self.current_unit.value,
                "description": "Currently used height unit, possible values: level (level), percentage (percentage), centimeter (centimeter)",
                "type": "HeightUnit(Enum)"
            }
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Restore entity class instance from dictionary data
        
        Args:
            data: Dictionary containing entity class data
            
        Returns:
            LowBeamHeadlight instance
        """
        instance = cls()
        
        # Set mode
        if "mode" in data:
            instance.mode = data["mode"]["value"]
        
        # Set height (level)
        if "height_level" in data:
            instance.height_level = data["height_level"]["value"]
        
        # Set current unit
        if "current_unit" in data:
            instance.current_unit = data["current_unit"]["value"]
            
        return instance
    
    @api("lowBeamHeadlight")
    def switch(self, action):
        """
        Set the working mode of low beam headlight
        
        Args:
            action: Working mode, possible values: on (on), off (off), auto (automatic)
            
        Returns:
            Dictionary containing operation result and status information
        """
        try:
            self.mode = action
            return {
                "success": True,
                "message": f"Low beam headlight has been switched to {action} mode",
                "status": self.to_dict()
            }
        except ValueError as e:
            return {
                "success": False,
                "message": str(e),
                "status": self.to_dict()
            }
    
    @api("lowBeamHeadlight")
    def height_increase(self, value=None, unit=None, degree=None):
        """
        Increase the height of low beam headlight
        
        Args:
            value: Numerical increment, used with unit, mutually exclusive with degree
            unit: Increment unit, possible values: level (level), percentage (percentage), centimeter (centimeter)
            degree: Increase degree, possible values: large (large), little (small), tiny (tiny)
            
        Returns:
            Dictionary containing operation result and status information
        """
        try:
            # Parameter validation
            if (value is not None or unit is not None) and degree is not None:
                raise ValueError("Parameter conflict: value/unit and degree cannot be used simultaneously")
                
            current_height = None
            
            # Adjust using degree
            if degree is not None:
                # Validate degree value
                if degree not in [d.value for d in self.AdjustmentDegree]:
                    raise ValueError(f"Invalid degree value: {degree}, possible values: {[d.value for d in self.AdjustmentDegree]}")
                
                # Get current unit
                current_unit = self.current_unit.value
                
                # Get increment based on degree
                if degree == self.AdjustmentDegree.LARGE.value:
                    increment = self.ADJUSTMENT_LARGE[current_unit]
                elif degree == self.AdjustmentDegree.LITTLE.value:
                    increment = self.ADJUSTMENT_LITTLE[current_unit]
                elif degree == self.AdjustmentDegree.TINY.value:
                    increment = self.ADJUSTMENT_TINY[current_unit]
                
                # Get current height
                current_height = self.get_height_by_unit()
                
                # Calculate new height
                new_height = current_height + increment
                
                # Set new height
                self.set_height_by_unit(new_height)
                
            # Adjust using value/unit
            elif value is not None:
                if not isinstance(value, (int, float)):
                    raise ValueError("value must be a number")
                
                # If unit is not specified, use current unit
                if unit is None:
                    unit = self.current_unit.value
                
                # Validate unit value
                if unit not in [u.value for u in self.HeightUnit]:
                    raise ValueError(f"Invalid unit value: {unit}, possible values: {[u.value for u in self.HeightUnit]}")
                
                # Get current height
                current_height = self.get_height_by_unit(unit)
                
                # Calculate new height
                new_height = current_height + value
                
                # Set new height
                self.set_height_by_unit(new_height, unit)
                
            # If no parameters provided, use default increment
            else:
                # Get current unit
                current_unit = self.current_unit.value
                
                # Use small increment as default
                increment = self.ADJUSTMENT_LITTLE[current_unit]
                
                # Get current height
                current_height = self.get_height_by_unit()
                
                # Calculate new height
                new_height = current_height + increment
                
                # Set new height
                self.set_height_by_unit(new_height)
            
            # Get updated height
            updated_height = self.get_height_by_unit()
            
            return {
                "success": True,
                "message": f"Low beam headlight height has been increased from {current_height} to {updated_height}",
                "status": self.to_dict()
            }
        except ValueError as e:
            return {
                "success": False,
                "message": str(e),
                "status": self.to_dict()
            }
    
    @api("lowBeamHeadlight")
    def height_decrease(self, value=None, unit=None, degree=None):
        """
        Decrease the height of low beam headlight
        
        Args:
            value: Numerical decrement, used with unit, mutually exclusive with degree
            unit: Decrement unit, possible values: level (level), percentage (percentage), centimeter (centimeter)
            degree: Decrease degree, possible values: large (large), little (small), tiny (tiny)
            
        Returns:
            Dictionary containing operation result and status information
        """
        try:
            # Parameter validation
            if (value is not None or unit is not None) and degree is not None:
                raise ValueError("Parameter conflict: value/unit and degree cannot be used simultaneously")
                
            current_height = None
            
            # Adjust using degree
            if degree is not None:
                # Validate degree value
                if degree not in [d.value for d in self.AdjustmentDegree]:
                    raise ValueError(f"Invalid degree value: {degree}, possible values: {[d.value for d in self.AdjustmentDegree]}")
                
                # Get current unit
                current_unit = self.current_unit.value
                
                # Get decrement based on degree
                if degree == self.AdjustmentDegree.LARGE.value:
                    decrement = self.ADJUSTMENT_LARGE[current_unit]
                elif degree == self.AdjustmentDegree.LITTLE.value:
                    decrement = self.ADJUSTMENT_LITTLE[current_unit]
                elif degree == self.AdjustmentDegree.TINY.value:
                    decrement = self.ADJUSTMENT_TINY[current_unit]
                
                # Get current height
                current_height = self.get_height_by_unit()
                
                # Calculate new height
                new_height = current_height - decrement
                
                # Set new height
                self.set_height_by_unit(new_height)
                
            # Adjust using value/unit
            elif value is not None:
                if not isinstance(value, (int, float)):
                    raise ValueError("value must be a number")
                
                # If unit is not specified, use current unit
                if unit is None:
                    unit = self.current_unit.value
                
                # Validate unit value
                if unit not in [u.value for u in self.HeightUnit]:
                    raise ValueError(f"Invalid unit value: {unit}, possible values: {[u.value for u in self.HeightUnit]}")
                
                # Get current height
                current_height = self.get_height_by_unit(unit)
                
                # Calculate new height
                new_height = current_height - value
                
                # Set new height
                self.set_height_by_unit(new_height, unit)
                
            # If no parameters provided, use default decrement
            else:
                # Get current unit
                current_unit = self.current_unit.value
                
                # Use small decrement as default
                decrement = self.ADJUSTMENT_LITTLE[current_unit]
                
                # Get current height
                current_height = self.get_height_by_unit()
                
                # Calculate new height
                new_height = current_height - decrement
                
                # Set new height
                self.set_height_by_unit(new_height)
            
            # Get updated height
            updated_height = self.get_height_by_unit()
            
            return {
                "success": True,
                "message": f"Low beam headlight height has been decreased from {current_height} to {updated_height}",
                "status": self.to_dict()
            }
        except ValueError as e:
            return {
                "success": False,
                "message": str(e),
                "status": self.to_dict()
            }
    
    @api("lowBeamHeadlight")
    def height_set(self, value=None, unit=None, degree=None):
        """
        Set the height of low beam headlight
        
        Args:
            value: Numerical value, used with unit, mutually exclusive with degree
            unit: Unit, possible values: level (level), percentage (percentage), centimeter (centimeter)
            degree: Preset level, possible values: max (maximum), high (high), medium (medium), low (low), min (minimum)
            
        Returns:
            Dictionary containing operation result and status information
        """
        try:
            # Parameter validation
            if (value is not None and unit is None) or (value is None and unit is not None):
                raise ValueError("value and unit must be provided together")
                
            if (value is not None or unit is not None) and degree is not None:
                raise ValueError("Parameter conflict: value/unit and degree cannot be used simultaneously")
                
            if value is None and degree is None:
                raise ValueError("Must provide value/unit or degree parameter")
                
            current_height = None
            
            # Set using degree
            if degree is not None:
                # Validate degree value
                if degree not in [d.value for d in self.HeightDegree]:
                    raise ValueError(f"Invalid degree value: {degree}, possible values: {[d.value for d in self.HeightDegree]}")
                
                # Get current unit
                current_unit = self.current_unit.value
                
                # Get current height
                current_height = self.get_height_by_unit()
                
                # Get new height based on degree and current unit
                new_height = self.HEIGHT_DEGREE_VALUES[degree][current_unit]
                
                # Set new height
                self.set_height_by_unit(new_height)
                
            # Set using value/unit
            elif value is not None and unit is not None:
                if not isinstance(value, (int, float)):
                    raise ValueError("value must be a number")
                
                # Validate unit value
                if unit not in [u.value for u in self.HeightUnit]:
                    raise ValueError(f"Invalid unit value: {unit}, possible values: {[u.value for u in self.HeightUnit]}")
                
                # Get current height
                current_height = self.get_height_by_unit(unit)
                
                # Set new height
                self.set_height_by_unit(value, unit)
                
                # Update current unit
                self.current_unit = unit
            
            # Get updated height
            updated_height = self.get_height_by_unit()
            
            return {
                "success": True,
                "message": f"Low beam headlight height has been set from {current_height} to {updated_height}",
                "status": self.to_dict()
            }
        except ValueError as e:
            return {
                "success": False,
                "message": str(e),
                "status": self.to_dict()
            }
        
    @classmethod
    def init1(cls):
        """
        Initialize low beam headlight, set to night driving mode
        
        Night driving mode: lights on, height set to high level (high)
        
        Returns:
            LowBeamHeadlight instance configured for night driving mode
        """
        instance = cls()
        # Set to on state
        instance.mode = cls.Mode.ON
        # Set to high height
        current_unit = instance.current_unit.value
        instance.set_height_by_unit(cls.HEIGHT_DEGREE_VALUES["high"][current_unit], current_unit)
        return instance

    @classmethod
    def init2(cls):
        """
        Initialize low beam headlight, set to automatic urban mode
        
        Automatic urban mode: lights in automatic control, height set to low level (low)
        
        Returns:
            LowBeamHeadlight instance configured for automatic urban mode
        """
        instance = cls()
        # Set to automatic state
        instance.mode = cls.Mode.AUTO
        # Set to low height
        current_unit = instance.current_unit.value
        instance.set_height_by_unit(cls.HEIGHT_DEGREE_VALUES["low"][current_unit], current_unit)
        # Set unit to centimeter
        instance.current_unit = cls.HeightUnit.CENTIMETER
        return instance