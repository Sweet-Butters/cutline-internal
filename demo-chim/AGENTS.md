# Video project instructions

This folder is a video project. Read style.md before editing. No paid APIs or uploads.

- sources/: original footage, never overwrite originals.
- timeline.json: {"version":1,"clips":[{"id":"intro","source":"sources/original.mp4","in":0,"out":20,"reason":"짧은 편집 이유"}]}
- in/out: seconds on the source; out is exclusive. Require 0 <= in < out <= source duration.
- id: unique stable letters/digits/underscore/hyphen, at most 80 chars. Preserve ids on trims/moves; use new ids for new selections so the panel highlights changes correctly.
- source: forward-slash relative path beneath sources/, no .. or absolute paths.
- transcripts/<source filename including extension>.json: [{"start":0,"end":20,"text":"..."}]. Nested directories mirror sources/. These transcripts are real Korean CPU ASR; recognition errors are possible.
- An empty clips array is valid. No transitions, overlays, speed changes, volume mixing, or separate audio tracks in schema v1.
- timeline.json saves reload the VS Code panel automatically. Write complete valid JSON atomically when possible. Do not modify the extension.

From this project folder, CLI: node tools/vidcli.js COMMAND (uses the existing read-only Cutline build).
From another working directory: node "D:/orca/projects/video-ide/tools/vidcli.js" --project "PROJECT_PATH" COMMAND.

Commands:
```
summary
search 핵심
add hook sources/original.mp4 0 10 "핵심 질문"
remove intro
trim idea 65 100
move result 0
validate
proxies
commit "20–25분 하이라이트"
export
```
move uses a zero-based destination index. Edits validate source existence and duration before writing.
Read transcripts and style, edit timeline.json or use the CLI, run validate, then commit a version if requested. Git is local. Do not push. You may keep an independent git repository when copying this folder elsewhere.
For this project, make a ~20–25 minute cut following style.md from the full original; avoid repeated content. Reason explains editorial intent, not implementation details.

## chim_003 demo task

Goal: make a ~20–25 minute cut following style.md. Read transcripts/original.mp4.json. Edit only timeline.json, using Korean reasons. Keep sources and reference unchanged. Do not access or modify video-ide; the local CLI wrapper only loads its existing runtime read-only. No uploads, remote, or push.

Score after editing: `node tools/compare.js`. This writes compare.json with source-time union precision/recall/F1 and playback durations. Reference alignment covers only 93.55% of the human video; the score does not measure pacing/order, subtitles, or creative quality. Do not read or copy reference/human_edit.timeline.json while selecting clips: use it only through the scoring tool after the edit. Validate: `node tools/vidcli.js validate`. Reference self-test: `node tools/compare.js --self-test`.
