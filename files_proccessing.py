import os

USERS_WAY = "C:/Users/boris/OneDrive/Рабочий стол/1 учеба/ML/Deep Learning School 1-ый семестр/проект/StyleTransfer/users/"
RES_WAY = "C:/Users/boris/OneDrive/Рабочий стол/1 учеба/ML/Deep Learning School 1-ый семестр/проект/StyleTransfer/results/"
def create_user_folder(user_id):
    path = USERS_WAY + str(user_id)
    if not os.path.exists(path):
        os.makedirs(path)
    return path 

def create_res_folder():
        max_folder_name = max(map(int,os.listdir(path=RES_WAY)))
        os.makedirs(RES_WAY + str(max_folder_name +1))
        return RES_WAY + str(max_folder_name +1)

def is_file_in_user_folder(user_id, filename):
    return os.path.exists(create_user_folder(user_id)+ "/" + filename)
def get_user_fileway(user_id):
    return USERS_WAY + str(user_id)
    