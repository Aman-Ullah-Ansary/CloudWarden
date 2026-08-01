from ai_agent import AIAgent


class RecommendationEngine:

    def __init__(self):
        self.ai = AIAgent()

    def generate(self, namespace, cost):

        report = f"""
Cluster Cost Analysis

Namespace: {namespace}

Current Cost: ${cost:.5f}

Generate:

1. Executive Summary

2. Why this namespace is expensive

3. CPU Analysis

4. Memory Analysis

5. Storage Analysis

6. Network Analysis

7. Optimization Recommendations

8. Estimated Savings

9. Overall Health Score
"""

        return self.ai.analyze(report)