# Self-Improving Agents with LangGraph

⏱️ Estimated reading time: 10 minutes

This repository is a concise cheat sheet explaining how to build **self-improving AI agents** using **LangGraph**.  
It focuses on three core agent architectures that allow models to critique, verify, and improve their own outputs.

---

## Why Self-Improving Agents?

Most LLM applications fail because they:
- Stop after the first response
- Don’t verify correctness
- Can’t use tools intelligently

Self-improving agents solve this by introducing **feedback loops** where the agent:
1. Generates an answer  
2. Reviews or verifies it  
3. Refines the output  

LangGraph makes these loops explicit and easy to design using graph-based state transitions.

---

## Agent Categories

| Agent Type | Description |
|-----------|-------------|
| **Reflection** | Model critiques its own answer |
| **Reflexion** | Model critiques using external feedback (tools/search) |
| **ReAct** | Model alternates reasoning and actions in a loop |

---

## LangGraph Basics

LangGraph represents agents as:
- **State** → usually message history
- **Nodes** → LLM calls or functions
- **Edges** → control flow with conditional routing

This structure makes agent behavior explicit, debuggable, and extensible.

---

## 1️⃣ Reflection Agents

Reflection agents improve answers using **internal self-critique only**.

### Workflow
1. Generate an answer  
2. Reflect on the answer  
3. Revise  
4. Repeat until a limit is reached  

### When to use
- Writing
- Explanations
- Idea refinement

### Conceptual Example

```python
generate_answer()
critique_answer()
loop_until_done()
```

### Limitations
- No new information enters the system
- Quality may plateau if the model misses errors

---

## 2️⃣ Reflexion Agents

Reflexion agents extend reflection by adding **external grounding**.

### Workflow
1. Draft an answer  
2. Call tools or search  
3. Revise using evidence  
4. Repeat if needed  

### Why it’s powerful
- Forces verification
- Reduces hallucinations
- Encourages explicit corrections

### When to use
- Fact-checking
- Research
- Coding with correctness constraints
- Tasks requiring citations

### Conceptual Example

```python
draft_answer()
execute_tool_or_search()
revise_with_evidence()
loop_until_verified()
```

### Trade-off
- Slower and more complex due to tool calls

---

## 3️⃣ ReAct Agents

ReAct (Reason + Act) agents **interleave thinking and acting**.

### Workflow
- Reason about the next step
- Call a tool if required
- Observe results
- Reason again
- Continue until a final answer is produced

### Key advantages
- Dynamic decision-making
- Flexible tool usage
- No separate reflection step

### When to use
- APIs
- Databases
- Multi-step workflows
- Planning tasks

### Conceptual Example

```python
think()
if tool_needed:
    act()
observe()
repeat_until_done()
```

---

## Comparison of Agent Styles

| Aspect | Reflection | Reflexion | ReAct |
|------|-----------|-----------|-------|
| Feedback source | Internal | External + internal | External (tools) |
| Accuracy | Medium | High | High |
| Complexity | Low | High | Medium |
| Best for | Writing & refinement | Verification & research | Tool-driven tasks |

---

## Final Takeaway

- **Reflection** → simplest self-improvement  
- **ReAct** → most flexible execution  
- **Reflexion** → highest reliability  

LangGraph allows you to start simple and evolve toward more powerful agent systems.

---

## Author

**Sridhar Royal**  
BTech Student | Agentic AI | LangGraph  
