from langchain.schema import Document
from .agents import RAGAgents

### Nodes
class Nodes():
    def __init__(self, llm, retriever):
        self.agents = RAGAgents(llm, retriever)

    def route_question(self, state):
        """
        Route question to web search or RAG.

        Args:
            state (dict): The current graph state

        Returns:
            str: Next node to call
        """

        print("---ROUTE QUESTION---")
        # define local data topics
        topics = "machine learning, deep learning, artificial intelligence"
        question = state["question"]
        source = self.agents.router_chain.invoke({"question": question, "topics": topics})
        print(f"---ROUTE QUESTION TO: {source['datasource']}---")
        return source['datasource']

    def retrieve_documents(self, state):
        """
        Retrieve documents from vectorstore

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, documents, that contains retrieved documents
        """
        print("---RETRIEVE DOCUMENTS---")
        question = state["question"]

        # Retrieval
        documents = self.agents.retriever.invoke(question)
        return {"documents": documents, "question": question}

    def generate_with_rag(self, state):
        """
        Generate answer using RAG on retrieved documents

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation, that contains LLM generation
        """
        print("---GENERATE WITH RAG---")
        question = state["question"]
        documents = state["documents"]

        generation = self.agents.rag_chain.invoke({"question": question, "context": documents})
        return {"documents": documents, "question": question, "generation": generation}

    def grade_retrieved_documents(self, state):
        """
        Determines whether the retrieved documents are relevant to the question
        If any document is not relevant, we will set a flag to run web search

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Filtered out irrelevant documents and updated web_search state
        """

        print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
        question = state["question"]
        documents = state["documents"]

        # Score each doc
        filtered_docs = []
        web_search = "No"
        for d in documents:
            score = self.agents.retrieval_grader.invoke({"question": question, "document": d.page_content})
            grade = score['score']
            # Document relevant
            if grade.lower() == "yes":
                filtered_docs.append(d)
            # Document not relevant
            else:
                # We do not include the document in filtered_docs
                # We set a flag to indicate that we want to run web search
                web_search = "Yes"
                continue
        return {"documents": filtered_docs, "question": question, "web_search": web_search}

    def perform_web_search(self, state):
        """
        Web search based based on the question

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Appended web results to documents
        """

        print("---WEB SEARCH---")
        question = state["question"]
        documents = state["documents"]

        # Web search
        docs = self.agents.web_search.invoke({"query": question})
        web_results = "\n".join([d["content"] for d in docs])
        web_results = Document(page_content=web_results)
        if documents is not None:
            documents.append(web_results)
        else:
            documents = [web_results]
        return {"documents": documents, "question": question}

    def decide_to_use_web_search(self, state):
        """
        Determines whether to generate an answer, or add web search

        Args:
            state (dict): The current graph state

        Returns:
            str: Binary decision for next node to call
        """

        print("---ASSESS GRADED DOCUMENTS---")
        web_search = state["web_search"]

        if web_search == "Yes":
            # All documents have been filtered check_relevance
            # We will re-generate a new query
            print("---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, INCLUDE WEB SEARCH---")
            return "websearch"
        else:
            # We have relevant documents, so generate answer
            print("---DECISION: GENERATE---")
            return "generate"

    def grade_generated_answer_vs_question(self, state):
        """
        Determines whether the generated answer does address to given question.

        Args:
            state (dict): The current graph state

        Returns:
            str: Decision for next node to call
        """

        print("---GRADE GENERATED ANSWER vs QUESTION---")
        question = state["question"]
        generation = state["generation"]

        # Check question-answering
        score = self.agents.answer_grader_chain.invoke({"question": question,"generation": generation})
        grade = score['score']
        if grade == "yes":
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"