# SI 201 Project 1
# Your name: Keming Yi
# Your student id: 13466916
# Your email: kmyi@umich.edu
# Functions authored by: Keming Yi (all functions)
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
    
    header = next(csvFile) 
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
            year_str = d["Year"].strip()
            pct_str = d["Female Enrollment (%)"].strip()

            i = 0
            while i < len(year_str) and year_str[i].isdigit():
                i = i + 1
            if i == 0:
                continue
            year_num_str = year_str[:i]
            if not year_num_str.isdigit():
                continue
            year = int(year_num_str)

            dot_count = 0
            ok = True
            for c in pct_str:
                if c == '.':
                    dot_count = dot_count + 1
                elif not c.isdigit():
                    ok = False
            if not ok or dot_count > 1 or pct_str == "":
                continue

            pct = float(pct_str)
            if pct < 0 or pct > 100:
                continue

            new_d = {
                "Country": d["Country"].strip(),
                "STEM Fields": d["STEM Fields"].strip(),
                "Year": year,
                "Female Enrollment (%)": pct
            }
            cleaned.append(new_d)
    return cleaned


def group_by_country_field(row_list):
    groups = {}
    for d in row_list:
        key = d["Country"] + "_" + d["STEM Fields"]
        if key not in groups:
            groups[key] = []
        groups[key].append(d)
    return groups


def calc_avg_enrollment_by_country(row_list):
    groups = group_by_country_field(row_list)
    avg_dict = {}
    for key in groups:
        total = 0
        count = 0
        for d in groups[key]:
            total = total + d["Female Enrollment (%)"]
            count = count + 1
        if count > 0:
            avg = total / count
            avg_dict[key] = avg
    return avg_dict


def calc_enrollment_change_earliest_latest(row_list):
    groups = group_by_country_field(row_list)
    result = []
    for key in groups:
        sorted_rows = sorted(groups[key], key=lambda x: x["Year"])
        if len(sorted_rows) >= 2:
            first = sorted_rows[0]
            last = sorted_rows[-1]
            y0 = first["Year"]
            y1 = last["Year"]
            p0 = first["Female Enrollment (%)"]
            p1 = last["Female Enrollment (%)"]
            net_change = p1 - p0
            year_gap = y1 - y0
            if year_gap != 0:
                per_year = net_change / year_gap
                result.append([key, y0, y1, net_change, per_year])
    return result


def write_csv_avg_enroll(file_name, avg_dict):
    outFile = open(file_name, "w", newline='')
    csvOut = csv.writer(outFile)
    csvOut.writerow(["Country_Field", "Avg Female Enrollment (%)"])
    for key in avg_dict:
        csvOut.writerow([key, "%.2f" % avg_dict[key]])
    outFile.close()


def write_csv_change(file_name, change_list):
    outFile = open(file_name, "w", newline='')
    csvOut = csv.writer(outFile)
    csvOut.writerow(["Country_Field", "Earliest Year", "Latest Year", "Net Change", "Per-Year Change"])
    for item in change_list:
        csvOut.writerow(item)
    outFile.close()


def main():
    file = "women_in_stem.csv"

    rows = load_rows(file)
    print("Total raw rows:", len(rows))

    clean = clean_rows(rows)
    print("Total cleaned rows:", len(clean))

    avg_dict = calc_avg_enrollment_by_country(clean)
    write_csv_avg_enroll("avg_enrollment.csv", avg_dict)
    print("Average enrollment written to avg_enrollment.csv")

    change_list = calc_enrollment_change_earliest_latest(clean)
    write_csv_change("enrollment_change.csv", change_list)
    print("Enrollment change written to enrollment_change.csv")

    print("Done!")

if __name__ == "__main__":
    main()