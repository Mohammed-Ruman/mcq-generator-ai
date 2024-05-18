import os,json,traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st

from langchain.callbacks import get_openai_callback
from src.mcqgenerator.mcqgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging


with open('ai_mcq_gen/Response.json','r') as file:
    RESPONSE_JSON=json.load(file)

st.title("MCQs Creator Application using Langchain and OpenAI")

with st.form("user_inputs"):
    uploaded_file=st.file_uploader("Upload a PDF or txt file")

    mcq_count=st.number_input("No of Questions", min_value=3, max_value=10)

    subject=st.text_input("Subject name", max_chars=20)

    tone=st.text_input("Complexity level", max_chars=20, placeholder="simple")

    button=st.form_submit_button("Generate MCQs")

    response=''

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating......."):
            try:
               text=read_file(uploaded_file)

               with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            "text":text,
                            "number":mcq_count,
                            "subject":subject,
                            "tone":tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    ) 
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("error")

            else:
                print(f"Total Tokens : {cb.total_tokens}")
                print(f"Prompt Tokens : {cb.prompt_tokens}")
                print(f"Completion Tokens : {cb.completion_tokens}")
                print(f"Total Cost : ${cb.total_cost}")

                if isinstance(response,dict):
                    mcqs=response.get('mcq',None)
                    if mcqs is not None:
                        data=get_table_data(mcqs)

                        if data is not None:
                            df=pd.DataFrame(data)
                            df.index=df.index+1
                            st.table(df)

                            st.text_area(label='Review', value=response['review'])
                        else:
                            str.write(response)

