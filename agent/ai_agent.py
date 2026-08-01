import os
from groq import Groq
from dotenv import load_dotenv

from prompts import SYSTEM_PROMPT, build_prompt

load_dotenv()


class AIAgent:
    """
    CloudWarden AI Agent powered by Groq.
    """

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile"
        )

    def analyze(self, cluster_data: str) -> str:
        """
        Analyze Kubernetes/OpenCost data using Groq.
        """

        prompt = build_prompt(cluster_data)

        try:

            response = self.client.chat.completions.create(

                model=self.model,

                temperature=0.2,

                max_tokens=1200,

                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.choices[0].message.content

        except Exception as error:

            return (
                "\n"
                "==============================\n"
                "CloudWarden AI Error\n"
                "==============================\n"
                f"{error}"
            )

    def chat(self, question: str, cluster_data: str) -> str:
        """
        Chat with CloudWarden AI about the cluster.
        """

        try:

            prompt = f"""
You are CloudWarden AI.

Current Cluster Data:

{cluster_data}

User Question:

{question}

Answer clearly in markdown.
If the question is unrelated to Kubernetes or cloud costs
(for example: Hi, Hello, Who are you),
reply naturally and continue the conversation.
"""

            response = self.client.chat.completions.create(

                model=self.model,

                temperature=0.3,

                max_tokens=1200,

                messages=[
                    {
                        "role": "system",
                        "content": "You are CloudWarden AI Assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.choices[0].message.content

        except Exception as error:

            return str(error)

    def analyze_namespace(
        self,
        namespace: str,
        cost: float
    ) -> str:

        report = f"""

Namespace

{namespace}

Current Cost

${cost:.5f}

"""

        return self.analyze(report)

    def analyze_cluster(
        self,
        namespace_cost: dict
    ) -> str:

        report = []

        total = 0

        for namespace, cost in namespace_cost.items():

            total += cost

            report.append(
                f"{namespace:<20} ${cost:.5f}"
            )

        text = "\n".join(report)

        cluster_report = f"""

Total Cluster Cost

${total:.5f}

Namespaces

{text}

"""

        return self.analyze(cluster_report)