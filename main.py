from APIControl import Controller

api = Controller(username='admin',
                 password='')

api.AuthenticateUserAsync()
api.RequestMeetingsListAsync()
api.RetrieveParticipantsForMeetingAsync('1f14c64b-82a5-45b0-8bf1-0069d229a3cc ', 'ON-PREMISE')


