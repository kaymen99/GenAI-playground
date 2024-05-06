from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from .prompt import *

class RAGAgents():
    def __init__(self, retriever):
        # tavily websearch tool
        self.web_search = TavilySearchResults()

        # Document retriever
        self.retriever = retriever

        # load llama3 model with Ollama
        llm = ChatOllama(model="llama3", temperature=0)

        # RAG chain
        rag_prompt = PromptTemplate(
            template=rag_prompt_template,
            input_variables=["question", "context"],
        )
        self.rag_chain = rag_prompt | llm | StrOutputParser()

        # use json output format
        llm = ChatOllama(model="llama3", format="json", temperature=0)

        # Router chain
        router_prompt = PromptTemplate(
            template=router_prompt_template,
            input_variables=["question", "topics"],
        )
        self.router_chain = router_prompt | llm | JsonOutputParser()

        # Retrieval grader chain
        retrieval_prompt = PromptTemplate(
            template=retrieval_prompt_template,
            input_variables=["question", "document"],
        )
        self.retrieval_grader = retrieval_prompt | llm | JsonOutputParser()

        # Answer grader chain
        grader_prompt = PromptTemplate(
            template=grader_prompt_template,
            input_variables=["generation", "question"],
        )
        self.answer_grader_chain = grader_prompt | llm | JsonOutputParser()