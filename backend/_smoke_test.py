"""Quick API smoke test."""
import urllib.request
import json

# Health check
resp = urllib.request.urlopen("http://localhost:8000/health")
health = json.loads(resp.read())
print(f"Health: {health}")

# Start interview
payload = {
    "sessionId": "verify-001",
    "candidate": {
        "member": {
            "id": "CAND-001",
            "name": "Sarah Johnson",
            "jobRole": "Senior Data Engineer",
            "yearsExperience": 9,
            "education": "MS Computer Science",
            "status": "COMPLETED",
        },
        "missions": [
            {"day": 7, "title": "Embeddings Explained", "passed": True, "attempts": 1},
            {"day": 29, "title": "Monitoring, Logging & Observability", "skipped": True},
        ],
        "signals": {"commitDays": 28, "missionsCompleted": 30, "missionsFirstTry": 20},
    },
}
data = json.dumps(payload).encode()
req = urllib.request.Request(
    "http://localhost:8000/api/interview",
    data=data,
    headers={"Content-Type": "application/json"},
)
resp = urllib.request.urlopen(req)
result = json.loads(resp.read())
print(f"Start: done={result['done']}, reply_len={len(result['reply'])}")
print(f"Reply: {result['reply'][:150]}...")

# Continue interview
payload2 = {
    "sessionId": "verify-001",
    "message": "I would use Prometheus for metrics collection, Grafana for dashboards, and implement structured logging with correlation IDs across microservices.",
}
data2 = json.dumps(payload2).encode()
req2 = urllib.request.Request(
    "http://localhost:8000/api/interview",
    data=data2,
    headers={"Content-Type": "application/json"},
)
resp2 = urllib.request.urlopen(req2)
result2 = json.loads(resp2.read())
print(f"Continue: done={result2['done']}, reply_len={len(result2['reply'])}")

print("\n=== API SMOKE TEST PASSED ===")
