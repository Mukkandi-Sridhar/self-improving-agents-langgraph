from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def think(state):
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

def act(state):
    tool_result = AIMessage(
        content="Tool result: NYC weather is sunny, 25°C."
    )
    return {"messages": state["messages"] + [tool_result]}

def decide(state):
    last = state["messages"][-1].content.lower()
    if "weather" in last:
        return "act"
    return END

graph = StateGraph(dict)
graph.add_node("think", think)
graph.add_node("act", act)
graph.set_entry_point("think")
graph.add_conditional_edges("think", decide, {"act": "act", END: END})
graph.add_edge("act", "think")

compiled = graph.compile()

if __name__ == "__main__":
    result = compiled.invoke({
        "messages": [HumanMessage(content="Check the weather in NYC")]
    })
    print(result["messages"][-1].content)
