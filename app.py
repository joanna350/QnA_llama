import os
import chainlit as cl

from langchain_community.llms import CTransformers
from langchain_core.prompts import PromptTemplate
from pymongo_get_database import get_database


llm = "TheBloke/zephyr-7B-beta-GGUF"  # model to download from

config = {
    "max_new_tokens": 1024, # curtails the output length
    "repetition_penalty": 1.1,
    "temperature": 0.5, # less determinstic with higher val
    "top_k": 30, 
    "top_p": 0.9,
    "stream": True,
    "threads": int(os.cpu_count() / 2)
}

llm_init = CTransformers(
    model=llm,
    model_type="zephyr",
    lib="avx2",
    **config
)

template = """Question: {question}

Response: Please stay factual and omit fiction.
"""

db = get_database()

@cl.on_chat_start
def main():
    prompt = PromptTemplate(template=template, input_variables=['question'])
    llm_chain = prompt | llm_init
    cl.user_session.set("llm_chain", llm_chain)

@cl.on_message
async def main(message: str):
    llm_chain = cl.user_session.get("llm_chain")
    dbresponse = db.collection.find({'question': message.content})
    try:
        # if the question is revistited
        res = dbresponse[0]['response']

    except Exception as e:
        # when new, use llm chain
        res = await llm_chain.ainvoke(message.content)

        # update the database
        await db.collection.insert_one({'question': message.content,
                                        'response': res})
    finally:
        await cl.Message(content=res).send()
