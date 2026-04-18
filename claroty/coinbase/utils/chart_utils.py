import glob
import json
import matplotlib.pyplot as plt
from datetime import datetime
import shutil
import os

from globals import CHART_PATH, CHART_FILE


class ChartUtils():

    def __init__(self, logger):
        self.logger = logger

    def set_graph_dynamic_data(self, response_amount):
        x = []
        y = []
        plt.ion()

        now = datetime.now()
        time = now.strftime("%S")
        x.append(time)
        y.append(response_amount)
        self.ax.plot(x, y, marker="o", color='blue')

    def save_graph(self):
        current_time = datetime.now().strftime("%m%d%H%M%S")
        file_name = f"./data/charts/btc_price_{current_time}.png"
        self.logger.info(f"saving graph in {file_name}")
        self.fig.savefig(file_name, dpi=300, bbox_inches="tight")

    def save_json(self, data: list, path: str):
        file = open(path, "w")
        self.logger.info(f"saving JSON Data in {path}")
        json.dump(data, file)

    def create_chart_with_json_data(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        times = [datetime.strptime(item["time"], "%H:%M:%S") for item in data]  # casting to time format , for easy data visualization

        prices = [float(item["price"]) for item in data]

        plt.figure(figsize=(10, 7))
        plt.plot(times, prices, marker="o")
        plt.title("BPI Over Time")
        plt.xlabel("Time")
        plt.ylabel("BPI")
        plt.grid(True)
        plt.tight_layout()

    def save_chart_with_timestamp(self, file_prefix='btc_price'):
        current_time = datetime.now().strftime("%m%d%H%M%S")
        path = f'./data/charts_timestemp/' + file_prefix + f'_{current_time}.png'
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        # count the number of files in folder as a base value to assert if file cretated
        file_count = len(glob.glob("./data/charts_timestemp/*.png"))
        self.logger.info(f"chart success to saved at {path},files count = {file_count}")
        return file_count

    def save_chart_no_timestemp(self, file_name=CHART_FILE):
        shutil.rmtree(CHART_PATH)  # delete all files in folder before each save , stability issue
        os.makedirs(CHART_PATH)
        plt.savefig(CHART_PATH + file_name, dpi=300, bbox_inches='tight')
        plt.close()
        self.logger.info(f"chart success to saved at {CHART_PATH}{file_name}")
        return len(glob.glob(f"{CHART_PATH}"+"*.png"))

    def count_files_in_folder_by_type(self, path: str):
        file_count = len(glob.glob(path))
        self.logger.info(f" {file_count} files found in {path}")

        return file_count

    def get_json_file(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
