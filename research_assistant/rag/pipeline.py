# rag/pipeline.py
from .embeddings import generate_embedding
from .vector_store import search
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 1️⃣ Retrieve context
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
    # os.remove("/uploads/")  # Clean up uploaded file after processing
    return context_chunks


def fix_code_blocks(markdown_text):
    if not markdown_text:
        return ""

    lines = markdown_text.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect fenced code block
        if stripped.startswith("```"):
            # Add blank line before if missing
            if i > 0 and lines[i-1].strip() != "":
                fixed_lines.append("")

            # Ensure at least 2 spaces indentation
            leading_spaces = len(line) - len(line.lstrip())
            if leading_spaces > 1 :
                line = "" + stripped

            # Optional: add default language if none
            if stripped == "```":
                line = ""

        fixed_lines.append(line)

    return "\n".join(fixed_lines)

# 2️⃣ Generate answer
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

        # Check if response seems complete
        if partial_answer.endswith((".", "?", "!", "\n\n")) or len(partial_answer) < 1024:
            break
        else:
            # Continue from where it left off
            temp_prompt = f"Continue the previous answer from where it stopped:\n{partial_answer}"
    
    # print("Answer with query only:", full_answer)
    fixed_answer = fix_code_blocks(full_answer)
    return fixed_answer

def generate_answer_withQuery_Only(query,query_chunk):
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

        # Check if response seems complete
        if partial_answer.endswith((".", "?", "!", "\n\n")) or len(partial_answer) < 1024:
            break
        else:
            # Continue from where it left off
            temp_prompt = f"Continue the previous answer from where it stopped:\n{partial_answer}"

    # print("Answer with query only:", full_answer)
    fixed_answer = fix_code_blocks(full_answer)
    return fixed_answer

# query chunks
queries=[]
def questions(query):
    global queries
    if len(queries)>2:
        queries.pop(0)
    queries.append(query)
    return queries

# 3️⃣ Full RAG pipeline
def run_rag_pipeline(query):
    context_chunks = retrieve_context(query)
    # if not context_chunks:
    #     return {"answer": "No relevant information found."}
    
    answer = generate_answer(query, context_chunks)

    query_chunk=questions(query)
    answer_with_query_only = generate_answer_withQuery_Only(query,query_chunk)  

    if answer_with_query_only and not context_chunks:
        answer = answer_with_query_only

    return {"answer": answer, "context_used": context_chunks}