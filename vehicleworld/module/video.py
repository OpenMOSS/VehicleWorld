import sys
from enum import Enum
from typing import List, Dict, Any, Optional
import datetime
from utils import api
from module.environment import Environment


class VideoQuality(Enum):
    """Video quality options"""
    SMOOTH_270P = "270P"
    SD_480P = "480P"
    HD_720P = "720P"
    BLURAY_1080P = "1080P"
   
class VolumeDegree(Enum):
    """Volume adjustment degrees for increase/decrease"""
    LARGE = "large"
    LITTLE = "little"
    TINY = "tiny"

class VolumeLevel(Enum):
    """Volume level settings"""
    MAX = "max"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MIN = "min"

class VideoItem:
    """Represents a video item in the system"""
    def __init__(self, video_id: str, title: str, description: str, path: str, is_local: bool, is_downloaded: bool):
        self.video_id = video_id
        self.title = title
        self.description = description
        self.path = path
        self.is_local = is_local
        self.is_downloaded = is_downloaded
        self.is_favorite = False
        self.is_liked = False
       
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert VideoItem to dictionary with property descriptions"""
        return {
            "video_id": {"value": self.video_id, "type": "str", "description": "Unique identifier for video"},
            "title": {"value": self.title, "type": "str", "description": "Title of the video"},
            "description": {"value": self.description, "type": "str", "description": "Description of the video"},
            "path": {"value": self.path, "type": "str", "description": "File path or URL of the video"},
            "is_local": {"value": self.is_local, "type": "bool", "description": "Whether video is stored locally"},
            "is_downloaded": {"value": self.is_downloaded, "type": "bool", "description": "Whether video has been downloaded"},
            "is_favorite": {"value": self.is_favorite, "type": "bool", "description": "Whether video is marked as favorite"},
            "is_liked": {"value": self.is_liked, "type": "bool", "description": "Whether video is liked"}
            
        }



class Video:
    """Video entity class for managing vehicle video system"""
    
    def __init__(self):
        """Initialize Video entity with default values"""
        # Video playback properties
        self._quality = VideoQuality.HD_720P
        self._is_playing = False
        self._current_video = None
        self._is_fullscreen = False
        self._danmaku_enabled = False
        self._skip_intro = False
        
        # Video collections
        self._local_videos = []  # List of local videos
        self._downloaded_videos = []  # List of downloaded videos
        self._history = []  # List of recently played videos with timestamp
        self._favorites = []  # List of favorite videos
        self._local_videos = [
            VideoItem(
                video_id="loc_001",
                title="Scenic Drive Through Mountains",
                description="A relaxing drive through mountain roads with beautiful scenery",
                path="/videos/local/scenic_drive.mp4",
                is_local=True,
                is_downloaded=False
            ),
            VideoItem(
                video_id="loc_002",
                title="City Night Drive",
                description="Exploring the city streets at night with ambient lighting",
                path="/videos/local/city_night.mp4",
                is_local=True,
                is_downloaded=False
            )
    ]
    
        # Sample downloaded videos
        self._downloaded_videos = [
            VideoItem(
                video_id="dl_001",
                title="City Night Drive",
                description="Exploring the city streets at night with ambient lighting",
                path="/videos/local/city_night.mp4",
                is_local=False,
                is_downloaded=True
            ),
            VideoItem(
                video_id="dl_002",
                title="Highway Safety Tutorial",
                description="Learn about best practices for highway driving and safety tips",
                path="/videos/downloads/safety_tutorial.mp4",
                is_local=False,
                is_downloaded=True
            )
        ]
    
        # Initialize history with one of the local videos
        sample_history_video = self._local_videos[0]
        
        self._history = [sample_history_video]
    
        # Initialize favorites with the downloaded video
        sample_favorite_video = self._downloaded_videos[0]
        sample_favorite_video.is_favorite = True
        self._favorites = [sample_favorite_video]
        # Set current video to None initially
        self._current_video = VideoItem(
                video_id="dl_001",
                title="Highway Safety Tutorial",
                description="Learn about best practices for highway driving and safety tips",
                path="/videos/downloads/safety_tutorial.mp4",
                is_local=False,
                is_downloaded=True
            )
        # Getter and setter methods for all properties

        
    def get_quality(self) -> VideoQuality:
        """Get current video quality setting"""
        return self._quality
    
    def set_quality(self, quality: VideoQuality):
        """Set video quality"""
        self._quality = quality
    
    def get_playing(self) -> bool:
        """Get playing status"""
        return self._is_playing
    
    def set_playing(self, playing: bool):
        """Set playing status"""
        self._is_playing = playing
        if playing and self._current_video:
            Environment.set_sound_channel("video")
    
    def get_current_video(self) -> Optional[VideoItem]:
        """Get currently selected video"""
        return self._current_video
    
    def set_current_video(self, video: VideoItem):
        """Set current video"""
        self._current_video = video
    
    def is_fullscreen(self) -> bool:
        """Get fullscreen status"""
        return self._is_fullscreen
    
    def set_fullscreen(self, fullscreen: bool):
        """Set fullscreen status"""
        self._is_fullscreen = fullscreen
    
    def is_danmaku_enabled(self) -> bool:
        """Get danmaku (comments) status"""
        return self._danmaku_enabled
    
    def set_danmaku_enabled(self, enabled: bool):
        """Set danmaku (comments) status"""
        self._danmaku_enabled = enabled
    
    def is_skip_intro(self) -> bool:
        """Get skip intro status"""
        return self._skip_intro
    
    def set_skip_intro(self, skip: bool):
        """Set skip intro status"""
        self._skip_intro = skip
    
    def get_local_videos(self) -> List[VideoItem]:
        """Get local videos"""
        return self._local_videos
    
    def get_downloaded_videos(self) -> List[VideoItem]:
        """Get downloaded videos"""
        return self._downloaded_videos
    
    def get_history(self) -> List[VideoItem]:
        """Get video playback history"""
        return self._history
    
    def get_favorites(self) -> List[VideoItem]:
        """Get favorite videos"""
        return self._favorites
    
    def add_to_favorites(self, video: VideoItem):
        """Add video to favorites"""
        if video not in self._favorites:
            self._favorites.append(video)
            video.is_favorite = True
    
    def remove_from_favorites(self, video: VideoItem):
        """Remove video from favorites"""
        if video in self._favorites:
            self._favorites.remove(video)
            video.is_favorite = False
    
    # API methods implementation
    @api("video")
    def video_soundVolume_increase(self, value: int = None, degree: str = None) -> Dict[str, Any]:
        """
        Increase video volume
        
        Args:
            value (int, optional): Specific volume increase value (0-100)
            degree (str, optional): Level of volume increase, options: ["large", "little", "tiny"]
        
        Returns:
            Dict: Result of operation with current volume
        """
        current_volume = Environment.get_volume()
        Environment.set_sound_channel("video")
        if value is not None:
            # Increase by specific value
            new_volume = min(current_volume + value, 100)
        elif degree is not None:
            # Increase by degree
            if degree == VolumeDegree.LARGE.value:
                new_volume = min(current_volume + 20, 100)
            elif degree == VolumeDegree.LITTLE.value:
                new_volume = min(current_volume + 10, 100)
            elif degree == VolumeDegree.TINY.value:
                new_volume = min(current_volume + 5, 100)
            else:
                return {"success": False, "message": "Invalid degree value", "volume": current_volume}
        else:
            # Default increase (medium)
            new_volume = min(current_volume + 10, 100)
        
        Environment.set_volume(new_volume)
        return {"success": True, "message": f"Volume increased to {new_volume}", "volume": new_volume}
    
    @api("video")
    def video_play_stop(self) -> Dict[str, Any]:
        """
        Stop playing the current video.
        
        Returns:
        Dict: Result of the operation with updated status
        """
        # Check if a video is currently playing
        if not self.get_playing:
            return {
                "success": False,
                "message": "No video is currently playing",
                "status": "Already stopped"
            }
        
        # Stop the current video
        self.set_playing(False)
        
        # Return success result
        return {
            "success": True,
            "message": "Video playback stopped",
            "status": "Stopped",
            "video_info": self._current_video.title if self._current_video else "None"
        }
    
    @api("video")
    def video_soundVolume_decrease(self, value: int = None, degree: str = None) -> Dict[str, Any]:
        """
        Decrease video volume
        
        Args:
            value (int, optional): Specific volume decrease value (0-100)
            degree (str, optional): Level of volume decrease, options: ["large", "little", "tiny"]
        
        Returns:
            Dict: Result of operation with current volume
        """
        current_volume = Environment.get_volume()
        Environment.set_sound_channel("video")
        if value is not None:
            # Decrease by specific value
            new_volume = max(current_volume - value, 0)
        elif degree is not None:
            # Decrease by degree
            if degree == VolumeDegree.LARGE.value:
                new_volume = max(current_volume - 20, 0)
            elif degree == VolumeDegree.LITTLE.value:
                new_volume = max(current_volume - 10, 0)
            elif degree == VolumeDegree.TINY.value:
                new_volume = max(current_volume - 5, 0)
            else:
                return {"success": False, "message": "Invalid degree value", "volume": current_volume}
        else:
            # Default decrease (medium)
            new_volume = max(current_volume - 10, 0)
        
        Environment.set_volume(new_volume)
        return {"success": True, "message": f"Volume decreased to {new_volume}", "volume": new_volume}
    
    @api("video")
    def video_soundVolume_set(self, value: int = None, degree: str = None) -> Dict[str, Any]:
        """
        Set video volume
        
        Args:
            value (int, optional): Specific volume value (0-100)
            degree (str, optional): Volume level, options: ["max", "high", "medium", "low", "min"]
        
        Returns:
            Dict: Result of operation with new volume
        """
        if value is not None:
            # Set to specific value
            if 0 <= value <= 100:
                new_volume = value
            else:
                return {"success": False, "message": "Volume value must be between 0 and 100", "volume": Environment.get_volume()}
        elif degree is not None:
            # Set by degree
            if degree == VolumeLevel.MAX.value:
                new_volume = 100
            elif degree == VolumeLevel.HIGH.value:
                new_volume = 80
            elif degree == VolumeLevel.MEDIUM.value:
                new_volume = 50
            elif degree == VolumeLevel.LOW.value:
                new_volume = 30
            elif degree == VolumeLevel.MIN.value:
                new_volume = 10
            else:
                return {"success": False, "message": "Invalid degree value", "volume": Environment.get_volume()}
        else:
            return {"success": False, "message": "Either value or degree must be provided", "volume": Environment.get_volume()}
        Environment.set_sound_channel("video")
        Environment.set_volume(new_volume)
        return {"success": True, "message": f"Volume set to {new_volume}", "volume": new_volume}
    
    @api("video")
    def video_common_history_view(self) -> Dict[str, Any]:
        """
        View video playback history
        
        Returns:
            Dict: Result with history information
        """
        history_items = [
            {
                "video_id": item.video_id,
                "title": item.title,
               
            } for item in self._history
        ]
        return {"success": True, "history": history_items, "count": len(history_items)}
    
    @api("video")
    def video_download_play(self) -> Dict[str, Any]:
        """
        Play the first video of the _downloaded_videos list.
        
        Returns:
            Dict: Result of operation
        """
        if not self._downloaded_videos:
            return {"success": False, "message": "No downloaded videos available"}
        
        # Play the first downloaded video or most recently played
        
        video_to_play = self._downloaded_videos[0]
        
        self.set_current_video(video_to_play)
        # Set sound channel to video when playing
        Environment.set_sound_channel("video")
        self.set_playing(True)
        
        return {
            "success": True, 
            "message": f"Playing downloaded video: {video_to_play.title}",
            "video": {
                "id": video_to_play.video_id,
                "title": video_to_play.title
            }
        }

    @api("video")
    def video_local_play(self) -> Dict[str, Any]:
        """
        Play the first video of the _local_videos list
        
        Returns:
            Dict: Result of operation
        """
        if not self._local_videos:
            return {"success": False, "message": "No local videos available"}
        
      
       
        video_to_play = self._local_videos[0]
        
        self.set_current_video(video_to_play)
        # Set sound channel to video when playing
        Environment.set_sound_channel("video")
        self.set_playing(True)
        
        return {
            "success": True, 
            "message": f"Playing local video: {video_to_play.title}",
            "video": {
                "id": video_to_play.video_id,
                "title": video_to_play.title
            }
        }

    
    @api("video")
    def video_favorite_collect(self, collect: bool) -> Dict[str, Any]:
        """
        Favorite/Unfavorite video
        
        Args:
            collect (bool): True to favorite, False to unfavorite
        
        Returns:
            Dict: Result of operation
        """
        if not self._current_video:
            return {"success": False, "message": "No video currently selected"}
        
        if collect:
            self.add_to_favorites(self._current_video)
            return {"success": True, "message": f"Added '{self._current_video.title}' to favorites"}
        else:
            self.remove_from_favorites(self._current_video)
            return {"success": True, "message": f"Removed '{self._current_video.title}' from favorites"}
    
    @api("video")
    def video_history_play(self) -> Dict[str, Any]:
        """
        Play the first video of the _history list
        
        Returns:
            Dict: Result of operation
        """
        if not self._history:
            return {"success": False, "message": "No history videos available"}
        
        # Play the most recently watched video
        video_to_play = self._history[0]
        self.set_current_video(video_to_play)
        # Set sound channel to video when playing
        Environment.set_sound_channel("video")
        self.set_playing(True)
        
        return {
            "success": True, 
            "message": f"Playing history video: {video_to_play.title}",
            "video": {
                "id": video_to_play.video_id,
                "title": video_to_play.title
            }
        }


    
    @api("video")
    def video_quality_set(self, mode: str) -> Dict[str, Any]:
        """
        Set video playback quality
        
        Args:
            mode (str): Quality options: ["1080P", "720P", "480P", "270P"]
        
        Returns:
            Dict: Result of operation
        """
        try:
            # Find the matching quality enum
            quality = next(q for q in VideoQuality if q.value == mode)
            self.set_quality(quality)
            return {"success": True, "message": f"Video quality set to {mode}", "quality": mode}
        except StopIteration:
            return {"success": False, "message": f"Invalid quality mode: {mode}"}
    
    @api("video")
    def video_quality_increase(self) -> Dict[str, Any]:
        """
        Increase video playback quality
        
        Returns:
            Dict: Result of operation
        """
        quality_levels = list(VideoQuality)
        current_index = quality_levels.index(self._quality)
        
        if current_index < len(quality_levels) - 1:
            new_quality = quality_levels[current_index + 1]
            self.set_quality(new_quality)
            return {"success": True, "message": f"Video quality increased to {new_quality.value}", "quality": new_quality.value}
        else:
            return {"success": False, "message": "Already at highest quality", "quality": self._quality.value}
    
    @api("video")
    def video_download_view(self) -> Dict[str, Any]:
        """
        View downloaded videos
        
        Returns:
            Dict: List of downloaded videos
        """
        downloaded_items = [
            {
                "video_id": item.video_id,
                "title": item.title,
                "description": item.description
            } for item in self._downloaded_videos
        ]
        return {"success": True, "videos": downloaded_items, "count": len(downloaded_items)}
    
    @api("video")
    def video_quality_decrease(self) -> Dict[str, Any]:
        """
        Decrease video playback quality
        
        Returns:
            Dict: Result of operation
        """
        quality_levels = list(VideoQuality)
        current_index = quality_levels.index(self._quality)
        
        if current_index > 0:
            new_quality = quality_levels[current_index - 1]
            self.set_quality(new_quality)
            return {"success": True, "message": f"Video quality decreased to {new_quality.value}", "quality": new_quality.value}
        else:
            return {"success": False, "message": "Already at lowest quality", "quality": self._quality.value}
    
    @api("video")
    def video_danmaku_switch(self, switch: bool) -> Dict[str, Any]:
        """
        Turn on/off video comments (danmaku)
        
        Args:
            switch (bool): True to turn on, False to turn off
        
        Returns:
            Dict: Result of operation
        """
        self.set_danmaku_enabled(switch)
        status = "on" if switch else "off"
        return {"success": True, "message": f"Danmaku turned {status}", "enabled": switch}
    
    @api("video")
    def video_titleSkip_switch(self, switch: bool) -> Dict[str, Any]:
        """
        Set whether to skip the intro of the video
        
        Args:
            switch (bool): True to skip, False to not skip
        
        Returns:
            Dict: Result of operation
        """
        self.set_skip_intro(switch)
        action = "skip" if switch else "not skip"
        return {"success": True, "message": f"Set to {action} video intro", "skip": switch}
    
    @api("video")
    def video_player_like(self, mode: bool) -> Dict[str, Any]:
        """
        Like/unlike this video
        
        Args:
            mode (bool): True for like, False for unlike
        
        Returns:
            Dict: Result of operation
        """
        if not self._current_video:
            return {"success": False, "message": "No video currently selected"}
        
        self._current_video.is_liked = mode
        action = "liked" if mode else "unliked"
        return {"success": True, "message": f"Video {action}", "liked": mode}
    
    @api("video")
    def video_profile_view(self) -> Dict[str, Any]:
        """
        View video description
        
        Returns:
            Dict: Video description information
        """
        if not self._current_video:
            return {"success": False, "message": "No video currently selected"}
        
        return {
            "success": True, 
            "video": {
                "id": self._current_video.video_id,
                "title": self._current_video.title,
                "description": self._current_video.description,
                "is_favorite": self._current_video.is_favorite,
                "is_liked": self._current_video.is_liked,
                
            }
        }
    
    @api("video")
    def video_collection_view(self) -> Dict[str, Any]:
        """
        View favorite videos
        
        Returns:
            Dict: List of favorite videos
        """
        favorite_items = [
            {
                "video_id": item.video_id,
                "title": item.title,
                "description": item.description
            } for item in self._favorites
        ]
        return {"success": True, "videos": favorite_items, "count": len(favorite_items)}
    
    @api("video")
    def video_local_view(self) -> Dict[str, Any]:
        """
        View local videos
        
        Returns:
            Dict: List of local videos
        """
        local_items = [
            {
                "video_id": item.video_id,
                "title": item.title,
                "description": item.description
            } for item in self._local_videos
        ]
        return {"success": True, "videos": local_items, "count": len(local_items)}
    
    @api("video")
    def video_favorite_play(self) -> Dict[str, Any]:
        """
        Play the first video of the _favorite list
        
        Returns:
            Dict: Result of operation
        """
        if not self._favorites:
            return {"success": False, "message": "No favorite videos available"}
        
        # Play the first favorite video or most recently played
        
        video_to_play = self._favorites[0]
        
        self.set_current_video(video_to_play)
        # Set sound channel to video when playing
        Environment.set_sound_channel("video")
        self.set_playing(True)
        
        return {
            "success": True, 
            "message": f"Playing favorite video: {video_to_play.title}",
            "video": {
                "id": video_to_play.video_id,
                "title": video_to_play.title
            }
        }
    
    @api("video")
    def video_currentDetail_view(self) -> Dict[str, Any]:
        """
        View details of currently playing video
        
        Returns:
            Dict: Current video details
        """
        if not self._current_video:
            return {"success": False, "message": "No video currently playing"}
        
        return {
            "success": True, 
            "playing": self._is_playing,
            "fullscreen": self._is_fullscreen,
            "quality": self._quality.value,
            "danmaku": self._danmaku_enabled,
            "skip_intro": self._skip_intro,
            "volume": Environment.get_volume(),
            "video": {
                "id": self._current_video.video_id,
                "title": self._current_video.title,
                "description": self._current_video.description,
                "is_favorite": self._current_video.is_favorite,
                "is_liked": self._current_video.is_liked,
               
            }
        }
    
    @api("video")
    def video_fullScreenPlay_switch(self, switch: bool) -> Dict[str, Any]:
        """
        Turn on/off full-screen video playback
        
        Args:
            switch (bool): True for full-screen, False for normal view
        
        Returns:
            Dict: Result of operation
        """
        self.set_fullscreen(switch)
        mode = "full-screen" if switch else "normal view"
        return {"success": True, "message": f"Video playback switched to {mode}", "fullscreen": switch}
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Video instance from dictionary data.
        
        Args:
            data (Dict): Dictionary containing Video properties
            
        Returns:
            Video: New Video instance with properties from the dictionary
        """
        video = cls()  # Create a new Video instance
        
        # Set quality if available
        if "quality" in data and data["quality"]["value"]:
            quality_value = data["quality"]["value"]
            quality = next((q for q in VideoQuality if q.value == quality_value), VideoQuality.HD_720P)
            video.set_quality(quality)
        
        # Set boolean properties
        if "is_playing" in data:
            video.set_playing(data["is_playing"]["value"])
        
        if "is_fullscreen" in data:
            video.set_fullscreen(data["is_fullscreen"]["value"])
        
        if "danmaku_enabled" in data:
            video.set_danmaku_enabled(data["danmaku_enabled"]["value"])
        
        if "skip_intro" in data:
            video.set_skip_intro(data["skip_intro"]["value"])
        
        # For collections, we would need to reconstruct them from their respective dictionaries
        # This would require additional logic to recreate VideoItem objects
        # Here's a simplified approach:
        
        if "local_videos" in data and isinstance(data["local_videos"].get("details"), list):
            for video_data in data["local_videos"]["details"]:
                video_item = VideoItem(
                    video_id=video_data.get("video_id", ""),
                    title=video_data.get("title", ""),
                    description=video_data.get("description", ""),
                    path=video_data.get("path", ""),
                    is_local=True,
                    is_downloaded=False
                )
                video._local_videos.append(video_item)
        
        if "downloaded_videos" in data and isinstance(data["downloaded_videos"].get("details"), list):
            for video_data in data["downloaded_videos"]["details"]:
                video_item = VideoItem(
                    video_id=video_data.get("video_id", ""),
                    title=video_data.get("title", ""),
                    description=video_data.get("description", ""),
                    path=video_data.get("path", ""),
                    is_local=False,
                    is_downloaded=True
                )
                video._downloaded_videos.append(video_item)
        
        if "favorites" in data and isinstance(data["favorites"].get("details"), list):
            for video_data in data["favorites"]["details"]:
                # Try to find this video in existing collections
                video_id = video_data.get("video_id", "")
                existing_video = next(
                    (v for v in video._local_videos + video._downloaded_videos 
                    if v.video_id == video_id), 
                    None
                )
                
                if existing_video:
                    existing_video.is_favorite = True
                    video._favorites.append(existing_video)
        
        if "history" in data and isinstance(data["history"].get("details"), list):
            for video_data in data["history"]["details"]:
                # Try to find this video in existing collections
                video_id = video_data.get("video_id", "")
                existing_video = next(
                    (v for v in video._local_videos + video._downloaded_videos 
                    if v.video_id == video_id), 
                    None
                )
                
                if existing_video:
                   
                    video._history.append(existing_video)
        
        # Set current video if specified
        if "current_video" in data and data["current_video"]["value"]:
            video_id = data["current_video"]["value"]
            current_video = next(
                (v for v in video._local_videos + video._downloaded_videos 
                if v.video_id == video_id),
                None
            )
            if current_video:
                video.set_current_video(current_video)
        
        return video
    



    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Video entity to dictionary with property descriptions
        
        Returns:
            Dict: Video properties with types and descriptions
        """
        return {
            "quality": {
                "value": self._quality.value if self._quality else None,
                "type": "VideoQuality enum",
                "description": "Current video quality setting",
                "enum_values": [q.value for q in VideoQuality]
            },
            "is_playing": {
                "value": self._is_playing,
                "type": "bool",
                "description": "Whether a video is currently playing,when you play a video,you need to set the value to True"
            },
            "current_video": {
                "value": self._current_video.to_dict() if self._current_video else None,
                "type": "VideoItem",
                "description": """Currently selected video.
                When the user want to play downloaded video,this should be replaced by the first video of the _downloaded_videos list.
                When the user want to play local video,this should be replaced by the first video of the _local_videos list.
                When the user want to play history video,this should be replaced by the first video of the _history list.
                When the user want to play favorite video,this should be replaced by the first video of the _favorite list.
                """
            },
            "is_fullscreen": {
                "value": self._is_fullscreen,
                "type": "bool",
                "description": "Whether video is in fullscreen mode"
            },
            "danmaku_enabled": {
                "value": self._danmaku_enabled,
                "type": "bool",
                "description": "Whether danmaku (comments) are enabled"
            },
            "skip_intro": {
                "value": self._skip_intro,
                "type": "bool",
                "description": "Whether to skip video introductions"
            },
            "local_videos": {
                "value": [local_video.to_dict() for local_video in self._local_videos],
                "type": "List[VideoItem]",
                "description": "List of local videos"
            },
            "downloaded_videos": {
                "value": [downloaded_video.to_dict() for downloaded_video in self._downloaded_videos],
                "type": "List[VideoItem]",
                "description": "List of downloaded videos"
            },
            "history": {
                "value": [his.to_dict() for his in  self._history],
                "type": "List[VideoItem]",
                "description": "List of recently played videos"
            },
            "favorites": {
                "value": [favorite.to_dict() for favorite in self._favorites],
                "type": "List[VideoItem]",
                "description": "List of favorite videos"
            }
        }
    @classmethod
    def init1(cls) -> 'Video':
        """
        Factory method to create a Video instance with a video playing and various VideoItems.
        
        Returns:
            Video: A Video instance with one video currently playing
        """
        # Create a new instance
        video = cls()
        
        # Replace the existing collections with more varied items
        
        # Create additional local videos
        video._local_videos = [
            VideoItem(
                video_id="loc_001",
                title="Scenic Drive Through Mountains",
                description="A relaxing drive through mountain roads with beautiful scenery",
                path="/videos/local/scenic_drive.mp4",
                is_local=True,
                is_downloaded=False
            ),
            VideoItem(
                video_id="loc_002",
                title="City Night Drive",
                description="Exploring the city streets at night with ambient lighting",
                path="/videos/local/city_night.mp4",
                is_local=True,
                is_downloaded=False
            ),
            VideoItem(
                video_id="loc_003",
                title="Highway Safety Guidelines",
                description="Essential safety instructions for highway driving",
                path="/videos/local/highway_safety.mp4",
                is_local=True,
                is_downloaded=False
            ),
            VideoItem(
                video_id="loc_004",
                title="Off-Road Adventure",
                description="4x4 driving techniques for challenging terrain",
                path="/videos/local/offroad_adventure.mp4",
                is_local=True,
                is_downloaded=False
            )
        ]
        
        # Create additional downloaded videos
        video._downloaded_videos = [
            VideoItem(
                video_id="dl_001",
                title="Advanced Driving Techniques",
                description="Professional driving instructor shares advanced vehicle control techniques",
                path="/videos/downloads/advanced_driving.mp4",
                is_local=False,
                is_downloaded=True
            ),
            VideoItem(
                video_id="dl_002",
                title="Highway Safety Tutorial",
                description="Learn about best practices for highway driving and safety tips",
                path="/videos/downloads/safety_tutorial.mp4",
                is_local=False,
                is_downloaded=True
            ),
            VideoItem(
                video_id="dl_003",
                title="Vehicle Maintenance Basics",
                description="Essential maintenance guidelines for keeping your vehicle in top condition",
                path="/videos/downloads/maintenance_basics.mp4",
                is_local=False,
                is_downloaded=True
            ),
            VideoItem(
                video_id="dl_004",
                title="Fuel Efficiency Tips",
                description="Driving techniques and habits that maximize your vehicle's fuel economy",
                path="/videos/downloads/fuel_efficiency.mp4",
                is_local=False,
                is_downloaded=True
            )
        ]
        
        # Set up history with a mix of local and downloaded videos
        video._history = [
            video._local_videos[0],    # Scenic Drive
            video._downloaded_videos[1],   # Highway Safety Tutorial
            video._local_videos[2]     # Highway Safety Guidelines
        ]
        
        # Set up favorites
        video._favorites = [
            video._local_videos[1],    # City Night Drive
            video._downloaded_videos[2]    # Vehicle Maintenance Basics
        ]
        
        # Mark favorite videos appropriately
        for favorite in video._favorites:
            favorite.is_favorite = True
        
        # Mark some videos as liked
        video._local_videos[0].is_liked = True
        video._downloaded_videos[2].is_liked = True
        
        # Select a video to play (using the first downloaded video)
        video.set_current_video(video._downloaded_videos[0])
        
        # Set as playing
        video.set_playing(True)
        Environment.set_sound_channel("video")
       
        
        # Configure additional settings
        video.set_quality(VideoQuality.HD_720P)
        video.set_fullscreen(False)
        video.set_danmaku_enabled(True)
        
        return video

    @classmethod
    def init2(cls) -> 'Video':
        """
        Factory method to create a Video instance with no video playing but with various VideoItems.
        
        Returns:
            Video: A Video instance with no video currently playing
        """
        # Create a new instance
        video = cls()
        
        # Replace the existing collections with more varied items
        
        # Create additional local videos
        video._local_videos = [
            VideoItem(
                video_id="loc_001",
                title="Scenic Drive Through Mountains",
                description="A relaxing drive through mountain roads with beautiful scenery",
                path="/videos/local/scenic_drive.mp4",
                is_local=True,
                is_downloaded=False
            ),
            VideoItem(
                video_id="loc_002",
                title="City Night Drive",
                description="Exploring the city streets at night with ambient lighting",
                path="/videos/local/city_night.mp4",
                is_local=True,
                is_downloaded=False
            ),
            VideoItem(
                video_id="loc_003",
                title="Highway Safety Guidelines",
                description="Essential safety instructions for highway driving",
                path="/videos/local/highway_safety.mp4",
                is_local=True,
                is_downloaded=False
            ),
            VideoItem(
                video_id="loc_004",
                title="Off-Road Adventure",
                description="4x4 driving techniques for challenging terrain",
                path="/videos/local/offroad_adventure.mp4",
                is_local=True,
                is_downloaded=False
            ),
            VideoItem(
                video_id="loc_005",
                title="Defensive Driving Course",
                description="Learn essential defensive driving techniques for everyday situations",
                path="/videos/local/defensive_driving.mp4",
                is_local=True,
                is_downloaded=False
            )
        ]
        
        # Create additional downloaded videos
        video._downloaded_videos = [
            VideoItem(
                video_id="dl_001",
                title="Advanced Driving Techniques",
                description="Professional driving instructor shares advanced vehicle control techniques",
                path="/videos/downloads/advanced_driving.mp4",
                is_local=False,
                is_downloaded=True
            ),
            VideoItem(
                video_id="dl_002",
                title="Highway Safety Tutorial",
                description="Learn about best practices for highway driving and safety tips",
                path="/videos/downloads/safety_tutorial.mp4",
                is_local=False,
                is_downloaded=True
            ),
            VideoItem(
                video_id="dl_003",
                title="Vehicle Maintenance Basics",
                description="Essential maintenance guidelines for keeping your vehicle in top condition",
                path="/videos/downloads/maintenance_basics.mp4",
                is_local=False,
                is_downloaded=True
            ),
            VideoItem(
                video_id="dl_004",
                title="Fuel Efficiency Tips",
                description="Driving techniques and habits that maximize your vehicle's fuel economy",
                path="/videos/downloads/fuel_efficiency.mp4",
                is_local=False,
                is_downloaded=True
            ),
            VideoItem(
                video_id="dl_005",
                title="Electric Vehicle Guide",
                description="Introduction to electric vehicle operation and charging",
                path="/videos/downloads/ev_guide.mp4",
                is_local=False,
                is_downloaded=True
            )
        ]
        
        # Set up history with a mix of local and downloaded videos
        video._history = [
            video._local_videos[0],    # Scenic Drive
            video._downloaded_videos[1],   # Highway Safety Tutorial
            video._local_videos[2],    # Highway Safety Guidelines
            video._downloaded_videos[0]    # Advanced Driving Techniques
        ]
        
        # Set up favorites
        video._favorites = [
            video._local_videos[1],    # City Night Drive
            video._downloaded_videos[2],   # Vehicle Maintenance Basics
            video._local_videos[4]     # Defensive Driving Course
        ]
        
        # Mark favorite videos appropriately
        for favorite in video._favorites:
            favorite.is_favorite = True
        
        # Mark some videos as liked
       
        video._downloaded_videos[0].is_liked = True
        video._downloaded_videos[2].is_liked = True
        
        # Set current video but not playing
        video.set_current_video(None)
        video.set_playing(False)
        
        # Configure additional settings
        video.set_quality(VideoQuality.BLURAY_1080P)
        video.set_skip_intro(True)
        
        return video