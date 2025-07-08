from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.tools.retriever import create_retriever_tool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

project_root = Path(__file__).parent.parent.parent.parent
reports_dir = project_root / "sample_data" / "reports"

paths = [
    reports_dir / "report_2025_march.pdf",
    reports_dir / "report_2025_april.pdf",
    reports_dir / "report_2025_may.pdf",
    reports_dir / "report_2025_june.pdf",
]

documents = []

for path in paths:
    loader = PyPDFLoader(str(path))
    docs = loader.load()

    month_name = path.stem.split("_")[-1].title()
    for doc in docs:
        doc.metadata["report_month"] = month_name
        doc.metadata["source"] = path.name
        documents.append(doc)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

splits = text_splitter.split_documents(documents)

filtered_splits = []
for split in splits:
    content = split.page_content.strip()
    if len(content) > 100 and not (content.startswith("Quantix Inc.") and len(content) < 150):
        month = split.metadata.get("report_month", "")
        if month and month.lower() not in content.lower():
            split.page_content = f"[{month} 2025 Report] {content}"
        filtered_splits.append(split)

vectorstore = InMemoryVectorStore.from_documents(
    documents=filtered_splits, embedding=OpenAIEmbeddings()
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 6,
    },
)

retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_report_data",
    "Search and return specific information from Quantix Inc. performance reports. "
    "Can retrieve metrics, financial data, customer information, and other details "
    "from March, April, May, and June 2025 reports. Always returns the most relevant "
    "sections that match the query.",
)
