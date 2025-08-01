import System

def uid_cvrt(uuid_str: str):
    """
    Convert a UUID string to a .NET System.Guid object.
    
    Args:
        uuid_str (str): The UUID string to convert.
    
    Returns:
        System.Guid: The converted .NET Guid object.
    """
    return System.Guid(uuid_str)


#print(uid_cvrt('{5ed130b7-7db2-4eb2-8959-27def32ed2bd}'))