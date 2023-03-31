import pandas as pd
from datetime import date
import sys
from arcgis.gis import GIS
gis = GIS("home")

# read in data from a csv or excel and create a list using the item ids
filename = r'C:\Users\RSUBRA-C\Documents\ArcGIS\AGOL\data\content.csv'

'''CSV OR Excel'''
# df = pd.read_excel(f'{filename}')
df = pd.read_csv(f'{filename}')
item_lst = df['ID'].tolist()
item_lst

user_to_save_to = gis.users.get('CONTENT_ARCHIEVE')
today = date.today()
today_formatted = today.strftime('%d''%b''%Y')

def log_writer(message):
    ### CREATE LOG FILE 
    #home_path = os.path.dirname(os.path.abspath(log_path)) + '\\'
    home_path = os.path.expanduser('~') + '\\' + r'Documents\ArcGIS' + '\\' + 'log.txt'
    print (home_path)
    writeFile = open(home_path, "a")
    writeFile.write(message)
    writeFile.close()

# # function to move data
def move_data(itemId, folderName):
    gis.content.create_folder(folderName, user_to_save_to)
    try:
        itemId.reassign_to(user_to_save_to.username, target_folder=folderName)
    except Exception:
        with open(f'C:\Users\RSUBRA-C\Documents\ArcGIS\AGOL\data\content.txt','a') as exf:
            print(Exception, file=exf)
            pass
    itemId.share(everyone=False, org=False)
    print(f'Moved {itemId.title} to Folder Titled: {folderName}. Owner is {itemId.owner}', file=f)


print('Creating a list of user names...')
log_writer("TOOL STARTED")
get_owner_name = [gis.content.get(item).owner for item in item_lst if 'CONTENT_ARCHIEVE' not in gis.content.get(item).owner]
user_name_list = list(set(get_owner_name))

# open a file and print what was moved to that file
print('Moving items...')
log_writer("Moving Items")
with open(f'home/ItemsMoved{today_formatted}.txt', 'w') as f:
    print(f'{today} Transfering {len(item_lst)} items for {len(user_name_list)} users', file=f)

    for user in user_name_list:
        user_gis = gis.users.get(user)
        user_gis_items = user_gis.items()
        
        # root folder
        for item in user_gis_items:
            if item.id in item_lst:
                print(f'Moving {item.id} from: {item.owner}')
                folder_name = item.owner.replace('_TXDOT', '')
                move_data(item, folder_name)
                print(f'Moved {item.title} to Folder Titled: {folder_name}. Owner is {item.owner}',file=f)


        # all other folders
        folders = user_gis.folders
        for folder in folders:
            folder_items = user_gis.items(folder=folder['title'])
            for item in folder_items:
                if item.id in item_lst:
                    print(f'Moving {item.id} from: {item.owner}')
                    folder_name = str(item.owner.replace('_TXDOT', '') + '_' + folder['title'])
                    move_data(item, folder_name)
                    print(f'Moved {item.title} to Folder Titled: {folder_name} Owner is {item.owner}',file=f)
                
print(f'Completed move to {user_to_save_to}')






