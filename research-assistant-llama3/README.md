# Research Assistant Bot using Local LangGraph RAG & Llama3

This project focuses on building a robust Research Assistant using a combination of Local Retrieval Augmented Generation (RAG) techniques, LangGraph agents, and the Llama-3 model.

## Summary

1. [What is RAG?](#what-is-rag)
   - [Problematic](#problematic)
   - [Solution](#solution)
2. [Limitations of standard RAG](#limitations-of-standard-rag)
3. [How can standard RAG be improved?](#how-can-standard-rag-be-improved)
4. [LangGraph and Agents](#langgraph-and-agents)
   - [What is an Agent?](#what-is-an-agent)
   - [LangGraph](#langgraph)
     - [Key Concepts](#key-concepts)
     - [Steps involved in creating a graph using LangGraph](#steps-involved-in-creating-a-graph-using-langgraph)
5. [Graph workflow for our research assistant](#graph-workflow-for-our-research-assistant)
6. [Tools and APIs Used](#tools-and-apis-used)
7. [How to run](#how-to-run)
8. [Additional resources](#additional-resources)

## What is RAG?

Retrieval Augmented Generation (RAG), as its name suggests, is a technique used to augment/improve the output of the LLMs models to users' questions. It is used in several tasks, but the main one is Question-Answering (QA).

### **Problematic**:

* With standalone LLM models, when a user asks a question, the model will try to answer using its previous knowledge from the data it was trained on. However, in most cases, this data is not sufficient or outdated (we all know, for example, that gpt-3.5-turbo is only trained up to 2021), and so the returned answer may be wrong or inaccurate.
  
* A simple intuitive fix would be to put all necessary information directly into the prompt as context for the model before answering the question. Still, this approach can't work because most LLMs have a limited context size, and the more tokens are added to the prompt, the more the model tends to forget some of the information. Additionally, such an approach would be very expensive as most deployed LLMs charge according to the input token count.

### **Solution**:

It's here where the RAG approach comes into play:

* Instead of sending the whole data as context for the model, we first divide it into smaller chunks, which we convert into vectors (embeddings).
* We store all the text chunks in a Vector DB. These kinds of databases allow us to retrieve elements based on a similarity score between them.
* Thus, using RAG when a user asks a question, we first perform a similarity search on our vector DB and extract only the most relevant chunks of information, which are given as context to the LLM model, which will need to formulate a correct answer based on them.

## Limitations of standard RAG

Although the RAG technique is very powerful, it has some limitations:

* It's difficult to choose the correct chunk size when splitting the data into smaller parts because if it's short, the model will not have enough context to answer, and if it's too long, we'll end up with the same limitation faced by standalone LLM, i.e., the model context size limit and cost.
* The same problem applies to the number of instances we must fetch from our vector store after the similarity search is performed. For example, choosing only the first three instances might lead to an incorrect answer as the correct context was in the fifth instance.
* Retrieved documents could be irrelevant to the user question, or the model could start hallucinating. In both cases, the model will output a wrong answer.
  
## How can standard RAG be improved?

Various solutions were proposed to enhance the standard RAG process; we can mention the following:

* **Adaptive RAG** [paper](https://arxiv.org/abs/2403.14403): It consists of adding a router agent responsible for routing the questions to different retrieval approaches. For example, if the asked question is related to our local vector store, then the local RAG will give the answer; if not, then a web search agent will handle it.

* **Corrective RAG** [paper](https://arxiv.org/pdf/2401.15884): This one introduces a fallback mechanism to answer the question when the retrieved documents from the local vector store are irrelevant to the question asked.

* **Self-RAG** [paper](https://arxiv.org/abs/2310.11511): It develops answer and hallucination grader agents, which evaluate the output response and regenerate the answers when the agent hallucinates or doesn’t address the question correctly.

## LangGraph and Agents

### What is an Agent?

An Agent is a sophisticated system that employs an LLM to select actions dynamically, enabling it to reason and adapt to various contexts, which differs from traditional agents with their hardcoded sequences of actions.

### LangGraph

[LangGraph](https://python.langchain.com/v0.1/docs/langgraph/) is a library that extends [LangChain](https://python.langchain.com/v0.1/docs/get_started/introduction), allowing for cyclic computational capabilities in LLM applications. It enables the creation of intricate, agent-like behaviors by incorporating cycles in the computation, facilitating dynamic decision-making and action-taking by the LLM.

#### Key Concepts

- **Stateful Graph**: LangGraph operates on the concept of a stateful graph, where each node represents a step in the computation process, and the graph maintains a global state that evolves as the computation progresses.
- **Nodes and Edges**: Nodes represent specific functions or computation steps, while edges define the flow of computation between nodes. LangGraph supports conditional edges, enabling dynamic routing based on the current state of the graph.

#### Steps involved in creating a graph using LangGraph:

1. **Define the Graph State**: Define the global state of the graph, capturing relevant information for computation.
2. **Define Graph Structure**: Design the graph structure by defining nodes and connecting them with edges.
3. **Define Nodes**: Specify the functions associated with each workflow state, encapsulating the logic for different actions.
4. **Add Nodes to the Graph**: Populate the graph with nodes and define the flow of computation using edges and conditional edges.
5. **Set Entry and End Points**: Establish entry and exit points for the graph, defining the start and end of the process.

## Graph workflow for our research assistant

Let's explore how our local RAG system will operate. After the user asks his question, we'll get the following steps:

1. **Question Routing**: The Router determines whether to retrieve context from a local vector store or perform a web search based on the nature of the question.
2. **Context Retrieval**:
   - If directed to retrieve from the vector store, relevant documents are fetched.
   - If a web search is required, the Tavily Search API is utilized to obtain relevant information.
3. **Document Grading**: Grading of retrieved documents from the local vector store as relevant or irrelevant is performed.
4. **Hallucination Detection**: If the context retrieved is graded as relevant, the Hallucination Grader checks for hallucination in the response.
5. **Response Generation**:
   - If the context is deemed relevant and free of hallucination, the response is presented to the user.
   - In the case of irrelevant context, a web search is performed to gather suitable content.
6. **Post-Retrieval Processing**: The Document Grader evaluates the relevance of the retrieved content from the web search. If deemed relevant, the response is synthesized using the Language Model and presented to the user.

## Tools and APIs Used

- **Python**
- **Flask**
- **Langchain & LangGraph**
- **Ollama-Llama3 model**
- **Pinecone vector DB**
- **Tavily Search API**
 
## How to run

* To be able to run this project, you must install Ollama on your machine [link](https://ollama.com/download) and then install the Llama3 model locally by running:

```bash
ollama run llama3
```

* We'll be using the Pinecone vector database for our local RAG model, so you'll need to create an account and get an API key (choose the free version) from [here](https://www.pinecone.io/)

* Lastly, you'll need a [Tavily search]() API key which is used by the agents to search the internet

* Clone the repository:

```bash
git clone https://github.com/kaymen99/GenAI-playground.git
cd GenAI-playground/research-assistant-llama3
```

* Install all the dependencies (you should create a virtual environment first):

```bash
pip install -r requirements.txt
```

* Create a `.env` file in the root directory and add your API keys as follows:

```ini
PINECONE_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TAVILY_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

* To construct the local data store for the research assistant, you must first download research papers. Don't worry, I already set up the `scripts/downloader.py` script for that you just need to add your research topic and the number of papers to download, then run:

```bash
python scripts/downloader.py
```

* You got your research data, now you must convert it into vectors and store them into the Pinecone vector DB, you just have to run:

```bash
python scripts/store_index.py
```

* You did it!!! start the app by running:

```bash
python app.py
```

* You can start chatting with your own assistant!!!

## Additional resources

- LangGraph RAG applications [examples](https://github.com/langchain-ai/langgraph/tree/main/examples/rag)
- Building Production-Ready RAG Applications: Jerry Liu [YouTube](https://www.youtube.com/watch?v=TRjq7t2Ms5I&t=226s)
