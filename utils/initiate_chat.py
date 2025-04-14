async def initiate_chat(agent, recipient, message):
    result = await agent.a_initiate_chat(recipient, message=message, clear_history=False)
    print(result)
    return result