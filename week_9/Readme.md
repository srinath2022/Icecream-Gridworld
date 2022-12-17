## What these modules do
- Allow user to create txt file containing data mimicking mouse cursor movement (left click to start recording, left click let up to stop and start new drawing, space bar to quit saving files)
- Use mouse data text file to have robot mimick movements from user mouse data and run applications to execute the data



## In order to run scripts
You will need to install python packages. Some of these are windows-based and need to be modified accordingly to function for mac(pywin32 library).

In terminal, donwload packages with command
- pip install pyautogui
- pip install pywin32
- pip install tk

To navigate to a drawing app, the default paint app was used and searched and started with "command_1" and "command_2". The commands were respetively "cd C:\Windows\System32" and "start mspaint.exe" in order start the paint app. 
The relative locations to select the pencil, pencil color, and pencil width were chosen based on screen dimensions and relative location for a laptop. These can therefore be tuned by running a python terminal and putting pointer over locations desired to click and runnung command pg.position() and replacing variables. These locations can then be clicked by using the "move_and_click()" funtion
and adding desired x and y cordinates along with time duration. 

