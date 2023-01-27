''' 
files_proccessing is class for creating folders needed for saving results of neural network.
'''

import os

PATH_TO_PROJECT = os.getcwd()
USERS_WAY = f"{PATH_TO_PROJECT}/users/"
RES_WAY = f"{PATH_TO_PROJECT}/results/"
def create_user_folder(user_id):
    if not os.path.exists(USERS_WAY):
        os.makedirs(USERS_WAY)
    path = USERS_WAY + str(user_id)
    if not os.path.exists(path):
        os.makedirs(path)
    return path 

def create_res_folder():
        if not os.path.exists(RES_WAY):
            os.makedirs(RES_WAY)
            os.makedirs(RES_WAY+'1')    
        max_folder_name = max(map(int,os.listdir(path=RES_WAY)))
        os.makedirs(RES_WAY + str(max_folder_name +1))
        return RES_WAY + str(max_folder_name +1)

def is_file_in_user_folder(user_id, filename):
    return os.path.exists(create_user_folder(user_id)+ "/" + filename)
def get_user_fileway(user_id):
    return USERS_WAY + str(user_id)
    