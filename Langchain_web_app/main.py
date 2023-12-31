import streamlit as st
from langchain import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap

template = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Here are some examples of words in different dialects:
    - Direct: Mandatory, Immediate, Must, Obligatory, Hey, please, self-centered, realism, angry
    - Diplomatic: Suggest,Encourage, Seek, Request, Express, Can you?,indirect expression

    Example Sentences from each dialect:
    - Direct:Failure to meet the deadline will result in consequences.
    - Diplomatic: Professor, if I may, I would gently recommend exploring alternative approaches to potentially enhance our current strategy.
    
    Please start the email with a warm introduction. Add the introduction if you need to.
    
    Below is the email, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}
    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
    template=template,
)



llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0,google_api_key="AIzaSyDblIWduEI26ciFyajfO46GRww8T6CmZqI")


st.set_page_config(page_title = "Rewrite Email", page_icon=":robot:")
st.header("Rewrite Email")


col1, col2 = st.columns(2)

with col1:
    st.markdown("Often professionals would like to improve their emails, but don't have the skills to do so. \n\n This tool \
                will help you improve your email skills by converting your emails into a more professional format. I used GEMINI model.")
with col2:
    st.image(image='/Users/pandabada/Desktop/langchain/Langchain_web_app/img.jpg', width=500)


st.markdown("## Enter Your Email to Convert")

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your email to have?',
        ('Formal', 'Informal')
    )
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('Direct', 'Diplomatic')
    )
    
def get_text():
    input_text = st.text_area(label="", placeholder="Your Email...", key = "email_input")
    return(input_text)

email_input  = get_text()

st.write(email_input)

# tone, dialect, email_input 모두 동적이므로 lambda 사용

chain = ({
     "tone": lambda x: option_tone, 
     "dialect": lambda x: option_dialect,
     "email": lambda x: email_input} | prompt |llm)
 


st.markdown("## Your converted Email")

if email_input:

    st.markdown(chain.invoke({'email': email_input}).content)
    

    

    
# streamlit run /Users/pandabada/Desktop/langchain/Langchain_web_app/main.py
# 입력 예시 Hi Prof. Matthew, I am Park from the English presentation class 2. I would like to inquire about why I received a grade of B+. I believe my performance is better than my friend Kim's.
