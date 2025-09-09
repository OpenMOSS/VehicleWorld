from module import *
from utils import modules_dict


class VehicleWorld:
    def __init__(self):
            self.navigation = Navigation()
            self.conversation = Conversation()
            self.music = Music()
            self.radio = Radio()
            self.video = Video()
            self.airConditioner = AirConditioner()
            self.door = Door()
            self.window = Window()
            self.footPedal = FootPedal()
            self.readingLight = ReadingLight()
            self.seat = Seat()
            self.bluetooth = Bluetooth()
            self.centerInformationDisplay = CenterInformationDisplay()
            self.fogLight = FogLight()
            self.frontTrunk = FrontTrunk()
            self.fuelPort = FuelPort()
            self.hazardLight = HazardLight()
            self.highBeamHeadlight = HighBeamHeadlight()
            self.HUD = HUD()
            self.instrumentPanel = InstrumentPanel()
            self.lowBeamHeadlight = LowBeamHeadlight()
            self.overheadScreen = OverheadScreen()
            self.positionLight = PositionLight()
            self.rearviewMirror = RearviewMirror()
            self.steeringWheel = SteeringWheel()
            self.sunroof = Sunroof()
            self.sunshade = Sunshade()
            self.tailLight = TailLight()
            self.trunk = Trunk()
            self.wiper = Wiper()
    def to_dict(self):
        return {
                "environment": {
                    "value": Environment.to_dict(),
                    "description": "World environment",
                    "type": type(Environment).__name__
                },
                "navigation": {
                    "value": self.navigation.to_dict(),
                    "description": "Navigation system",
                    "type": type(self.navigation).__name__
                },
                "conversation": {
                    "value": self.conversation.to_dict(),
                    "description": "Call system",
                    "type": type(self.conversation).__name__
                },
                "music": {
                    "value": self.music.to_dict(),
                    "description": "Music system",
                    "type": type(self.music).__name__
                },
                "radio": {
                    "value": self.radio.to_dict(),
                    "description": "Radio system",
                    "type": type(self.radio).__name__
                },
                "video": {
                    "value": self.video.to_dict(),
                    "description": "Video system",
                    "type": type(self.video).__name__
                },
                "airConditioner":{
                    "value": self.airConditioner.to_dict(),
                    "description": "Air conditioning system",
                    "type": type(self.airConditioner).__name__
                },
                "door":{
                    "value": self.door.to_dict(),
                    "description": "Door",
                    "type": type(self.door).__name__
                },
                "window":{
                    "value": self.window.to_dict(),
                    "description": "Window",
                    "type": type(self.window).__name__
                },
                "footPedal":{
                    "value": self.footPedal.to_dict(),
                    "description": "Foot pedal",
                    "type": type(self.footPedal).__name__
                },
                "readingLight":{
                    "value": self.readingLight.to_dict(),
                    "description": "Reading light",
                    "type": type(self.readingLight).__name__
                },
                "seat":{
                    "value": self.seat.to_dict(),
                    "description": "Seat",
                    "type": type(self.seat).__name__
                },
                "bluetooth":{
                "value": self.bluetooth.to_dict(),
                "description": "Bluetooth",
                "type": type(self.bluetooth).__name__
                },

                # New components
                "centerInformationDisplay": {
                    "value": self.centerInformationDisplay.to_dict(),
                    "description": "Center information display",
                    "type": type(self.centerInformationDisplay).__name__
                },
                "fogLight": {
                    "value": self.fogLight.to_dict(),
                    "description": "Fog light",
                    "type": type(self.fogLight).__name__
                },
                "frontTrunk": {
                    "value": self.frontTrunk.to_dict(),
                    "description": "Front trunk",
                    "type": type(self.frontTrunk).__name__
                },
                "fuelPort": {
                    "value": self.fuelPort.to_dict(),
                    "description": "Fuel port",
                    "type": type(self.fuelPort).__name__
                },
                "hazardLight": {
                    "value": self.hazardLight.to_dict(),
                    "description": "Hazard warning light",
                    "type": type(self.hazardLight).__name__
                },
                "highBeamHeadlight": {
                    "value": self.highBeamHeadlight.to_dict(),
                    "description": "High beam headlight",
                    "type": type(self.highBeamHeadlight).__name__
                },
                "HUD": {
                    "value": self.HUD.to_dict(),
                    "description": "Head-up display",
                    "type": type(self.HUD).__name__
                },
                "instrumentPanel": {
                    "value": self.instrumentPanel.to_dict(),
                    "description": "Instrument panel",
                    "type": type(self.instrumentPanel).__name__
                },
                "lowBeamHeadlight": {
                    "value": self.lowBeamHeadlight.to_dict(),
                    "description": "Low beam headlight",
                    "type": type(self.lowBeamHeadlight).__name__
                },
                "overheadScreen": {
                    "value": self.overheadScreen.to_dict(),
                    "description": "Overhead screen",
                    "type": type(self.overheadScreen).__name__
                },
                "positionLight": {
                    "value": self.positionLight.to_dict(),
                    "description": "Position light",
                    "type": type(self.positionLight).__name__
                },
                "rearviewMirror": {
                    "value": self.rearviewMirror.to_dict(),
                    "description": "Rearview mirror",
                    "type": type(self.rearviewMirror).__name__
                },
                "steeringWheel": {
                    "value": self.steeringWheel.to_dict(),
                    "description": "Steering wheel",
                    "type": type(self.steeringWheel).__name__
                },
                "sunroof": {
                    "value": self.sunroof.to_dict(),
                    "description": "Sunroof",
                    "type": type(self.sunroof).__name__
                },
                "sunshade": {
                    "value": self.sunshade.to_dict(),
                    "description": "Sunshade",
                    "type": type(self.sunshade).__name__
                },
                "tailLight": {
                    "value": self.tailLight.to_dict(),
                    "description": "Tail light",
                    "type": type(self.tailLight).__name__
                },
                "trunk": {
                    "value": self.trunk.to_dict(),
                    "description": "Trunk",
                    "type": type(self.trunk).__name__
                },
                "wiper": {
                    "value": self.wiper.to_dict(),
                    "description": "Wiper",
                    "type": type(self.wiper).__name__
                }
        }

    @classmethod
    def from_dict(cls, data):
        """
        Restore VehicleWorld object from dictionary form.
        Missing fields will be initialized using default constructor.
        """
        vehicle_world = cls.__new__(cls)

        # Handle Environment (static class)
        if "environment" in data:
            Environment.from_dict(data["environment"]["value"])

        # Remaining fields: dynamically restore or default initialize
        for key in modules_dict:
            class_name = key.capitalize()
            klass = globals().get(class_name)
            if not klass:
                raise ValueError(f"Class {class_name} not found")

            if key in data:
                value = data[key]["value"]
                setattr(vehicle_world, key, klass.from_dict(value))
            else:
                setattr(vehicle_world, key, klass())  # Default constructor

        return vehicle_world