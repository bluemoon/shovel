import os

def whatRcsType(directory):
    assert directory
    old_cwd = os.getcwd()
    rcs = {
            '.git':'git',
            '.svn':'svn'
            }

    os.chdir(directory)
    for key, value in rcs.items():
        if os.path.exists(key):
            typ = value
            break 

    os.chdir(old_cwd)
    try:
        return typ
    except UnboundLocalError:
        return None
