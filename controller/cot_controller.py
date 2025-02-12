# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# from controller.question_controller import QuestionController
# from hashlib import sha256
#
# load_dotenv()
#
# class RATController:
#     def __init__(self):
#         self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
#         self.question_controller = QuestionController()
#         self.cache = {}  # Simple in-memory cache
#
#     def _generate_cache_key(self, articles, question):
#         hash_input = question + ''.join(article['content'][:500] for article in articles)
#         return sha256(hash_input.encode('utf-8')).hexdigest()
#
#     def generate_retrieval_augmented_thoughts(self, input_vector, question, max_iterations=5):
#         """
#         Implements the Retrieval Augmented Thoughts (RAT) pipeline for generating an informed response.
#         """
#         thoughts = self._initialize_thoughts(question)
#         T_star = [thoughts[0]]  # Start with the first thought
#         i = 1
#         cite_list = []
#
#         while i < max_iterations:
#             retrieved_info = self._retrieve_from_pinecone(input_vector)
#             T_star = self._revise_thoughts(question, T_star, retrieved_info)
#             if i < len(thoughts):
#                 T_star.append(thoughts[i])
#             cite_list.extend(self._extract_citations(retrieved_info))
#             i += 1
#
#         return " ".join(T_star) + "\n\nCitations:\n" + "\n".join(
#             [f"- {c['title']} ({c['published_date']}), Source: {c['source']}, URL: {c['url']}" for c in cite_list])
#
#     def _initialize_thoughts(self, question):
#         prompt = f"""
#         You are an expert in Vietnamese economic news analysis.
#
#         Generate a structured step-by-step breakdown to answer the question:
#         "{question}"
#
#         Instructions:
#         1. Analyze the provided excerpts and identify the main points relevant to the question.
#         2. Summarize the economic context and any recurring themes or key details across the excerpts.
#         3. Provide a synthesized answer to the question based on these insights.
#         4. If there is no relevant information, respond with 'Currently we have no relevant information.' Avoid adding any information not present in the article content.
#
#         Note: The answer should be in Vietnamese.
#         """
#         response = self.client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=300
#         )
#         return response.choices[0].message.content.split("\n")
#
#     def _retrieve_from_pinecone(self, input_vector, top_k=3):
#         """
#         Retrieve relevant information from Pinecone vector database based on the input vector.
#         """
#         return self.question_controller.query_by_vector(input_vector, top_k=top_k)
#
#     def _revise_thoughts(self, question, current_thoughts, retrieved_info):
#         prompt = f"""
#         Question: {question}
#         Current Thought Process: {current_thoughts}
#         Retrieved Information from Pinecone: {retrieved_info}
#         Refine the thoughts using the retrieved information.
#         """
#         response = self.client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=300
#         )
#         return response.choices[0].message.content.split("\n")
#
#     def _extract_citations(self, retrieved_info):
#         """
#         Extract citation information from retrieved Pinecone results.
#         """
#         citations = []
#         for article in retrieved_info:
#             citations.append({
#                 'title': article['metadata'].get('title', 'N/A'),
#                 'source': article['metadata'].get('source', 'N/A'),
#                 'published_date': article['metadata'].get('published_date', 'N/A'),
#                 'url': article['metadata'].get('url', 'N/A')
#             })
#         return citations
#
#     def _clean_html(self, text):
#         """
#         Remove unwanted HTML tags and redundant text from the final output.
#         """
#         import re
#         text = re.sub(r'<[^>]+>', '', text)
#         text = re.sub(r'Các bài báo tham khảo.*$', '', text, flags=re.S)
#         return text.strip()


from openai import OpenAI
import os
from dotenv import load_dotenv
from controller.rag_controller import RAGController
from hashlib import sha256

load_dotenv()

class CoTController:
    def __init__(self):
        # Initialize OpenAI API with API key from environment
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.rag_controller = RAGController()
        self.cache = {}  # Simple in-memory cache

    def _generate_cache_key(self, articles, question):
        """
        Generate a unique cache key based on the question and article contents.
        """
        hash_input = question + ''.join(article['content'][:500] for article in articles)
        return sha256(hash_input.encode('utf-8')).hexdigest()

    def generate_chain_of_thoughts(self, articles, question):
        """
        Generate the final answer based on analyzing multiple articles using Chain of Thought.
        """
        # Rerank the articles using RAGController and get the top 5 articles
        top_articles = self.rag_controller.rerank_articles(question, articles, top_k=5)

        # Check cache for results
        cache_key = self._generate_cache_key(top_articles, question)
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Prepare the content for analysis in a single prompt
        content_for_prompt = ""
        cite_list = []

        for article in top_articles:
            title = article.get('title', 'N/A')
            published_date = article.get('published_date', 'N/A')
            source = article.get('source', 'N/A')
            content = article.get('content', 'N/A')[:500]  # Limit content to 500 characters

            # Add content to the prompt
            content_for_prompt += f"Content: {content}\n\n"

            # Collect citation information for potential later use
            cite_list.append({
                'title': title,
                'source': source,
                'published_date': published_date,
                'url': article.get('url', 'N/A')
            })

        # Final combined prompt
        final_prompt = f"""
        You are an expert in Vietnamese economic news analysis.

        Question: {question}

        Below are the relevant article excerpts:

        {content_for_prompt}

        Instructions:
        1. Analyze the provided excerpts and identify the main points relevant to the question.
        2. Summarize the economic context and any recurring themes or key details across the excerpts.
        3. Provide a synthesized answer to the question based on these insights.
        4. If there is no relevant information, respond with 'Currently we have no relevant information.' Avoid adding any information not present in the article content.

        Note: The answer should be in Vietnamese.
        """

        # Call OpenAI API to generate the final answer
        final_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": final_prompt}],
            max_tokens=700,  # Reduced max_tokens for faster response
            temperature=0.7
        )

        # Extract the final answer
        final_answer = final_response.choices[0].message.content

        # Clean up the final answer to remove unwanted HTML or redundant parts
        final_answer = self._clean_html(final_answer)

        # Cache the result
        self.cache[cache_key] = (final_answer, cite_list)
        return final_answer, cite_list

    def _clean_html(self, text):
        """
        Remove unwanted HTML tags and redundant text from the final output.
        """
        import re
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove redundant or unwanted sections
        text = re.sub(r'Các bài báo tham khảo.*$', '', text, flags=re.S)
        return text.strip()

