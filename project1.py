import csv
import os

def load_rows(file):
    rows = []
    inFile = open(file)
    csvFile = csv.reader(inFile, quotechar='"', delimiter=',',
                         quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)
    
    headers = next(csvFile) 
    for row in csvFile:
        if len(row) >= 4:
            d = {}
            d["Country"] = row[0].strip()
            d["STEM Fields"] = row[1].strip()
            d["Year"] = row[2].strip()
            d["Female Enrollment (%)"] = row[3].strip()
            rows.append(d)
    inFile.close()
    return rows



def write_csv(file_name, data_list):
    outFile = open(file_name, "w", newline='')
    csvOut = csv.writer(outFile)
    for row in data_list:
        csvOut.writerow(row)
    outFile.close()

def main():
    file = "women_in_stem.csv"
  