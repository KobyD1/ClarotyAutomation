import time
from datetime import datetime
import requests
from globals import BASE_URL, JSON_PATH, CHART_PATH, CHART_FILE, CHART_COUNTER_E2E, CHART_INTERVAL_E2E_SEC


class TestBtcToUsd():



    def test_bpi_process_e2e(self,configure_test):

        logger,mail_utils,chart_utils = configure_test
        results = []
        current_date = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
        logger.info(f"Analyze BPI details :start date-{current_date},counter-{CHART_COUNTER_E2E},sleep-{CHART_INTERVAL_E2E_SEC} Sec.")


        for i in range (CHART_COUNTER_E2E):
            response = requests.get(BASE_URL + "prices/BTC-USD/spot")
            response_amount = response.json()["data"]["amount"]
            current_time  = datetime.now().strftime("%H:%M:%S")
            results.append({"time": current_time,"price": response_amount})
            time.sleep(CHART_INTERVAL_E2E_SEC)
        logger.info(f"Analyze BPI end date : {datetime.now().strftime("%Y:%m:%d:%H:%M:%S")}")

        chart_utils.save_json(results,JSON_PATH)
        chart_utils.create_chart_with_json_data(JSON_PATH)
        chart_utils.save_chart_no_timestemp(CHART_FILE)
        max_rate = mail_utils.get_max_price()

        mail_as_dict= {
            "to": "kobyd100@gmail.com",
            "subject" : "Max rate for BPI found at E2E test",
            "attachment" : f'{CHART_PATH}{CHART_FILE}',
            "content" : f"Hi,\nFollowing your request, Max value for BPI found.\nThe value is: {max_rate}"
        }

        mail_utils.send_gmail(mail_as_dict)








