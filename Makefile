register:
	curl -X POST http://localhost:9070/deployments \
	     -H "Content-Type: application/json" \
	     -d '{"uri": "http://hl_agent-ai-agent-1:9080"}'

chat:
	python3 chat_cli.py