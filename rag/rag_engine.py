import json
import os
import re


# ============================================================
# KNOWLEDGE BASE
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_FILE = os.path.join(BASE_DIR, "knowledge_base.json")


def load_knowledge_base():

    with open(
        KNOWLEDGE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# TEXT PROCESSING
# ============================================================

def tokenize(text):

    return set(
        re.findall(
            r"\b[a-zA-Z]{3,}\b",
            text.lower()
        )
    )


# ============================================================
# SIMPLE RETRIEVAL
# ============================================================

def calculate_relevance(query, document):

    query_words = tokenize(query)

    document_text = (
        document.get("topic", "")
        + " "
        + document.get("category", "")
        + " "
        + document.get("content", "")
    )

    document_words = tokenize(document_text)

    if not query_words or not document_words:
        return 0

    common_words = query_words.intersection(
        document_words
    )

    return len(common_words)


def retrieve_context(query, top_k=3):

    knowledge_base = load_knowledge_base()

    scored_documents = []

    for document in knowledge_base:

        score = calculate_relevance(
            query,
            document
        )

        scored_documents.append(
            (score, document)
        )

    scored_documents.sort(
        key=lambda item: item[0],
        reverse=True
    )

    results = []

    for score, document in scored_documents[:top_k]:

        if score > 0:

            results.append({
                "score": score,
                "id": document["id"],
                "topic": document["topic"],
                "category": document["category"],
                "content": document["content"]
            })

    return results


# ============================================================
# RAG CONTEXT FORMATTER
# ============================================================

def build_rag_context(query, top_k=3):

    results = retrieve_context(
        query,
        top_k
    )

    if not results:
        return "No relevant information was found in the knowledge base."

    context_parts = []

    for result in results:

        context_parts.append(
            f"""
Topic: {result['topic']}
Category: {result['category']}
Information: {result['content']}
"""
        )

    return "\n".join(context_parts)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_query = (
        "There is garbage piling up near our "
        "residential area."
    )

    print("\nRAG TEST")
    print("=" * 50)

    results = retrieve_context(
        test_query
    )

    for result in results:

        print(
            f"\nTopic: {result['topic']}"
        )

        print(
            f"Category: {result['category']}"
        )

        print(
            f"Score: {result['score']}"
        )

        print(
            f"Information: {result['content']}"
        )

    print("\n")
    print("FORMATTED RAG CONTEXT")
    print("=" * 50)

    print(
        build_rag_context(
            test_query
        )
    )