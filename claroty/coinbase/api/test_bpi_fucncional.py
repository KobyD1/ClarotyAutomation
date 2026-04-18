import time
from datetime import datetime
import requests
from globals import BASE_URL, JSON_PATH, CHART_PATH, CHART_FILE,CHART_COUNTER_FUNC

class TestBtcToUsd():
    def test_bpi_response_code(self):
        response = requests.get(BASE_URL+"prices/BTC-USD/spot")
        assert response.status_code == 200 , "Response Cose is not 200 as a result of HTTP Get request"

    def test_bpi_details(self):
        response = requests.get(BASE_URL+"prices/BTC-USD/spot")
        assert response.json()["data"]["base"] == "BTC" , "Response base did not include BTC as base "
        assert response.json()["data"]["currency"] == "USD" , "Response base did not include USD "


    def test_bpi_to_chart_file(self,configure_test):

        logger,mail_utils,chart_utils = configure_test
        results = []

        for i in range (CHART_COUNTER_FUNC):
            response = requests.get(BASE_URL + "prices/BTC-USD/spot")
            response_amount = response.json()["data"]["amount"]
            current_time  = datetime.now().strftime("%H:%M:%S")
            logger.debug(f"data for results JSON current_time:{current_time}, response amount: {response_amount}")
            results.append({"time": current_time,"price": response_amount})

            time.sleep(1)
        chart_utils.save_json(results,JSON_PATH)
        charts_before= chart_utils.count_files_in_folder_by_type("./data/charts_timestemp/*.png")
        chart_utils.create_chart_with_json_data(JSON_PATH)
        charts_after = chart_utils.save_chart_with_timestamp("btc_price_func")
        assert charts_before<charts_after , "Chart files did not increased at a results of BPI to Chart file"

    def test_get_max_bpi_and_send_mail(self,configure_test):
        logger,mail_utils,chart_utils = configure_test
        max_rate = mail_utils.get_max_price()

        mail_as_dict= {
            "to": "kobyd100@gmail.com",
            "subject" : "Max rate for BPI found at Coinbase",
            "attachment" : f'{CHART_PATH}{CHART_FILE}',
            "content" : f"Hi,\nFollowing your request, Max value for BPI found.\nThe value is: {max_rate}"
        }

        mail_utils.send_gmail(mail_as_dict)

    def test_result_json_items(self,configure_test):
        logger,mail_utils,chart_utils = configure_test
        json  = chart_utils.get_json_file(JSON_PATH)
        assert len(json)==CHART_COUNTER_FUNC, "Number of items into JSON results is not as expected"








