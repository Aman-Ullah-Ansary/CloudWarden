from collector import CostCollector

collector = CostCollector()

data = collector.collect()

print(data)

collector.close()