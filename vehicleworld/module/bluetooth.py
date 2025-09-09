from enum import Enum
from typing import List, Dict, Any, Optional
from utils import api

class Bluetooth:
    """
    Bluetooth entity class for car control systems.
    Manages Bluetooth connectivity, device pairing, and connection states.
    """
    
    class ConnectionState(Enum):
        """
        Enum representing possible Bluetooth connection states.
        """
        DISCONNECTED = 0
        CONNECTED = 1
        
    
            
    def __init__(self):
        """
        Initialize the Bluetooth entity with default values.
        """
        self._is_enabled = False
        self._connection_state = Bluetooth.ConnectionState.DISCONNECTED
          
       
        
    @property
    def is_enabled(self) -> bool:
        """
        Get the current Bluetooth enabled state.
        """
        return self._is_enabled
        
    @is_enabled.setter
    def is_enabled(self, value: bool) -> None:
        """
        Set the Bluetooth enabled state.
        """
        self._is_enabled = value
        if not value:
            # When Bluetooth is turned off, reset connection state and disconnect all devices
            self._connection_state = Bluetooth.ConnectionState.DISCONNECTED
            
            
            
    @property
    def connection_state(self) -> ConnectionState:
        """
        Get the current Bluetooth connection state.
        """
        return self._connection_state
        
    @connection_state.setter
    def connection_state(self, value: ConnectionState) -> None:
        """
        Set the Bluetooth connection state.
        """
        self._connection_state = value
    



    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Bluetooth instance to a dictionary.
        """
        return {
            "is_enabled": {
                "value": self.is_enabled,
                "description": "Whether Bluetooth is enabled",
                "type": type(self.is_enabled).__name__
            },
            "connection_state": {
                "value": self.connection_state.name,
                "description": "Current Bluetooth connection state (DISCONNECTED, CONNECTED)",
                "type": "Enum"
            }
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Bluetooth':
        """
        Create a Bluetooth instance from a dictionary.
        """
        bluetooth = cls()
        bluetooth.is_enabled = data["is_enabled"]["value"]
        
        # Set connection state
        conn_state_name = data["connection_state"]["value"]
        bluetooth.connection_state = Bluetooth.ConnectionState[conn_state_name]
        
        return bluetooth
    
    @classmethod
    def init1(cls) -> 'Bluetooth':
        """
        Class method to create a Bluetooth instance with Bluetooth enabled.
        
        Returns:
            Bluetooth: A new Bluetooth instance with Bluetooth enabled and ready to connect.
        """
        bluetooth = cls()
        bluetooth.is_enabled = True
        bluetooth.connection_state = Bluetooth.ConnectionState.CONNECTED
        return bluetooth
        
    @classmethod
    def init2(cls) -> 'Bluetooth':
        """
        Class method to create a Bluetooth instance with Bluetooth disabled.
        
        Returns:
            Bluetooth: A new Bluetooth instance with Bluetooth disabled.
        """
        bluetooth = cls()
        bluetooth.is_enabled = False
        bluetooth.connection_state = Bluetooth.ConnectionState.DISCONNECTED
        return bluetooth

    @api("bluetooth")
    def carcontrol_connection_bluetooth_switch(self, switch: bool) -> Dict[str, Any]:
        """
        Turn on/off Bluetooth for connecting the car system to mobile devices and other equipment.
        
        Args:
            switch (bool): Bluetooth switch, true means on, false means off
            
        Returns:
            Dict: Result of the operation including success status and current Bluetooth state
        """
        # Parameter validation
        if not isinstance(switch, bool):
            return {
                "success": False,
                "error": "Invalid parameter: 'switch' must be a boolean value",
                "current_state": self.to_dict()
            }
            
        # If the Bluetooth state is already set to the requested value, do nothing
        if self.is_enabled == switch:
            return {
                "success": True,
                "message": f"Bluetooth is already {'enabled' if switch else 'disabled'}",
                "current_state": self.to_dict()
            }
            
        try:
            # Set the new Bluetooth state
            self.is_enabled = switch
            
            # If turning on Bluetooth, update connection state
            if switch:
                self.connection_state = Bluetooth.ConnectionState.CONNECTED
                
                
            else:
                # If turning off Bluetooth, ensure all devices are disconnected
                self.connection_state = Bluetooth.ConnectionState.DISCONNECTED
                
            return {
                "success": True,
                "message": f"Bluetooth {'enabled' if switch else 'disabled'} successfully",
                "current_state": self.to_dict()
            }
        except Exception as e:
        
            return {
                "success": False,
                "error": f"Error changing Bluetooth state: {str(e)}",
                "current_state": self.to_dict()
            }
