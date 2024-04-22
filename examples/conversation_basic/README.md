# Multi-Agent Conversation in AgentScope
This is a demo of how to program a multi-agent conversation in AgentScope.

In a nutshell, This example will show
- How to initialize an application with different LLM model configurations;
- How to use `DialogAgent` and `UserAgent`;
- How to use `sequentialpipeline` to simplify the workflow.

Complete code is in `conversation.py`, which set up a user agent and an
assistant agent to have a conversation. When user input "exit", the
conversation ends.
You can modify the `sys_prompt` to change the persona of assistant agent.
```bash
# Note: Set your api_key in conversation.py first
python conversation.py
```


## Tested Models

These models are tested with this example.
- [openai_chat](../model_configs_template/openai_chat_template.json)
- [dashscope_chat](../model_configs_template/dashscope_chat_template.json)
- [gemini_chat](../model_configs_template/gemini_chat_template.json)
- [ollama_chat](../model_configs_template/ollama_chat_template.json)



To set up model serving with open-source LLMs, follow the guidance in
[scripts/REAMDE.md](../../scripts/README.md).

## Prerequisites
No additional package is required.