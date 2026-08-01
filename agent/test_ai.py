from ai_agent import AIAgent

agent = AIAgent()

sample = """
Cluster Cost : $0.79

Namespaces

payments      $0.48
kube-system   $0.23
default       $0.06
monitoring    $0.01
opencost      $0.01
"""

print("Sending request to Groq...\n")

response = agent.analyze(sample)

print(response)