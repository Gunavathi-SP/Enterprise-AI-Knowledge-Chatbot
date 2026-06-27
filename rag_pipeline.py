# app/rag_pipeline.py

def build_rag(vectorstore):
    # Configure the retriever to fetch the top 3 most relevant chunks
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    class SimpleQA:
        def __init__(self, retriever):
            self.retriever = retriever

        def run(self, query):
            # FIXED: .invoke() is the modern standard for LangChain retrievers
            docs = self.retriever.invoke(query) 

            if not docs:
                return "No answer found"

            # Combine retrieved chunks into a single context string
            context = " ".join([doc.page_content for doc in docs])
            
            # Split context into individual sentences for scoring
            sentences = context.replace("\n", " ").split(".")
            query_words = query.lower().split()

            best_sentence = ""
            max_score = 0

            # Simple Keyword Matching Logic: 
            # Finds the sentence with the highest overlap of words from the query
            for sentence in sentences:
                sentence_lower = sentence.lower()
                score = sum(word in sentence_lower for word in query_words)

                if score > max_score:
                    max_score = score
                    best_sentence = sentence.strip()

            return best_sentence if best_sentence else "No answer found"

    return SimpleQA(retriever)