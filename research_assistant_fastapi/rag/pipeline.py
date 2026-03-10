import os
from dotenv import load_dotenv
from groq import Groq

from .embedding import generate_embedding
from .vector_store import search

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Retrieve context
def retrieve_context(query, top_k=3):
    query_embedding = generate_embedding(query)
    results = search(query_embedding, top_k=top_k)
    context_chunks = []
    for item in results:
        if isinstance(item, str):
            context_chunks.append(item)
        elif hasattr(item, "text"):
            context_chunks.append(item.text)
    print("Context retrieved:", context_chunks)
    return context_chunks

# Fix code blocks
def fix_code_blocks(markdown_text):
    if not markdown_text:
        return ""
    lines = markdown_text.split("\n")
    fixed_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            if i > 0 and lines[i-1].strip() != "":
                fixed_lines.append("")
            leading_spaces = len(line) - len(line.lstrip())
            if leading_spaces > 1:
                line = "" + stripped
            if stripped == "```":
                line = ""
        fixed_lines.append(line)
    return "\n".join(fixed_lines)

# Generate answer
def generate_answer(query, context_chunks):
    if not context_chunks:
        return "No document found. Please upload a relevant document first (pdf,image)."

    context = "\n\n".join(context_chunks)
    prompt = f"""
Answer the question using ONLY the provided context and return adjusted and complete answer until content related to the topic is fully complete.
Context:
{context} 

Question:
{query}

Answer:
"""
    full_answer = ""
    temp_prompt = prompt
    while True:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": temp_prompt}],
            max_tokens=2000
        )
        partial_answer = response.choices[0].message.content.strip()
        full_answer += partial_answer
        if partial_answer.endswith((".", "?", "!", "\n\n")) or len(partial_answer) < 1024:
            break
        else:
            temp_prompt = f"Continue the previous answer from where it stopped:\n{partial_answer}"
    return fix_code_blocks(full_answer)

# Generate answer with query only
def generate_answer_withQuery_Only(query, query_chunk):
    prompt = f"""
Answer the question related to that topic and return adjusted and complete answer until unless content related to topic is complete.

Context:
{query_chunk}
Question:
{query}

Answer:
"""
    full_answer = ""
    temp_prompt = prompt
    while True:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": temp_prompt}],
            max_tokens=2000
        )
        partial_answer = response.choices[0].message.content.strip()
        full_answer += partial_answer
        if partial_answer.endswith((".", "?", "!", "\n\n")) or len(partial_answer) < 1024:
            break
        else:
            temp_prompt = f"Continue the previous answer from where it stopped:\n{partial_answer}"
    return fix_code_blocks(full_answer)

# Query chunks
query_chunk = []

# Full RAG pipeline
def run_rag_pipeline(query):
    global query_chunk
    context_chunks = retrieve_context(query)
    answer = generate_answer(query, context_chunks)
    answer_with_query_only = generate_answer_withQuery_Only(query, query_chunk)
    query_chunk.append(answer_with_query_only)
    if len(query_chunk) > 2:
        query_chunk.pop(0)
    if answer_with_query_only and not context_chunks:
        answer = answer_with_query_only
    return {"answer": answer, "context_used": context_chunks}
