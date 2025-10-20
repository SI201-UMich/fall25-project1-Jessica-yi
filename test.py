# SI 201 Project 1
# Your name: Keming Yi
# Your student id: 13466916
# Your email: kmyi@umich.edu
# Functions authored by: Keming Yi (all functions)
# Who or what you worked with on this project (including generative AI like ChatGPT):
# I worked alone on this project without other teammates.
# I asked Chatgpt hints for debugging and suggesting the general sturcture of the code. 
# It also gives me some tips and ideas for code logic.

from project1 import clean_rows, group_by_country_field, calc_avg_enrollment_by_country, calc_enrollment_change_earliest_latest, write_csv_avg_enroll


def mkrow(country, field, year, pct):
    return {"Country": country, "STEM Fields": field,
            "Year": str(year), "Female Enrollment (%)": str(pct)}

def test_clean_rows():
    print("Testing clean_rows...")

    rows = [mkrow("US", "Engineering", 2015, 30)]
    result = clean_rows(rows)
    assert len(result) == 1
    assert result[0]["Year"] == 2015 and result[0]["Female Enrollment (%)"] == 30.0

    rows = [
        mkrow("US", "Eng", 2015, 20),
        mkrow("US", "Eng", 2016, 40)
    ]
    result = clean_rows(rows)
    assert len(result) == 2

    rows = [mkrow("US", "CS", "20x6", 40)]
    result = clean_rows(rows)
    assert len(result) == 0

    rows = [mkrow("CN", "CS", 2018, 150)]
    result = clean_rows(rows)
    assert len(result) == 0

    print("clean_rows passed!")


def test_group_by_country_field():
    print("Testing group_by_country_field...")

    rows = [
        {"Country":"US","STEM Fields":"Eng","Year":2015,"Female Enrollment (%)":20},
        {"Country":"US","STEM Fields":"Eng","Year":2016,"Female Enrollment (%)":40},
        {"Country":"CN","STEM Fields":"CS","Year":2016,"Female Enrollment (%)":50},
    ]
    groups = group_by_country_field(rows)
    assert "US_Eng" in groups and "CN_CS" in groups
    assert len(groups["US_Eng"]) == 2 and len(groups["CN_CS"]) == 1

    rows = [
        {"Country":"US","STEM Fields":"Math","Year":2015,"Female Enrollment (%)":30},
        {"Country":"US","STEM Fields":"Math","Year":2016,"Female Enrollment (%)":35},
        {"Country":"US","STEM Fields":"Math","Year":2017,"Female Enrollment (%)":40},
    ]
    groups = group_by_country_field(rows)
    assert len(groups) == 1 and len(groups["US_Math"]) == 3


    groups = group_by_country_field([])
    assert len(groups) == 0

    rows = [{"Country":"JP","STEM Fields":"Bio","Year":2020,"Female Enrollment (%)":45}]
    groups = group_by_country_field(rows)
    assert list(groups.keys()) == ["JP_Bio"] and len(groups["JP_Bio"]) == 1

    print("group_by_country_field passed!")



def test_calc_avg_enrollment_by_country():
    print("Testing calc_avg_enrollment_by_country...")

    rows = [
        {"Country": "US", "STEM Fields": "Eng", "Year": 2015, "Female Enrollment (%)": 20},
        {"Country": "US", "STEM Fields": "Eng", "Year": 2016, "Female Enrollment (%)": 40}
    ]
    avg = calc_avg_enrollment_by_country(rows)
    assert abs(avg["US_Eng"] - 30) < 0.001

    rows.append({"Country": "CN", "STEM Fields": "CS", "Year": 2016, "Female Enrollment (%)": 50})
    avg = calc_avg_enrollment_by_country(rows)
    assert abs(avg["CN_CS"] - 50) < 0.001

    avg = calc_avg_enrollment_by_country([])
    assert len(avg) == 0

    rows = [{"Country": "JP", "STEM Fields": "Math", "Year": 2020, "Female Enrollment (%)": 40}]
    avg = calc_avg_enrollment_by_country(rows)
    assert abs(avg["JP_Math"] - 40) < 0.001

    print("calc_avg_enrollment_by_country passed!")



def test_calc_enrollment_change_earliest_latest():
    print("Testing calc_enrollment_change_earliest_latest...")


    rows = [
        {"Country": "US", "STEM Fields": "Eng", "Year": 2015, "Female Enrollment (%)": 20},
        {"Country": "US", "STEM Fields": "Eng", "Year": 2018, "Female Enrollment (%)": 32}
    ]
    changes = calc_enrollment_change_earliest_latest(rows)
    assert len(changes) == 1
    assert abs(changes[0][3] - 12) < 0.001   
    assert abs(changes[0][4] - 4) < 0.001    


    rows.extend([
        {"Country": "CN", "STEM Fields": "CS", "Year": 2019, "Female Enrollment (%)": 40},
        {"Country": "CN", "STEM Fields": "CS", "Year": 2022, "Female Enrollment (%)": 46}
    ])
    changes = calc_enrollment_change_earliest_latest(rows)
    found = False
    for c in changes:
        if "CN_CS" in c[0]:
            found = True
    assert found == True


    rows = [{"Country": "JP", "STEM Fields": "Math", "Year": 2020, "Female Enrollment (%)": 50}]
    changes = calc_enrollment_change_earliest_latest(rows)
    assert len(changes) == 0


    rows = [
        {"Country": "KR", "STEM Fields": "Bio", "Year": 2019, "Female Enrollment (%)": 40},
        {"Country": "KR", "STEM Fields": "Bio", "Year": 2019, "Female Enrollment (%)": 42}
    ]
    changes = calc_enrollment_change_earliest_latest(rows)
    assert len(changes) == 0

    print("calc_enrollment_change_earliest_latest passed!")


def test_write_csv_avg_enroll():
    print("Testing write_csv_avg_enroll...")


    avg = {"US_Eng": 30.0, "CN_CS": 50.0}
    fname = "tmp_avg.csv"
    write_csv_avg_enroll(fname, avg)
    f = open(fname, "r")
    text = f.read().strip()
    f.close()
    lines = text.splitlines()
    assert lines[0] == "Country_Field,Avg Female Enrollment (%)"
    joined = "\n".join(lines[1:])
    assert "US_Eng,30.00" in joined and "CN_CS,50.00" in joined


    avg = {"JP_Math": 40.0}
    fname = "tmp_avg_single.csv"
    write_csv_avg_enroll(fname, avg)
    f = open(fname, "r")
    text = f.read().strip()
    f.close()
    lines = text.splitlines()
    assert len(lines) == 2

  
    avg = {}
    fname = "tmp_avg_empty.csv"
    write_csv_avg_enroll(fname, avg)
    f = open(fname, "r")
    text = f.read().strip()
    f.close()
    lines = text.splitlines()
    assert len(lines) == 1


    avg = {"US_Eng": 33.3333}
    fname = "tmp_avg_round.csv"
    write_csv_avg_enroll(fname, avg)
    f = open(fname, "r")
    text = f.read()
    f.close()
    assert "33.33" in text

    print("write_csv_avg_enroll passed!")



def main():
    test_clean_rows()
    test_calc_avg_enrollment_by_country()
    test_calc_enrollment_change_earliest_latest()
    test_group_by_country_field()
    test_write_csv_avg_enroll()
    print("Yeah!All tests passed!")

main()