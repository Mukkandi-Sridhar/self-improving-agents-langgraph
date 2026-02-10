from langgraph.graph import MessageGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
MAX_STEPS = 3

def generate_answer(state):
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

def reflect_answer(state):
    last_answer = state["messages"][-1].content
    critique_prompt = HumanMessage(
        content=f"Critique and improve the following answer:\n{last_answer}"
    )
    critique = llm.invoke([critique_prompt])
    return {"messages": state["messages"] + [critique]}

def should_continue(state):
    ai_msgs = [m for m in state["messages"] if isinstance(m, AIMessage)]
    return "reflect" if len(ai_msgs) < MAX_STEPS * 2 else END

builder = MessageGraph()
builder.add_node("generate", generate_answer)
builder.add_node("reflect", reflect_answer)
builder.set_entry_point("generate")
builder.add_conditional_edges("generate", should_continue)
builder.add_edge("reflect", "generate")

graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({
        "messages": [HumanMessage(content="Explain photosynthesis simply.")]
    })
    print(result["messages"][-1].content)
