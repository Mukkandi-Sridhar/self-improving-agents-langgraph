from langgraph.graph import MessageGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
MAX_LOOPS = 2

def draft_answer(state):
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

def execute_tool(state):
    evidence = SystemMessage(
        content="Verified fact: The capital of France is Paris (source: Wikipedia)."
    )
    return {"messages": state["messages"] + [evidence]}

def revise_answer(state):
    prompt = HumanMessage(
        content="Revise your answer using the verified evidence above."
    )
    revised = llm.invoke(state["messages"] + [prompt])
    return {"messages": state["messages"] + [revised]}

def continue_loop(state):
    ai_count = len([m for m in state["messages"] if isinstance(m, AIMessage)])
    return "execute_tool" if ai_count <= MAX_LOOPS else END

builder = MessageGraph()
builder.add_node("draft", draft_answer)
builder.add_node("execute_tool", execute_tool)
builder.add_node("revise", revise_answer)

builder.set_entry_point("draft")
builder.add_edge("draft", "execute_tool")
builder.add_edge("execute_tool", "revise")
builder.add_conditional_edges("revise", continue_loop)

graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({
        "messages": [HumanMessage(content="What is the capital of France?")]
    })
    print(result["messages"][-1].content)
