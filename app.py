from flask import Flask, request, abort
from flask import render_template
from flask import make_response
import csmapi

csmapi.ENDPOINT = 'https://6.iottalk.tw'

registered_address = ''

app = Flask(__name__)

df_list = [ 1, 1, 1, 1, 1]

df_dict = {'Button': 0, 'Color-I': 1, 'Keypad': 2, 'Knob': 3, 'Switch': 4}

@app.route('/<mac_addr>', methods=['GET', 'POST'])
def SwitchSetCount(mac_addr):

    registered_address = mac_addr
    try:    
        profile = csmapi.pull(registered_address, 'profile')
    except Exception as e:
        print("some error")  
    else:
        if profile:
            control_channel_output = csmapi.pull(registered_address, '__Ctl_O__') #Pull the Output of Control Channel 
            if control_channel_output:
                selected_device_feature_flags = control_channel_output[0][1][1]['cmd_params'][0]
                print("Selected device feature flags = ", selected_device_feature_flags)
                s = list(selected_device_feature_flags)
                s = list(map(int, s))
                buc = s[:9]
                coc = s[9:18]
                kec = s[18:27]
                knc = s[27:36]
                swc = s[36:]
                df_list[0] = sum(buc)
                df_list[1] = sum(coc)
                df_list[2] = sum(kec)
                df_list[3] = sum(knc)
                df_list[4] = sum(swc)
                print(df_list)
    finally:
        return make_response(render_template('index.html', mac_addr=mac_addr, count=df_list))
        

if __name__ == "__main__":
    app.run('127.0.0.1', port=25565, threaded=True, use_reloader=False)
