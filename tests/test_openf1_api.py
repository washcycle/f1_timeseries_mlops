
#%%
from openf1.api import OpenF1API

#%% Example usage
if __name__ == "__main__":
    api = OpenF1API()
    car_data = api.get_car_data(driver_number=55, session_key="9159")
    for data in car_data:
        print(data)
        
# %%
