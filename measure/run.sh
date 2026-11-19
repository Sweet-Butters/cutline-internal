#!/bin/bash
# usage: run.sh <variant> <prompt>
M=D:/orca/projects/cutline-measure; v=$1; cd $M/$v || exit 1
unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN
start=$(date +%s)
claude -p "$2" --output-format stream-json --verbose --permission-mode acceptEdits \
  --tools 'Read,Glob,Grep,Edit,Write,Bash' \
  --allowedTools 'Read,Glob,Grep,Edit,Write,Bash(node tools/vidcli.js *)' \
  --strict-mcp-config --setting-sources '' > $M/$v.stream.jsonl 2> $M/$v.err
echo "exit=$? seconds=$(( $(date +%s) - start ))" > $M/$v.time
