import sys
sys.path.append("../")
from utils import api
from module.environment import Environment

class Conversation:
    class ContactInfo:
        """
        Inner class for storing contact information.
        """

        def __init__(self, name):
            self.name = name
            self.phone_number = ""  # Contact phone number

        def to_dict(self):
            return {
                "name": {
                    "value": self.name,
                    "description": "Contact name",
                    "type": type(self.name).__name__
                },
                "phone_number": {
                    "value": self.phone_number,
                    "description": "Contact phone number", 
                    "type": type(self.phone_number).__name__
                }
            }

        @classmethod
        def from_dict(cls, data):
            contact = cls(data["name"]["value"])
            contact.phone_number = data["phone_number"]["value"]
            return contact

    class CallRecord:
        """
        Inner class for storing call record information.
        """

        def __init__(self, contact, timestamp, duration=0, incoming=True, missed=False):
            self.contact = contact  # Contact
            self.timestamp = timestamp  # Call timestamp
            self.duration = duration  # Call duration (seconds)
            self.incoming = incoming  # Whether it's an incoming call
            self.missed = missed  # Whether it's a missed call

        def to_dict(self):
            return {
                "contact": {
                    "value": self.contact,
                    "description": "Call contact",
                    "type": type(self.contact).__name__
                },
                "timestamp": {
                    "value": self.timestamp,
                    "description": "Call timestamp",
                    "type": type(self.timestamp).__name__
                },
                "duration": {
                    "value": self.duration,
                    "description": "Call duration (seconds)",
                    "type": type(self.duration).__name__
                },
                "incoming": {
                    "value": self.incoming,
                    "description": "Whether it's an incoming call, True means incoming, False means outgoing",
                    "type": type(self.incoming).__name__
                },
                "missed": {
                    "value": self.missed,
                    "description": "Whether it's a missed call, True means missed, False means answered",
                    "type": type(self.missed).__name__
                }
            }

        @classmethod
        def from_dict(cls, data):
            return cls(
                data["contact"]["value"],
                data["timestamp"]["value"],
                data["duration"]["value"],
                data["incoming"]["value"],
                data["missed"]["value"]
            )

    class Message:
        """
        Inner class for storing SMS information.
        """

        def __init__(self, contact, content, timestamp, incoming=True, read=False):
            self.contact = contact  # Contact
            self.content = content  # SMS content
            self.timestamp = timestamp  # SMS timestamp
            self.incoming = incoming  # Whether it's an incoming SMS
            self.read = read  # Whether it's read

        def to_dict(self):
            return {
                "contact": {
                    "value": self.contact,
                    "description": "SMS contact",
                    "type": type(self.contact).__name__
                },
                "content": {
                    "value": self.content,
                    "description": "SMS content",
                    "type": type(self.content).__name__
                },
                "timestamp": {
                    "value": self.timestamp,
                    "description": "SMS timestamp",
                    "type": type(self.timestamp).__name__
                },
                "incoming": {
                    "value": self.incoming,
                    "description": "Whether it's an incoming SMS, True means received, False means sent",
                    "type": type(self.incoming).__name__
                },
                "read": {
                    "value": self.read,
                    "description": "Whether it's read, True means read, False means unread",
                    "type": type(self.read).__name__
                }
            }

        @classmethod
        def from_dict(cls, data):
            return cls(
                data["contact"]["value"],
                data["content"]["value"],
                data["timestamp"]["value"],
                data["incoming"]["value"],
                data["read"]["value"]
            )

    def __init__(self):
        # Call state related
        self._call_state = "idle"  # Call state: idle(idle), active(in call)
        self._current_contact = "Default Contact"  # Current call contact
        self._hands_free = False  # Whether to use hands-free

        # Contact dictionary
        self._contacts = {"Default Contact":Conversation.ContactInfo(name="Default Contact")}  # Contact dictionary, key is contact name, value is ContactInfo object

        # Call records
        self._call_records = [Conversation.CallRecord(contact="Default Contact", timestamp=None)]  # Call record list
        self._last_called_contact = "Default Contact"  # Last called contact, used for redial function

        # SMS
        self._messages = [Conversation.Message(contact="Default Contact", content="Default content", timestamp=None)]  # SMS list

    # Call state property getter and setter
    @property
    def call_state(self):
        return self._call_state

    @call_state.setter
    def call_state(self, value):
        valid_states = ["idle", "active"]
        if value in valid_states:
            self._call_state = value
        else:
            raise ValueError(f"Invalid call state, must be one of: {valid_states}")

    # Current call contact getter and setter
    @property
    def current_contact(self):
        return self._current_contact

    @current_contact.setter
    def current_contact(self, value):
        self._current_contact = value

    # Hands-free state getter and setter
    @property
    def hands_free(self):
        return self._hands_free

    @hands_free.setter
    def hands_free(self, value):
        if isinstance(value, bool):
            self._hands_free = value
        else:
            raise ValueError("Hands-free state must be a boolean value")

    # Contact list getter
    @property
    def contacts(self):
        return self._contacts

    # Call records getter
    @property
    def call_records(self):
        return self._call_records

    # Last called contact getter and setter
    @property
    def last_called_contact(self):
        return self._last_called_contact

    @last_called_contact.setter
    def last_called_contact(self, value):
        self._last_called_contact = value

    # SMS list getter
    @property
    def messages(self):
        return self._messages

    # Helper method: adjust volume by degree
    def _adjust_volume_by_degree(self, degree, is_increase=True):
        degree_map = {
            "large": 20,
            "little": 10,
            "tiny": 5
        }

        adjustment = degree_map.get(degree, 10)
        if not is_increase:
            adjustment = -adjustment

        new_volume = max(0, min(100, Environment.get_volume() + adjustment))
        return new_volume

    # Helper method: set volume by degree
    def _set_volume_by_degree(self, degree):
        degree_map = {
            "max": 100,
            "high": 80,
            "medium": 50,
            "low": 20,
            "min": 0
        }

        new_volume = degree_map.get(degree, 50)
        return new_volume
    


    def to_dict(self):
        """
        Convert the Conversation object to dictionary form, including descriptions and type information for all properties.
        """
        return {
            "call_state": {
                "value": self.call_state,
                "description": """Call state, values: idle(idle), active(in call),
                            When making outgoing calls, set to active,
                            When hanging up the call, set to idle,
                            When answering calls, set to active
                """,
                "type": type(self.call_state).__name__
            },
            "current_contact": {
                "value": self.current_contact,
                "description": "Current call contact, needs to be set to None when hanging up",
                "type": "str or None"
            },
            "hands_free": {
                "value": self.hands_free,
                "description": "Whether to use hands-free, True means using hands-free, False means not using hands-free, prohibited to modify this parameter if not in a call; needs to be set to False when hanging up",
                "type": type(self.hands_free).__name__
            },
            "contacts": {
                "value": [contact.to_dict() for contact in self.contacts.values()],
                "description": "Contact dictionary, key is contact name, value is ContactInfo object, can only call or send messages to contacts in the list",
                "type": "list"
            },
            "call_records": {
                "value": [record.to_dict() for record in self.call_records],
                "description": "Call record list",
                "type": "list"
            },
            "last_called_contact": {
                "value": self.last_called_contact,
                "description": "Last called contact, used for redial function, needs to be updated to current call contact when hanging up; redial not allowed if this contact doesn't exist in contact list",
                "type": "str or None"
            },
            "messages": {
                "value": [message.to_dict() for message in self.messages],
                "description": "SMS list",
                "type": "list"
            }
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Restore Conversation object from dictionary form.
        
        Args:
            data (dict): Dictionary containing all properties of Conversation object
            
        Returns:
            Conversation: Restored Conversation object instance
        """
        # Create a new Conversation instance
        conversation = cls()
        
        # Restore basic properties
        conversation._call_state = data["call_state"]["value"]
        conversation._current_contact = data["current_contact"]["value"]
        conversation._hands_free = data["hands_free"]["value"]
        conversation._last_called_contact = data["last_called_contact"]["value"]
        
        # Restore contact dictionary
        conversation._contacts = {}
        for contact_data in data["contacts"]["value"]:
            contact_info = cls.ContactInfo.from_dict(contact_data)
            conversation._contacts[contact_info.name] = contact_info
        
        # Restore call record list
        conversation._call_records = []
        for record_data in data["call_records"]["value"]:
            call_record = cls.CallRecord.from_dict(record_data)
            conversation._call_records.append(call_record)
        
        # Restore SMS list
        conversation._messages = []
        for message_data in data["messages"]["value"]:
            message = cls.Message.from_dict(message_data)
            conversation._messages.append(message)
        
        return conversation

    # The following are API method implementations

    @api("conversation")
    def conversation_soundVolume_increase(self, value=None, degree=None):
        """
        Increase call volume.

        Args:
            value (int, optional): Specified increase in volume, between 0-100
            degree (str, optional): Degree of volume increase, optional values: ["large", "little", "tiny"], mutually exclusive with value

        Returns:
            dict: Dictionary containing operation results
        """
        # Parameter validation
        if value is not None and degree is not None:
            return {"success": False, "error": "value and degree parameters cannot be used simultaneously"}

        # Set sound channel to conversation
    
        old_volume = Environment.get_volume()
        if value is not None:
            # Adjust by specific value
            if not isinstance(value, int):
                return {"success": False, "error": "value parameter must be an integer"}

            new_volume = max(0, min(100, Environment.get_volume() + value))
            Environment.set_volume(new_volume)
        else:
            # Adjust by degree
            if degree not in ["large", "little", "tiny"] and degree is not None:
                return {"success": False, "error": "degree parameter must be one of: large, little, tiny"}

            # If degree is None, use default little
            degree = degree or "little"
            new_volume = self._adjust_volume_by_degree(degree, True)

            # Synchronize Environment volume
            Environment.set_volume(new_volume)
        Environment.set_sound_channel("conversation")
        return {
            "success": True,
            "old_volume": old_volume,
            "new_volume": new_volume,
            "sound_channel": Environment.get_sound_channel()
        }

    @api("conversation")
    def conversation_soundVolume_decrease(self, value=None, degree=None):
        """
        Decrease call volume.

        Args:
            value (int, optional): Specified decrease in volume, between 0-100
            degree (str, optional): Degree of volume decrease, optional values: ["large", "little", "tiny"], mutually exclusive with value

        Returns:
            dict: Dictionary containing operation results
        """
        # Parameter validation
        if value is not None and degree is not None:
            return {"success": False, "error": "value and degree parameters cannot be used simultaneously"}

        # Set sound channel to conversation
        
        old_volume = Environment.get_volume()
        if value is not None:
            # Adjust by specific value
            if not isinstance(value, int):
                return {"success": False, "error": "value parameter must be an integer"}

            new_volume = max(0, min(100, Environment.get_volume() - value))
            Environment.set_volume(new_volume)
        else:
            # Adjust by degree
            if degree not in ["large", "little", "tiny"] and degree is not None:
                return {"success": False, "error": "degree parameter must be one of: large, little, tiny"}

            # If degree is None, use default little
            degree = degree or "little"
            new_volume = self._adjust_volume_by_degree(degree, False)
            Environment.set_volume(new_volume)
        # Synchronize Environment volume
        
        Environment.set_sound_channel("conversation")
        return {
            "success": True,
            "old_volume": old_volume,
            "new_volume": new_volume,
            "sound_channel": Environment.get_sound_channel()
        }

    @api("conversation")
    def conversation_soundVolume_set(self, value=None, degree=None):
        """
        Set call volume.

        Args:
            value (int, optional): Specified volume setting, range 0-100, between 0-100
            degree (str, optional): Degree of volume setting, optional values: ["max", "high", "medium", "low", "min"], mutually exclusive with value

        Returns:
            dict: Dictionary containing operation results
        """
        # Parameter validation
        if value is None and degree is None:
            return {"success": False, "error": "At least one of value and degree parameters must be provided"}

        if value is not None and degree is not None:
            return {"success": False, "error": "value and degree parameters cannot be used simultaneously"}

        # Set sound channel to conversation
   
        old_volume = Environment.get_volume()
        if value is not None:
            # Set by specific value
            if not isinstance(value, int):
                return {"success": False, "error": "value parameter must be an integer"}

            if not 0 <= value <= 100:
                return {"success": False, "error": "value parameter must be between 0-100"}
            new_volume = self._set_volume_by_degree(degree)
            Environment.set_volume(value)
        else:
            # Set by degree
            if degree not in ["max", "high", "medium", "low", "min"]:
                return {"success": False, "error": "degree parameter must be one of: max, high, medium, low, min"}

            new_volume = self._set_volume_by_degree(degree)
            Environment.set_volume(new_volume)
        # Synchronize Environment volume
        
        Environment.set_sound_channel("conversation")
        return {
            "success": True,
            "old_volume": old_volume,
            "new_volume": new_volume,
            "sound_channel": Environment.get_sound_channel()
        }

    @api("conversation")
    def conversation_phone_call(self, contact):
        """
        Make a phone call.

        Args:
            contact (str): Contact name

        Returns:
            dict: Dictionary containing operation results
        """
        # Parameter validation
        if self.call_state != "idle":
            return {"success": False, "error": f"Current call state is {self.call_state}, cannot make new call"}

        if not contact:
            return {"success": False, "error": "Contact cannot be empty"}

        if contact not in self.contacts:
            return {"success": False, "error": "Contact does not exist"}
        # Check current call state
        
        # Set sound channel to conversation
        Environment.set_sound_channel("conversation")

        # Update call state
        self.call_state = "active"
        self.current_contact = contact
        self.last_called_contact = contact

        return {
            "success": True,
            "call_state": self.call_state,
            "contact": contact,
            "message": f"Calling {contact}"
        }

    @api("conversation")
    def conversation_phone_redial(self):
        """
        Redial the last number.

        Returns:
            dict: Dictionary containing operation results
        """
        # Check if there's a last call record
        if not self.last_called_contact:
            return {"success": False, "error": "No call record to redial"}
        if self._last_called_contact not in self.contacts:
            return {"success": False, "error": "Contact does not exist"}
        # Call phone call API
        return self.conversation_phone_call(self.last_called_contact)

    @api("conversation")
    def conversation_phone_answer(self):
        """
        Answer phone call.

        Returns:
            dict: Dictionary containing operation results
        """
        # Check current call state
        if self.call_state != "active":
            return {"success": False, "error": "No incoming call to answer"}

        # Set sound channel to conversation
        Environment.set_sound_channel("conversation")

        # Update call state
        self.call_state = "active"

        # Add call record
        import time
        if self.current_contact:
            record = Conversation.CallRecord(
                self.current_contact,
                time.time(),
                0,  # Initial duration is 0
                True,  # Incoming call
                False  # Not missed
            )
            self.call_records.append(record)

        return {
            "success": True,
            "call_state": self.call_state,
            "contact": self.current_contact,
            "message": f"Answered call from {self.current_contact}"
        }

    @api("conversation")
    def conversation_phone_hangup(self):
        """
        Hang up the phone call.

        Returns:
            dict: Dictionary containing operation results
        """
        # Check current call state
        if self.call_state == "idle":
            return {"success": False, "error": "No call to hang up"}

        # Record call state and contact for return information
        prev_state = self.call_state
        contact = self.current_contact
        self.last_called_contact = contact
        

        # Update call state
        self.call_state = "idle"
        self.current_contact = None
        self.hands_free = False

        

        return {
            "success": True,
            "previous_state": prev_state,
            "contact": contact,
            "message": f"Hung up call with {contact}"
        }

    @api("conversation")
    def conversation_message_send(self, contact, content=""):
        """
        Send SMS.

        Args:
            contact (str): Contact name
            content (str, optional): SMS content

        Returns:
            dict: Dictionary containing operation results
        """
        # Parameter validation
        if not contact:
            return {"success": False, "error": "Contact cannot be empty"}

        # If contact doesn't exist, create one
        if contact not in self.contacts:
            return {"success": False, "error": "Contact does not exist"}

        # Create SMS record
        import time
        message = Conversation.Message(
            contact,
            content,
            time.time(),
            False,  # Sent SMS
            True  # Already read
        )

        # Add to SMS list
        self.messages.append(message)

        return {
            "success": True,
            "contact": contact,
            "content": content,
            "message": f"SMS sent to {contact}"
        }

    @api("conversation")
    def conversation_message_view(self, contact=None):
        """
        View SMS.

        Args:
            contact (str, optional): Contact name, if not provided, view all unread SMS

        Returns:
            dict: Dictionary containing operation results
        """
        # Filter SMS
        filtered_messages = []

        if contact:
            # View SMS from specific contact
            filtered_messages = [msg for msg in self.messages if msg.contact == contact]

            # Mark these SMS as read
            for msg in filtered_messages:
                msg.read = True

            if not filtered_messages:
                return {"success": False, "error": f"No SMS record found with {contact}"}
        else:
            # View all unread SMS
            filtered_messages = [msg for msg in self.messages if not msg.read]

            # Mark these SMS as read
            for msg in filtered_messages:
                msg.read = True

            if not filtered_messages:
                return {"success": False, "error": "No unread SMS"}

        # Format SMS information
        messages_info = []
        for msg in filtered_messages:
            timestamp_str = Environment.get_timestamp()
            messages_info.append(
                {
                    "contact": msg.contact,
                    "content": msg.content,
                    "timestamp": timestamp_str,
                    "incoming": msg.incoming,
                }
            )
        owner_text = 'unread' if not contact else f"{contact}'s"

        return {
            "success": True,
            "messages": messages_info,
            "count": len(messages_info),
            "message": f"Viewed {owner_text} SMS, total {len(messages_info)} messages"
        }

    @api("conversation")
    def conversation_contact_view(self, contact):
        """
        Look up contact information.

        Args:
            contact (str): Contact name

        Returns:
            dict: Dictionary containing operation results
        """
        # Parameter validation
        if not contact:
            return {"success": False, "error": "Contact cannot be empty"}

        # Find contact
        if contact not in self.contacts:
            return {"success": False, "error": f"Contact {contact} not found"}

        contact_info = self.contacts[contact]

        return {
            "success": True,
            "contact": contact,
            "phone_number": contact_info.phone_number,
            "message": f"Found contact {contact}"
        }

    @api("conversation")
    def conversation_call_miss_view(self):
        """
        View missed calls.

        Returns:
            dict: Dictionary containing operation results
        """
        # Filter missed calls
        missed_calls = [record for record in self.call_records if record.missed]

        if not missed_calls:
            return {"success": False, "error": "No missed call records"}

        # Format missed call information
        calls_info = []
        for call in missed_calls:
            timestamp_str = Environment.get_timestamp()
            calls_info.append({
                "contact": call.contact,
                "timestamp": timestamp_str
            })

        return {
            "success": True,
            "missed_calls": calls_info,
            "count": len(calls_info),
            "message": f"Total {len(calls_info)} missed calls"
        }

    @api("conversation")
    def conversation_call_record_view(self):
        """
        View call records.

        Returns:
            dict: Dictionary containing operation results
        """
        if not self.call_records:
            return {"success": False, "error": "No call records"}

        # Format call record information
        records_info = []
        for record in self.call_records:
            timestamp_str = Environment.get_timestamp()
            records_info.append(
                {
                    "contact": record.contact,
                    "timestamp": timestamp_str,
                    "duration": record.duration,
                    "incoming": record.incoming,
                    "missed": record.missed,
                }
            )

        return {
            "success": True,
            "call_records": records_info,
            "count": len(records_info),
            "message": f"Total {len(records_info)} call records"
        }

    @api("conversation")
    def conversation_contact_hag_view(self):
        """
        Query user's contact list information.

        Returns:
            dict: Dictionary containing operation results
        """
        if not self.contacts:
            return {"success": False, "error": "Contact list is empty"}

        # Format contact information
        contacts_info = []
        for name, info in self.contacts.items():
            contacts_info.append({
                "name": name,
                "phone_number": info.phone_number
            })

        return {
            "success": True,
            "contacts": contacts_info,
            "count": len(contacts_info),
            "message": f"Total {len(contacts_info)} contacts"
        }

    @api("conversation")
    def conversation_call_handsFree_switch(self, switch):
        """
        Hands-free switch.

        Args:
            switch (bool): True means enable hands-free, False means disable hands-free

        Returns:
            dict: Dictionary containing operation results
        """
        # Parameter validation
        if not isinstance(switch, bool):
            return {"success": False, "error": "switch parameter must be a boolean value"}

        # Check current call state
        if self.call_state != "active":
            return {"success": False, "error": "No active call, cannot switch hands-free state"}

        # Update hands-free state
        self.hands_free = switch
        
        return {
            "success": True,
            "hands_free": self.hands_free,
            "message": f"{'Enabled' if switch else 'Disabled'} hands-free mode"
        }

    @api("conversation")
    def conversation_contact_delete(self, contact):
        """
        Delete contact.

        Args:
            contact (str): Contact name

        Returns:
            dict: Dictionary containing operation results
        """
        # Parameter validation
        if not contact:
            return {"success": False, "error": "Contact cannot be empty"}

        # Check if contact exists
        if contact not in self.contacts:
            return {"success": False, "error": f"Contact {contact} not found"}

        # Delete contact
        del self.contacts[contact]

        return {
            "success": True,
            "contact": contact,
            "message": f"Deleted contact {contact}"
        }
    @classmethod
    def init1(cls):
        """
        Initialize a Conversation instance that is making a phone call.
        
        Returns:
            Conversation: A Conversation instance that is making a phone call
        """
        # Create a Conversation instance
        conversation = cls()
        
        # Add some contacts
        zhang_san = cls.ContactInfo("Zhang San")
        zhang_san.phone_number = "13800138000"
        conversation._contacts["Zhang San"] = zhang_san
        
        li_si = cls.ContactInfo("Li Si")
        li_si.phone_number = "13900139000"
        conversation._contacts["Li Si"] = li_si
        
        wang_wu = cls.ContactInfo("Wang Wu")
        wang_wu.phone_number = "13700137000"
        conversation._contacts["Wang Wu"] = wang_wu
        
        # Set to making a phone call
        conversation.call_state = "active"
        conversation.current_contact = "Zhang San"
        conversation.last_called_contact = "Zhang San"
        conversation.hands_free = False

        Environment.set_sound_channel("conversation")
      
        
        return conversation

    @classmethod
    def init2(cls):
        """
        Initialize a Conversation instance with no calls.
        
        Returns:
            Conversation: A Conversation instance in idle state
        """
        # Create a Conversation instance
        conversation = cls()
        
        # Add some contacts
        zhang_san = cls.ContactInfo("Zhang San")
        zhang_san.phone_number = "13800138000"
        conversation._contacts["Zhang San"] = zhang_san
        
        li_si = cls.ContactInfo("Li Si")
        li_si.phone_number = "13900139000"
        conversation._contacts["Li Si"] = li_si
        
        wang_wu = cls.ContactInfo("Wang Wu")
        wang_wu.phone_number = "13700137000"
        conversation._contacts["Wang Wu"] = wang_wu
        
        # Add some call records
        import time
        record1 = cls.CallRecord("Zhang San", time.time() - 3600, 120, True, False)
        record2 = cls.CallRecord("Li Si", time.time() - 7200, 0, True, True)
        conversation._call_records = [record1, record2]
        
        # Add some SMS
        message1 = cls.Message("Zhang San", "Hello, please call back", time.time() - 1800, True, False)
        message2 = cls.Message("Li Si", "Tomorrow's meeting cancelled", time.time() - 3600, True, True)
        conversation._messages = [message1, message2]
        
        # Ensure set to idle state
        conversation.call_state = "idle"
        conversation.current_contact = None
        conversation.hands_free = False
        conversation.last_called_contact = "Zhang San"  # Last call contact
        
        return conversation