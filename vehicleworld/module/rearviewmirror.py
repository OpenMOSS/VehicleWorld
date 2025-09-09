from enum import Enum
from utils import api

class RearviewMirror:
    """
    RearviewMirror entity class representing vehicle rearview mirrors with various functionalities.
    """

    class Position(Enum):
        """
        Enum representing possible positions of rearview mirrors.
        """
        LEFT = "left side"
        RIGHT = "right side"
        ALL = "all"

    class AdjustmentUnit(Enum):
        """
        Enum representing units for mirror adjustments.
        """
        GEAR = "gear"
        PERCENTAGE = "percentage"
        CENTIMETER = "centimeter"

    class AdjustmentDegree(Enum):
        """
        Enum representing degrees of adjustment for mirrors.
        """
        LARGE = "large"
        LITTLE = "little"
        TINY = "tiny"

    class HeightDegree(Enum):
        """
        Enum representing predefined height positions for mirrors.
        """
        MAX = "max"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        MIN = "min"

    class MirrorState:
        """
        Inner class representing the state of an individual mirror.
        """
        def __init__(self, is_open=True, height=50.0, horizontal_position=50.0):
            self._is_open = is_open  # True means open/extended, False means closed/folded
            self._height = height    # Percentage value (0-100)
            self._horizontal_position = horizontal_position  # Percentage value (0-100), 0=full inward, 100=full outward

        @property
        def is_open(self):
            return self._is_open

        @is_open.setter
        def is_open(self, value):
            if not isinstance(value, bool):
                raise ValueError("is_open must be a boolean value")
            self._is_open = value

        @property
        def height(self):
            return self._height

        @height.setter
        def height(self, value):
            if not isinstance(value, float) and not isinstance(value, int):
                raise ValueError("height must be a numeric value")
            if value < 0 or value > 100:
                raise ValueError("height must be between 0 and 100")
            self._height = float(value)

        @property
        def horizontal_position(self):
            return self._horizontal_position

        @horizontal_position.setter
        def horizontal_position(self, value):
            if not isinstance(value, float) and not isinstance(value, int):
                raise ValueError("horizontal_position must be a numeric value")
            if value < 0 or value > 100:
                raise ValueError("horizontal_position must be between 0 and 100")
            self._horizontal_position = float(value)

        def to_dict(self):
            return {
                "is_open": {
                    "value": self.is_open,
                    "description": "Mirror open/extended (True) or closed/folded (False) state",
                    "type": type(self.is_open).__name__
                },
                "height": {
                    "value": self.height,
                    "description": "Mirror height position (0-100%). Converts from gears (1-10, each gear = 10%) and centimeters (0-10cm, each cm = 10%). Can be adjusted relatively by degree (tiny=±5%, little=±10%, large=±20%) or absolutely (min=0%, low=25%, medium=50%, high=75%, max=100%)",
                    "type": type(self.height).__name__
                },
                "horizontal_position": {
                    "value": self.horizontal_position,
                    "description": "Mirror horizontal position (0-100%, 0=full inward, 100=full outward)",
                    "type": type(self.horizontal_position).__name__
                }
            }
        
        @classmethod
        def from_dict(cls, data):
            instance = cls()
            instance.is_open = data["is_open"]["value"]
            instance.height = data["height"]["value"]
            instance.horizontal_position = data["horizontal_position"]["value"]
            return instance

    def __init__(self):
        # Individual mirror states
        self._left_mirror = RearviewMirror.MirrorState()
        self._right_mirror = RearviewMirror.MirrorState()
        
        # View page state
        self._view_page_open = False
        
        # Auto mode settings
        self._auto_flip_enabled = False  # Auto-flip when reversing
        self._auto_fold_enabled = False  # Auto-fold when locking
        self._auto_adjust_enabled = False  # Auto-adjust position
        
        # Additional features
        self._heating_enabled = False  # Mirror heating
        self._auxiliary_view_enabled = False  # Auxiliary view mode

    # Left mirror properties
    @property
    def left_mirror(self):
        return self._left_mirror

    # Right mirror properties
    @property
    def right_mirror(self):
        return self._right_mirror

    # View page properties
    @property
    def view_page_open(self):
        return self._view_page_open

    @view_page_open.setter
    def view_page_open(self, value):
        if not isinstance(value, bool):
            raise ValueError("view_page_open must be a boolean value")
        self._view_page_open = value

    # Auto-flip properties
    @property
    def auto_flip_enabled(self):
        return self._auto_flip_enabled

    @auto_flip_enabled.setter
    def auto_flip_enabled(self, value):
        if not isinstance(value, bool):
            raise ValueError("auto_flip_enabled must be a boolean value")
        self._auto_flip_enabled = value

    # Auto-fold properties
    @property
    def auto_fold_enabled(self):
        return self._auto_fold_enabled

    @auto_fold_enabled.setter
    def auto_fold_enabled(self, value):
        if not isinstance(value, bool):
            raise ValueError("auto_fold_enabled must be a boolean value")
        self._auto_fold_enabled = value

    # Auto-adjust properties
    @property
    def auto_adjust_enabled(self):
        return self._auto_adjust_enabled

    @auto_adjust_enabled.setter
    def auto_adjust_enabled(self, value):
        if not isinstance(value, bool):
            raise ValueError("auto_adjust_enabled must be a boolean value")
        self._auto_adjust_enabled = value

    # Heating properties
    @property
    def heating_enabled(self):
        return self._heating_enabled

    @heating_enabled.setter
    def heating_enabled(self, value):
        if not isinstance(value, bool):
            raise ValueError("heating_enabled must be a boolean value")
        self._heating_enabled = value

    # Auxiliary view properties
    @property
    def auxiliary_view_enabled(self):
        return self._auxiliary_view_enabled

    @auxiliary_view_enabled.setter
    def auxiliary_view_enabled(self, value):
        if not isinstance(value, bool):
            raise ValueError("auxiliary_view_enabled must be a boolean value")
        self._auxiliary_view_enabled = value

    # Helper methods
    def _get_mirror_by_position(self, position):
        """
        Internal helper to get mirror instance(s) based on position.
        
        Args:
            position (str): The position of the mirror ('left side', 'right side', or 'all')
            
        Returns:
            list: List of tuples containing (mirror_instance, position_name)
        """
        position = RearviewMirror.Position(position)
        
        if position == RearviewMirror.Position.LEFT:
            return [(self.left_mirror, "left_mirror")]
        elif position == RearviewMirror.Position.RIGHT:
            return [(self.right_mirror, "right_mirror")]
        else:  # ALL
            return [(self.left_mirror, "left_mirror"), (self.right_mirror, "right_mirror")]

    def _convert_value_with_unit(self, value, unit, current_value=None):
        """
        Convert a value with specified unit to percentage (0-100).
        
        Args:
            value (float): The value to convert
            unit (str): The unit of the value
            current_value (float, optional): Current value, used for relative adjustments
            
        Returns:
            float: The converted value as percentage
        """
        unit = RearviewMirror.AdjustmentUnit(unit)
        
        if unit == RearviewMirror.AdjustmentUnit.PERCENTAGE:
            return min(max(value, 0), 100)
        elif unit == RearviewMirror.AdjustmentUnit.GEAR:
            # Assuming gears are 1-10, convert to percentage
            return min(max(value * 10, 0), 100)
        elif unit == RearviewMirror.AdjustmentUnit.CENTIMETER:
            # Assuming max range is 10cm, convert to percentage
            return min(max(value * 10, 0), 100)
        else:
            raise ValueError(f"Unsupported unit: {unit}")

    def _adjust_by_degree(self, degree, current_value, adjustment_type="relative"):
        """
        Adjust a value based on degree (large, little, tiny).
        
        Args:
            degree (str): The degree of adjustment
            current_value (float): Current value
            adjustment_type (str): Type of adjustment ("relative" or "absolute")
            
        Returns:
            float: The adjusted value
        """
        if adjustment_type == "relative":
            # For relative adjustments (increase/decrease)
            degree_map = {
                "large": 20.0,
                "little": 10.0,
                "tiny": 5.0
            }
            return min(max(current_value + degree_map.get(degree, 10.0), 0), 100)
        else:
            # For absolute settings (set to specific level)
            degree_map = {
                "max": 100.0,
                "high": 75.0,
                "medium": 50.0,
                "low": 25.0,
                "min": 0.0
            }
            return degree_map.get(degree, 50.0)

    # API Methods
    @api("rearviewMirror")
    def switch(self, switch, position="all"):
        """
        Open (extend) or close (fold) vehicle rearview mirror.
        
        Args:
            switch (bool): True to open mirrors, False to close mirrors
            position (str, optional): Mirror position ('left side', 'right side', or 'all')
                                     Enum values: ['left side', 'right side', 'all']
                                     
        Returns:
            dict: Operation result and updated mirror states
        """
        if not isinstance(switch, bool):
            raise ValueError("switch must be a boolean value")
            
        try:
            mirrors = self._get_mirror_by_position(position)
            updated_mirrors = {}
            
            for mirror, mirror_name in mirrors:
                mirror.is_open = switch
                updated_mirrors[mirror_name] = mirror.to_dict()
                
            return {
                "success": True,
                "message": f"{'Opened' if switch else 'Closed'} {position} rearview mirror(s)",
                "updated_mirrors": updated_mirrors
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @api("rearviewMirror")
    def view_switch(self, switch):
        """
        Open or close rearview mirror page.
        
        Args:
            switch (bool): True to open the page, False to close the page
            
        Returns:
            dict: Operation result and updated page state
        """
        if not isinstance(switch, bool):
            raise ValueError("switch must be a boolean value")
            
        try:
            self.view_page_open = switch
            
            return {
                "success": True,
                "message": f"{'Opened' if switch else 'Closed'} rearview mirror page",
                "view_page_state": {
                    "open": self.view_page_open
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @api("rearviewMirror")
    def mode_autoFlip(self, switch):
        """
        Enable or disable rearview mirror automatic downward flipping when reversing.
        
        Args:
            switch (bool): True to enable auto-flip, False to disable
            
        Returns:
            dict: Operation result and updated auto-flip state
        """
        if not isinstance(switch, bool):
            raise ValueError("switch must be a boolean value")
            
        try:
            self.auto_flip_enabled = switch
            
            return {
                "success": True,
                "message": f"{'Enabled' if switch else 'Disabled'} rearview mirror auto-flip when reversing",
                "auto_flip_state": {
                    "enabled": self.auto_flip_enabled
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @api("rearviewMirror")
    def mode_autoFold(self, switch):
        """
        Enable or disable rearview mirror automatic folding when locking.
        
        Args:
            switch (bool): True to enable auto-fold, False to disable
            
        Returns:
            dict: Operation result and updated auto-fold state
        """
        if not isinstance(switch, bool):
            raise ValueError("switch must be a boolean value")
            
        try:
            self.auto_fold_enabled = switch
            
            return {
                "success": True,
                "message": f"{'Enabled' if switch else 'Disabled'} rearview mirror auto-fold when locking",
                "auto_fold_state": {
                    "enabled": self.auto_fold_enabled
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @api("rearviewMirror")
    def height_increase(self, position="all", value=None, unit=None, degree=None):
        """
        Increase the height of the rearview mirror.
        
        Args:
            position (str): Mirror position ('left side', 'right side', or 'all')
                           Enum values: ['left side', 'right side', 'all']
            value (float, optional): Amount to increase by, with unit
            unit (str, optional): Unit for the value
                                 Enum values: ['gear', 'percentage', 'centimeter']
            degree (str, optional): Degree of adjustment if value/unit not provided
                                   Enum values: ['large', 'little', 'tiny']
                                   
        Returns:
            dict: Operation result and updated mirror states
        """
        try:
            mirrors = self._get_mirror_by_position(position)
            updated_mirrors = {}
            
            for mirror, mirror_name in mirrors:
                current_height = mirror.height
                
                if value is not None and unit is not None:
                    # Convert value to percentage adjustment
                    adjustment = self._convert_value_with_unit(value, unit)
                    new_height = min(current_height + adjustment, 100)
                elif degree is not None:
                    # Adjust based on degree
                    new_height = self._adjust_by_degree(degree, current_height)
                else:
                    # Default adjustment (10%)
                    new_height = min(current_height + 10, 100)
                
                mirror.height = new_height
                updated_mirrors[mirror_name] = mirror.to_dict()
                
            return {
                "success": True,
                "message": f"Increased height of {position} rearview mirror(s)",
                "updated_mirrors": updated_mirrors
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @api("rearviewMirror")
    def height_decrease(self, position="all", value=None, unit=None, degree=None):
        """
        Decrease the height of the rearview mirror.
        
        Args:
            position (str): Mirror position ('left side', 'right side', or 'all')
                           Enum values: ['left side', 'right side', 'all']
            value (float, optional): Amount to decrease by, with unit
            unit (str, optional): Unit for the value
                                 Enum values: ['gear', 'percentage', 'centimeter']
            degree (str, optional): Degree of adjustment if value/unit not provided
                                   Enum values: ['large', 'little', 'tiny']
                                   
        Returns:
            dict: Operation result and updated mirror states
        """
        try:
            mirrors = self._get_mirror_by_position(position)
            updated_mirrors = {}
            
            for mirror, mirror_name in mirrors:
                current_height = mirror.height
                
                if value is not None and unit is not None:
                    # Convert value to percentage adjustment
                    adjustment = self._convert_value_with_unit(value, unit)
                    new_height = max(current_height - adjustment, 0)
                elif degree is not None:
                    # Adjust based on degree (negate for decrease)
                    new_height = self._adjust_by_degree(degree, current_height, "relative")
                    # For decrease, we negate the adjustment
                    new_height = max(2 * current_height - new_height, 0)
                else:
                    # Default adjustment (10%)
                    new_height = max(current_height - 10, 0)
                
                mirror.height = new_height
                updated_mirrors[mirror_name] = mirror.to_dict()
                
            return {
                "success": True,
                "message": f"Decreased height of {position} rearview mirror(s)",
                "updated_mirrors": updated_mirrors
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @api("rearviewMirror")
    def height_set(self, position="all", value=None, unit=None, degree=None):
        """
        Set the height of the rearview mirror to a specific value.
        
        Args:
            position (str): Mirror position ('left side', 'right side', or 'all')
                           Enum values: ['left side', 'right side', 'all']
            value (float, optional): Specific value to set, with unit
            unit (str, optional): Unit for the value
                                 Enum values: ['gear', 'percentage', 'centimeter']
            degree (str, optional): Predefined level if value/unit not provided
                                   Enum values: ['max', 'high', 'medium', 'low', 'min']
                                   
        Returns:
            dict: Operation result and updated mirror states
        """
        if (value is None or unit is None) and degree is None:
            raise ValueError("Either (value and unit) or degree must be provided")
            
        try:
            mirrors = self._get_mirror_by_position(position)
            updated_mirrors = {}
            
            for mirror, mirror_name in mirrors:
                if value is not None and unit is not None:
                    # Convert value to absolute percentage
                    new_height = self._convert_value_with_unit(value, unit)
                elif degree is not None:
                    # Set to predefined level
                    new_height = self._adjust_by_degree(degree, 0, "absolute")
                
                mirror.height = new_height
                updated_mirrors[mirror_name] = mirror.to_dict()
                
            return {
                "success": True,
                "message": f"Set height of {position} rearview mirror(s)",
                "updated_mirrors": updated_mirrors
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @api("rearviewMirror")
    def adjustment_outside(self, position="all", value=None, unit=None, degree=None):
        """
        Adjust the rearview mirror outwards.
        
        Args:
            position (str): Mirror position ('left side', 'right side', or 'all')
                           Enum values: ['left side', 'right side', 'all']
            value (float, optional): Amount to adjust by, with unit
            unit (str, optional): Unit for the value
                                 Enum values: ['gear', 'percentage', 'centimeter']
            degree (str, optional): Degree of adjustment if value/unit not provided
                                   Enum values: ['large', 'little', 'tiny']
                                   
        Returns:
            dict: Operation result and updated mirror states
        """
        try:
            mirrors = self._get_mirror_by_position(position)
            updated_mirrors = {}
            
            for mirror, mirror_name in mirrors:
                current_position = mirror.horizontal_position
                
                if value is not None and unit is not None:
                    # Convert value to percentage adjustment
                    adjustment = self._convert_value_with_unit(value, unit)
                    new_position = min(current_position + adjustment, 100)
                elif degree is not None:
                    # Adjust based on degree
                    new_position = self._adjust_by_degree(degree, current_position)
                else:
                    # Default adjustment (10%)
                    new_position = min(current_position + 10, 100)
                
                mirror.horizontal_position = new_position
                updated_mirrors[mirror_name] = mirror.to_dict()
                
            return {
                "success": True,
                "message": f"Adjusted {position} rearview mirror(s) outwards",
                "updated_mirrors": updated_mirrors
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @api("rearviewMirror")
    def adjustment_inside(self, position="all", value=None, unit=None, degree=None):
        """
        Adjust the rearview mirror inwards.
        
        Args:
            position (str): Mirror position ('left side', 'right side', or 'all')
                           Enum values: ['left side', 'right side', 'all']
            value (float, optional): Amount to adjust by, with unit
            unit (str, optional): Unit for the value
                                 Enum values: ['gear', 'percentage', 'centimeter']
            degree (str, optional): Degree of adjustment if value/unit not provided
                                   Enum values: ['large', 'little', 'tiny']
                                   
        Returns:
            dict: Operation result and updated mirror states
        """
        try:
            mirrors = self._get_mirror_by_position(position)
            updated_mirrors = {}
            
            for mirror, mirror_name in mirrors:
                current_position = mirror.horizontal_position
                
                if value is not None and unit is not None:
                    # Convert value to percentage adjustment
                    adjustment = self._convert_value_with_unit(value, unit)
                    new_position = max(current_position - adjustment, 0)
                elif degree is not None:
                    # Adjust based on degree (negate for inward)
                    new_position = self._adjust_by_degree(degree, current_position, "relative")
                    # For inward, we negate the adjustment
                    new_position = max(2 * current_position - new_position, 0)
                else:
                    # Default adjustment (10%)
                    new_position = max(current_position - 10, 0)
                
                mirror.horizontal_position = new_position
                updated_mirrors[mirror_name] = mirror.to_dict()
                
            return {
                "success": True,
                "message": f"Adjusted {position} rearview mirror(s) inwards",
                "updated_mirrors": updated_mirrors
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @api("rearviewMirror")
    def mode_autoAdjust(self, switch):
        """
        Enable or disable automatic position adjustment for rearview mirror.
        
        Args:
            switch (bool): True to enable auto-adjust, False to disable
            
        Returns:
            dict: Operation result and updated auto-adjust state
        """
        if not isinstance(switch, bool):
            raise ValueError("switch must be a boolean value")
            
        try:
            self.auto_adjust_enabled = switch
            
            return {
                "success": True,
                "message": f"{'Enabled' if switch else 'Disabled'} rearview mirror position auto-adjust",
                "auto_adjust_state": {
                    "enabled": self.auto_adjust_enabled
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @api("rearviewMirror")
    def mode_heating(self, switch):
        """
        Enable or disable rearview mirror heating function.
        
        Args:
            switch (bool): True to enable heating, False to disable
            
        Returns:
            dict: Operation result and updated heating state
        """
        if not isinstance(switch, bool):
            raise ValueError("switch must be a boolean value")
            
        try:
            self.heating_enabled = switch
            
            return {
                "success": True,
                "message": f"{'Enabled' if switch else 'Disabled'} rearview mirror heating",
                "heating_state": {
                    "enabled": self.heating_enabled
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @api("rearviewMirror")
    def mode_assist(self, switch):
        """
        Enable or disable rearview mirror auxiliary view mode.
        
        Args:
            switch (bool): True to enable auxiliary view, False to disable
            
        Returns:
            dict: Operation result and updated auxiliary view state
        """
        if not isinstance(switch, bool):
            raise ValueError("switch must be a boolean value")
            
        try:
            self.auxiliary_view_enabled = switch
            
            return {
                "success": True,
                "message": f"{'Enabled' if switch else 'Disabled'} rearview mirror auxiliary view mode",
                "auxiliary_view_state": {
                    "enabled": self.auxiliary_view_enabled
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }



    def to_dict(self):
        """
        Convert the RearviewMirror instance to a dictionary.
        
        Returns:
            dict: Dictionary representation of the instance
        """
        return {
            "left_mirror": {
                "value": self.left_mirror.to_dict(),
                "description": "State of the left rearview mirror",
                "type": "MirrorState"
            },
            "right_mirror": {
                "value": self.right_mirror.to_dict(),
                "description": "State of the right rearview mirror",
                "type": "MirrorState"
            },
            "view_page_open": {
                "value": self.view_page_open,
                "description": "Rearview mirror page state (open or closed)",
                "type": type(self.view_page_open).__name__
            },
            "auto_flip_enabled": {
                "value": self.auto_flip_enabled,
                "description": "Auto-flip when reversing feature state (enabled or disabled)",
                "type": type(self.auto_flip_enabled).__name__
            },
            "auto_fold_enabled": {
                "value": self.auto_fold_enabled,
                "description": "Auto-fold when locking feature state (enabled or disabled)",
                "type": type(self.auto_fold_enabled).__name__
            },
            "auto_adjust_enabled": {
                "value": self.auto_adjust_enabled,
                "description": "Auto-adjust position feature state (enabled or disabled)",
                "type": type(self.auto_adjust_enabled).__name__
            },
            "heating_enabled": {
                "value": self.heating_enabled,
                "description": "Heating feature state (enabled or disabled)",
                "type": type(self.heating_enabled).__name__
            },
            "auxiliary_view_enabled": {
                "value": self.auxiliary_view_enabled,
                "description": "Auxiliary view mode state (enabled or disabled)",
                "type": type(self.auxiliary_view_enabled).__name__
            }
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a RearviewMirror instance from a dictionary.
        
        Args:
            data (dict): Dictionary representation of a RearviewMirror instance
            
        Returns:
            RearviewMirror: A new instance created from the dictionary
        """
        instance = cls()
        
        # Restore mirror states
        instance._left_mirror = RearviewMirror.MirrorState.from_dict(data["left_mirror"]["value"])
        instance._right_mirror = RearviewMirror.MirrorState.from_dict(data["right_mirror"]["value"])
        
        # Restore other properties
        instance.view_page_open = data["view_page_open"]["value"]
        instance.auto_flip_enabled = data["auto_flip_enabled"]["value"]
        instance.auto_fold_enabled = data["auto_fold_enabled"]["value"]
        instance.auto_adjust_enabled = data["auto_adjust_enabled"]["value"]
        instance.heating_enabled = data["heating_enabled"]["value"]
        instance.auxiliary_view_enabled = data["auxiliary_view_enabled"]["value"]
        
        return instance
    
    @classmethod
    def init1(cls):
        """
        Initialize a RearviewMirror instance with a driving configuration.
        Mirrors are open with standard driving positions.
        
        Returns:
            RearviewMirror: A new instance with driving configuration
        """
        instance = cls()
        
        # Configure mirrors for standard driving position
        instance._left_mirror = RearviewMirror.MirrorState(
            is_open=True,
            height=50.0,  # Medium height
            horizontal_position=75.0  # More outward position for better visibility
        )
        
        instance._right_mirror = RearviewMirror.MirrorState(
            is_open=True,
            height=50.0,  # Medium height
            horizontal_position=75.0  # More outward position for better visibility
        )
        
        # Enable safety features
        instance._auto_flip_enabled = True  # Auto flip when reversing
        instance._auto_fold_enabled = True  # Auto fold when locking
        
        # Other features default to off
        instance._heating_enabled = False
        instance._auxiliary_view_enabled = False
        instance._auto_adjust_enabled = False
        instance._view_page_open = False
        
        return instance

    @classmethod
    def init2(cls):
        """
        Initialize a RearviewMirror instance with a parking/storage configuration.
        Mirrors are closed/folded with automatic features enabled.
        
        Returns:
            RearviewMirror: A new instance with parking/storage configuration
        """
        instance = cls()
        
        # Configure mirrors for parking/storage
        instance._left_mirror = RearviewMirror.MirrorState(
            is_open=False,  # Closed/folded
            height=25.0,    # Lower position
            horizontal_position=25.0  # More inward position
        )
        
        instance._right_mirror = RearviewMirror.MirrorState(
            is_open=False,  # Closed/folded
            height=25.0,    # Lower position
            horizontal_position=25.0  # More inward position
        )
        
        # Enable all automatic features for convenience
        instance._auto_flip_enabled = True
        instance._auto_fold_enabled = True
        instance._auto_adjust_enabled = True
        
        # Enable heating for defrosting capability
        instance._heating_enabled = True
        
        # Additional view features
        instance._auxiliary_view_enabled = False
        instance._view_page_open = False
        
        return instance