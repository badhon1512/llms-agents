from typing import Dict, TypedDict, List
from langgraph.graph import START,END, StateGraph
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI(model='gpt-4.1-mini')

# Initialize Groq LLM (llama3-8b-8192)
# llm = ChatGroq(
#     model="llama3-8b-8192",
#     temperature=0.7,
#     api_key=os.getenv("GROQ_API_KEY")
# )


class AgentState(TypedDict):
    messages:List[HumanMessage]


def bot(state:AgentState)->AgentState:

    response = llm.invoke(state['messages'])

    print(response.content)

    return state

graph = StateGraph(AgentState)

graph.add_node('chat', bot)
graph.add_edge(START, 'chat')
graph.add_edge('chat', END)

app = graph.compile()

input_text = ''
while input_text.lower()!='exit':

    input_text = input('Human message : ')

    if input_text.lower()=='exit':
        break

    app.invoke({'messages':[HumanMessage(content=input_text)]})



