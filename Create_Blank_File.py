def Create_Blank_File(filename, directory, filesizeMB):
    import os
    cwd = os.getcwd()
    try
        os.chdir(directory)
    except
        pass
    
    with open(filename, "wb") as out:
        out.truncate(1024 * filesizeMB)
    os.chdir(cwd)
