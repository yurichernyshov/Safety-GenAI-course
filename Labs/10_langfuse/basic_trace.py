import os
import base64

os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-65129ab4-67d7-43c8-985c-c080203b9cf9"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-5b31349f-acaf-46e7-823e-f7925c94e533"
os.environ["LANGFUSE_HOST"] = "http://localhost:3000"

LANGFUSE_AUTH = base64.b64encode(
    f"{os.environ['LANGFUSE_PUBLIC_KEY']}:{os.environ['LANGFUSE_SECRET_KEY']}".encode()
).decode()


from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from sentence_transformers import SentenceTransformer, util


from langfuse import observe, get_client

langfuse = get_client()

llm = ChatOllama(model="qwen3:4b")
retriever_model = SentenceTransformer("BAAI/bge-m3")

documents = [
    "Langfuse — это инструмент для трассировки пайплайнов LLM.",
    "LangChain — это фреймворк для построения цепочек вызова LLM.",
    "RAG использует retriever и генератор для ответов на вопросы.",
    "Prompt — способ задать контекст.",
    "Embedding — векторное представление текста."
]


@observe(name="retrieval", capture_input=True, capture_output=True)
def retrieve_context(query, top_k=3):
    doc_embeddings = retriever_model.encode(documents, convert_to_tensor=True)
    query_embedding = retriever_model.encode(query, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(query_embedding, doc_embeddings)[0]
    top_indices = similarities.topk(k=top_k).indices
    selected = [documents[i] for i in top_indices]

    context = "\n".join(selected)
    return context


@observe(name="llm_query", capture_input=True, capture_output=True)
def llm_qa(query, context):
    prompt = ChatPromptTemplate.from_template(
        "Ответь на вопрос используя контекст:\n\n{context}\n\nВопрос: {question}"
    )
    chain = prompt | llm
    result = chain.invoke({"context": context, "question": query})
    return result.content


question = "Что такое Langfuse?"
context = retrieve_context(question)
answer = llm_qa(question, context)
print("Ответ:", answer)
