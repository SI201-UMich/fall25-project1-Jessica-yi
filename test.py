# SI 201 Project1
# Your name: Keming Yi
# Your student id: 13466916
# Your email: kmyi@umich.edu
# Who or what you worked with on this project (including generative AI like ChatGPT):
# I worked alone on this project without other teammates.
# I asked Chatgpt hints for debugging and suggesting the general sturcture of the code. 
# It also gives me some tips and ideas for code logic.

from project1 import load_rows, clean_rows, calc_avg_enrollment_by_country, calc_enrollment_change_earliest_latest


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



def main():
    test_clean_rows()
    print("Yeah!All tests passed!")
    test_calc_avg_enrollment_by_country()
    test_calc_enrollment_change_earliest_latest()

main()