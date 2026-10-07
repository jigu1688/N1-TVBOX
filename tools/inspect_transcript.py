import json
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

transcript_path = r'C:\Users\jigu\.gemini\antigravity-ide\brain\3a664381-8939-4916-9404-683857cb0b2a\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        idx = data.get('step_index', 0)
        if 2970 <= idx <= 3080:
            stype = data.get('type')
            calls = data.get('tool_calls')
            content = data.get('content', '')
            if stype == 'USER_INPUT':
                print(f'=== STEP {idx} USER_INPUT ===\n{content[:200]}')
            elif calls:
                print(f'=== STEP {idx} TOOL: {calls[0].get("name")}')
                print('   args:', str(calls[0].get('args'))[:150])
            elif stype == 'RUN_COMMAND':
                print(f'=== STEP {idx} CMD_RES: {content[:150]}')
