### The immediately available documentation presently comprises HOW TOs of various kinds, as listed below:

- [How to retrieve the list of participants by meeting;]()
- [How to start/close a meeting;]()
- [How to authenticate;](#how-to-authenticate)
- [How to retrieve meeting information raw/filtered (e.g., camera information);]()
- [How to retrieve the list of meetings;]()

## How to authenticate
Dicentis Wrapper requires authentication before everything else, which means that one user will not be able to leverage other functionalities (e.g., retrieve a list of meetings) until their presence is recognized by the system. This can be achieved by a two-step procedure, which unfolds as follows:


```
api = Controller(username='admin', password='') -> Hands in the credentials
api.AuthenticateUserAsync() -> Verifies the credentials and consequently rejects/confirms identity;
```

>[!NOTE]
> Authentication does not guarantee full authorization. 
> In other words, once authenticated, only a specific set of rights will be made available. 
> That specific set of rights might INCLUDE/NOT INCLUDE actions (e.g., start/close a meeting) that fall outside of the wrapper functional scope.




