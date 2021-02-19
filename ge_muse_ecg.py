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

patient_list = np.load('patient.npy')

if __name__ == '__main__':
    a = Image.open('a.png')
    b = Image.open('b.png')
    c = Image.open('c.png')
    error = Image.open('error.png')
    
    f = open('failures.txt', 'w')
    print('ready')
    
    time.sleep(5)
    print('go')
    
    for idx, id in enumerate(patient_list):
        start_time = timeit.default_timer()
        pyperclip.copy(str(id))

        # 0. Click "Home" button
        pyautogui.click(224, 57)
        time.sleep(30)
        print(idx, ':0')
        
        img = pyautogui.screenshot().crop((752, 391, 1156, 638))
        diff = ImageChops.difference(img, error)
        if not diff.getbbox():
            pyautogui.click(1086, 615)
            time.sleep(3)
            pyautogui.click(224, 57)
            time.sleep(30)
        
        img = pyautogui.screenshot().crop((98, 363, 177, 507))
        diff = ImageChops.difference(img, a)
        if diff.getbbox():
            terminate_time = timeit.default_timer()
            f.write('(%d, %s), ' % (idx, str(id)))
            sendMail(mail_from, mail_to, 'Failure: #%s %d/%d [%ds]' % (str(id), idx+1, patient_list.shape[0], terminate_time - start_time))
            continue
        
        # 1. Make folder
        os.system('mkdir ' + disklocation + '\\' + str(id))
        print(idx, ':1')
                
        # 2. Drag "Patient ID" area
        pyautogui.click(237, 823)
        for k in range(10):
            pyautogui.press('backspace')
        print(idx, ':2')
        
        # 3. Copy & paste ID
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        print(idx, ':3')
        
        # 4. Click "Search" button
        pyautogui.click(71, 1006)
        time.sleep(3)
        print(idx, ':4')
        
        # 5. Double-click the first area
        pyautogui.click(381, 815, clicks=2)
        time.sleep(1)
        print(idx, ':5')
        
        img = pyautogui.screenshot().crop((1140, 146, 1356, 219))
        diff = ImageChops.difference(img, b)
        if diff.getbbox():
            terminate_time = timeit.default_timer()
            f.write('(%d, %s), ' % (idx, str(id)))
            sendMail(mail_from, mail_to, 'Failure: #%s %d/%d [%ds]' % (str(id), idx+1, patient_list.shape[0], terminate_time - start_time))
            continue
        
        # 6. Click top of the list and scroll down to the bottom
        pyautogui.click(57, 512)
        time.sleep(1)
        pyautogui.press('f11')
        time.sleep(1)
        print(idx, ':6')
        
        # 7. Recognize the counts
        print(idx, ':7')
        img = pyautogui.screenshot().crop((1171, 507, 1172, 1020))
        img_ = np.asarray(img)
        count = 0
        for i in range(513):
            if np.array_equal(img_[i, 0, :], [104, 117, 163]):
                count += 1
        num = math.ceil(count / 16)
        if num == 0:
            terminate_time = timeit.default_timer()
            f.write('(%d, %s), ' % (idx, str(id)))
            sendMail(mail_from, mail_to, 'Failure (No data): #%s %d/%d [%ds]' % (str(id), idx+1, patient_list.shape[0], terminate_time - start_time))
            continue
        elif num < 30:
            t = 20 + num * 2
        else:
            t = 300
        print(idx, '7')
        
        # 9. Click "Print Test" button
        pyautogui.click(414, 60)
        time.sleep(1)
        print(idx, ':8')
        
        img = pyautogui.screenshot().crop((1203, 369, 1265, 445))
        diff = ImageChops.difference(img, c)
        if diff.getbbox():
            terminate_time = timeit.default_timer()
            f.write('(%d, %s), ' % (idx, str(id)))
            sendMail(mail_from, mail_to, 'Failure: #%s %d/%d [%ds]' % (str(id), idx+1, patient_list.shape[0], terminate_time - start_time))
            continue
        
        # 10. Click the area and drag for 10 seconds
        pyautogui.click(749, 311)
        time.sleep(1)
        for k in range(20):
            pyautogui.press('down')
        print(idx, ':9')
        
        # 11. Click "OK" button
        pyautogui.click(1194, 797)
        time.sleep(t)
        print(idx, ':10')
        
        # 12. Move '*.xml' files during calculated times
        os.system('move ' + savelocation + '\\*.xml ' + disklocation + '\\' + str(id) + '\\')
        time.sleep(10)
        print(idx, ':11')
        
        #13. Send confirmation mail
        terminate_time = timeit.default_timer()
        sendMail(mail_from, mail_to, 'Success: #%s %d/%d [%ds]' % (str(id), idx+1, patient_list.shape[0], terminate_time - start_time))
        print(idx, ':12')
    
    f.close()
    # os.system('shutdown -s -t 0')
