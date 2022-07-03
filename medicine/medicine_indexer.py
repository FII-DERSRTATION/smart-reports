import ast
import json

from db.connector import connect_to_kis_db_no_config_file
from utils.bucketutil import BucketUtil


def collect_medicine(medicine_json, parse_exit_medicine=False):
    """
        parse the medicine field from the sql db and collects all de medicines in an list
    """
    parsed_medicine = json.loads(medicine_json)
    medicines = []
    iterobject = None

    if parse_exit_medicine:
        iterobject = parsed_medicine["MediAustritt"]
    else:
        iterobject = parsed_medicine["MediEintritt"]

    try:
        for e in iterobject['Medis']['List']:
            medicines.append(e['Markenname'])
    except Exception as e:
        print(e)

    return medicines


def collect_diagnostics(diagnostic_json):
    """
        parse the diagnosed json from the sql db and return the list with the collected diagnostics.
    """

    a = json.loads(diagnostic_json)

    diagnostic = []

    try:
        for e in a['Diagnosen']['Diagnosen']['List']:
            if 'Titel' not in e:
                continue

            title = e['Titel']
            diagnostic.append(title)
    except Exception as e:
        print(e)

    return diagnostic


def populate_medicine_jsons(db):
    f = open('medicine_entrance.json')
    medicine_entrance = ast.literal_eval(f.read())
    f.close()

    f = open('mecicine_exit.json')
    medicine_exit = ast.literal_eval(f.read())
    f.close()

    cursor = db.cursor()
    cursor.execute(
        "select distinct kis_reports.report_nf.diagnosen, kis_reports.report_nf.mediAustritt, kis_reports.report_nf.mediEintritt from kis_reports.report_nf where kis_reports.report_nf.mediAustritt != '' and kis_reports.report_nf.mediEintritt != '' limit 50000")
    records = cursor.fetchall()

    for record in records:
        diagnostics = collect_diagnostics(record[0])
        probabilistic_diag = BucketUtil.find_appropriate_disease_german(diagnostics)

        meds_entry = collect_medicine(record[2].decode("UTF-8"))
        meds_exit = collect_medicine(record[1].decode("UTF-8"), parse_exit_medicine=True)

        for med in meds_entry:
            if med == '':
                continue

            if med in medicine_entrance[probabilistic_diag]:
                medicine_entrance[probabilistic_diag][med] += 1
            else:
                medicine_entrance[probabilistic_diag][med] = 1

        for med in meds_exit:
            if med == '':
                continue

            if med in medicine_exit[probabilistic_diag]:
                medicine_exit[probabilistic_diag][med] += 1
            else:
                medicine_exit[probabilistic_diag][med] = 1

    with open("/Users/danilamarius-cristian/PycharmProjects/pythonProject2/medicine/medicine_entrance.json", "w") as f:
        json.dump(medicine_entrance, f)

    with open("/Users/danilamarius-cristian/PycharmProjects/pythonProject2/medicine/mecicine_exit.json", "w") as f:
        json.dump(medicine_exit, f)


def pick_medicine_suggestions(diagnostic):
    f = open('/Users/danilamarius-cristian/PycharmProjects/pythonProject2/medicine/medicine_entrance.json')
    medicine_entrance = ast.literal_eval(f.read())
    f.close()

    f = open('/Users/danilamarius-cristian/PycharmProjects/pythonProject2/medicine/mecicine_exit.json')
    medicine_exit = ast.literal_eval(f.read())
    f.close()

    recomandation_entrance = []
    recomandation_exit = []

    count = 0
    for medicine in medicine_entrance[diagnostic]:
        if count > 10:
            break
        recomandation_entrance.append(medicine)

    count = 0
    for medicine in medicine_exit[diagnostic]:
        if count > 10:
            break
        recomandation_exit.append(medicine)

    return recomandation_entrance, recomandation_exit



if __name__ == "__main__":
    db = connect_to_kis_db_no_config_file()
    populate_medicine_jsons(db)
