import pytest
import notification_manager
import main
import flight_data
import flight_search
import data_manager


def Test_notification_manager():

    notification_manager.NotificationManager.send_message()

