import threading
from typing import Dict, Any
from module import *
from utils import modules_dict, get_api_content
 
class Environment:
    # Create thread-local storage object to ensure thread safety
    _thread_local = threading.local()
    
    # Default values used for initializing thread-local variables
    _defaults = {
        "volume": 50,
        "sound_channel": "music",
        "unit_system": "mile",
        "timestamp": "2025-04-13 12:00:00",
        "speaker":"driver's seat",
        "temperature":14,
        "language": "Chinese",
        "time_display_format": "24-hour-format"
    }
    
    @classmethod
    def _ensure_initialized(cls):
        """Ensure thread-local variables are initialized"""
        if not hasattr(cls._thread_local, 'volume'):
            cls._thread_local.volume = cls._defaults["volume"]
            cls._thread_local.sound_channel = cls._defaults["sound_channel"]
            cls._thread_local.unit_system = cls._defaults["unit_system"]
            cls._thread_local.timestamp = cls._defaults["timestamp"]
            cls._thread_local.speaker = cls._defaults["speaker"]
            cls._thread_local.temperature = cls._defaults["temperature"]
            cls._thread_local.language = cls._defaults["language"]
            cls._thread_local.time_display_format = cls._defaults["time_display_format"]

    # ----------- Language -----------
    @classmethod
    def set_language(cls, language):
        cls._ensure_initialized()
        cls._thread_local.language = language

    @classmethod
    def get_language(cls):
        cls._ensure_initialized()
        return cls._thread_local.language

    # ----------- Time Display Format -----------
    @classmethod
    def set_time_display_format(cls, time_format):
        cls._ensure_initialized()
        cls._thread_local.time_display_format = time_format

    @classmethod
    def get_time_display_format(cls):
        cls._ensure_initialized()
        return cls._thread_local.time_display_format
    @classmethod
    def get_current_speaker(cls):
        cls._ensure_initialized()
        return cls._thread_local.speaker
    @classmethod
    def set_temperature(cls, temperature):
        cls._ensure_initialized()
        cls._thread_local.temperature = temperature

    @classmethod
    def get_temperature(cls):
        cls._ensure_initialized()
        return cls._thread_local.temperature

    # ----------- Volume -----------
    @classmethod
    def get_timestamp(cls):
        cls._ensure_initialized()
        return cls._thread_local.timestamp

    @classmethod
    def set_volume(cls, volume):
        cls._ensure_initialized()
        cls._thread_local.volume = volume

    @classmethod
    def get_volume(cls):
        cls._ensure_initialized()
        return cls._thread_local.volume

    # ----------- Sound Channel -----------
    @classmethod
    def set_sound_channel(cls, channel):
        cls._ensure_initialized()
        cls._thread_local.sound_channel = channel

    @classmethod
    def get_sound_channel(cls):
        cls._ensure_initialized()
        return cls._thread_local.sound_channel

    # ----------- Unit System -----------
    @classmethod
    def set_unit_system(cls, unit):
        cls._ensure_initialized()
        cls._thread_local.unit_system = unit

    @classmethod
    def get_unit_system(cls):
        cls._ensure_initialized()
        return cls._thread_local.unit_system
        
    @classmethod
    def set_timestamp(cls, timestamp):
        cls._ensure_initialized()
        cls._thread_local.timestamp = timestamp

    # ----------- To Dictionary -----------
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Output Environment class attributes and their descriptions in a structured format"""
        cls._ensure_initialized()
        return {
            "volume": {
                "type": "int",
                "value": cls._thread_local.volume,
                "description": "Volume level (0-100)"
            },
            "sound_channel": {
                "type": "str",
                "value": cls._thread_local.sound_channel,
                "description":  """
                                Current sound channel type, can be music, video, navigation, radio, conversation; There is only one player in the current environment and only one system can use the player at a time, so you need to modify the sound_channel field in the environment to use different systems.
                                - Set to conversation only when making/receiving calls and adjusting call volume
                                - Set to music only when playing music and adjusting music volume
                                - Set to navigation only when adjusting navigation volume, starting navigation, switching destinations, adding/removing waypoints, turning announcements on/off, switching announcement modes
                                - Set to radio only when playing radio and adjusting radio volume
                                - Set to video only when adjusting video volume and playing videos
                                """
            },
            "unit_system": {
                "type": "str",
                "value": cls._thread_local.unit_system,
                "description": "Distance unit system, supports mile or kilometer"
            },
            "timestamp": {
                "type": "str",
                "value": cls._thread_local.timestamp,
                "description": "Current system time"
            },
            "speaker": {
                "type": "str",
                "value": cls._thread_local.speaker,
                "description": """Current speaker location, one of [driver's seat,passenger seat,second row left,second row right,third row left,third row right]
                      User's statements may depend on current speaker:
                      - Front row: the row in front of the speaker, e.g., if speaker is in third row, front row refers to second row
                      - Rear row: the row behind the speaker, e.g., if speaker is in first row, rear row refers to second row
                """
            },
            "temperature": {
                "type": "int",
                "value": cls._thread_local.temperature,
                "description": "Current environment temperature. When air conditioning is on in the car, in cooling mode, environment temperature should be set to the lowest temperature value among all air conditioners; in heating mode, it should be set to the highest temperature value among all air conditioners."
            },
            "language": {
            "type": "str",
            "value": cls._thread_local.language,
            "description": "Current system language"
            },
            "time_display_format": {
                "type": "str",
                "value": cls._thread_local.time_display_format,
                "description": "Time display format, can be '24-hour-format' or '12-hour-format'"
            }
        }


    @classmethod
    def from_dict(cls, data):
        """
        Restore Environment class state from dictionary format.
        
        Args:
            data (dict): Dictionary containing all Environment class attributes
            
        Returns:
            Environment: Configured Environment class
        """
        cls._ensure_initialized()
        
        # Restore each attribute from dictionary
        if "volume" in data and "value" in data["volume"]:
            cls._thread_local.volume = data["volume"]["value"]
        
        if "sound_channel" in data and "value" in data["sound_channel"]:
            cls._thread_local.sound_channel = data["sound_channel"]["value"]
        
        if "unit_system" in data and "value" in data["unit_system"]:
            cls._thread_local.unit_system = data["unit_system"]["value"]
        
        if "timestamp" in data and "value" in data["timestamp"]:
            cls._thread_local.timestamp = data["timestamp"]["value"]
        
        if "speaker" in data and "value" in data["speaker"]:
            cls._thread_local.speaker = data["speaker"]["value"]
    
        if "temperature" in data and "value" in data["temperature"]:
            cls._thread_local.temperature = data["temperature"]["value"]
        
        if "language" in data and "value" in data["language"]:
            cls._thread_local.language = data["language"]["value"]
            
        if "time_display_format" in data and "value" in data["time_display_format"]:
            cls._thread_local.time_display_format = data["time_display_format"]["value"]

        return cls
    
    @classmethod
    def init1(cls):
        """
        Set and return environment with music channel
        
        Returns:
            Environment: Environment set to music channel
        """
        cls._ensure_initialized()
        cls._thread_local.volume = 60
        cls._thread_local.sound_channel = "music"
        cls._thread_local.unit_system = "mile"
        cls._thread_local.timestamp = "2025-04-13 11:00:00"
        return cls
    
    @classmethod
    def init2(cls):
        """
        Set and return environment with video channel
        
        Returns:
            Environment: Environment set to video channel
        """
        cls._ensure_initialized()
        cls._thread_local.volume = 75
        cls._thread_local.sound_channel = "video"
        cls._thread_local.unit_system = "mile"
        cls._thread_local.timestamp = "2025-04-13 12:10:00"
        return cls
    
    @classmethod
    def init3(cls):
        """
        Set and return environment with navigation channel
        
        Returns:
            Environment: Environment set to navigation channel
        """
        cls._ensure_initialized()
        cls._thread_local.volume = 80
        cls._thread_local.sound_channel = "navigation"
        cls._thread_local.unit_system = "kilometer"
        cls._thread_local.timestamp = "2025-04-13 11:30:00"
        return cls
    
    @classmethod
    def init4(cls):
        """
        Set and return environment with radio channel
        
        Returns:
            Environment: Environment set to radio channel
        """
        cls._ensure_initialized()
        cls._thread_local.volume = 50
        cls._thread_local.sound_channel = "radio"
        cls._thread_local.unit_system = "mile"
        cls._thread_local.timestamp = "2025-04-13 13:00:00"
        return cls
    
    @classmethod
    def init5(cls):
        """
        Set and return environment with conversation channel
        
        Returns:
            Environment: Environment set to conversation channel
        """
        cls._ensure_initialized()
        cls._thread_local.volume = 70
        cls._thread_local.sound_channel = "conversation"
        cls._thread_local.unit_system = "mile"
        cls._thread_local.timestamp = "2025-04-13 13:30:00"
        return cls
    @classmethod
    def init6(cls):
        """
        Set and return environment with music channel

        Returns:
            Environment: Environment set to music channel
        """
        cls._ensure_initialized()
        cls._thread_local.volume = 60
        cls._thread_local.sound_channel = "music"
        cls._thread_local.unit_system = "mile"
        cls._thread_local.timestamp = "2025-04-13 12:00:00"
        cls._thread_local.speaker = "driver's seat"
        cls._thread_local.temperature = 15
        return cls
    
    @classmethod
    def init7(cls):
        """
        Set and return environment with music channel

        Returns:
            Environment: Environment set to music channel
        """
        cls._ensure_initialized()
        cls._thread_local.volume = 60
        cls._thread_local.sound_channel = "music"
        cls._thread_local.unit_system = "mile"
        cls._thread_local.timestamp = "2025-04-13 12:00:00"
        cls._thread_local.speaker = "second row left"
        cls._thread_local.temperature = 15
        cls._thread_local.language = "Chinese"
        cls._thread_local.time_display_format = "24-hour-format"
        return cls
    
    @classmethod
    def get_modules(cls):
        return modules_dict
     
    @classmethod
    def get_module_API(cls, modules=[]):
        api_content = get_api_content(modules)
        return api_content
    
    @classmethod
    def export_context(cls):
        cls._ensure_initialized()
        return {
            "volume": cls._thread_local.volume,
            "sound_channel": cls._thread_local.sound_channel,
            "unit_system": cls._thread_local.unit_system,
            "timestamp": cls._thread_local.timestamp,
            "speaker": cls._thread_local.speaker,
            "temperature": cls._thread_local.temperature,
            "language": cls._thread_local.language,
            "time_display_format": cls._thread_local.time_display_format
        }

    @classmethod
    def import_context(cls, context: Dict[str, Any]):
        cls._ensure_initialized()
        for key, value in context.items():
            setattr(cls._thread_local, key, value)