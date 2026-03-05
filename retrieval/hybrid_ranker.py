from datetime import datetime


class HybridRanker:

    @staticmethod
    def score(vector_score, graph_score, year):
        recency = 1 / (datetime.now().year - int(year) + 1)
        return 0.6 * vector_score + 0.3 * graph_score + 0.1 * recency