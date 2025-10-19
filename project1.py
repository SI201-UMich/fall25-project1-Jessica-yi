# SI 201 Project1
# Your name: Keming Yi
# Your student id: 13466916
# Your email: kmyi@umich.edu
# Who or what you worked with on this project (including generative AI like ChatGPT):
# I worked alone on this project without other teammates.
# I asked Chatgpt hints for debugging and suggesting the general sturcture of the code. 
# It also gives me some tips and ideas for code logic.


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

def clean_rows(row_list):
    cleaned = []
    for d in row_list:
        if d["Country"] != "" and d["STEM Fields"] != "" and d["Year"] != "" and d["Female Enrollment (%)"] != "":
            if d["Year"].isdigit():
                year = int(d["Year"])
                pct = 0
                dot_count = 0
                for c in d["Female Enrollment (%)"]:
                    if c == '.':
                        dot_count = dot_count + 1

                if d["Female Enrollment (%)"].replace('.', '').isdigit() and dot_count <= 1:
                    pct = float(d["Female Enrollment (%)"])
                    if pct >= 0 and pct <= 100:
                        new_d = {}
                        new_d["Country"] = d["Country"]
                        new_d["STEM Fields"] = d["STEM Fields"]
                        new_d["Year"] = year
                        new_d["Female Enrollment (%)"] = pct
                        cleaned.append(new_d)
    return cleaned




def main():
    file = "women_in_stem.csv"
    rows = load_rows(file)
    print("Total raw rows:", len(rows))
    clean = clean_rows(rows)
    print("Total cleaned rows:", len(clean))

    print("Done!")