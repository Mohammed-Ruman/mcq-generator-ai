import os, PyPDF2,json, traceback

def read_file(file):
    if file.name.endswith('.pdf'):
        try :
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=''

            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception as e:
            raise Exception("Error reading PDF File")
    
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    
    else:
        raise Exception('Unsupported File Format - PDF & Text is allowed')

def get_table_data(quiz_str):
    mcqs_string=quiz_str.strip('` \n\t').replace('json','')
    try:
        mcqs_json=json.loads(mcqs_string)
        quiz_table_data=[]

        for key, value in mcqs_json.items():
            mcq = value["mcq"]
            options = " || ".join(
                [
                    f"{option}: {option_value}"
                    for option, option_value in value["options"].items()
                    ]
                )
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e),e,e.__traceback__)
        return False
    