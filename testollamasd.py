import ollama
import asyncio
from stablediffusion import generate
from ollama import ChatResponse

async def main():
    client = ollama.AsyncClient()

    prompt =input("Jyothisree input something!")
    availablefunctions ={
        'generate':generate,
    }
    response: ChatResponse =await client.chat(
        'mistral-nemo',
        messages=[{'role' : 'user', 'content':prompt}],
        tools = [generate]
    )
    if response.message.tool_calls:
                for tool in response.message.tool_calls:
                    if function_to_call := availablefunctions.get(tool.function.name):
                        print('Calling function:', tool.function.name)
                        print('Arguments:', tool.function.arguments)
                        print('Function output:', function_to_call(**tool.function.arguments))
                    else:
                        print('Function', tool.function.name, 'not found')

if __name__ == "__main__":
        asyncio.run(main())   
                         