### The immediately available documentation presently comprises HOW TOs of various kinds, as listed below:

- [How to retrieve the list of participants by meeting;](#👥-how-to-retrieve-the-list-of-participants-by-meeting)
- [How to start/close a meeting;](#▶️-how-to-startclose-a-meeting)
- [How to authenticate;](#🔒-how-to-authenticate)
- [How to retrieve meeting information raw/filtered (e.g., camera information);](#👥-how-to-retrieve-the-list-of-participants-by-meeting)
- [How to retrieve the list of meetings;](#📅-how-to-retrieve-the-list-of-meetings)

## 🔒 How to authenticate? 
Praesensa Wrapper requires authentication before everything else, which means that one user will not be able to leverage other functionalities (e.g., retrieve a list of meetings) until their presence is recognized by the system. This can be achieved by a two-step procedure, which should be unfolded as follows:


```
api = Controller(username='admin', password='', connection_type=False) -> Hand in the credentials
api.Connect() -> Log in
```

>[!NOTE]
> Authentication does not guarantee full authorization. 
> In other words, once authenticated, only a specific set of rights will be made available. 
> That specific set of rights might INCLUDE/NOT INCLUDE specific actions (e.g., start/close a call) that fall/do not fall outside of the wrapper functional scope.

## 📅 How to retrieve the a group of zones?
Retrieving a group of zones should return a `sequence of tags` (e.g., unique tags: Zone1). Each tag corresponds to a zone within a specific group. Whenever a call is initialized by means of `CreateCallEx2` a zone/group of zones is also required. Thus, later on these tags will be passed on as arguments in the call initialization function's crown.

Action:
```
api.GetZoneGroupNames() -> Returns group tags
api.GetZoneNames() -> Return zone tags
```

Mock-Result:
```
Work in progress...
```

## How to create a call?
In order to create a call, a couple of arguments — as parts of two categories, mandatory and optional, respectively — are required.

### Mandatory Arguments
| Argument         | Type / Range                                                                                                                                                                                                                          | Description                                                                               |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **routing**      | `list[str]`                                                                                                                                                                                                                           | List of zones. Example: `['Zone1', 'Zone2']`                                              |
| **priority**     | `int` <br> **0 … 31** = BGM call priority (always partial call) <br> **32 … 223** = Normal call priority <br> **224 … 255** = Emergency call priority (always partial call; returns parameter error if emergency control is disabled) | Call priority level                                                                       |
| **live\_speech** | `bool`                                                                                                                                                                                                                                | Whether the call has a live speech phase (`True` = live speech, `False` = no live speech) |

### Call Handling
| Argument               | Type / Values                                                | Description                                                                                                                                                                                                               |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **output\_handling**   | `OICOH_PARTIAL` / `OICOH_STACKED`                            | - **Partial**: Proceeds even if not all required zones are available. <br> - **Stacked**: Extends partial calls with replays to previously unavailable zones.                                                             |
| **stacking\_mode**     | `OICSM_WAIT_FOR_ALL` / `OICSM_WAIT_FOR_EACH`                 | Stacked call replay behavior: <br> - **WAIT\_FOR\_ALL**: Wait for all zones to become available before replay. <br> - **WAIT\_FOR\_EACH**: Replay for each zone as soon as it becomes available.                          |
| **stacking\_timeout**  | `int` (1–3600 sec) / `OICST_INFINITE`                        | Wait time for resources in a stacked call. Countdown starts after original call ends. Ignored if `output_handling` = `OICOH_PARTIAL`.                                                                                     |
| **call\_timing**       | `OICTM_IMMEDIATE` / `OICTM_TIME_SHIFTED` / `OICTM_MONITORED` | Call broadcast timing: <br> - **IMMEDIATE**: Start immediately. <br> - **TIME\_SHIFTED**: Start after original call ends (avoid feedback). <br> - **MONITORED**: Start unless cancelled within 2s after monitoring phase. |
| **pre\_monitor\_dest** | `str`                                                        | Destination zone for pre-monitor phase (ignored unless call is pre-monitored and `call_timing` is not IMMEDIATE or TIME\_SHIFTED).                                                                                        |
### Audio & Chimes
| Argument                      | Type / Range    | Description                                                                                     |
| ----------------------------- | --------------- | ----------------------------------------------------------------------------------------------- |
| **audio\_input**              | `str`           | Name of the audio input (used only when `live_speech = True`). Example: `'Call station (*01)'`. |
| **start\_chime**              | `str`           | Name of the start chime. Can be empty (`''`).                                                   |
| **end\_chime**                | `str`           | Name of the end chime. Can be empty (`''`).                                                     |
| **start\_chime\_attenuation** | `int` (0–60 dB) | Attenuation for start chime phase.                                                              |
| **end\_chime\_attenuation**   | `int` (0–60 dB) | Attenuation for end chime phase.                                                                |
| **live\_speech\_attenuation** | `int` (0–60 dB) | Attenuation during live speech phase.                                                           |

### Messages
| Argument                 | Type / Range           | Description                                                                                      |
| ------------------------ | ---------------------- | ------------------------------------------------------------------------------------------------ |
| **message**              | `list[str]`            | List of prerecorded messages (comma-separated; no spaces before/after commas). Can be empty.     |
| **repeat**               | `int` (-1, 0, 1–32767) | - **-1**: Repeat infinitely <br> - **0**: Play once <br> - **1**: Repeat once (play twice total) |
| **message\_attenuation** | `int` (0–60 dB)        | Attenuation during prerecorded message phase.                                                    |
### Miscellaneous
| Argument     | Type  | Description                       |
| ------------ | ----- | --------------------------------- |
| **call\_id** | `int` | Reference ID number for the call. |

