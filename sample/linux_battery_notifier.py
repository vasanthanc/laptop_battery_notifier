#!/usr/bin/python3
import os
import json
import subprocess
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify
class LinuxBatteryNotifier(object):
    BATTERY_INFO_ROOT_PATH = "/sys/class/power_supply/"
    BATTERY_CURRENT_CAPACITY = "BAT0/capacity"
    BATTERY_CURRENT_STATUS = "AC/online"
    PROGRAM_DATA_LOCATION = os.path.expanduser("~/.battery_noti/info.txt")

    def get_information_from_file_path(self,path):
        file_text = None
        with open(path,'r',encoding = 'utf-8') as input_file:
            file_text = input_file.read()
        file_text = file_text.rstrip()
        return file_text

    def write_data_to_the_file(self,file_path,data):
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(file_path,'w',encoding = 'utf-8') as input_file:
            input_file.write(data)

    def get_battery_related_information(self):
        capacity_path = os.path.join(self.BATTERY_INFO_ROOT_PATH,self.BATTERY_CURRENT_CAPACITY)
        current_status_path = os.path.join(self.BATTERY_INFO_ROOT_PATH,self.BATTERY_CURRENT_STATUS)
        capacity_info_text = self.get_information_from_file_path(capacity_path)
        current_status_info = self.get_information_from_file_path(current_status_path)
        return {"capacity": capacity_info_text, "status": current_status_info}

    def get_battery_related_information_and_write_to_a_file(self):
        battery_status_info = self.get_battery_related_information()
        battery_status_json_info = json.dumps(battery_status_info, ensure_ascii=False)
        self.write_data_to_the_file(self.PROGRAM_DATA_LOCATION,battery_status_json_info)

    def read_last_battery_information_form_program_location(self):
        current_status_info = self.get_battery_related_information()
        last_battery_information = self.get_information_from_file_path(self.PROGRAM_DATA_LOCATION)
        last_battery_info = json.loads(last_battery_information)
        last_capacity = int(last_battery_info["capacity"])
        current_capacity = int(current_status_info["capacity"])
        last_status = int(last_battery_info["status"])
        current_status = int(current_status_info["status"])
        if not last_status == current_status:
            summary = "Battery Status"
            body = ""
            if current_status == 1:
                body = "Charging"
            else:
                body = "Discharging"
            self.show_notification(summary,body)
            #os.system('notify-send "TITLE" {}'.format(current_status))
        if last_capacity < 100 and current_capacity == 100:
            summary = "Power Alert"
            detail = "Charge Full Please remove power card"
            self.show_notification(summary,detail)
            #os.system('notify-send "TITLE" "Charge Full Please remove power card"')
        if current_capacity <= 35 and last_capacity > 35:
            summary = "Power Alert"
            detail = "Please connect to Charger"
            self.show_notification(summary,detail)
            #os.system('notify-send "TITLE" "Please connect to Charger"')
    
    def show_notification(self,summary="",detail=""):
        Notify.init("Linux Battery Notifier")
        # Create the notification object
        notification = Notify.Notification.new(summary,detail)
        # Actually show on screen
        notification.show()

if __name__ == "__main__":
    l = LinuxBatteryNotifier()
    l.read_last_battery_information_form_program_location()
    l.get_battery_related_information_and_write_to_a_file()

