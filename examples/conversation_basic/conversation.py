# -*- coding: utf-8 -*-
"""A simple example for conversation between user and assistant agent."""
import json
import os
import agentscope
from agentscope.agents import DialogAgent
from agentscope.agents.user_agent import UserAgent
from agentscope.pipelines.functional import sequentialpipeline


def main() -> None:
    """A basic conversation demo"""

    # replace the following JSON file with other available JSON files,
    # or create your own model config to use other LLM models.
    # E.g.,
    # ../model_configs_template/gemini_chat_template.json
    # ../model_configs_template/dashscope_chat_template.json
    with open(
        "../model_configs_template/openai_chat_template.json",
        encoding="utf-8",
    ) as f:
        model_configs = json.load(f)

    # you need to set the api_key as your API key
    api_key = os.getenv("OPENAI_API_KEY")
    for config in model_configs:
        if "api_key" in config:
            config["api_key"] = api_key

    agentscope.init(
        model_configs=model_configs,
    )

    # Init two agents
    dialog_agent = DialogAgent(
        name="Assistant",
        sys_prompt="You're a helpful assistant.",
        # replace by your model config name
        model_config_name="openai_chat_gpt-3.5-turbo",
    )
    user_agent = UserAgent()

    # start the conversation between user and assistant
    x = None
    while x is None or x.content != "exit":
        x = sequentialpipeline([dialog_agent, user_agent], x)


if __name__ == "__main__":
    main()
