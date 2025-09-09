from enum import Enum
from utils import api

class TailLight:
    """
    Tail light entity class, provides control and state management for vehicle tail lights
    """
    
    def __init__(self, is_on=False):
        """
        Initialize TailLight instance
        
        Args:
            is_on (bool): Tail light switch status, default is off
            
        """
        self._is_on = is_on

    
    @property
    def is_on(self):
        """Get tail light switch status"""
        return self._is_on
    
    @is_on.setter
    def is_on(self, value):
        """
        Set tail light switch status
        
        Args:
            value (bool): Tail light switch status, True means on, False means off
        """
        if not isinstance(value, bool):
            raise TypeError("Switch status must be a boolean type")
        
        self._is_on = value
  
    


    def to_dict(self):
        """
        Convert TailLight instance to dictionary
        
        Returns:
            dict: Dictionary containing TailLight instance properties, types, and descriptions
        """
        return {
            "is_on": {
                "value": self.is_on,
                "description": "Tail light switch status, True means on, False means off",
                "type": type(self.is_on).__name__
            }
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Restore TailLight instance from dictionary
        
        Args:
            data (dict): Dictionary containing TailLight instance properties
            
        Returns:
            TailLight: Restored TailLight instance
        """
        is_on = data["is_on"]["value"]
        instance = cls(is_on)
        return instance
    
    @api("tailLight")
    def switch(self, switch):
        """
        Turn on or off the vehicle tail light
        
        Args:
            switch (bool): Tail light switch status, True means on, False means off
            
        Returns:
            dict: Operation result and tail light status information
        """
        try:
            # Set tail light switch status
            self.is_on = switch
            
            return {
                "success": True,
                "message": f"Tail light has been {'turned on' if switch else 'turned off'}",
                "status": self.to_dict()
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "status": self.to_dict()
            }
    
    @classmethod
    def init1(cls):
        """
        Create a tail light instance in standby state
        
        Returns:
            TailLight: Tail light instance in standby state, characterized by:
                    - Off state
                    
        """
        instance = cls(is_on=False)
        return instance

    @classmethod
    def init2(cls):
        """
        Create a tail light instance in warning flash mode
        
        Returns:
            TailLight: Tail light instance in warning flash mode, characterized by:
                    - On state          
        """
        # Create instance
        instance = cls(is_on=True)
        return instance