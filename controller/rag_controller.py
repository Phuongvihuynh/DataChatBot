from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class RAGController:
    def __init__(self):
        # Load the Jina Rerank model
        self.rerank_model = AutoModelForSequenceClassification.from_pretrained(
            'jinaai/jina-reranker-v2-base-multilingual',
            torch_dtype="auto",
            trust_remote_code=True,
        )
        self.tokenizer = AutoTokenizer.from_pretrained('jinaai/jina-reranker-v2-base-multilingual')
        self.rerank_model.eval()

    def rerank_articles(self, question, articles, top_k=50):
        """
        Rerank articles based on their relevance to the question using Jina Reranker.
        Return the top K most relevant articles.
        """
        # Create sentence pairs between the query and each article (title + content)
        sentence_pairs = [[question, f"{article.get('title', 'N/A')}. {article.get('content', 'N/A')}"] for article in
                          articles]

        # Tokenize the sentence pairs for the rerank model
        inputs = self.tokenizer(sentence_pairs, padding=True, truncation=True, return_tensors="pt", max_length=512)

        # Predict the scores using the rerank model
        with torch.no_grad():
            outputs = self.rerank_model(**inputs)
            logits = outputs.logits.squeeze()  # Ensure logits are correctly shaped

        # If logits is 1D (single class), treat it directly
        if len(logits.shape) == 1:
            scores = logits
        else:
            # Otherwise, use the second column (relevance score) as originally planned
            scores = logits[:, 1]  # This assumes a binary classification problem

        # Combine articles with their scores
        ranked_articles = [(article, score.item()) for article, score in zip(articles, scores)]

        # Sort articles by their scores (highest score first)
        ranked_articles.sort(key=lambda x: x[1], reverse=True)

        # Return the top K most relevant articles in the same format as the original code
        return [article for article, _ in ranked_articles[:top_k]]
