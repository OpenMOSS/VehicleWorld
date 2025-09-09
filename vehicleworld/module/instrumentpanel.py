from utils import api
from enum import Enum
from module.environment import Environment
class InstrumentPanel:
    class BrightnessUnit(Enum):
        """
        Enum class defining the units for instrument panel brightness
        """
        GEAR = "gear"
        PERCENTAGE = "percentage" 
        NIT = "nit"
    
    class BrightnessDegreeAdjustment(Enum):
        """
        Enum class defining the degree of instrument panel brightness adjustment (for increasing and decreasing brightness)
        """
        LARGE = "large"
        LITTLE = "little"
        TINY = "tiny"
    
    class BrightnessDegreeLevel(Enum):
        """
        Enum class defining preset levels for instrument panel brightness
        """
        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"
    
    class DistanceUnit(Enum):
        """
        Enum class defining distance units
        """
        KILOMETERS = "Kilometers"
        MILES = "Miles"
    
    class Theme(Enum):
        """
        Enum class defining instrument panel themes
        """
        SCENE = "Scene"
        MAP = "Map"
    
    def __init__(self):
        # Basic instrument panel properties
        self._vehicle_mileage = 0.0  # Vehicle mileage
        self._distance_unit = InstrumentPanel.DistanceUnit.KILOMETERS  # Distance unit, default is kilometers
        self._theme = InstrumentPanel.Theme.SCENE  # Instrument panel theme, default is scene
        
        # Brightness-related properties
        self._brightness = 50.0  # Brightness value, default is 50%
        self._brightness_unit = InstrumentPanel.BrightnessUnit.PERCENTAGE  # Brightness unit, default is percentage
        self._auto_brightness = True  # Automatic brightness adjustment, enabled by default
        
        # Brightness range limits
        self._min_brightness = {
            InstrumentPanel.BrightnessUnit.GEAR: 1,
            InstrumentPanel.BrightnessUnit.PERCENTAGE: 10.0,
            InstrumentPanel.BrightnessUnit.NIT: 50.0
        }
        self._max_brightness = {
            InstrumentPanel.BrightnessUnit.GEAR: 5,
            InstrumentPanel.BrightnessUnit.PERCENTAGE: 100.0,
            InstrumentPanel.BrightnessUnit.NIT: 500.0
        }
        
        # Brightness adjustment magnitude
        self._brightness_adjustment = {
            InstrumentPanel.BrightnessUnit.GEAR: {
                InstrumentPanel.BrightnessDegreeAdjustment.TINY: 0.2,
                InstrumentPanel.BrightnessDegreeAdjustment.LITTLE: 0.5,
                InstrumentPanel.BrightnessDegreeAdjustment.LARGE: 1.0
            },
            InstrumentPanel.BrightnessUnit.PERCENTAGE: {
                InstrumentPanel.BrightnessDegreeAdjustment.TINY: 5.0,
                InstrumentPanel.BrightnessDegreeAdjustment.LITTLE: 10.0,
                InstrumentPanel.BrightnessDegreeAdjustment.LARGE: 20.0
            },
            InstrumentPanel.BrightnessUnit.NIT: {
                InstrumentPanel.BrightnessDegreeAdjustment.TINY: 20.0,
                InstrumentPanel.BrightnessDegreeAdjustment.LITTLE: 50.0,
                InstrumentPanel.BrightnessDegreeAdjustment.LARGE: 100.0
            }
        }
        
        # Brightness level corresponding to percentage values
        self._brightness_levels = {
            InstrumentPanel.BrightnessDegreeLevel.MIN: 10.0,
            InstrumentPanel.BrightnessDegreeLevel.LOW: 25.0,
            InstrumentPanel.BrightnessDegreeLevel.MEDIUM: 50.0,
            InstrumentPanel.BrightnessDegreeLevel.HIGH: 75.0,
            InstrumentPanel.BrightnessDegreeLevel.MAX: 100.0
        }

    # Vehicle mileage getter and setter
    @property
    def vehicle_mileage(self):
        return self._vehicle_mileage
    
    @vehicle_mileage.setter
    def vehicle_mileage(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Vehicle mileage must be a non-negative number")
        self._vehicle_mileage = float(value)
    
    # Distance unit getter and setter
    @property
    def distance_unit(self):
        return self._distance_unit
    
    @distance_unit.setter
    def distance_unit(self, value):
        if not isinstance(value, InstrumentPanel.DistanceUnit):
            if isinstance(value, str) and value in [unit.value for unit in InstrumentPanel.DistanceUnit]:
                value = InstrumentPanel.DistanceUnit(value)
            else:
                raise ValueError(f"Distance unit must be one of {[unit.value for unit in InstrumentPanel.DistanceUnit]}")
        self._distance_unit = value
    
    # Instrument panel theme getter and setter
    @property
    def theme(self):
        return self._theme
    
    @theme.setter
    def theme(self, value):
        if not isinstance(value, InstrumentPanel.Theme):
            if isinstance(value, str) and value in [theme.value for theme in InstrumentPanel.Theme]:
                value = InstrumentPanel.Theme(value)
            else:
                raise ValueError(f"Theme must be one of {[theme.value for theme in InstrumentPanel.Theme]}")
        self._theme = value
    
    # Brightness getter and setter
    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Brightness must be a number")
        
        # Ensure brightness is within valid range for current unit
        min_val = self._min_brightness[self._brightness_unit]
        max_val = self._max_brightness[self._brightness_unit]
        
        if value < min_val:
            value = min_val
        elif value > max_val:
            value = max_val
            
        self._brightness = float(value)
    
    # Brightness unit getter and setter
    @property
    def brightness_unit(self):
        return self._brightness_unit
    
    @brightness_unit.setter
    def brightness_unit(self, value):
        if not isinstance(value, InstrumentPanel.BrightnessUnit):
            if isinstance(value, str) and value in [unit.value for unit in InstrumentPanel.BrightnessUnit]:
                value = InstrumentPanel.BrightnessUnit(value)
            else:
                raise ValueError(f"Brightness unit must be one of {[unit.value for unit in InstrumentPanel.BrightnessUnit]}")
        self._brightness_unit = value
    
    # Auto brightness getter and setter
    @property
    def auto_brightness(self):
        return self._auto_brightness
    
    @auto_brightness.setter
    def auto_brightness(self, value):
        if not isinstance(value, bool):
            raise ValueError("Auto brightness must be a boolean value")
        self._auto_brightness = value
    
    # API method implementations
    @api("instrumentPanel")
    def carcontrol_instrumentPanel_vehicleMileage_view(self):
        """
        View vehicle mileage
        
        Returns:
            dict: Contains operation result and vehicle mileage information
        """
        return {
            "success": True,
            "vehicle_mileage": self.vehicle_mileage,
            "unit": self.distance_unit.value
        }
    
    @api("instrumentPanel")
    def carcontrol_instrumentPanel_meter_unit(self, mode):
        """
        Set display distance unit on instrument panel
        
        Args:
            mode (str): Distance unit option, values can be ["Kilometers", "Miles"]
            
        Returns:
            dict: Contains operation result and updated distance unit
        """
        try:
            self.distance_unit = mode
            return {
                "success": True,
                "updated_unit": self.distance_unit.value
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("instrumentPanel")
    def carcontrol_instrumentPanel_timeDisplayFormat_set(self, mode):
        """
        Set time display format on instrument panel
        
        Args:
            mode (str): Time display format option, values can be ["12-hour format", "24-hour format"]
            
        Returns:
            dict: Contains operation result and updated time display format
        """
        try:
            if mode not in ["12-hour format", "24-hour format"]:
                raise ValueError("Time display format must be one of ['12-hour format', '24-hour format']")
            
            # Call Environment class method to set time display format
            Environment.set_time_display_format(mode)
            
            return {
                "success": True,
                "updated_time_format": mode
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("instrumentPanel")
    def carcontrol_instrumentPanel_language_set(self, mode):
        """
        Set instrument panel language type, change the language of the instrument panel
        
        Args:
            mode (str): Language option, values can be ["Chinese", "English"]
            
        Returns:
            dict: Contains operation result and updated language setting
        """
        try:
            if mode not in ["Chinese", "English"]:
                raise ValueError("Language must be one of ['Chinese', 'English']")
            
            # Call Environment class method to set language
            Environment.set_language(mode)
            
            return {
                "success": True,
                "updated_language": mode
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("instrumentPanel")
    def carcontrol_instrumentPanel_mode_autoBrightness(self, switch):
        """
        Enable or disable the instrument panel <automatic brightness adjustment> function.
        Automatic brightness adjustment: Brightness will change according to the brightness changes in the surrounding environment.
        
        Args:
            switch (bool): Instrument panel brightness automatic adjustment switch, true means enable, false means disable
            
        Returns:
            dict: Contains operation result and updated automatic brightness adjustment status
        """
        try:
            self.auto_brightness = switch
            return {
                "success": True,
                "auto_brightness": self.auto_brightness
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("instrumentPanel")
    def carcontrol_instrumentPanel_brightness_increase(self, value=None, unit=None, degree=None):
        """
        When called, the instrument panel brightness will increase
        
        Args:
            value (float, optional): Specific instrument panel brightness adjustment numerical value, unit refers to unit field, mutually exclusive with degree
            unit (str, optional): Specific instrument panel brightness adjustment unit part, mutually exclusive with degree,
                                values can be ["gear", "percentage", "nit"]
            degree (str, optional): Different levels of instrument panel brightness adjustment, tiny is minimum, large is maximum, mutually exclusive with value/unit,
                                values can be ["large", "little", "tiny"]
                                
        Returns:
            dict: Contains operation result and updated brightness settings
        """
        try:
            # Cannot manually adjust brightness in auto brightness mode
            self.auto_brightness=False
               
            
            # Handle different adjustment methods
            if degree is not None:
                # Adjust brightness by degree
                if degree not in [deg.value for deg in InstrumentPanel.BrightnessDegreeAdjustment]:
                    raise ValueError(f"Degree must be one of {[deg.value for deg in InstrumentPanel.BrightnessDegreeAdjustment]}")
                
                degree_enum = InstrumentPanel.BrightnessDegreeAdjustment(degree)
                adjustment = self._brightness_adjustment[self.brightness_unit][degree_enum]
                self.brightness += adjustment
            
            elif value is not None and unit is not None:
                # Adjust brightness by specific value and unit
                if unit not in [u.value for u in InstrumentPanel.BrightnessUnit]:
                    raise ValueError(f"Unit must be one of {[u.value for u in InstrumentPanel.BrightnessUnit]}")
                
                # If provided unit differs from current unit, conversion is needed
                if unit != self.brightness_unit.value:
                    # In actual implementation, there should be conversion logic between units
                    # For simplicity, we assume direct adoption of provided unit
                    self.brightness_unit = InstrumentPanel.BrightnessUnit(unit)
                
                self.brightness += value
            
            else:
                # By default, increase brightness by medium degree
                adjustment = self._brightness_adjustment[self.brightness_unit][InstrumentPanel.BrightnessDegreeAdjustment.LITTLE]
                self.brightness += adjustment
            
            return {
                "success": True,
                "updated_brightness": self.brightness,
                "unit": self.brightness_unit.value
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("instrumentPanel")
    def carcontrol_instrumentPanel_brightness_decrease(self, value=None, unit=None, degree=None):
        """
        When called, the instrument panel brightness will decrease
        
        Args:
            value (float, optional): Specific instrument panel brightness adjustment numerical value, unit refers to unit field, mutually exclusive with degree
            unit (str, optional): Specific instrument panel brightness adjustment unit part, mutually exclusive with degree,
                                values can be ["gear", "percentage", "nit"]
            degree (str, optional): Different levels of instrument panel brightness adjustment, tiny is minimum, large is maximum, mutually exclusive with value/unit,
                                values can be ["large", "little", "tiny"]
                                
        Returns:
            dict: Contains operation result and updated brightness settings
        """
        try:
            # Cannot manually adjust brightness in auto brightness mode
            self.auto_brightness = False
            
            # Handle different adjustment methods
            if degree is not None:
                # Adjust brightness by degree
                if degree not in [deg.value for deg in InstrumentPanel.BrightnessDegreeAdjustment]:
                    raise ValueError(f"Degree must be one of {[deg.value for deg in InstrumentPanel.BrightnessDegreeAdjustment]}")
                
                degree_enum = InstrumentPanel.BrightnessDegreeAdjustment(degree)
                adjustment = self._brightness_adjustment[self.brightness_unit][degree_enum]
                self.brightness -= adjustment
            
            elif value is not None and unit is not None:
                # Adjust brightness by specific value and unit
                if unit not in [u.value for u in InstrumentPanel.BrightnessUnit]:
                    raise ValueError(f"Unit must be one of {[u.value for u in InstrumentPanel.BrightnessUnit]}")
                
                # If provided unit differs from current unit, conversion is needed
                if unit != self.brightness_unit.value:
                    # In actual implementation, there should be conversion logic between units
                    # For simplicity, we assume direct adoption of provided unit
                    self.brightness_unit = InstrumentPanel.BrightnessUnit(unit)
                
                self.brightness -= value
            
            else:
                # By default, decrease brightness by medium degree
                adjustment = self._brightness_adjustment[self.brightness_unit][InstrumentPanel.BrightnessDegreeAdjustment.LITTLE]
                self.brightness -= adjustment
            
            return {
                "success": True,
                "updated_brightness": self.brightness,
                "unit": self.brightness_unit.value
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("instrumentPanel")
    def carcontrol_instrumentPanel_brightness_set(self, value=None, unit=None, degree=None):
        """
        When called, the instrument panel brightness will be set to a specified value
        
        Args:
            value (float, optional): Specific instrument panel brightness numerical value, unit refers to unit field, mutually exclusive with degree
            unit (str, optional): Specific instrument panel brightness unit part, mutually exclusive with degree,
                                values can be ["gear", "percentage", "nit"]
            degree (str, optional): Different levels of instrument panel brightness, mutually exclusive with value/unit,
                                values can be ["max", "high", "medium", "low", "min"]
                                
        Returns:
            dict: Contains operation result and updated brightness settings
        """
        try:
            # Cannot manually set brightness in auto brightness mode
            self.auto_brightness = False
               
            # Check if parameters are valid (at least need to provide degree or value+unit)
            if degree is None and (value is None or unit is None):
                return {
                    "success": False,
                    "error": "Must provide either 'degree' or both 'value' and 'unit'"
                }
            
            # Handle different setting methods
            if degree is not None:
                # Set brightness by preset level
                if degree not in [deg.value for deg in InstrumentPanel.BrightnessDegreeLevel]:
                    raise ValueError(f"Degree must be one of {[deg.value for deg in InstrumentPanel.BrightnessDegreeLevel]}")
                
                degree_enum = InstrumentPanel.BrightnessDegreeLevel(degree)
                # Set brightness to corresponding level's percentage value
                self.brightness_unit = InstrumentPanel.BrightnessUnit.PERCENTAGE
                self.brightness = self._brightness_levels[degree_enum]
            
            else:  # value is not None and unit is not None
                # Set brightness by specific value and unit
                if unit not in [u.value for u in InstrumentPanel.BrightnessUnit]:
                    raise ValueError(f"Unit must be one of {[u.value for u in InstrumentPanel.BrightnessUnit]}")
                
                self.brightness_unit = InstrumentPanel.BrightnessUnit(unit)
                self.brightness = value
            
            return {
                "success": True,
                "brightness": self.brightness,
                "unit": self.brightness_unit.value
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @api("instrumentPanel")
    def carcontrol_display_theme_set(self, mode):
        """
        Set instrument panel theme
        
        Args:
            mode (str): Instrument panel theme, values can be ["Scene", "Map"]
            
        Returns:
            dict: Contains operation result and updated theme
        """
        try:
            self.theme = mode
            return {
                "success": True,
                "updated_theme": self.theme.value
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }


    def to_dict(self):
        """
        Convert InstrumentPanel object to dictionary, containing values, types, and descriptions of all properties
        
        Returns:
            dict: Dictionary containing all property information of InstrumentPanel
        """
        return {
            "vehicle_mileage": {
                "value": self.vehicle_mileage,
                "description": "Vehicle mileage",
                "type": type(self.vehicle_mileage).__name__
            },
            "distance_unit": {
                "value": self.distance_unit.value,
                "description": "Distance unit, values can be [Kilometers, Miles]",
                "type": "DistanceUnit"
            },
            "theme": {
                "value": self.theme.value,
                "description": "Instrument panel theme, values can be [Scene, Map]",
                "type": "Theme"
            },
            "brightness": {
                "value": self.brightness,
                "description": "Instrument panel brightness value",
                "type": type(self.brightness).__name__
            },
            "brightness_unit": {
                "value": self.brightness_unit.value,
                "description": "Brightness unit, values can be [gear, percentage, nit]",
                "type": "BrightnessUnit"
            },
            "auto_brightness": {
                "value": self.auto_brightness,
                "description": "Automatic brightness adjustment function switch,if you want to change the brightness specifically,you need to set it to False",
                "type": type(self.auto_brightness).__name__
            }
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Restore InstrumentPanel instance from dictionary data
        
        Args:
            data (dict): Dictionary containing InstrumentPanel properties
            
        Returns:
            InstrumentPanel: Restored InstrumentPanel instance
        """
        instance = cls()
        
        # Restore basic properties
        if "vehicle_mileage" in data:
            instance.vehicle_mileage = data["vehicle_mileage"]["value"]
        
        if "distance_unit" in data:
            instance.distance_unit = data["distance_unit"]["value"]
        
        if "theme" in data:
            instance.theme = data["theme"]["value"]
        
        if "brightness" in data:
            instance.brightness = data["brightness"]["value"]
        
        if "brightness_unit" in data:
            instance.brightness_unit = data["brightness_unit"]["value"]
        
        if "auto_brightness" in data:
            instance.auto_brightness = data["auto_brightness"]["value"]
        
        return instance

    
    @classmethod
    def init1(cls):
        """
        Initialize an instrument panel instance for night mode
        
        Returns:
            InstrumentPanel: Instrument panel instance configured for night mode
        """
        instance = cls()
        instance.brightness = 25.0  # Set lower brightness value, suitable for night use
        instance.brightness_unit = InstrumentPanel.BrightnessUnit.PERCENTAGE
        instance.auto_brightness = False  # Disable automatic brightness adjustment
        instance.theme = InstrumentPanel.Theme.SCENE  # Use scene theme
        instance.distance_unit = InstrumentPanel.DistanceUnit.KILOMETERS
        # Call Environment class to set English and 24-hour format
        Environment.set_language("English")
        Environment.set_time_display_format("24-hour format")
        return instance

    @classmethod
    def init2(cls):
        """
        Initialize an instrument panel instance for day navigation mode
        
        Returns:
            InstrumentPanel: Instrument panel instance configured for day navigation mode
        """
        instance = cls()
        instance.brightness = 75.0  # Set higher brightness value, suitable for day use
        instance.brightness_unit = InstrumentPanel.BrightnessUnit.PERCENTAGE
        instance.auto_brightness = True  # Enable automatic brightness adjustment
        instance.theme = InstrumentPanel.Theme.MAP  # Use map theme
        instance.distance_unit = InstrumentPanel.DistanceUnit.MILES  # Use miles unit
        # Call Environment class to set Chinese and 12-hour format
        Environment.set_language("Chinese")
        Environment.set_time_display_format("12-hour format")
        return instance