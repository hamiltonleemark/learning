""" Test FAISS vector store functionality.

Experiement with FAISS and persistent storage of vector indices.
"""
import os
import pytest
from functools import wraps
from langchain_community.vectorstores import FAISS
##
# FakeEmbeddings is useful for testing but does not handle semenatic
# relevance.
from langchain_community.embeddings import FakeEmbeddings
##
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv


load_dotenv()

@pytest.fixture
def faiss_index(request):
    # request.node.name is the test function name
    path = os.path.join("faiss_index", request.node.name)
    print(path)
    return path

def test_faiss_vectorstore(faiss_index):
    """Test FAISS vector store creation and similarity search. """

    embedding = OpenAIEmbeddings()

    if os.path.exists(faiss_index):
        vectorstore = FAISS.load_local(faiss_index, embedding,
                                       allow_dangerous_deserialization=True)
    else:
        docs = [
            Document(page_content="Employees accrue 1 day of PTO monthly."),
            Document(page_content="Health insurance starts after 90 days.")
        ]
        vectorstore = FAISS.from_documents(docs, embedding)
        vectorstore.save_local(faiss_index)

    results = vectorstore.similarity_search("How much vacation do I get after 6 months?")
    print(results[0].page_content)


def test_retrieves_correct_document(faiss_index):
    """Test FAISS retrieves the most relevant document."""

    embedding = OpenAIEmbeddings()

    print("MARK: faiss_index =", faiss_index)
    if os.path.exists(faiss_index):
        vectorstore = FAISS.load_local(faiss_index, embedding,
                                       allow_dangerous_deserialization=True)
    else:
        docs = [
            Document(page_content="Employees accrue PTO monthly."),
            Document(page_content="Health insurance starts after 90 days."),
            Document(page_content="Payroll is processed bi-weekly.")
        ]
        vectorstore = FAISS.from_documents(docs, embedding)
        vectorstore.save_local(faiss_index)

    results = vectorstore.similarity_search(
        "How does vacation time work?",
        k=1
    )

    assert len(results) == 1
    assert "PTO" in results[0].page_content
    print(results[0].page_content)


def test_metadata_filtering(faiss_index):
    """Test FAISS vector store with metadata filtering."""

    if os.path.exists(faiss_index):
        vectorstore = FAISS.load_local(faiss_index, embedding,
                                       allow_dangerous_deserialization=True)
    else:
        docs = [
            Document(
                page_content="Employees accrue PTO monthly.",
                metadata={"department": "HR"}
            ),
            Document(
                page_content="Kubernetes clusters are auto-scaled.",
                metadata={"department": "Engineering"}
            )
        ]

        vectorstore = FAISS.from_documents(docs, embedding)
        vectorstore.save_local(faiss_index)

    results = vectorstore.similarity_search(
        "vacation policy",
        k=5,
        filter={"department": "HR"}
    )

    assert len(results) == 1
    assert results[0].metadata["department"] == "HR"
