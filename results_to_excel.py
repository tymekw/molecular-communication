import csv
import os

dirs = ['results_tymek/', 'resultskuba/', 'kp-results/', 'ResultsJb/']
results_names=['distance', 'modulation level', 'modulation strength', 'seed', 'ber']
with open('FINAL_RESULTS.csv', 'a+', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(results_names)

for dirname in dirs:
    directory = os.fsencode(dirname)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if '4' in filename:
            dist = '4'
        elif '8' in filename:
            dist = '8'
        else:
            dist = '2'

        with open(dirname + filename, 'r') as res:
            data = res.readlines()

        for idx, line in enumerate(data):
            if 'RESULTS' in line:
                tmp = line.split("_")
                seed = tmp[2]
                mod_lvl = tmp[5]
                mod_str = tmp[8].strip()
                ber = data[idx + 1].split(": ")[1].strip()
                results = [dist, mod_lvl, mod_str, seed, ber]
                with open('FINAL_RESULTS.csv', 'a+', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(results)

