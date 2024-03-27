import pandas as pd
from datetime import datetime

FILENAME = "RHT20 03-04-24  15.53.27.xls"
FORMATTED_FILE = f"{FILENAME[:-4]}_formatted{FILENAME[-4:]}"
OUTPUT_FILE = f"{FILENAME[:-4]}_processed{FILENAME[-4:]}"

with open(FILENAME, "rt") as f_input:
    with open(FORMATTED_FILE, "wt") as f_output:
        # header
        for i in range(10):
            f_output.write(f_input.readline())

        # table header
        table_header = f_input.readline().strip().replace("\t", "")
        table_header = ','.join(table_header.split())
        f_output.write(table_header + "\n")

        # data lines
        while True:
            line = f_input.readline()
            if not line:
                break
            line = line.replace("\t", " ").replace(
                "C", " ").replace("%RH", " ")
            line = line.split()
            line = line[0:-2] + [line[-2] + " " + line[-1]]
            line = ','.join(line)
            f_output.write(line + "\n")

df = pd.read_csv(FORMATTED_FILE, skiprows=10, usecols=["Temp", "RH", "TIME"])

TIME_FORMAT = "%m/%d/%y %H:%M:%S"


def convert_string_to_timestamp(my_date: str):
    dt_object = datetime.strptime(my_date, TIME_FORMAT)
    return int(dt_object.timestamp())


df["TIME"] = df["TIME"].apply(convert_string_to_timestamp)
df.to_csv(OUTPUT_FILE, index=False)