import pyautogui
import time
import os
import smtplib
from email.mime.text import MIMEText
import numpy as np
import pyperclip
import timeit
from PIL import Image
from PIL import ImageChops
import math


def sendMail(me, you, msg):
    try:
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(me, mail_from_password)
        msg = MIMEText(msg)
        msg['Subject'] = 'SNUH'
        smtp.sendmail(me, you, msg.as_string())
        smtp.quit()
    except:
        print('Mail transmit error')

mail_from = 'your_transmitting_address'
mail_from_password = 'your_transmitting_address_password'
mail_to = 'your_receiving_address'
savelocation = 'muse_save_location'
disklocation = 'location_to_save_results'


if __name__ == '__main__':
    start_time = timeit.default_timer()
    
    data_count = 0
    patient_count = 0
    prev_img = np.zeros(580, 557)
    while True:
        # Click "Patient List"
        pyautogui.click(324, 128)
        
        # Click top item on the list
        pyautogui.click(773, 200)
        
        # Move to a specific patient
        for i in range(count):
            pyautogui.press('down')
            img = pyautogui.screenshot().crop((666, 170, 1245, 726))
            diff = ImageChops.difference(img, prev_img)
            if diff.getbbox():
                break
        patient_count += 1
        
        # Press enter key
        pyautogui.press('enter')
        
        # Click "Catalog"
        pyautogui.click(453, 830)
        
        while True:
            # Concentrate the element
            pyautogui.click(683, 259)
            
            # Right click the element and click an appropriate option
            pyautogui.click(775, 259, button='right')
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.press('enter')
            
            # Results Export Wizard
            pyautogui.press('enter')
            pyautogui.press('enter')
            pyautogui.press('enter')
            pyautogui.press('enter')
            pyautogui.press('enter')
            data_count += 1
            
            prev_img = pyautogui.screenshot().crop((666, 170, 1245, 726))
            pyautogui.press('down')
            img = pyautogui.screenshot().crop((666, 170, 1245, 726))
            diff = ImageChops.difference(img, prev_img)
            if not diff.getbbox():
                break
    
    terminate_time = timeit.default_timer()
    print('Successfully finished! ' + str(data_count) + ' data from ' + str(patient_count) + ' patients have been exported. Elapsed time : ' + str(terminate_time - start_time) + 's')
    
    # Shutdown (default = off)
    # os.system('shutdown -s -t 0')