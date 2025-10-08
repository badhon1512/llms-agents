from langgraph.graph import StateGraph, START,END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from typing import TypedDict, Union, List
from dotenv import load_dotenv

load_dotenv()

llm= ChatOpenAI(model = 'gpt-4.1-mini')

class AgentState(TypedDict):
    messages:List[Union[HumanMessage, AIMessage]]

def chat_bot(state:AgentState)->AgentState:

    response = llm.invoke(state['messages'])
    print(response.content)

    state['messages'].append(AIMessage(content=response.content))
    print(state['messages'])

    return state

graph = StateGraph(AgentState)

graph.add_node('chat_bot', chat_bot)

graph.add_edge(START, 'chat_bot')
graph.add_edge('chat_bot', END)

agent = graph.compile()

conversation_logs = []
while True:

    user_input = input('User Message: ')

    if user_input.lower() == 'exit':
        break

    conversation_logs.append(HumanMessage(content=user_input))
    response = agent.invoke({'messages':conversation_logs})

    conversation_logs = response['messages']



with open('logs.text', 'w') as file:
    file.write("Start of the logs \n")

    for messgae in conversation_logs:
        if isinstance(messgae, HumanMessage):
            file.write(f"You: {messgae.content} \n")
        elif isinstance(messgae, AIMessage):
            file.write(f"AI: {messgae.content}\n")    
    file.write("End of the logs")
