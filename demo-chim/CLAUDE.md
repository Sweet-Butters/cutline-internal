# Video editing workspace

Read and follow ./AGENTS.md and ./style.md before editing. AGENTS.md documents all files, the timeline schema, and the local vidcli commands. Edit timeline.json to make cuts; preserve existing clip ids for trims/moves. Validate with `node tools/vidcli.js validate`. The live panel reacts when the file is saved. Use git commits for versions, and never push.

## chim_003 demo task

Goal: make a ~20–25 minute cut following style.md. Read transcripts/original.mp4.json. Edit only timeline.json, using Korean reasons. Keep sources and reference unchanged. Do not access or modify video-ide; the local CLI wrapper only loads its existing runtime read-only. No uploads, remote, or push.

Score after editing: `node tools/compare.js`. This writes compare.json with source-time union precision/recall/F1 and playback durations. Reference alignment covers only 93.55% of the human video; the score does not measure pacing/order, subtitles, or creative quality. Do not read or copy reference/human_edit.timeline.json while selecting clips: use it only through the scoring tool after the edit. Validate: `node tools/vidcli.js validate`. Reference self-test: `node tools/compare.js --self-test`.
