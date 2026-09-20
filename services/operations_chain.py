from dotenv import load_dotenv

from models.operations_answer import OperationsAnswer

load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

prompt = ChatPromptTemplate.from_template("""
You are a hospital operations analyst.
Given the question and data below, answer using ONLY the data provided.

Question: {question}
Data: {data}
""")

model = ChatGoogleGenerativeAI(model="gemini-3.6-flash").with_structured_output(OperationsAnswer)

operations_chain = prompt | model
