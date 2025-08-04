### The immediately available documentation presently comprises HOW TOs of various kinds, as listed below:

- [How to retrieve the list of participants by meeting;](#👥-how-to-retrieve-the-list-of-participants-by-meeting)
- [How to start/close a meeting;](#▶️-how-to-startclose-a-meeting)
- [How to authenticate;](#🔒-how-to-authenticate)
- [How to retrieve meeting information raw/filtered (e.g., camera information);](#👥-how-to-retrieve-the-list-of-participants-by-meeting)
- [How to retrieve the list of meetings;](#📅-how-to-retrieve-the-list-of-meetings)

## 🔒 How to authenticate? 
Dicentis Wrapper requires authentication before everything else, which means that one user will not be able to leverage other functionalities (e.g., retrieve a list of meetings) until their presence is recognized by the system. This can be achieved by a two-step procedure, which unfolds as follows:


```
api = Controller(username='admin', password='') -> Hands in the credentials
api.AuthenticateUserAsync() -> Verifies the credentials and consequently rejects/confirms identity;
```

>[!NOTE]
> Authentication does not guarantee full authorization. 
> In other words, once authenticated, only a specific set of rights will be made available. 
> That specific set of rights might INCLUDE/NOT INCLUDE actions (e.g., start/close a meeting) that fall outside of the wrapper functional scope.

## 📅 How to retrieve the list of meetings?
Retrieving the list of meetings will usually return a so-called `sequence of UUIDs` (e.g., unique identifiers). Each identifier corresponds to a meeting that had/is/will be taken place and comes into practical application when meeting-specific actions/information are to be carried out (e.g., starting a specific meeting requires the meeting's unique identifier).

Action:
```
api.RequestMeetingsListAsync()
```

Mock-Result:
```
UUID: 3f9a8b26-9c44-4f1e-92a7-61b5e0247d2e
Meeting Name: Project Kickoff
Summary: Initial meeting to outline project goals, milestones, and team roles.

UUID: a8d6f3c1-5217-4d84-9a3d-1e3f6e7b9e90
Meeting Name: Marketing Strategy Review
Summary: Discuss marketing campaigns, budget allocation, and upcoming promotions.

UUID: 7c3e4f98-0d45-4f0b-8323-2a6bc18c1fdf
Meeting Name: Sprint Planning
Summary: Plan tasks and assign responsibilities for the upcoming development sprint.

UUID: d91b1cfc-8ea2-4a5d-b76c-5f8e17b12344
Meeting Name: Client Feedback Session
Summary: Review client feedback and decide on necessary product adjustments.

UUID: f6a4b5d2-37e8-4d3f-b0b1-2c7b9dce4f73
Meeting Name: Quarterly Financial Review
Summary: Analyze financial performance and discuss forecasts for the next quarter.

```

## 👥 How to retrieve the list of participants by meeting?
As previously stated, in order to retrieve all the persons who are supposed to attend a meeting, the correspondent UUID is required, as shown below. **By default the function returns both remote and on-premise participants**:

```
api.RetrieveParticipantsForMeetingAsync('3f9a8b26-9c44-4f1e-92a7-61b5e0247d2e')
```

If filtered information is required (e.g., listing only REMOTE participants), then its second argument comes into action as follows:

```
api.RetrieveParticipantsForMeetingAsync(`3f9a8b26-9c44-4f1e-92a7-61b5e0247d2e',`REMOTE`) -> Displaying only remotely connected participants
```

or, for video resources such as CAMERAS the second argument changes from `REMOTE` to `CAMERAS`:

```
api.RetrieveParticipantsForMeetingAsync(`3f9a8b26-9c44-4f1e-92a7-61b5e0247d2e',`CAMERAS`) -> Displaying ONLY individuals video-resources were assigned to;
```

## ▶️ How to start/close a meeting?
In order to start a meeting, a couple of arguments — as parts of two categories, mandatory and optional, respectively — are required.
- **UUID**, mandatory and specific to the meeting intended to be activated; **TIME**, an optional argument, which indicates for how long (e.g., the span) the meeting should occur; **CLOSE AUTO**, an optional argument that, by default, stays OFF. However, when a time span is indicated, this argument string value OFF must be changed to ON. The demonstration reads as follows:

```
api.ActivateMeetingAsync(3f9a8b26-9c44-4f1e-92a7-61b5e0247d2e) -> Meeting activated
```

```
api.ActivateMeetingAsync(3f9a8b26-9c44-4f1e-92a7-61b5e0247d2e, 60, ON) -> The meeting will be activated only for 60 seconds
```

> [!WARNING]
> By this very moment, only the second option serves as a mean to shut off a meeting, as the `CloseMeetingAsync` is still under development.