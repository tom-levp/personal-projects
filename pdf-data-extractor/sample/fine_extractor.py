from PyPDF2 import PdfReader, PdfWriter
import multiprocessing, pathlib, re, json, time, locale, calendar
import pandas as pd

locale.setlocale(locale.LC_ALL, u'fr')

ROOT_DIR = pathlib.Path(__file__).resolve().parent
RAW_DATA_DIR = pathlib.Path(ROOT_DIR.parent, "data", "input")
PROCESSED_DATA_DIR = pathlib.Path(ROOT_DIR.parent, "data", "output", "pdf")
STRUCTURED_DATA_DIR = pathlib.Path(ROOT_DIR.parent, "data", "output", "extraction")

# Substrings allowing to target relevant pagesin multiple-page files
SUBSTRINGS = ["post-stationnement", "www.stationnement.gouv.fr"]

NUMBER_OF_PROCESSES = 6

def get_pdf_path(dict):
    ''''''
    year = dict['Date'][-4:]
    month = dict['Date'][3:5]
    month_name = month + "-" + calendar.month_name[int(month)].capitalize()

    final_dir = pathlib.Path(PROCESSED_DATA_DIR, f"{year}", f"{month_name}")
    if final_dir.exists():
        pass
    else:
        final_dir.mkdir(parents=True, exist_ok=True)
    path_to_file = pathlib.Path(final_dir, f"{dict['id']}.pdf")

    return path_to_file


def pdf_extractor(file):
    ''''''
    if file.suffix == ".pdf" and file.is_file():
        filePath = file.as_posix()
        reader = PdfReader(filePath)
        
        file_structured_data = []

        last_page = ""

        for page in reader.pages:

            text = page.extract_text()
            fine = '\n'.join(text).replace('\r', '').replace('\n', '')
            
            if SUBSTRINGS[0] in text and SUBSTRINGS[1] not in text: # Means current page is main fine page
                if last_page == "fine_page":
                    pdf_path = get_pdf_path(fine_dict)
                    try:
                        with pdf_path.open("wb") as output_stream:
                            output.write(output_stream)
                    except:
                        print(f"Could not create {fine_dict['id']}.pdf")                 
                
                fine_dict = data_structuration(fine)
                file_structured_data.append(fine_dict)

                output = PdfWriter()
                output.add_page(page)

                last_page = "fine_page"
            
            elif SUBSTRINGS[0] not in text and SUBSTRINGS[1] in text: # Means current page is not main fine page
                output.add_page(page)

                pdf_path = get_pdf_path(fine_dict)

                try:
                    with pdf_path.open("wb") as output_stream:
                        output.write(output_stream)
                except:
                    print(f"Could not create {fine_dict['id']}.pdf")
                
                last_page = "modalites_page"

        if last_page == "fine_page":
            pdf_path = get_pdf_path(fine_dict)
            try:
                with pdf_path.open("wb") as output_stream:
                    output.write(output_stream)
            except:
                print(f"Could not create {fine_dict['id']}.pdf")
                 
    try:
        file.unlink()
    except FileNotFoundError:
        print("File not found")
    
    return file_structured_data


def data_structuration(fine):
    ''''''
    try:
        immat_vehicule = re.search("\w\s*\w\s*-\s*\d\s*\d\s*\d\s*-\s*\w\s*\w", fine).group().replace(" ", "")
        if immat_vehicule[0:2] == "GO":
            immat_vehicule = immat_vehicule.replace("GO", "GD")
    except AttributeError:
        immat_vehicule = ""

    try:
        date = re.search("[Ll]e\s*([\d\s]+\/[\d\s]+\/[\d\s]{4}?)", fine).group(1).replace(" ", "")
    except AttributeError:
        date = ""

    try:
        hour = re.search("[Ll]e\s*[\d\s]+\/[\d\s]+\/[\d\s]{4}\s*à\s*([A-Za-z0-9]{1}\s*[A-Za-z0-9]{1}\s*[Hh]\s*[A-Za-z0-9]{1}\s*[A-Za-z0-9]{1})", fine).group(1).replace(" ", "").replace("O", "0")
    except AttributeError:
        hour = ""

    try:
        address = re.search("Lieu\s*:[\s~\-]*(\d*\s[a-zA-Z_ ÈÊÉ\-\r\n']*)\s+\d*", fine).group(1).strip()
        # "Lieu\s*:\s*[A-Z ÀÈÉ\r\n'-:]*"
    except AttributeError:
        address = ""

    try:
        zip_code = re.search("Lieu\s*:[\s~\-]*\d*\s[a-zA-Z_ ÈÊÉ\-\r\n']*\s+([A-Za-z0-9]{5}?)", fine).group(1)
        if not zip_code.isnumeric():
            zip_code = ""
    except AttributeError:
        zip_code = ""

    try:
        amount = re.search("\s*à\s*:\s*(\d{1,3}\,?\d{1,3})\s*euros", fine).group(1)
    except AttributeError:
        amount = ""

    fine_id = date[-4:] + date[3:5] + date[0:2] + "_" + hour.replace("h", "") + "_" + immat_vehicule.replace("-", "")

    dict = {

        "id": fine_id,
        "Plate": immat_vehicule,
        "Date": date,
        "Hour": hour,
        "Amount": amount,
        "Address": address,
        "Zip Code": zip_code

    }

    return dict


def pool_handler():
    ''''''
    # Start the stopwatch / counter
    t1_start = time.perf_counter()

    pool = multiprocessing.Pool(processes=NUMBER_OF_PROCESSES)
    file_dicts_list = pool.map(pdf_extractor, RAW_DATA_DIR.glob('**/*')) # arg1=target_function | arg2=target_function_iterable

    fines = []

    for file_dicts in file_dicts_list:
        for dict in file_dicts:
            fines.append(dict.copy())
    
    # Stop the stopwatch / counter
    t1_stop = time.perf_counter()

    print("Temps écoulé en secondes :", t1_stop-t1_start)

    return fines


def save_data(retrieved_data, fileName):
    ''''''
    json_path = pathlib.Path(STRUCTURED_DATA_DIR, f"{fileName}.json")
    csv_path = pathlib.Path(STRUCTURED_DATA_DIR, f"{fileName}.csv")

    if pathlib.Path(json_path).is_file():
        with open(json_path, 'r', encoding="utf8") as ledger:
            jsonData = json.load(ledger)
        jsonData.extend(retrieved_data)
    else:
        jsonData = retrieved_data.copy()

    jsonData_clean = [i for n, i in enumerate(jsonData) if i not in jsonData[n + 1:]] # Removes duplicates

    # write JSON files:
    with json_path.open("w", encoding="UTF-8") as target: 
        json.dump(jsonData_clean, target, indent=4, ensure_ascii=False)

    # write CSV files:
    df = pd.read_json(json_path, encoding='utf-8-sig')
    df.to_csv(csv_path, index = None, encoding='utf-8-sig')

def main():
    retrieved_data = pool_handler()
    save_data(retrieved_data, "structured_data")

if __name__ == '__main__':
    main()