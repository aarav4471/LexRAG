class Evaluator:

    @staticmethod
    def normalize(text):
        return text.lower().strip()

    @staticmethod
    def precision_at_k(relevant, retrieved, k):

        relevant = [Evaluator.normalize(r) for r in relevant]
        retrieved = [Evaluator.normalize(r) for r in retrieved]

        retrieved_k = retrieved[:k]

        return len(set(relevant) & set(retrieved_k)) / k

    @staticmethod
    def recall_at_k(relevant, retrieved, k):

        relevant = [Evaluator.normalize(r) for r in relevant]
        retrieved = [Evaluator.normalize(r) for r in retrieved]

        retrieved_k = retrieved[:k]

        return len(set(relevant) & set(retrieved_k)) / len(relevant)

    @staticmethod
    def mrr(relevant, retrieved):

        relevant = [Evaluator.normalize(r) for r in relevant]
        retrieved = [Evaluator.normalize(r) for r in retrieved]

        for idx, doc in enumerate(retrieved):
            if doc in relevant:
                return 1 / (idx + 1)

        return 0

    @staticmethod
    def f1(p, r):
        return 2 * (p * r) / (p + r) if (p + r) else 0