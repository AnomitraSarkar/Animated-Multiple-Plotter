import time
import csv

if __name__ == "__main__":
    with open("../sensor_data.csv") as f:
        csv_reader = csv.reader(f)
        for i in csv_reader:
            with open("data.csv","a",newline="") as dump:
                csv_writer = csv.writer(dump)
                csv_writer.writerow(i)
            time.sleep(0.1)
            
        