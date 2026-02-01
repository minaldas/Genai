import os
from dotenv import load_dotenv
import logging
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Silence logs
logging.getLogger("httpx").setLevel(logging.WARNING)
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    print("❌ ERROR: OPENAI_API_KEY not found in .env file!")

class HRBotBackend:
    def __init__(self, data_dir="./Data", db_dir="./chroma_db"):
        self.data_dir = data_dir
        self.db_dir = db_dir
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.vector_db = None
        self.rag_chain = None

    def prepare_database(self):
        """Loads docs, splits them, and creates/loads the vector store."""
        if os.path.exists(self.db_dir):
            self.vector_db = Chroma(persist_directory=self.db_dir, embedding_function=self.embeddings)
        else:
            loaders = {".pdf": PyPDFLoader, ".docx": Docx2txtLoader}
            all_docs = []
            for ext, loader_cls in loaders.items():
                loader = DirectoryLoader(path=self.data_dir, glob=f"*{ext}", loader_cls=loader_cls)
                all_docs.extend(loader.load())
            
            splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
            split_docs = splitter.split_documents(all_docs)
            self.vector_db = Chroma.from_documents(
                documents=split_docs, embedding=self.embeddings, persist_directory=self.db_dir
            )
        
        # Setup Chain
        retriever = self.vector_db.as_retriever(search_kwargs={"k": 5})
        template = """You are an HR assistant. Use only the context to answer. 
        Context: {context} \nQuestion: {question}"""
        prompt = ChatPromptTemplate.from_template(template)
        
        self.rag_chain = (
            {"context": retriever | (lambda docs: "\n\n".join(d.page_content for d in docs)), 
             "question": RunnablePassthrough()}
            | prompt | self.llm | StrOutputParser()
        )

    def ask(self, query):
        return self.rag_chain.invoke(query)