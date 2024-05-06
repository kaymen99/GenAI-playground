from langgraph.graph import END, StateGraph
from .state import GraphState
from .nodes import Nodes

class Workflow():
    def __init__(self, docs_retriever):
      # initiate graph state & nodes
      workflow = StateGraph(GraphState)
      nodes = Nodes(docs_retriever)

      # Define nodes
      workflow.add_node("retrieve_documents", nodes.retrieve_documents)
      workflow.add_node("grade_retrieved_documents", nodes.grade_retrieved_documents)
      workflow.add_node("generate", nodes.generate_with_rag)
      workflow.add_node("websearch", nodes.perform_web_search)

      # Build graph
      workflow.set_conditional_entry_point(
          nodes.route_question,
          {
              "websearch": "websearch",
              "vectorstore": "retrieve_documents"
          }
      )
      workflow.add_edge("retrieve_documents", "grade_retrieved_documents")
      workflow.add_conditional_edges(
          "grade_retrieved_documents",
          nodes.decide_to_use_web_search,
          {
              "websearch": "websearch",
              "generate": "generate"
          }
      )
      workflow.add_edge("websearch", "generate")
      workflow.add_conditional_edges(
          "generate",
          nodes.grade_generated_answer_vs_question,
          {
              "useful": END,
              "not useful": "websearch"
          }
      )

      # Compile
      self.app = workflow.compile()