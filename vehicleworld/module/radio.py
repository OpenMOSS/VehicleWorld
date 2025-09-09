from enum import Enum
from typing import List, Dict, Optional, Union, Any
import time
from dataclasses import dataclass
from utils import api
from module.environment import Environment


class VolumeAdjustmentDegree(Enum):
    """Enum for volume adjustment degrees"""
    MAX = "max"       # Maximum volume
    HIGH = "high"     # High volume
    MEDIUM = "medium" # Medium volume
    LOW = "low"       # Low volume
    MIN = "min"       # Minimum volume


class VolumeChangeDegree(Enum):
    """Enum for volume change degrees"""
    LARGE = "large"   # Large volume change
    LITTLE = "little" # Little volume change
    TINY = "tiny"     # Tiny volume change


@dataclass
class RadioStation:
    """Radio station data structure"""
    name: str                  # Name of the radio station
    frequency_value: str       # Frequency value of the radio station (e.g., "98.5 MHz")
    city: str = ""             # City where the radio station is available
    app_name: str = ""         # App name used to play this radio station
    timestamp: float = 0.0     # Timestamp when this station was last played
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert RadioStation to dictionary"""
        return {
            "name": {"type": "str", "value": self.name, "description": "Name of the radio station"},
            "frequency_value": {"type": "str", "value": self.frequency_value, "description": "Frequency value of the radio station"},
            "city": {"type": "str", "value": self.city, "description": "City where the radio station is available"},
            "app_name": {"type": "str", "value": self.app_name, "description": "App name used to play this radio station"},
            "timestamp": {"type": "float", "value": self.timestamp, "description": "Timestamp when this station was last played"}
        }


class Radio:
    """Radio entity class implementing all radio related APIs"""
    
    def __init__(self):
        """Initialize Radio class with default values"""
        station1 = RadioStation(
        name="WBEZ Chicago",
        frequency_value="91.5 MHz",
        city="Chicago",
        app_name="Chicago Public Radio",
        timestamp=time.time() - 3600  # 1 hour ago
        )
        
        station2 = RadioStation(
            name="WNYC",
            frequency_value="93.9 MHz",
            city="New York",
            app_name="NYC Public Radio",
            timestamp=time.time() - 7200  # 2 hours ago
        )
        # History of played radio stations (most recent first)
        self._history: List[RadioStation] = [station1, station2]
        
        # Collection of favorite radio stations
        self._collection: List[RadioStation] = [
            RadioStation(
            name="Classic Rock",
            frequency_value="98.5 MHz",
            city="Los Angeles",
            app_name="Rock Radio"
        )]
        
        # Currently playing radio station
        self._current_station: Optional[RadioStation] = None
        
        # Radio play state
        self._is_playing: bool = False
        
        # Maximum history size
        self._max_history_size: int = 50
        
        # Volume change mapping for degrees
        self._volume_change_mapping = {
            VolumeChangeDegree.LARGE.value: 20,
            VolumeChangeDegree.LITTLE.value: 10,
            VolumeChangeDegree.TINY.value: 5
        }
        
        # Volume setting mapping for degrees
        self._volume_set_mapping = {
            VolumeAdjustmentDegree.MAX.value: 100,
            VolumeAdjustmentDegree.HIGH.value: 80,
            VolumeAdjustmentDegree.MEDIUM.value: 50,
            VolumeAdjustmentDegree.LOW.value: 30,
            VolumeAdjustmentDegree.MIN.value: 10
        }
    
    # Getter and setter for history
    def get_history(self) -> List[RadioStation]:
        """Get the history of played radio stations"""
        return self._history
    
    def set_history(self, history: List[RadioStation]) -> None:
        """Set the history of played radio stations"""
        self._history = history
    
    def add_to_history(self, station: RadioStation) -> None:
        """Add a radio station to history"""
        # Check if this station already exists in history
        for i, hist_station in enumerate(self._history):
            if hist_station.name == station.name and hist_station.frequency_value == station.frequency_value:
                # Remove the existing entry
                self._history.pop(i)
                break
        
        # Add to the beginning of history (most recent)
        station.timestamp = Environment.get_timestamp()
        self._history.insert(0, station)
        
        # Limit history size
        if len(self._history) > self._max_history_size:
            self._history = self._history[:self._max_history_size]
    
    # Getter and setter for collection
    def get_collection(self) -> List[RadioStation]:
        """Get the collection of favorite radio stations"""
        return self._collection
    
    def set_collection(self, collection: List[RadioStation]) -> None:
        """Set the collection of favorite radio stations"""
        self._collection = collection
    
    def add_to_collection(self, station: RadioStation) -> bool:
        """Add a radio station to collection if not already present"""
        for coll_station in self._collection:
            if coll_station.name == station.name and coll_station.frequency_value == station.frequency_value:
                return False  # Already in collection
        
        self._collection.append(station)
        return True
    
    def remove_from_collection(self, station: RadioStation) -> bool:
        """Remove a radio station from collection if present"""
        for i, coll_station in enumerate(self._collection):
            if coll_station.name == station.name and coll_station.frequency_value == station.frequency_value:
                self._collection.pop(i)
                return True
        
        return False  # Not in collection
    
    def is_in_collection(self, station: RadioStation) -> bool:
        """Check if a radio station is in collection"""
        for coll_station in self._collection:
            if coll_station.name == station.name and coll_station.frequency_value == station.frequency_value:
                return True
        
        return False
    
    # Getter and setter for current station
    def get_current_station(self) -> Optional[RadioStation]:
        """Get the currently playing radio station"""
        return self._current_station
    
    def set_current_station(self, station: Optional[RadioStation]) -> None:
        """Set the currently playing radio station"""
        self._current_station = station
        if station:
            # Add to history when setting a new station
            self.add_to_history(station)
    
    # Getter and setter for is_playing
    def get_is_playing(self) -> bool:
        """Get the radio play state"""
        return self._is_playing
    
    def set_is_playing(self, is_playing: bool) -> None:
        """Set the radio play state"""
        self._is_playing = is_playing
        
        # Set sound channel to radio when playing
        if is_playing:
            Environment.set_sound_channel("radio")


    
    # API implementation methods
    @api("radio")
    def radio_history_view(self) -> Dict[str, Any]:
        """View history of radio"""
        return {
            "status": "success",
            "history": [station.to_dict() for station in self._history],
            "count": len(self._history)
        }
    
    @api("radio")
    def radio_play_stop(self) -> Dict[str, Any]:
        """
        Stop playing the current radio station.
        
        Returns:
        Dict: Dictionary containing operation results
        """
        # Check if radio is currently playing
        if not self.is_playing:
            return {
                "success": False,
                "message": "Radio is not currently playing",
                "status": "Already stopped"
            }
        
        # Set the current playing state to false
        self.set_is_playing(False)
        
        # Return success message
        return {
            "success": True,
            "message": "Radio playback stopped",
            "status": "Stopped",
            "station_info": self._current_station.name if self._current_station else "None"
        }

    @api("radio")
    def radio_local_play(self) -> Dict[str, Any]:
        """Play local radio"""
        # If there's no local station in history, create a default one
        local_station = None
        
        for station in self._history:
            if station.city:  # If city is set, consider it a local station
                local_station = station
                break
        
        if not local_station:
            # Create a default local station
            local_station = RadioStation(
                name="Local Radio",
                frequency_value="102.5 MHz",
                city="Current City",  # In a real system, this would be obtained from GPS
                app_name="Default Radio App"
            )
        
        # Set and play the local station
        self.set_current_station(local_station)
        self.set_is_playing(True)
        Environment.set_sound_channel("radio")
        return {
            "status": "success",
            "message": f"Playing local radio: {local_station.name}",
            "station": local_station.to_dict()
        }
    
    @api("radio")
    def radio_recent_play(self) -> Dict[str, Any]:
        """Play recently played radio"""
        if not self._history:
            return {
                "status": "error",
                "message": "No recently played radio stations"
            }
        
        # Get the most recent station (first in history)
        recent_station = self._history[0]
        Environment.set_sound_channel("radio")
        # Set and play the recent station
        self.set_current_station(recent_station)
        self.set_is_playing(True)
        
        return {
            "status": "success",
            "message": f"Playing recently played radio: {recent_station.name}",
            "station": recent_station.to_dict()
        }
    
    @api("radio")
    def radio_collect(self, collect: bool) -> Dict[str, Any]:
        """Favorite/Unfavorite radio
        
        Args:
            collect (bool): True to favorite radio, False to unfavorite
        """
        current_station = self.get_current_station()
        
        if not current_station:
            return {
                "status": "error",
                "message": "No radio station is currently playing"
            }
        
        if collect:
            # Add to collection
            result = self.add_to_collection(current_station)
            if result:
                return {
                    "status": "success",
                    "message": f"Added {current_station.name} to favorites",
                    "station": current_station.to_dict()
                }
            else:
                return {
                    "status": "info",
                    "message": f"{current_station.name} is already in favorites",
                    "station": current_station.to_dict()
                }
        else:
            # Remove from collection
            result = self.remove_from_collection(current_station)
            if result:
                return {
                    "status": "success",
                    "message": f"Removed {current_station.name} from favorites",
                    "station": current_station.to_dict()
                }
            else:
                return {
                    "status": "info",
                    "message": f"{current_station.name} is not in favorites",
                    "station": current_station.to_dict()
                }
    
    @api("radio")
    def radio_collection_view(self) -> Dict[str, Any]:
        """View favorite radio"""
        return {
            "status": "success",
            "favorites": [station.to_dict() for station in self._collection],
            "count": len(self._collection)
        }
    
    @api("radio")
    def radio_favorite_play(self) -> Dict[str, Any]:
        """Play favorite (saved) radio"""
        if not self._collection:
            return {
                "status": "error",
                "message": "No favorite radio stations"
            }
        Environment.set_sound_channel("radio")
        # Get the first favorite station
        favorite_station = self._collection[0]
        
        # Set and play the favorite station
        self.set_current_station(favorite_station)
        self.set_is_playing(True)
        
        return {
            "status": "success",
            "message": f"Playing favorite radio: {favorite_station.name}",
            "station": favorite_station.to_dict()
        }
    
    @api("radio")
    def radio_soundVolume_increase(self, value: Optional[int] = None, 
                                  degree: Optional[str] = None) -> Dict[str, Any]:
        """Increase radio volume
        
        Args:
            value (Optional[int]): Numeric part of specific volume increase value, 
                                  mutually exclusive with degree, between 0-100
            degree (Optional[str]): Different levels of volume increase, 
                                   mutually exclusive with value.
                                   Enum values: ["large", "little", "tiny"]
        """
        Environment.set_sound_channel("radio")
        current_volume = Environment.get_volume()
        new_volume = current_volume
        
        if value is not None:
            # Increase by specific value
            new_volume = min(current_volume + value, 100)
        elif degree is not None:
            # Increase by degree
            if degree not in [d.value for d in VolumeChangeDegree]:
                return {
                    "status": "error",
                    "message": f"Invalid degree: {degree}. Must be one of {[d.value for d in VolumeChangeDegree]}"
                }
            
            volume_change = self._volume_change_mapping.get(degree, 10)
            new_volume = min(current_volume + volume_change, 100)
        else:
            # Default increase (if neither value nor degree is provided)
            new_volume = min(current_volume + 10, 100)
        
        # Set the new volume
        Environment.set_volume(new_volume)
        
        return {
            "status": "success",
            "message": f"Increased volume from {current_volume} to {new_volume}",
            "previous_volume": current_volume,
            "current_volume": new_volume
        }
    
    @api("radio")
    def radio_soundVolume_decrease(self, value: Optional[int] = None, 
                                  degree: Optional[str] = None) -> Dict[str, Any]:
        """Decrease radio volume
        
        Args:
            value (Optional[int]): Numeric part of specific volume decrease value, 
                                  mutually exclusive with degree, between 0-100
            degree (Optional[str]): Different levels of volume decrease, 
                                   mutually exclusive with value.
                                   Enum values: ["large", "little", "tiny"]
        """
        Environment.set_sound_channel("radio")
        current_volume = Environment.get_volume()
        new_volume = current_volume
        
        if value is not None:
            # Decrease by specific value
            new_volume = max(current_volume - value, 0)
        elif degree is not None:
            # Decrease by degree
            if degree not in [d.value for d in VolumeChangeDegree]:
                return {
                    "status": "error",
                    "message": f"Invalid degree: {degree}. Must be one of {[d.value for d in VolumeChangeDegree]}"
                }
            
            volume_change = self._volume_change_mapping.get(degree, 10)
            new_volume = max(current_volume - volume_change, 0)
        else:
            # Default decrease (if neither value nor degree is provided)
            new_volume = max(current_volume - 10, 0)
        
        # Set the new volume
        Environment.set_volume(new_volume)
        
        return {
            "status": "success",
            "message": f"Decreased volume from {current_volume} to {new_volume}",
            "previous_volume": current_volume,
            "current_volume": new_volume
        }
    
    @api("radio")
    def radio_soundVolume_set(self, value: Optional[int] = None, 
                             degree: Optional[str] = None) -> Dict[str, Any]:
        """Set radio volume adjustment
        
        Args:
            value (Optional[int]): Numeric part of specific volume adjustment value, 
                                  mutually exclusive with degree, between 0-100
            degree (Optional[str]): Different levels of volume adjustment, 
                                   mutually exclusive with value.
                                   Enum values: ["max", "high", "medium", "low", "min"]
        """
        Environment.set_sound_channel("radio")
        if value is None and degree is None:
            return {
                "status": "error",
                "message": "Either value or degree must be provided"
            }
        
        current_volume = Environment.get_volume()
        new_volume = current_volume
        
        if value is not None:
            # Set to specific value
            if value < 0 or value > 100:
                return {
                    "status": "error",
                    "message": f"Invalid volume value: {value}. Must be between 0 and 100"
                }
            
            new_volume = value
        elif degree is not None:
            # Set by degree
            if degree not in [d.value for d in VolumeAdjustmentDegree]:
                return {
                    "status": "error",
                    "message": f"Invalid degree: {degree}. Must be one of {[d.value for d in VolumeAdjustmentDegree]}"
                }
            
            new_volume = self._volume_set_mapping.get(degree, 50)
        
        # Set the new volume
        Environment.set_volume(new_volume)
        
        return {
            "status": "success",
            "message": f"Set volume from {current_volume} to {new_volume}",
            "previous_volume": current_volume,
            "current_volume": new_volume
        }
    
    @api("radio")
    def radio_play(self, radioValue: Optional[str] = None, 
                  radioName: Optional[str] = None,
                  city: Optional[str] = None,
                  appName: Optional[str] = None) -> Dict[str, Any]:
        """Play radio
        
        Args:
            radioValue (Optional[str]): Selected frequency band
            radioName (Optional[str]): Selected radio station name
            city (Optional[str]): Selected city radio station
            appName (Optional[str]): Name of the application used
        """
        # If the radio is already playing, toggle it off
        if self._is_playing and self._current_station:
            # self.set_is_playing(False)
            station = self._current_station
            return {
                "status": "success",
                "message": f"{station.name} is already playing",
                "station": station.to_dict(),
                "is_playing": True
            }
        
        # If no parameters provided, resume current station or play the most recent
        if not any([radioValue, radioName, city, appName]):
            if self._current_station:
                # Resume current station
                self.set_is_playing(True)
                return {
                    "status": "success",
                    "message": f"Resumed radio: {self._current_station.name}",
                    "station": self._current_station.to_dict(),
                    "is_playing": True
                }
            elif self._history:
                # Play most recent station
                return self.radio_recent_play()
            else:
                # No station to play
                return {
                    "status": "error",
                    "message": "No radio station to play"
                }
        
        # Create a new station with the provided parameters
        name = radioName or "Unknown Station"
        frequency = radioValue or "Unknown Frequency"
        
        new_station = RadioStation(
            name=name,
            frequency_value=frequency,
            city=city or "",
            app_name=appName or ""
        )
        
        # Set and play the new station
        Environment.set_sound_channel("radio")
        self.set_current_station(new_station)
        self.set_is_playing(True)
        
        return {
            "status": "success",
            "message": f"Playing radio: {new_station.name}",
            "station": new_station.to_dict(),
            "is_playing": True
        }
    


    def to_dict(self) -> Dict[str, Any]:
        """Convert Radio instance to dictionary with attribute types and descriptions"""
        
        return {
            "_history": {
                "type": "List[RadioStation]",
                "value": [station.to_dict() for station in self._history],
                "description": "History of played radio stations (most recent first),when you play a radio,you need to insert the radio to the first of the list"
            },
            "_collection": {
                "type": "List[RadioStation]",
                "value": [station.to_dict() for station in self._collection],
                "description": "Collection of favorite radio stations"
            },
            "_current_station": {
                "type": "Optional[RadioStation]",
                "value": self._current_station.to_dict() if self._current_station else None,
                "description": "Currently playing radio station: if _is_playing is set to True, plays the most recently played station by default when no specific station is specified."
            },
            "_is_playing": {
                "type": "bool",
                "value": self._is_playing,
                "description": "Radio play state"
            },
            "_max_history_size": {
                "type": "int",
                "value": self._max_history_size,
                "description": "Maximum history size"
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Radio':
        """
        Reconstruct a Radio instance from a dictionary.
        
        Args:
            data (Dict[str, Any]): Dictionary containing Radio data
            
        Returns:
            Radio: A new Radio instance with the data from the dictionary
        """
        radio = cls()
        
        # Restore history
        if "_history" in data and "value" in data["_history"]:
            history_data = data["_history"]["value"]
            radio._history = []
            for station_dict in history_data:
                station = RadioStation(
                    name=station_dict["name"]["value"],
                    frequency_value=station_dict["frequency_value"]["value"],
                    city=station_dict["city"]["value"],
                    app_name=station_dict["app_name"]["value"],
                    timestamp=station_dict["timestamp"]["value"]
                )
                radio._history.append(station)
        
        # Restore collection
        if "_collection" in data and "value" in data["_collection"]:
            collection_data = data["_collection"]["value"]
            radio._collection = []
            for station_dict in collection_data:
                station = RadioStation(
                    name=station_dict["name"]["value"],
                    frequency_value=station_dict["frequency_value"]["value"],
                    city=station_dict["city"]["value"],
                    app_name=station_dict["app_name"]["value"],
                    timestamp=station_dict["timestamp"]["value"]
                )
                radio._collection.append(station)
        
        # Restore current station
        if "_current_station" in data and "value" in data["_current_station"] and data["_current_station"]["value"]:
            station_dict = data["_current_station"]["value"]
            radio._current_station = RadioStation(
                name=station_dict["name"]["value"],
                frequency_value=station_dict["frequency_value"]["value"],
                city=station_dict["city"]["value"],
                app_name=station_dict["app_name"]["value"],
                timestamp=station_dict["timestamp"]["value"]
            )
        else:
            radio._current_station = None
        
        # Restore playing state
        if "_is_playing" in data and "value" in data["_is_playing"]:
            radio._is_playing = data["_is_playing"]["value"]
        
        # Restore max history size
        if "_max_history_size" in data and "value" in data["_max_history_size"]:
            radio._max_history_size = data["_max_history_size"]["value"]
        
        return radio
    
    @classmethod
    def init1(cls):
        """
        Create a Radio instance that is already playing a station with a collection
        of various preset stations added to history and favorites.
        
        Returns:
            Radio: A new Radio instance with a station already playing and diverse stations in collection
        """
        radio = cls()
        
        # Create a variety of radio stations
        pop_station = RadioStation(
            name="Top 40 Hits",
            frequency_value="102.7 MHz",
            city="Los Angeles",
            app_name="iHeartRadio",
            timestamp=Environment.get_timestamp()
        )
        
        rock_station = RadioStation(
            name="Classic Rock FM",
            frequency_value="98.5 MHz",
            city="Seattle",
            app_name="Rock Radio",
            timestamp=Environment.get_timestamp() # 1 hour ago
        )
        
        news_station = RadioStation(
            name="News 24/7",
            frequency_value="89.9 MHz",
            city="Washington DC",
            app_name="NPR One",
            timestamp=Environment.get_timestamp()  # 2 hours ago
        )
        
        jazz_station = RadioStation(
            name="Smooth Jazz",
            frequency_value="104.3 MHz",
            city="New Orleans",
            app_name="Jazz FM",
            timestamp=Environment.get_timestamp()  # 3 hours ago
        )
        
        classical_station = RadioStation(
            name="Classical Masterpieces",
            frequency_value="91.3 MHz",
            city="Boston",
            app_name="Classical Radio",
            timestamp=Environment.get_timestamp()  # 4 hours ago
        )
        
        country_station = RadioStation(
            name="Country Hits",
            frequency_value="95.5 MHz",
            city="Nashville",
            app_name="Country Music App",
            timestamp=Environment.get_timestamp()  # 5 hours ago
        )
        
        # Set current playing station
        radio.set_current_station(pop_station)
        radio._is_playing = True
        Environment.set_sound_channel("radio")
        
        # Add stations to history (most recent first)
        radio._history = [
            pop_station,
            rock_station,
            news_station,
            jazz_station,
            classical_station,
            country_station
        ]
        
        # Add some stations to favorites collection
        radio._collection = [
            rock_station,
            jazz_station,
            country_station
        ]
        

        return radio

    @classmethod
    def init2(cls):
        """
        Create a Radio instance with radio turned off but with a diverse collection
        of stations in history and favorites.
        
        Returns:
            Radio: A new Radio instance with radio turned off and diverse stations in collection
        """
        radio = cls()
        
        # Create a variety of radio stations
        local_news = RadioStation(
            name="Local News Radio",
            frequency_value="88.1 MHz",
            city="Chicago",
            app_name="City News App",
            timestamp=Environment.get_timestamp()
        )
        
        sports_station = RadioStation(
            name="Sports Talk Radio",
            frequency_value="97.1 MHz",
            city="Dallas",
            app_name="Sports FM",
            timestamp=Environment.get_timestamp()
        )
        
        talk_station = RadioStation(
            name="Talk Radio Today",
            frequency_value="106.7 MHz",
            city="Atlanta",
            app_name="Talk Radio App",
            timestamp=Environment.get_timestamp()
        )
        
        indie_station = RadioStation(
            name="Indie Music Channel",
            frequency_value="90.5 MHz",
            city="Portland",
            app_name="Independent Music",
            timestamp=Environment.get_timestamp()
        )
        
        international_station = RadioStation(
            name="World Music",
            frequency_value="99.1 MHz",
            city="San Francisco",
            app_name="Global Sounds",
            timestamp=Environment.get_timestamp()
        )
        
        oldies_station = RadioStation(
            name="Oldies But Goodies",
            frequency_value="94.7 MHz",
            city="Miami",
            app_name="Retro Hits",
            timestamp=Environment.get_timestamp()
        )
        
        # Set history with diverse stations
        radio._history = [
            local_news,
            sports_station,
            talk_station,
            indie_station,
            international_station,
            oldies_station
        ]
        
        # Add some stations to favorites collection
        radio._collection = [
            indie_station,
            oldies_station,
            international_station
        ]
        
        # Set current station but keep radio off
        radio._current_station = None
        radio.set_is_playing(False)
        
        return radio