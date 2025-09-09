from enum import Enum
from utils import api

class FuelPort:
    """
    FuelPort entity class representing a vehicle's fuel port system.
    Manages the state of the fuel port including open/close status and lock status.
    """
    
    class FuelPortState(Enum):
        """
        Enum representing the possible states of the fuel port.
        """
        CLOSED = 0
        OPEN = 1
    
    class FuelPortLockState(Enum):
        """
        Enum representing the possible lock states of the fuel port.
        """
        UNLOCKED = 0
        LOCKED = 1
    
    def __init__(self):
        """
        Initialize the fuel port with default values.
        By default, the fuel port is closed and unlocked.
        """
        self._state = FuelPort.FuelPortState.CLOSED
        self._lock_state = FuelPort.FuelPortLockState.UNLOCKED
    
    # Property for state (open/closed)
    @property
    def state(self):
        """Get the current state of the fuel port (open/closed)."""
        return self._state
    
    @state.setter
    def state(self, value):
        """Set the state of the fuel port."""
        if not isinstance(value, FuelPort.FuelPortState):
            raise TypeError("State must be a FuelPortState enum value")
        self._state = value
    
    # Property for lock_state (locked/unlocked)
    @property
    def lock_state(self):
        """Get the current lock state of the fuel port."""
        return self._lock_state
    
    @lock_state.setter
    def lock_state(self, value):
        """Set the lock state of the fuel port."""
        if not isinstance(value, FuelPort.FuelPortLockState):
            raise TypeError("Lock state must be a FuelPortLockState enum value")
        self._lock_state = value
    
    # Helper property to check if fuel port is open
    @property
    def is_open(self):
        """Check if the fuel port is open."""
        return self._state == FuelPort.FuelPortState.OPEN
    
    # Helper property to check if fuel port is locked
    @property
    def is_locked(self):
        """Check if the fuel port is locked."""
        return self._lock_state == FuelPort.FuelPortLockState.LOCKED
    
    @api("fuelPort")
    def switch(self, switch):
        """
        Open or close the vehicle's fuel port.
        
        Args:
            switch (bool): True to open the fuel port, False to close it.
                           
        Returns:
            dict: A dictionary containing operation result and current state.
        
        Raises:
            ValueError: If the fuel port is locked and an attempt is made to open it.
        """
        try:
            # Parameter validation
            if not isinstance(switch, bool):
                raise TypeError("Switch parameter must be a boolean")
            
            # Check if fuel port is locked when trying to open
            if switch and self.is_locked:
                raise ValueError("Cannot open fuel port while it is locked")
            
            # Set the state
            if switch:
                self.state = FuelPort.FuelPortState.OPEN
            else:
                self.state = FuelPort.FuelPortState.CLOSED
                
            return {
                "success": True,
                "message": f"Fuel port {'opened' if switch else 'closed'} successfully",
                "current_state": self.to_dict()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "current_state": self.to_dict()
            }
    
    @api("fuelPort")
    def lock_switch(self, switch):
        """
        Lock or unlock the vehicle's fuel port.
        
        Args:
            switch (bool): True to lock the fuel port, False to unlock it.
                           
        Returns:
            dict: A dictionary containing operation result and current state.
            
        Raises:
            ValueError: If the fuel port is open and an attempt is made to lock it.
        """
        try:
            # Parameter validation
            if not isinstance(switch, bool):
                raise TypeError("Switch parameter must be a boolean")
            
            # Check if fuel port is open when trying to lock
            if switch and self.is_open:
                raise ValueError("Cannot lock fuel port while it is open")
            
            # Set the lock state
            if switch:
                self.lock_state = FuelPort.FuelPortLockState.LOCKED
            else:
                self.lock_state = FuelPort.FuelPortLockState.UNLOCKED
                
            return {
                "success": True,
                "message": f"Fuel port {'locked' if switch else 'unlocked'} successfully",
                "current_state": self.to_dict()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "current_state": self.to_dict()
            }
    


    def to_dict(self):
        """
        Convert the FuelPort instance to a dictionary with detailed information.
        
        Returns:
            dict: Dictionary representation of the FuelPort instance.
        """
        return {
            "state": {
                "value": self.state.name,
                "description": "Current state of the fuel port (OPEN/CLOSED)",
                "type": "FuelPortState",
                "enum_values": [state.name for state in FuelPort.FuelPortState]
            },
            "lock_state": {
                "value": self.lock_state.name,
                "description": "Current lock state of the fuel port (LOCKED/UNLOCKED)",
                "type": "FuelPortLockState",
                "enum_values": [state.name for state in FuelPort.FuelPortLockState]
            },
            "is_open": {
                "value": self.is_open,
                "description": "Indicates if the fuel port is currently open",
                "type": "bool"
            },
            "is_locked": {
                "value": self.is_locked,
                "description": "Indicates if the fuel port is currently locked",
                "type": "bool"
            }
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a FuelPort instance from dictionary data.
        
        Args:
            data (dict): Dictionary containing FuelPort properties.
            
        Returns:
            FuelPort: A new FuelPort instance with the specified properties.
        """
        instance = cls()
        
        # Set state
        state_name = data.get("state", {}).get("value", "CLOSED")
        if hasattr(FuelPort.FuelPortState, state_name):
            instance.state = getattr(FuelPort.FuelPortState, state_name)
        
        # Set lock state
        lock_state_name = data.get("lock_state", {}).get("value", "UNLOCKED")
        if hasattr(FuelPort.FuelPortLockState, lock_state_name):
            instance.lock_state = getattr(FuelPort.FuelPortLockState, lock_state_name)
        
        return instance
    
    @classmethod
    def init1(cls):
        """
        Initialize a FuelPort instance with an open and unlocked state.
        
        Returns:
            FuelPort: A new FuelPort instance in open and unlocked state.
        """
        instance = cls()
        instance.state = FuelPort.FuelPortState.OPEN
        instance.lock_state = FuelPort.FuelPortLockState.UNLOCKED
        return instance

    @classmethod
    def init2(cls):
        """
        Initialize a FuelPort instance with a closed and locked state.
        
        Returns:
            FuelPort: A new FuelPort instance in closed and locked state.
        """
        instance = cls()
        instance.state = FuelPort.FuelPortState.CLOSED
        instance.lock_state = FuelPort.FuelPortLockState.LOCKED
        return instance