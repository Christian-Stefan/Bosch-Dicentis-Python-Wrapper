from dependencies import *
from UUID_converted import uid_cvrt
import json



class Controller:
    def __init__(self, 
                 username:str,
                 password:str,
                 AUTOMATIC_OFF = 'ON'):
        
        # --- Constructor intialization arguments --- #
        self.username = username
        self.password = password

        #TODO User parallel job method to carry out operations and simmultaneously keep the counting
        self.AUTOMATIC_OFF = AUTOMATIC_OFF 

        # 1. Add the path to the system path
        sys.path.append(path)

        # 2. Initialize Bases and Interfaces
        #TODO Possibility to initialize interfaces/bases
        self.Interfaces, self.imports= self.initailize_references_and_open()


# --- Routine Procedures comprising API initialization and User authentification --- # BEGINING
    def initailize_references_and_open(self):  
        clr.AddReference("Bosch.Dcnm.Interfaces.Api.Interfaces")
        from Bosch.Dcnm.Interfaces.Api.Interfaces import IApi, IDeviceApi, IControlMeeting, IControlParticipant, DcnmDeviceConnectionState, DcnmPowerState, IEquipment, IPrepareParticipant2, IPrepareCamera, DcnmOverviewCameraPreparationInfo
 
        clr.AddReference("Bosch.Dcnm.Interfaces.Api")
        from Bosch.Dcnm.Interfaces.Api import WindowsApiInstance

        api = WindowsApiInstance()

        base_api = api.Base
        device_api = api.Device
        equipment_api = api.Equipment
        ctrl_meeting_api = api.ControlMeeting
        ctrl_participant_api = api.ControlParticipant
        prep_participant_api_2 = api.PrepareParticipant2 
        prep_Voting = api.PrepareVoting
        prep_Audio = api.SystemAudioControlApi
        prep_Area = api.ConfigArea 
        prep_Meeting = api.PrepareMeeting 
        speaker = api.Speaker 
        prepare_Discussion = api.PrepareDiscussion
    
        print("API Refferences intialized")

        r = IApi.OpenAsync(base_api).Result
        self.WaitForProperty(object=base_api, 
                             property=IApi.IsOpen, 
                             value=True,
                             max_attempts= 60, 
                             failure_text="Openen API not succeeded in time")

        print("API was opened\nHowever, no user was authentificated yet so API stays in IDLE mode")

        # Wait for ability to connect as a device
        self.WaitForProperty(device_api, IDeviceApi.CanConnectAsDevice, True, 30, "Timeout while waiting for ability to connect as a device")
        # Now connect as a device
        r = IDeviceApi.ConnectAsDeviceAsync(device_api, socket.gethostname() + "-PythonTestScript").Result
        self.WaitForProperty(device_api, IDeviceApi.CurrentDeviceConnectionState, DcnmDeviceConnectionState.Connected, 30, "Connect as a device not done in time")
 
        if self.AUTOMATIC_OFF == 'ON':
            print("---ACTIVATED MODE: AUTOMATIC OFF, which automaticaly disengage the API after 10 seconds")

        return [[api, 
                 base_api, 
                 device_api,
                 equipment_api, 
                 ctrl_meeting_api, 
                 ctrl_participant_api,
                 prep_participant_api_2,
                 prep_Voting,
                 prep_Audio,
                 prep_Area,
                 prep_Meeting,
                 speaker,
                 prepare_Discussion],
                            [IApi,
                            IDeviceApi, 
                            IControlMeeting, 
                            IControlParticipant, 
                            DcnmDeviceConnectionState, 
                            DcnmPowerState, 
                            IEquipment,
                            IPrepareParticipant2,
                            DcnmOverviewCameraPreparationInfo,
                            IPrepareCamera]]
        #TODO Change the list into a dictionary since more convinient in notation/terminology
    
    def AuthenticateUserAsync(self):

        try:
            if not self.username and not self.password:
                self.Interfaces[0].Shutdown()
                raise ValueError("No credentials (e.g., username and password) were provided yet since API cannot be initialized")


        except ValueError as e:
            self.Interfaces[0].Shutdown()
            print(e)

        self.WaitForProperty(self.Interfaces[1], self.imports[0].CanAuthenticate, True, 30, "Can authenticate still not possible")
        r = self.imports[0].AuthenticateUserAsync(self.Interfaces[1], 
                                    self.username, 
                                    self.password).Result 
        try:
            if not r:
                raise TypeError
            else:
                print("Login as {} successfully done".format(self.username))
        except TypeError:
            print("Authentification failed for {}. The set of credentials might be incorrect".format(self.username))
            self.Interfaces[0].Shutdown()

        # if self.AUTOMATIC_OFF == 'ON':
        #     time.sleep(10)
        #     self.Interfaces[0].Shutdown()
        #     print("API connection was terminated")

# --- Routine Procedures comprising API initialization and User authentification --- # END

# --- Reading-Actions including retrieving participants, meetings ID, meetings agenda... --- # BEGINING

    def RequestMeetingsListAsync(self, UNSUBSCRIBE_AUTO = 'OFF'):
        """
        Requests the list of meetings asynchronously and listens for the MeetingsListChanged event.
        """
        # Ensure the user can read meeting information
        self.WaitForProperty(
            self.Interfaces[4],
            self.imports[2].CanActivateMeeting,
            True,
            60,
            "CanActivateMeeting not possible in time"
        )

        # Define the callback for the MeetingsListChanged event
        def on_meetings_list_changed(sender, args):
            print("Meetings list has been updated.")
            if hasattr(args, "Parameter"):
                meetings = args.Parameter
                for meeting in meetings:
                    print("\nMeeting name: {} Meeting ID: {} \n".format(meeting.Title, meeting.MeetingId))
                    print("Summary: {}".format(meeting.Description))
                    print("---------------------")


        # Subscribe to the MeetingsListChanged event
        self.Interfaces[4].MeetingsListChanged += on_meetings_list_changed
        
        # Trigger the asynchronous request for the meetings list
        r = self.Interfaces[4].RequestMeetingsListAsync().Result

        # Optionally unsubscribe from the event if no longer needed
        if UNSUBSCRIBE_AUTO:
            self.Interfaces[4].MeetingsListChanged -= on_meetings_list_changed

    def RetrieveParticipantsForMeetingAsync(self, 
                                            MEETING_ID:str,
                                            delegate_type:list = ['ALL']):
        
        # 1.1 Verifies whether the user was granted with retrieving participants rights 
        self.WaitForProperty(
            self.Interfaces[6], # Object 
            self.imports[7].CanPrepareParticipants, # Property
            True,
            5,
            "RetreiveParticipant not possible in time. Perhaps the user hasn't been granted with admin rights"
        )
        
        # 2. Request retrieving the participant(s) of a specific meeting:
        r = self.Interfaces[6].RetrieveParticipantsForMeetingAsync(uid_cvrt(MEETING_ID)).Result

        # 3. Reading out the participants in r and forming the container that comprises all the participants
        participant_container = [participant.ParticipantInfo for participant in [participant for participant in r]]


        # Filter-printer type function - Participant
        def filter_participant_info(participant, *arg):
            
            for filters in arg:

                if 'REMOTE' in filters and 'ALL' and 'ON-PREMISE' not in filters: 
                    if str(participant.AssignedAt) == '00000000-0000-0000-0000-000000000000':
                        self._print_participant_info(participant)

                elif 'ON-PREMISE' in filters and 'ALL' and 'REMOTE' not in filters:
                    if str(participant.AssignedAt) != '00000000-0000-0000-0000-000000000000':
                        self._print_participant_info(participant)
                    
        # Filter-printer type function - Camera


        # 3. Printing out the participant(s) information
        # 3.1 Setting up the filter `delegate_type`:
        if 'ALL' in delegate_type :
            print("Listing  ALL the participants...\n")
            for participant in participant_container:
                self._print_participant_info(participant)
        
        elif 'REMOTE' in delegate_type and ('ON-PREMISE' or 'ALL') in delegate_type:
            print("Listing  ALL the participants...\n")
            for participant in participant_container:
                self._print_participant_info(participant)

        elif 'REMOTE' in delegate_type and 'ALL' and 'ON-PREMISE' not in delegate_type:
            print("Listing  only the REMOTE participants...\n")
            for participant in participant_container:
                filter_participant_info(participant, 'REMOTE')

        elif 'ON-PREMISE' in delegate_type and 'ALL' and 'REMOTE' not in delegate_type:
            print("Listing  only ON-PREMISE participants...\n")
            for participant in participant_container:
                filter_participant_info(participant, 'ON-PREMISE')
            
        elif 'CAMERAS' in delegate_type:
            cameras_and_seat = self._print_camera_info()
            print("Listing the CAMERAS and participants...\n")
            for participant in participant_container:
                for info_index in range(len(list(cameras_and_seat.values()))):
                    for seat_id in list(cameras_and_seat.values())[info_index]:
                        if str(participant.AssignedAt) in seat_id:
                            self._print_participant_info(participant)
                            print(f"Camera ID: {list(cameras_and_seat.keys())[info_index]}")
                            print(f"Camera assinged to seat: {seat_id}")


    #TODO - Bring everything together in one single function, seat, participants and rooms + cameras;
    #TODO - Checker for .CSV file;

    def ParticipantInformation(self, 
                               ID:str, 
                               MEETING_ID:str, 
                               CanDiscuss:bool, 
                               CanManageMeeting:bool, 
                               CanUsePriority:bool, 
                               CanVote:bool, 
                               HasSpecialPermission:bool, 
                               sAuthenticated:bool, 
                               PersonInfo:bool, 
                               VipType:bool, 
                               VoteWeight:bool):
        pass

# --- Reading-Actions including retrieving participants, meetings ID, meetings agenda... --- # END
    def ActivateMeetingAsync(self, ID, time=None, CLOSE_AUTO='OFF'):
        """
        Activates a meeting and optionally closes it after a given time.
        
        :param ID: The meeting ID to activate.
        :param time: The time (in seconds) after which the meeting should be closed automatically.
        :param CLOSE_AUTO: Whether to close the meeting automatically ('ON' or 'OFF').
        """
        from UUID_converted import uid_cvrt

        # Check if the logged in user can activate a meeting
        self.WaitForProperty(self.Interfaces[4], self.imports[2].CanActivateMeeting, True, 60, "CanActivateMeeting not possible in time")

        # Request a meeting to be opened
        r = self.Interfaces[4].ActivateMeetingAsync(uid_cvrt(ID), None).Result
        print(f"Meeting {ID} activated: {r}")

        # If CLOSE_AUTO is enabled, close the meeting after the given time
        if CLOSE_AUTO == 'ON' and time is not None:
            while time > 0:
                print(f"Meeting will close in... {time} seconds")
                time -= 1
                import time as t
                t.sleep(1)
  
            # Deactivate the meeting
            r = self.Interfaces[4].CloseMeetingAsync().Result
            print(f"Meeting {ID} deactivated: {r}")

    # def CloseMeetingAsync(self, ID):

    # BROADCAST video in Synoptic View
    def WaitForProperty(self,
                        object, 
                        property, 
                        value, 
                        max_attempts, 
                        failure_text):
        """
        Wait for a property to become a certain value. Maximum number of
        attempts and text when the property is not set in time  
        are given as parameters. Not necessarily needed to make a call unless not sure
        how much time it will take
    
        :param object: The object to check the property on.
        :param property: The property to check.
        :param value: The value to wait for.
        :param max_attempts: The maximum number of attempts to check the property.
        :param failure_text: The text to print if the property is not set in time.
        :return: None

        :raises Exception: If the property is not set in time.
        """

        i = max_attempts
        propvalue = property.GetValue(object)
 
        while (i > 0 and propvalue != value):
            i = i-1
            time.sleep(1)
            propvalue = property.GetValue(object)

        if propvalue != value:
            print(failure_text)
            self.Interfaces[0].Shutdown()

            raise Exception(failure_text)

    def _print_participant_info(self,
                                participant):  
                """
                Prints a descriptive message for a participant based on their attributes.
                
                :param participant: The participant object with the specified attributes.
                """
                print(f"""
                Participant Information:
                -------------------------
                UserName: {participant.UserName}
                UserId: {participant.UserId}
                MeetingId: {participant.MeetingId}
                AssignedAt: {participant.AssignedAt}
                ScreenLine: {participant.ScreenLine}
                CanDiscuss: {participant.CanDiscuss}
                CanManageMeeting: {participant.CanManageMeeting}
                CanUsePriority: {participant.CanUsePriority}
                CanVote: {participant.CanVote}
                HasSpecialPermission: {participant.HasSpecialPermission}
                VipType: {participant.VipType}
                VoteWeight: {participant.VoteWeight}
                -------------------------
                """)
        
    def _print_camera_info(self, path:str ='C:\ProgramData\Bosch\DICENTIS\MediaGateway\MediaGatewaySettings.jsonc'):

        user_and_camera:dict = {} # Container that holds both user and their associated camera
        
        try:
            # Check if path exists
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")
            # Read the JSON file
            with open(path, 'r') as file:
                data = json.load(file) 
        except:
            print(f"Error reading the file: {path}. Please check the wheter the path {path} exists. In case it doesn't, please provide the correct path")


        # 1. Retrieve and display camera information
        camera_info = data.get('inputs')
        if camera_info:
            print("Camera Information:")
            for camera in camera_info:
                # print(f"Camera ID: {camera.get('id')}")
                # print(f"Camera RTSP: {camera.get('video-uri')}")
                # print(f"Camera Type: {camera.get('ptz-controller-type')}")
                # print()
                # Store camera information in the dictionary
                user_and_camera[camera.get('id')]={
                    (camera.get('video-uri'), camera.get('ptz-controller-type'))
                }
        else:
            print("No camera information found.")

        # 2. Iterate through `seatmaps` to identify users which were assigned cameras and retrieve their seat information
        seatmaps = data.get('seatmaps')
        for info_group in seatmaps:
            if info_group['prepositions']:
                for info_source in info_group['prepositions']:
                    if info_source['source-id']:
                        if info_source['source-id'] in user_and_camera.keys():
                            user_and_camera[info_source['source-id']].add((info_group['seat-id'], info_group['seat-name']))

        return user_and_camera