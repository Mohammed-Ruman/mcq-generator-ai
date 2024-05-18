import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file,get_table_data

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

load_dotenv()
# KEY=os.getenv("API_KEY")
KEY="sk-87e26a08cec34502a0aa6d26df227317"



llm=ChatOpenAI(api_key=KEY, 
               base_url="https://api.deepseek.com",
               model_name='deepseek-chat', temperature=0.7
               )


TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

mcq_generation_template=PromptTemplate(
    input_variables=['text','number','subject','tone','response_json'],
    template=TEMPLATE 
)

mcq_chain=LLMChain(llm=llm,prompt=mcq_generation_template, output_key='mcq', verbose=True)

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{mcq}

Check from an expert English Writer of the above quiz:
"""

mcq_evalution_prompt=PromptTemplate(
    input_variables=['subject','mcq'],
    template=TEMPLATE2
    )

review_chain=LLMChain(llm=llm,prompt=mcq_evalution_prompt,output_key='review', verbose=True)

generate_evaluate_chain=SequentialChain(chains=[mcq_chain, review_chain], 
                                        input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["mcq", "review"], verbose=True,)