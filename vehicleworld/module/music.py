import sys
sys.path.append("../")
from enum import Enum
from typing import List, Dict, Optional, Any, Union
import json
from utils import api
from module.environment import Environment

class VolumeAdjustmentDegree(Enum):
    """Volume adjustment degree enumeration"""
    # Increase/decrease volume degree
    LARGE = "large"
    LITTLE = "little" 
    TINY = "tiny"
    # Set volume degree
    MAX = "max"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MIN = "min"


class PlaybackMode(Enum):
    """Playback mode enumeration"""
    SINGLE_REPEAT = "Single Repeat"
    SHUFFLE_PLAY = "Shuffle Play"
    SEQUENTIAL_PLAY = "Sequential Play"
    LIST_REPEAT = "List Repeat"


class MusicTrack:
    """Music track class"""
    def __init__(self, 
                 id: str = "", 
                 title: str = "", 
                 artist: str = "", 
                 album: str = "",
                 duration: int = 0,
                 is_favorite: bool = False,
                 is_local: bool = False,
                 is_downloaded: bool = False,
                 lyrics: str = "",
                 play_count: int = 0,
                 last_played: Optional[str] = None):
        self.id = id                          # Music ID
        self.title = title                    # Song title
        self.artist = artist                  # Artist
        self.album = album                    # Album name
        self.duration = duration              # Duration (seconds)
        self.is_favorite = is_favorite        # Is favorite
        self.is_local = is_local              # Is local music
        self.is_downloaded = is_downloaded    # Is downloaded
        self.lyrics = lyrics                  # Lyrics
        self.play_count = play_count          # Play count
        self.last_played = last_played        # Last played time
    

    
    def to_dict(self) -> Dict[str, Any]:
        """Convert MusicTrack instance to dictionary with attribute types and descriptions"""
        return {
            "id": {
                "type": "str",
                "value": self.id,
                "description": "Music ID"
            },
            "title": {
                "type": "str",
                "value": self.title,
                "description": "Song title"
            },
            "artist": {
                "type": "str",
                "value": self.artist,
                "description": "Artist"
            },
            "album": {
                "type": "str",
                "value": self.album,
                "description": "Album name"
            },
            "duration": {
                "type": "int",
                "value": self.duration,
                "description": "Duration (seconds)"
            },
            "is_favorite": {
                "type": "bool",
                "value": self.is_favorite,
                "description": "Is favorite"
            },
            "is_local": {
                "type": "bool",
                "value": self.is_local,
                "description": "Is local music"
            },
            "is_downloaded": {
                "type": "bool",
                "value": self.is_downloaded,
                "description": "Is downloaded"
            },
            "lyrics": {
                "type": "str",
                "value": self.lyrics,
                "description": "Lyrics"
            },
            "play_count": {
                "type": "int",
                "value": self.play_count,
                "description": "Play count"
            },
            "last_played": {
                "type": "Optional[str]",
                "value": self.last_played,
                "description": "Last played time"
            }
        }


class Musician:
    """Musician information class"""
    def __init__(self, 
                 name: str = "", 
                 gender: str = "", 
                 nationality: str = "", 
                 birth_date: str = ""):
        self.name = name                      # Name
        self.gender = gender                  # Gender
        self.nationality = nationality        # Nationality
        self.birth_date = birth_date          # Birth date
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Musician instance to dictionary with attribute types and descriptions"""
        return {
            "name": {
                "type": "str",
                "value": self.name,
                "description": "Name"
            },
            "gender": {
                "type": "str",
                "value": self.gender,
                "description": "Gender"
            },
            "nationality": {
                "type": "str",
                "value": self.nationality,
                "description": "Nationality"
            },
            "birth_date": {
                "type": "str",
                "value": self.birth_date,
                "description": "Birth date"
            }
        }
    
    def __str__(self) -> str:
        return f"{self.name}, {self.gender}, {self.nationality}, {self.birth_date}"


class Music:
    """Music system entity class"""
    
    def __init__(self):
        # Playback status
        self._is_playing = False                      # Is playing
        self._current_track_index = -1                # Current track index
        self._playback_mode = PlaybackMode.SEQUENTIAL_PLAY  # Playback mode
        self._show_lyrics = False                     # Show lyrics
        self._show_playlist = False                   # Show playlist
        
        # Track collections
        self._tracks = []                             # All tracks list
        self._current_playlist = []                   # Current playlist
        self._history_tracks = []                     # History playlist
        self._favorite_tracks = []                    # Favorite tracks list
        self._local_tracks = []                       # Local tracks list
        self._downloaded_tracks = []                  # Downloaded tracks list
        
        # Initialize demo data
        self._initialize_demo_data()
    
    def _initialize_demo_data(self):
        """Initialize demo data"""
        # Create some demo music tracks
        track1 = MusicTrack(
            id="1", 
            title="Shape of You", 
            artist="Ed Sheeran", 
            album="÷ (Divide)",
            duration=235,
            is_favorite=True,
            is_local=True,
            is_downloaded=True,
            lyrics="I'm in love with the shape of you...",
            play_count=10,
            last_played="2025-04-05 14:30:00"
        )
        
        track2 = MusicTrack(
            id="2", 
            title="Blinding Lights", 
            artist="The Weeknd", 
            album="After Hours",
            duration=201,
            is_favorite=False,
            is_local=False,
            is_downloaded=True,
            lyrics="I've been tryna call, I've been on my own for long enough...",
            play_count=5,
            last_played="2025-04-07 10:15:00"
        )
        
        track3 = MusicTrack(
            id="3", 
            title="Dynamite", 
            artist="BTS", 
            album="BE",
            duration=198,
            is_favorite=True,
            is_local=False,
            is_downloaded=False,
            lyrics="Cause I-I-I'm in the stars tonight...",
            play_count=8,
            last_played="2025-04-09 20:45:00"
        )
        
        # Add to various lists
        self._tracks = [track1, track2, track3]
        self._current_playlist = [track1, track2, track3]
        self._history_tracks = [track3, track2, track1]  # Most recent playback order
        self._favorite_tracks = [track1, track3]
        self._local_tracks = [track1]
        self._downloaded_tracks = [track1, track2]
        
        # Set currently playing track
        self._current_track_index = 0
        self._is_playing = True
        
        # Initialize musician information
        self._musicians = {
            "Ed Sheeran": Musician(
                name="Ed Sheeran",
                gender="Male",
                nationality="United Kingdom",
                birth_date="1991-02-17"
            ),
            "The Weeknd": Musician(
                name="The Weeknd",
                gender="Male",
                nationality="Canada",
                birth_date="1990-02-16"
            ),
            "BTS": Musician(
                name="BTS",
                gender="Male Group",
                nationality="South Korea",
                birth_date="2013-06-13"
            )
        }
    
    # Getter and Setter methods
    def get_is_playing(self) -> bool:
        """Get playing status"""
        return self._is_playing
    
    def set_is_playing(self, is_playing: bool):
        """Set playing status"""
        self._is_playing = is_playing
    
    def get_current_track_index(self) -> int:
        """Get current track index"""
        return self._current_track_index
    
    def set_current_track_index(self, index: int):
        """Set current track index"""
        if 0 <= index < len(self._current_playlist):
            self._current_track_index = index
    
    def get_current_track(self) -> Optional[MusicTrack]:
        """Get current track"""
        if 0 <= self._current_track_index < len(self._current_playlist):
            return self._current_playlist[self._current_track_index]
        return None
    
    def get_playback_mode(self) -> PlaybackMode:
        """Get playback mode"""
        return self._playback_mode
    
    def set_playback_mode(self, mode: PlaybackMode):
        """Set playback mode"""
        self._playback_mode = mode
    
    def get_show_lyrics(self) -> bool:
        """Get lyrics display status"""
        return self._show_lyrics
    
    def set_show_lyrics(self, show: bool):
        """Set lyrics display status"""
        self._show_lyrics = show
    
    def get_show_playlist(self) -> bool:
        """Get playlist display status"""
        return self._show_playlist
    
    def set_show_playlist(self, show: bool):
        """Set playlist display status"""
        self._show_playlist = show
    
    def get_tracks(self) -> List[MusicTrack]:
        """Get all tracks"""
        return self._tracks
    
    def get_current_playlist(self) -> List[MusicTrack]:
        """Get current playlist"""
        return self._current_playlist
    
    def get_history_tracks(self) -> List[MusicTrack]:
        """Get history tracks"""
        return self._history_tracks
    
    def get_favorite_tracks(self) -> List[MusicTrack]:
        """Get favorite tracks"""
        return self._favorite_tracks
    
    def get_local_tracks(self) -> List[MusicTrack]:
        """Get local tracks"""
        return self._local_tracks
    
    def get_downloaded_tracks(self) -> List[MusicTrack]:
        """Get downloaded tracks"""
        return self._downloaded_tracks
    
    # API implementation methods
    @api("music")
    def music_soundVolume_increase(self, value: Optional[int] = None, degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Increase music volume
        
        Args:
            value (Optional[int]): Specific value to increase, mutually exclusive with degree, between 0-100
            degree (Optional[str]): Degree of volume increase, options: ["large", "little", "tiny"]
        
        Returns:
            Dict[str, Any]: Operation result and status info
        """
        # Ensure sound channel is music
        Environment.set_sound_channel("music")
        
        current_volume = Environment.get_volume()
        new_volume = current_volume
        
        # Increase volume based on value or degree
        if value is not None:
            new_volume = current_volume + value
        elif degree is not None:
            if degree == VolumeAdjustmentDegree.LARGE.value:
                new_volume = current_volume + 20
            elif degree == VolumeAdjustmentDegree.LITTLE.value:
                new_volume = current_volume + 10
            elif degree == VolumeAdjustmentDegree.TINY.value:
                new_volume = current_volume + 5
        
        # Ensure volume is within valid range
        new_volume = max(0, min(100, new_volume))
        Environment.set_volume(new_volume)
        
        return {
            "success": True,
            "old_volume": current_volume,
            "new_volume": new_volume,
            "sound_channel": Environment.get_sound_channel()
        }
    
    @api("music")
    def music_soundVolume_decrease(self, value: Optional[int] = None, degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Decrease music volume
        
        Args:
            value (Optional[int]): Specific value to decrease, mutually exclusive with degree, between 0-100
            degree (Optional[str]): Degree of volume decrease, options: ["large", "little", "tiny"]
        
        Returns:
            Dict[str, Any]: Operation result and status info
        """
        # Ensure sound channel is music
        Environment.set_sound_channel("music")
        
        current_volume = Environment.get_volume()
        new_volume = current_volume
        
        # Decrease volume based on value or degree
        if value is not None:
            new_volume = current_volume - value
        elif degree is not None:
            if degree == VolumeAdjustmentDegree.LARGE.value:
                new_volume = current_volume - 20
            elif degree == VolumeAdjustmentDegree.LITTLE.value:
                new_volume = current_volume - 10
            elif degree == VolumeAdjustmentDegree.TINY.value:
                new_volume = current_volume - 5
        
        # Ensure volume is within valid range
        new_volume = max(0, min(100, new_volume))
        Environment.set_volume(new_volume)
        
        return {
            "success": True,
            "old_volume": current_volume,
            "new_volume": new_volume,
            "sound_channel": Environment.get_sound_channel()
        }
    
    @api("music")
    def music_soundVolume_set(self, value: Optional[int] = None, degree: Optional[str] = None) -> Dict[str, Any]:
        """
        Set music volume
        
        Args:
            value (Optional[int]): Specific volume value, mutually exclusive with degree, between 0-100
            degree (Optional[str]): Volume level, options: ["max", "high", "medium", "low", "min"]
        
        Returns:
            Dict[str, Any]: Operation result and status info
        """
        # Ensure sound channel is music
        Environment.set_sound_channel("music")
        
        current_volume = Environment.get_volume()
        new_volume = current_volume
        
        # Check parameter validity
        if value is None and degree is None:
            return {
                "success": False,
                "error": "Must provide value or degree parameter"
            }
        
        # Set volume based on value or degree
        if value is not None:
            new_volume = value
        elif degree is not None:
            if degree == VolumeAdjustmentDegree.MAX.value:
                new_volume = 100
            elif degree == VolumeAdjustmentDegree.HIGH.value:
                new_volume = 80
            elif degree == VolumeAdjustmentDegree.MEDIUM.value:
                new_volume = 50
            elif degree == VolumeAdjustmentDegree.LOW.value:
                new_volume = 20
            elif degree == VolumeAdjustmentDegree.MIN.value:
                new_volume = 0
        
        # Ensure volume is within valid range
        new_volume = max(0, min(100, new_volume))
        Environment.set_volume(new_volume)
        
        return {
            "success": True,
            "old_volume": current_volume,
            "new_volume": new_volume,
            "sound_channel": Environment.get_sound_channel()
        }
    
    @api("music")
    def music_history_play(self) -> Dict[str, Any]:
        """
        Play history music
        
        Returns:
            Dict[str, Any]: Operation result and status info
        """
        # Ensure sound channel is music
        Environment.set_sound_channel("music")
        
        if not self._history_tracks:
            return {
                "success": False,
                "error": "History list is empty"
            }
        
        # Set history tracks as current playlist
        self._current_playlist = self._history_tracks.copy()
        self._current_track_index = 0
        self._is_playing = True
        
        current_track = self.get_current_track()
        
        return {
            "success": True,
            "is_playing": True,
            "current_track": current_track.title if current_track else None,
            "playlist_size": len(self._current_playlist)
        }
    
    @api("music")
    def music_player_setMode(self, mode: str) -> Dict[str, Any]:
        """
        Set music playback mode
        
        Args:
            mode (str): Playback mode, options: ["Single Repeat", "Shuffle Play", "Sequential Play", "List Repeat"]
        
        Returns:
            Dict[str, Any]: Operation result and status info
        """
        # Check mode validity
        try:
            play_mode = PlaybackMode(mode)
            self.set_playback_mode(play_mode)
            
            return {
                "success": True,
                "mode": play_mode.value
            }
        except ValueError:
            return {
                "success": False,
                "error": f"Invalid playback mode: {mode}",
                "valid_modes": [m.value for m in PlaybackMode]
            }
    
    @api("music")
    def music_favorite_collect(self, collect: bool) -> Dict[str, Any]:
        """
        Favorite/unfavorite current music
        
        Args:
            collect (bool): True for favorite, False for unfavorite
        
        Returns:
            Dict[str, Any]: Operation result and status info
        """
        current_track = self.get_current_track()
        
        if not current_track:
            return {
                "success": False,
                "error": "No currently playing music"
            }
        
        # Update favorite status
        current_track.is_favorite = collect
        
        # Update favorite list
        if collect and current_track not in self._favorite_tracks:
            self._favorite_tracks.append(current_track)
        elif not collect and current_track in self._favorite_tracks:
            self._favorite_tracks.remove(current_track)
        
        return {
            "success": True,
            "track_title": current_track.title,
            "is_favorite": collect,
            "favorite_count": len(self._favorite_tracks)
        }
    
    @api("music")
    def music_favorite_play(self) -> Dict[str, Any]:
        """
        Play favorite music
        
        Returns:
            Dict[str, Any]: Operation result and status info
        """
        # Ensure sound channel is music
        Environment.set_sound_channel("music")
        
        if not self._favorite_tracks:
            return {
                "success": False,
                "error": "Favorite list is empty"
            }
        
        # Set favorite tracks as current playlist
        self._current_playlist = self._favorite_tracks.copy()
        self._current_track_index = 0
        self._is_playing = True
        
        current_track = self.get_current_track()
        
        # Update play history
        if current_track and current_track not in self._history_tracks:
            self._history_tracks.insert(0, current_track)
        
        return {
            "success": True,
            "is_playing": True,
            "current_track": current_track.title if current_track else None,
            "playlist_size": len(self._current_playlist)
        }
    
    @api("music")
    def music_recent_play(self) -> Dict[str, Any]:
        """
        Play recently played music
        
        Returns:
            Dict[str, Any]: Operation result and status info
        """
        # Same as history_play function
        return self.music_history_play()
    
    @api("music")
    def music_local_play(self) -> Dict[str, Any]:
        """
        Play local music
        
        Returns:
            Dict[str, Any]: Operation result and status info
        """
        # Ensure sound channel is music
        Environment.set_sound_channel("music")
        
        if not self._local_tracks:
            return {
                "success": False,
                "error": "Local music list is empty"
            }
        
        # Set local tracks as current playlist
        self._current_playlist = self._local_tracks.copy()
        self._current_track_index = 0
        self._is_playing = True
        
        current_track = self.get_current_track()
        
        # Update play history
        if current_track and current_track not in self._history_tracks:
            self._history_tracks.insert(0, current_track)
        
        return {
            "success": True,
            "is_playing": True,
            "current_track": current_track.title if current_track else None,
            "playlist_size": len(self._current_playlist)
        }
    
    @api("music")
    def music_download_play(self) -> Dict[str, Any]:
        """
        Play downloaded music
        
        Returns:
            Dict[str, Any]: Operation result and status info
        """
        # Ensure sound channel is music
        Environment.set_sound_channel("music")
        
        if not self._downloaded_tracks:
            return {
                "success": False,
                "error": "Downloaded music list is empty"
            }
        
        # Set downloaded tracks as current playlist
        self._current_playlist = self._downloaded_tracks.copy()
        self._current_track_index = 0
        self._is_playing = True
        
        current_track = self.get_current_track()
        
        # Update play history
        if current_track and current_track not in self._history_tracks:
            self._history_tracks.insert(0, current_track)
        
        return {
            "success": True,
            "is_playing": True,
            "current_track": current_track.title if current_track else None,
            "playlist_size": len(self._current_playlist)
        }
    
    @api("music")
    def music_history_view(self) -> Dict[str, Any]:
        """
        View music history
        
        Returns:
            Dict[str, Any]: History info
        """
        history_info = [
            {"title": track.title, "artist": track.artist, "last_played": track.last_played}
            for track in self._history_tracks
        ]
        
        return {
            "success": True,
            "history_count": len(history_info),
            "history": history_info
        }
    
    @api("music")
    def music_collection_view(self) -> Dict[str, Any]:
        """
        View favorite music
        
        Returns:
            Dict[str, Any]: Favorite music info
        """
        favorite_info = [
            {"title": track.title, "artist": track.artist, "album": track.album}
            for track in self._favorite_tracks
        ]
        
        return {
            "success": True,
            "favorite_count": len(favorite_info),
            "favorites": favorite_info
        }
    
    @api("music")
    def music_local_view(self) -> Dict[str, Any]:
        """
        View local music
        
        Returns:
            Dict[str, Any]: Local music info
        """
        local_info = [
            {"title": track.title, "artist": track.artist, "album": track.album}
            for track in self._local_tracks
        ]
        
        return {
            "success": True,
            "local_count": len(local_info),
            "local_tracks": local_info
        }
    
    @api("music")
    def music_download_view(self) -> Dict[str, Any]:
        """
        View downloaded music
        
        Returns:
            Dict[str, Any]: Downloaded music info
        """
        download_info = [
            {"title": track.title, "artist": track.artist, "album": track.album}
            for track in self._downloaded_tracks
        ]
        
        return {
            "success": True,
            "download_count": len(download_info),
            "downloaded_tracks": download_info
        }
    
    @api("music")
    def music_currentDetail_view(self) -> Dict[str, Any]:
        """
        View current playing music details
        
        Returns:
            Dict[str, Any]: Current playing music detailed info
        """
        current_track = self.get_current_track()
        
        if not current_track:
            return {
                "success": False,
                "error": "No currently playing music"
            }
        
        return {
            "success": True,
            "track_info": {
                "title": current_track.title,
                "artist": current_track.artist,
                "album": current_track.album,
                "duration": current_track.duration,
                "is_favorite": current_track.is_favorite,
                "play_count": current_track.play_count
            }
        }
    
    @api("music")
    def music_get_currentMusician(self) -> Dict[str, Any]:
        """
        Get current playing song's artist
        
        Returns:
            Dict[str, Any]: Response containing current artist info
        """
        current_track = self.get_current_track()
        
        if not current_track:
            return {
                "success": False,
                "error": "No currently playing music"
            }
        
        artist = current_track.artist
        musician_info = self._musicians.get(artist)
        
        if not musician_info:
            return {
                "success": False,
                "error": f"Artist info not found: {artist}"
            }
        
        return {
            "success": True,
            "currentmusicianInfo": str(musician_info)
        }
    
    @api("music")
    def music_get_currentAlbum(self) -> Dict[str, Any]:
        """
        Get current playing song's album name
        
        Returns:
            Dict[str, Any]: Response containing current album info
        """
        current_track = self.get_current_track()
        
        if not current_track:
            return {
                "success": False,
                "error": "No currently playing music"
            }
        
        return {
            "success": True,
            "currentAlbumInfo": current_track.album
        }
    
    @api("music")
    def music_playList_switch(self, switch: bool) -> Dict[str, Any]:
        """
        Show/hide music playlist
        
        Args:
            switch (bool): True to show, False to hide
        
        Returns:
            Dict[str, Any]: Operation result and status info
        """
        self.set_show_playlist(switch)
        
        return {
            "success": True,
            "playlist_visible": switch,
            "playlist_size": len(self._current_playlist) if switch else None
        }
    
    @api("music")
    def music_player_showLyric(self, switch: bool) -> Dict[str, Any]:
        """
        Show/hide lyrics
        
        Args:
            switch (bool): True to show, False to hide
        
        Returns:
            Dict[str, Any]: Operation result and status info
        """
        self.set_show_lyrics(switch)
        
        current_track = self.get_current_track()
        
        return {
            "success": True,
            "lyrics_visible": switch,
            "current_track": current_track.title if current_track else None,
            "lyrics": current_track.lyrics if switch and current_track else None
        }
    


    def to_dict(self) -> Dict[str, Any]:
        """Convert Music instance to dictionary with attribute types and descriptions"""
        # Get enum values for documentation
        volume_adjustment_degrees = [degree.value for degree in VolumeAdjustmentDegree]
        playback_modes = [mode.value for mode in PlaybackMode]
        
        return {
            "_is_playing": {
                "type": "bool",
                "value": self._is_playing,
                "description": "Is playing music"
            },
            "_current_track_index": {
                "type": "int",
                "value": self._current_track_index,
                "description": "Current track index, should be set to 0 when user requests playing downloaded/favorite/local/history music to start from beginning"
            },
            "_playback_mode": {
                "type": "PlaybackMode",
                "value": self._playback_mode.value,
                "description": "Playback mode",
                "enum_values": playback_modes
            },
            "_show_lyrics": {
                "type": "bool",
                "value": self._show_lyrics,
                "description": "Show lyrics"
            },
            "_show_playlist": {
                "type": "bool",
                "value": self._show_playlist,
                "description": "Show playlist"
            },
            "_tracks": {
                "type": "List[MusicTrack]",
                "value": [track.to_dict() for track in self._tracks],
                "description": "All tracks list"
            },
            "_current_playlist": {
                "type": "List[MusicTrack]",
                "value": [track.to_dict() for track in self._current_playlist],
                "description": "Current playlist"
            },
            "_history_tracks": {
                "type": "List[MusicTrack]",
                "value": [track.to_dict() for track in self._history_tracks],
                "description": "History playlist"
            },
            "_favorite_tracks": {
                "type": "List[MusicTrack]",
                "value": [track.to_dict() for track in self._favorite_tracks],
                "description": "Favorite tracks list"
            },
            "_local_tracks": {
                "type": "List[MusicTrack]",
                "value": [track.to_dict() for track in self._local_tracks],
                "description": "Local tracks list"
            },
            "_downloaded_tracks": {
                "type": "List[MusicTrack]",
                "value": [track.to_dict() for track in self._downloaded_tracks],
                "description": "Downloaded tracks list"
            },
            "_musicians": {
                "type": "Dict[str, Musician]",
                "value": {name: musician.to_dict() for name, musician in self._musicians.items()},
                "description": "Artists info dictionary"
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Music':
        """
        Reconstruct Music instance from dictionary
        
        Args:
            data (Dict[str, Any]): Dictionary containing Music data
            
        Returns:
            Music: A new Music instance with dictionary data
        """
        music = cls()
        
        # Restore basic attributes
        if "_is_playing" in data and "type" in data["attributes"]["_is_playing"]:
            music._is_playing = data.get("_is_playing", False)
        
        if "_current_track_index" in data and "type" in data["attributes"]["_current_track_index"]:
            music._current_track_index = data.get("_current_track_index", -1)
        
        if "_playback_mode" in data and "type" in data["attributes"]["_playback_mode"]:
            mode_str = data.get("_playback_mode")
            # Try to convert string to enum value
            try:
                music._playback_mode = PlaybackMode(mode_str)
            except (ValueError, TypeError):
                music._playback_mode = PlaybackMode.SEQUENTIAL_PLAY
        
        if "_show_lyrics" in data and "type" in data["attributes"]["_show_lyrics"]:
            music._show_lyrics = data.get("_show_lyrics", False)
        
        if "_show_playlist" in data and "type" in data["attributes"]["_show_playlist"]:
            music._show_playlist = data.get("_show_playlist", False)
        
        # Restore track lists
        if "_tracks" in data and "type" in data["attributes"]["_tracks"]:
            tracks_data = data.get("_tracks", [])
            music._tracks = []
            for track_dict in tracks_data:
                track = MusicTrack(
                    id=track_dict.get("id", ""),
                    title=track_dict.get("title", ""),
                    artist=track_dict.get("artist", ""),
                    album=track_dict.get("album", ""),
                    duration=track_dict.get("duration", 0),
                    is_favorite=track_dict.get("is_favorite", False),
                    is_local=track_dict.get("is_local", False),
                    is_downloaded=track_dict.get("is_downloaded", False),
                    lyrics=track_dict.get("lyrics", ""),
                    play_count=track_dict.get("play_count", 0),
                    last_played=track_dict.get("last_played", None)
                )
                music._tracks.append(track)
        
        # Restore current playlist
        if "_current_playlist" in data and "type" in data["attributes"]["_current_playlist"]:
            playlist_data = data.get("_current_playlist", [])
            music._current_playlist = []
            for track_dict in playlist_data:
                track = MusicTrack(
                    id=track_dict.get("id", ""),
                    title=track_dict.get("title", ""),
                    artist=track_dict.get("artist", ""),
                    album=track_dict.get("album", ""),
                    duration=track_dict.get("duration", 0),
                    is_favorite=track_dict.get("is_favorite", False),
                    is_local=track_dict.get("is_local", False),
                    is_downloaded=track_dict.get("is_downloaded", False),
                    lyrics=track_dict.get("lyrics", ""),
                    play_count=track_dict.get("play_count", 0),
                    last_played=track_dict.get("last_played", None)
                )
                music._current_playlist.append(track)
        
        # Restore history playlist
        if "_history_tracks" in data and "type" in data["attributes"]["_history_tracks"]:
            history_data = data.get("_history_tracks", [])
            music._history_tracks = []
            for track_dict in history_data:
                track = MusicTrack(
                    id=track_dict.get("id", ""),
                    title=track_dict.get("title", ""),
                    artist=track_dict.get("artist", ""),
                    album=track_dict.get("album", ""),
                    duration=track_dict.get("duration", 0),
                    is_favorite=track_dict.get("is_favorite", False),
                    is_local=track_dict.get("is_local", False),
                    is_downloaded=track_dict.get("is_downloaded", False),
                    lyrics=track_dict.get("lyrics", ""),
                    play_count=track_dict.get("play_count", 0),
                    last_played=track_dict.get("last_played", None)
                )
                music._history_tracks.append(track)
        
        # Restore favorite tracks list
        if "_favorite_tracks" in data and "type" in data["attributes"]["_favorite_tracks"]:
            favorite_data = data.get("_favorite_tracks", [])
            music._favorite_tracks = []
            for track_dict in favorite_data:
                track = MusicTrack(
                    id=track_dict.get("id", ""),
                    title=track_dict.get("title", ""),
                    artist=track_dict.get("artist", ""),
                    album=track_dict.get("album", ""),
                    duration=track_dict.get("duration", 0),
                    is_favorite=track_dict.get("is_favorite", False),
                    is_local=track_dict.get("is_local", False),
                    is_downloaded=track_dict.get("is_downloaded", False),
                    lyrics=track_dict.get("lyrics", ""),
                    play_count=track_dict.get("play_count", 0),
                    last_played=track_dict.get("last_played", None)
                )
                music._favorite_tracks.append(track)
        
        # Restore local tracks list
        if "_local_tracks" in data and "type" in data["attributes"]["_local_tracks"]:
            local_data = data.get("_local_tracks", [])
            music._local_tracks = []
            for track_dict in local_data:
                track = MusicTrack(
                    id=track_dict.get("id", ""),
                    title=track_dict.get("title", ""),
                    artist=track_dict.get("artist", ""),
                    album=track_dict.get("album", ""),
                    duration=track_dict.get("duration", 0),
                    is_favorite=track_dict.get("is_favorite", False),
                    is_local=track_dict.get("is_local", False),
                    is_downloaded=track_dict.get("is_downloaded", False),
                    lyrics=track_dict.get("lyrics", ""),
                    play_count=track_dict.get("play_count", 0),
                    last_played=track_dict.get("last_played", None)
                )
                music._local_tracks.append(track)
        
        # Restore downloaded tracks list
        if "_downloaded_tracks" in data and "type" in data["attributes"]["_downloaded_tracks"]:
            downloaded_data = data.get("_downloaded_tracks", [])
            music._downloaded_tracks = []
            for track_dict in downloaded_data:
                track = MusicTrack(
                    id=track_dict.get("id", ""),
                    title=track_dict.get("title", ""),
                    artist=track_dict.get("artist", ""),
                    album=track_dict.get("album", ""),
                    duration=track_dict.get("duration", 0),
                    is_favorite=track_dict.get("is_favorite", False),
                    is_local=track_dict.get("is_local", False),
                    is_downloaded=track_dict.get("is_downloaded", False),
                    lyrics=track_dict.get("lyrics", ""),
                    play_count=track_dict.get("play_count", 0),
                    last_played=track_dict.get("last_played", None)
                )
                music._downloaded_tracks.append(track)
        
        # Restore musician information
        if "_musicians" in data and "type" in data["attributes"]["_musicians"]:
            musicians_data = data.get("_musicians", {})
            music._musicians = {}
            for name, musician_dict in musicians_data.items():
                musician = Musician(
                    name=musician_dict.get("name", ""),
                    gender=musician_dict.get("gender", ""),
                    nationality=musician_dict.get("nationality", ""),
                    birth_date=musician_dict.get("birth_date", "")
                )
                music._musicians[name] = musician
        
        return music
    
    @classmethod
    def init1(cls) -> 'Music':
        """
        Initialize a Music instance with rock music tracks
        
        Returns:
            Music: A music instance with rock music collection
        """
        music = cls()
        
        # Clear default data
        music._tracks = []
        music._current_playlist = []
        music._history_tracks = []
        music._favorite_tracks = []
        music._local_tracks = []
        music._downloaded_tracks = []
        music._musicians = {}
        
        # Create rock music tracks
        track1 = MusicTrack(
            id="101", 
            title="Stairway to Heaven", 
            artist="Led Zeppelin", 
            album="Led Zeppelin IV",
            duration=482,  # 8:02
            is_favorite=True,
            is_local=True,
            is_downloaded=True,
            lyrics="There's a lady who's sure all that glitters is gold...",
            play_count=15,
            last_played="2025-04-14 19:30:00"
        )
        
        track2 = MusicTrack(
            id="102", 
            title="Bohemian Rhapsody", 
            artist="Queen", 
            album="A Night at the Opera",
            duration=354,  # 5:54
            is_favorite=True,
            is_local=False,
            is_downloaded=True,
            lyrics="Is this the real life? Is this just fantasy?...",
            play_count=18,
            last_played="2025-04-15 08:45:00"
        )
        
        track3 = MusicTrack(
            id="103", 
            title="Sweet Child O' Mine", 
            artist="Guns N' Roses", 
            album="Appetite for Destruction",
            duration=356,  # 5:56
            is_favorite=False,
            is_local=False,
            is_downloaded=False,
            lyrics="She's got a smile that it seems to me...",
            play_count=12,
            last_played="2025-04-10 14:20:00"
        )
        
        # Add to collections
        music._tracks = [track1, track2, track3]
        music._current_playlist = [track1, track2, track3]
        music._history_tracks = [track2, track1, track3]  # Most recent first
        music._favorite_tracks = [track2]
        music._local_tracks = [track1]
        music._downloaded_tracks = [track1, track2]
        
        # Set current playback state
        music._current_track_index = 0
        music._is_playing = True
        Environment.set_sound_channel("music")
        music._playback_mode = PlaybackMode.SEQUENTIAL_PLAY
        music._show_lyrics = True
        music._show_playlist = True
        
        # Add musician information
        music._musicians = {
            "Led Zeppelin": Musician(
                name="Led Zeppelin",
                gender="Male Group",
                nationality="United Kingdom",
                birth_date="1968-09-25"
            ),
            "Queen": Musician(
                name="Queen",
                gender="Male Group",
                nationality="United Kingdom",
                birth_date="1970-06-27"
            ),
            "Guns N' Roses": Musician(
                name="Guns N' Roses",
                gender="Male Group",
                nationality="United States",
                birth_date="1985-03-26"
            )
        }
        
        return music

    @classmethod
    def init2(cls) -> 'Music':
        """
        Initialize a Music instance with electronic music tracks that is not playing
        
        Returns:
            Music: A music instance with electronic music collection
        """
        music = cls()
        
        # Clear default data
        music._tracks = []
        music._current_playlist = []
        music._history_tracks = []
        music._favorite_tracks = []
        music._local_tracks = []
        music._downloaded_tracks = []
        music._musicians = {}
        
        # Create electronic music tracks
        track1 = MusicTrack(
            id="201", 
            title="Strobe", 
            artist="Deadmau5", 
            album="For Lack of a Better Name",
            duration=634,  # 10:34
            is_favorite=True,
            is_local=False,
            is_downloaded=True,
            lyrics="",  # Instrumental
            play_count=15,
            last_played="2025-04-15 23:10:00"
        )
        
        track2 = MusicTrack(
            id="202", 
            title="Clarity", 
            artist="Zedd", 
            album="Clarity",
            duration=271,  # 4:31
            is_favorite=True,
            is_local=True,
            is_downloaded=True,
            lyrics="High dive into frozen waves where the past comes back to life...",
            play_count=20,
            last_played="2025-04-16 00:30:00"
        )
        
        track3 = MusicTrack(
            id="203", 
            title="Levels", 
            artist="Avicii", 
            album="Levels - Single",
            duration=202,  # 3:22
            is_favorite=True,
            is_local=False,
            is_downloaded=True,
            lyrics="",  # Mostly instrumental with samples
            play_count=22,
            last_played="2025-04-13 15:45:00"
        )
        
        # Add to collections
        music._tracks = [track1, track2, track3]
        music._current_playlist = [track1, track2, track3]
        music._history_tracks = [track2, track1, track3]  # Most recent first
        music._favorite_tracks = [track1, track2, track3]
        music._local_tracks = [track2]
        music._downloaded_tracks = [track1, track2, track3]
        
        # Set current playback state
        music._current_track_index = 1  # Currently on track2, but not playing
        music._is_playing = False
        music._playback_mode = PlaybackMode.SHUFFLE_PLAY
        music._show_lyrics = False
        music._show_playlist = True
        
        # Add musician information
        music._musicians = {
            "Deadmau5": Musician(
                name="Deadmau5",
                gender="Male",
                nationality="Canada",
                birth_date="1981-01-05"
            ),
            "Zedd": Musician(
                name="Zedd",
                gender="Male",
                nationality="Russia",
                birth_date="1989-09-02"
            ),
            "Avicii": Musician(
                name="Avicii",
                gender="Male",
                nationality="Sweden",
                birth_date="1989-09-08"
            )
        }
        
        return music