"""Capture only allowed Cutline inputs and initialize editable deck content."""
import json, shutil, hashlib, re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
V=Path('D:/orca/projects/video-ide'); D=Path('D:/orca/projects/cutline-demo-chim/project')
for p in ['assets','evidence','out','out/slides']: (ROOT/p).mkdir(parents=True,exist_ok=True)
allowed=[V/'README.md',V/'VERIFICATION.md',D/'README.md',D/'compare.json',D/'reference/alignment_summary.json',D/'reference/human_edit.timeline.json',D/'reference/starting.compare.json',D/'reference/validation.json']
manifest=[]
for p in allowed:
    dest=ROOT/'evidence'/((('video-ide-' if V in p.parents else 'demo-')+p.name))
    shutil.copy2(p,dest)
    manifest.append({'source':str(p),'snapshot':str(dest.relative_to(ROOT)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
for name in ['cutline-launch-2.png','cutline-chim.png','cutline-launch.png']:
    p=V/'app/screenshots'/name; shutil.copy2(p,ROOT/'assets'/name)
    manifest.append({'source':str(p),'snapshot':'assets/'+name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(ROOT/'evidence/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
a=json.loads((D/'reference/alignment_summary.json').read_text(encoding='utf-8-sig'))
def fact(v,display,source,field,note=''): return dict(value=v,display=display,source=str(source),field=field,note=note)
facts={
 'ORIGINAL_DURATION':fact(a['original_duration'],'2:01:33',D/'reference/alignment_summary.json','original_duration','반올림한 원본 재생 길이'),
 'HUMAN_DURATION':fact(a['edited_duration'],'23:18',D/'reference/alignment_summary.json','edited_duration','사람이 만든 편집본 길이; AI 결과 아님'),
 'ALIGNMENT_COVERAGE':fact(a['alignment_ratio'],'93.55%',D/'reference/alignment_summary.json','alignment_ratio','편집본 시간 중 원본 위치가 복원된 비율; 정확도 아님'),
 'ALIGNED_SECONDS':fact(a['aligned_seconds'],'1,307.980초',D/'reference/alignment_summary.json','aligned_seconds'),
 'UNALIGNED_SECONDS':fact(a['unaligned_seconds'],'90.210초',D/'reference/alignment_summary.json','unaligned_seconds'),
 'HUMAN_BLOCKS':fact(a['clips'],'99개',D/'reference/alignment_summary.json','clips','정렬 블록 수; 샷 수 아님'),
 'DIFF_LATENCY':fact(1175,'1,175ms',V/'VERIFICATION.md','설치된 확장 통합 테스트','저장→웹뷰 DOM 갱신 응답, 단일 측정; 평균/보장 아님'),
 'TESTS_PASSED':fact(5,'5개 통과',V/'VERIFICATION.md','npm test','보고서에 기록된 테스트 수; 여기서 재실행하지 않음'),
 'AI_vs_HUMAN_F1':fact(None,None,D/'compare.json','f1','현재 파일은 원본 전체 시작 상태. 에이전트 편집 결과가 확인되기 전에는 채우지 않음'),
 'AGENT_EDIT_TIME':fact(None,None,D/'reference/agent_edit_report.json','elapsed_seconds','아직 제공되지 않은 측정 보고서 슬롯'),
 'ASR_TIME':fact(None,None,D/'reference/asr_report.json','elapsed_seconds','빌드 시점에 보고서 없음'),
 'CREATOR_AB':fact(None,None,ROOT/'evidence/creator_ab.json','preference','미수행; 향후 근거 파일 필요'),
 'TARGET_DURATION':fact(20,'20분',ROOT/'brief.md','demo_prompt','사용자가 지정한 시연 요청 길이; 성능 측정치 아님'),
 'MVP_WEIGHT':fact(25,'25%',ROOT/'brief.md','judging.MVP'),
 'VALUE_WEIGHT':fact(20,'20%',ROOT/'brief.md','judging.value'),
 'AI_WEIGHT':fact(20,'20%',ROOT/'brief.md','judging.AI'),
 'BIZ_WEIGHT':fact(20,'20%',ROOT/'brief.md','judging.business'),
 'DEMO_WEIGHT':fact(15,'15%',ROOT/'brief.md','judging.presentation'),
}
(ROOT/'facts.json').write_text(json.dumps(facts,ensure_ascii=False,indent=2),encoding='utf-8')
slides=[]
def slide(layout,title,kicker,subtitle='',**kw): slides.append(dict(layout=layout,title=title,kicker=kicker,subtitle=subtitle,**kw))
slide('hero','Cutline','YONSEI AI STARTUP HACKATHON','에이전트가 편집하고,\n옆에서 바로 본다.',tagline='영상 편집의 Cursor',team='팀 {{TEAM_NAME}}  ·  {{TEAM_MEMBERS}}',bottom='파일로 편집  /  바로 재생  /  채널의 선택을 기억')
slide('cards','자동화 다음에 남는 질문,\n“우리 채널은 무엇을 남길까?”','문제 해결 · 사용자 가치 {{VALUE_WEIGHT}}',
 '첫 고객 [가설]  ·  긴 방송을 편집하는 1인 크리에이터와 스트리머',cards=[
 ['반복 작업은 자동화','전사에서 문장을 지우고\n무음 구간을 잘라내는 도구는\n이미 있습니다.'],
 ['선택의 기준은 사람에게','어떤 반응을 살리고\n얼마나 기다렸다 자를지,\n채널 맥락이 필요합니다. [가설]'],
 ['검토까지 한 화면에서','지시 → 결과 확인 → 수정의\n왕복을 줄이면 편집 초안의\n검토가 쉬워집니다. [가설]']],
 foot='도구 근거: Adobe Text-Based Editing · https://helpx.adobe.com/premiere/desktop/edit-projects/edit-video-using-text-based-editing/detect-and-delete-pauses-in-transcripts.html\nAuto-Editor · https://github.com/WyattBlue/auto-editor')
slide('insight','영상 편집도, 파일을 고치는 일입니다.','제품 통찰','코딩 에이전트의 기존 작업 방식을 영상 타임라인에 연결합니다.',
 left=['이미 익숙한 작업','파일 읽기 → 변경 → 검증 → 커밋','Claude Code / Codex'],right=['Cutline의 연결점','timeline.json → 옆 패널에서 재생','원본은 그대로, 선택 구간만 변경'],
 code='timeline.json\n{ "id": "reaction",\n  "source": "sources/original.mp4",\n  "in": 120, "out": 135,\n  "reason": "질문 뒤 반응을 보존" }',
 note='스키마 설명용 코드 · 시간값은 편집 성능 수치가 아닙니다.')
slide('product','파일과 결과가 같은 작업 공간에','MVP 구현 완성도 {{MVP_WEIGHT}}','VSCodium 기반 다운로드 앱 + Cutline 확장',image='assets/cutline-launch-2.png',
 callouts=[['timeline.json','에이전트가 수정하는 편집 파일'],['터미널 에이전트','설치·인증한 CLI를 직접 실행'],['영상 패널','저장한 선택 구간을 바로 확인'],['Diff 배너','추가 / 삭제 / 트림 · 길이 변화'],['Versions','git 커밋 비교 · 복원']],
 foot='실제 앱 실행 캡처 · 합성 테스트 영상의 초기 상태. Diff 변화와 Versions는 기능 설명이며 이 화면에는 펼쳐져 있지 않습니다.\n출처: video-ide/app/screenshots/cutline-launch-2.png · README.md · VERIFICATION.md')
slide('flow','지시부터 검토·내보내기까지','발표 및 시연 {{DEMO_WEIGHT}}','발표에서는 준비된 프로젝트로 핵심 흐름을 보여줍니다.',steps=[
 ['프로젝트 열기','원본 · 대본 · style.md\n폴더를 그대로 엽니다.'],
 ['에이전트에게 요청','“style.md대로\n{{TARGET_DURATION}} 편집본을 만들어 줘.”'],
 ['변경을 보고 재생','+추가 / −삭제 / 트림\n길이 전후와 선택 이유 확인'],
 ['비교하고 확정','Human vs AI 비교\n커밋 · 복원 · MP4 출력']],
 note='현재 검증: 파일 저장·CLI 변경 경로. 실제 구독 에이전트의 전체 편집 세션은 측정 중.\n긴 전사·프록시는 사전 준비하고, 녹화 축약 시 실제 경과 시간을 표시합니다.')
slide('architecture','에이전트는 판단하고, 앱은 검증·재생합니다.','AI 활용 · 기술 적절성 {{AI_WEIGHT}}','VSCodium + Cutline 확장  |  편집 상태는 공개 파일 규약',nodes=[
 ['프로젝트 입력','sources + transcripts\n+ style.md'],['구독 CLI 에이전트','Claude Code / Codex\n계획 · 구간 선택 · JSON 편집'],['timeline.json','스키마 · 원본 범위 검증\n저장 변경 감지'],['라이브 패널','diff · 재생 · 비교\ngit 커밋 이력'],['ffmpeg','원본 컷 연결\nMP4 내보내기']],
 note='별도 유료 API 연동 없이, 사용자가 설치·인증한 구독 CLI를 실행합니다.\n구독·사용량 제한은 각 서비스에 따르며, 클라우드 에이전트에는 읽은 대본이 전달될 수 있습니다.\n매 편집 버전은 명시적 git commit으로 남깁니다. 저장마다 자동 커밋하지 않습니다.')
slide('style','채널의 과거 선택을, 다음 편집의 근거로','차별성 · 스타일 메모리','현재: 단일 쌍의 관찰 규칙·정렬·비교  /  다음: 여러 쌍에서 자동 프로필 생성',
 stages=[['원본 ↔ 사람 편집본','원본 시각에 keep / drop 정렬\n미정렬은 unknown으로 보존'],['측정 가능한 스타일','내용 유형별 보존율 · 컷 길이\n발화/웃음 대비 컷 위치 [계획]'],['style.md + score 도구','근거 시각 · 유사 선택을 전달\n효과는 독립 원본에서 검증']],
 track_title='같은 원본 시간축으로 비교  ·  실제 reference 구간을 시각화',
 foot='Computational Video Editing for Dialogue-Driven Scenes · https://graphics.stanford.edu/papers/roughcut/\nPHD-GIFs: Personalized Highlight Detection for Automatic GIF Creation · https://arxiv.org/abs/1804.06604\nRethinking the Evaluation of Video Summaries · https://arxiv.org/abs/1903.11328')
slide('results','검증된 동작과, 아직 측정할 성과','MVP 구현 완성도 {{MVP_WEIGHT}}','숫자는 Cutline 파일에서 확인한 값만 사용합니다.',metrics=[
 ['{{ORIGINAL_DURATION}} → {{HUMAN_DURATION}}','원본 → 사람 편집본','AI가 줄인 결과가 아닙니다.'],
 ['{{ALIGNMENT_COVERAGE}}','편집본 정렬 커버리지','복원 {{ALIGNED_SECONDS}} / 미정렬 {{UNALIGNED_SECONDS}}'],
 ['{{DIFF_LATENCY}}','저장 → diff DOM 갱신','설치 확장 통합 테스트의 단일 측정'],
 ['{{TESTS_PASSED}}','npm test','실제 ffmpeg 출력·검증 포함']],pending=[['AI vs Human F1','{{AI_vs_HUMAN_F1}}'],['에이전트 편집 시간','{{AGENT_EDIT_TIME}}'],['창작자 블라인드 A/B','{{CREATOR_AB}}']],
 foot='출처: cutline-demo-chim/project/reference/alignment_summary.json · video-ide/VERIFICATION.md\n현재 compare.json은 원본 전체 시작 상태. 시간 겹침 F1은 순서·자막·재미·채널다움을 평가하지 않습니다.')
slide('cards','AI를 필요한 곳에 나눠 씁니다.','AI 활용 · 기술 적절성 {{AI_WEIGHT}}','특정 모델에 편집 프로젝트를 묶지 않는 구조',cards=[
 ['계획과 편집 · 에이전트','CLI가 대본과 style.md를 읽고\n선택 이유와 timeline을 작성.\n같은 파일 규약으로 교체 가능.'],
 ['전사 · 로컬 CPU','faster-whisper CPU int8 경로.\nGPU 없는 노트북의 준비 작업.\n완료·처리 시간: {{ASR_TIME}}'],
 ['정렬 · 평가 근거','사람 편집의 원본 위치를 복원.\n미정렬은 정답에서 제외.\n콘텐츠 품질은 사람 평가로.']],
 foot='faster-whisper · https://github.com/SYSTRAN/faster-whisper · CPU int8는 도구 지원 기능이며 이 PC 처리 속도 보장 아님.\nASR은 별도 준비 파이프라인이며 앱 자동 전사는 아직 범위 밖. 로컬 처리와 에이전트 구독 비용을 구분합니다.')
slide('position','파일로 편집하는 에이전트 × 채널의 기억','창업 · 사업화 가능성 {{BIZ_WEIGHT}}','주요 사용 흐름 기준의 Cutline 팀 평가 · 기능의 절대적 유무나 시장 전수조사 아님',
 foot='제품 공식 소개: descript.com · capcut.com · vrew.ai · opus.pro · cursor.com · Adobe Text-Based Editing\nCutline의 상단 위치는 개발 목표입니다. 현재 구현은 파일 편집·비교, 스타일 개선 효과는 검증 중.')
slide('cards','이미 AI를 구독하는 크리에이터부터','창업 · 사업화 가능성 {{BIZ_WEIGHT}}','초기 고객·수익모델·유통은 검증할 사업 가설입니다.',cards=[
 ['첫 고객 [가설]','혼자 긴 방송을 편집하며\n이미 AI CLI를 사용하는\n크리에이터·스트리머'],
 ['수익모델 [가설]','앱은 무료로 배포\n채널별 스타일 메모리 유료\n협업·공유를 위한 팀 플랜'],
 ['유통과 검증 [가설]','오픈소스 배포로 첫 사용 유도\n채널 원본·편집본으로 파일럿\n반복 사용과 지불 의향 확인']],
 bottom='유료 가치는 “AI 호출”보다 축적되는 채널 기준과 팀의 검토 이력에 둡니다. [가설]')
slide('roadmap','오늘의 작동 범위에서, 검증 가능한 다음 단계로','검증 범위 · 로드맵',columns=[
 ['오늘 확인','Windows 앱 실행\nJSON 변경 → 패널 반영\ngit 읽기·복원 로직\nffmpeg 출력 · 정렬 reference'],
 ['지금의 한계','구독 에이전트 실측 미완료\n긴 영상 재생·청감 미검증\n컷 경계에 seek 지연 가능\n자막 합성·믹싱·전환 미지원'],
 ['다음 검증','더 많은 독립 원본·편집 쌍\n같은 길이 기준선 + 블라인드 A/B\n스타일 자동 생성·MCP 서버\n다른 OS · 실제 제작자 사용']],
 note='스타일 개선과 시간 절감은 아직 주장하지 않습니다.\n먼저 “편집할 수 있는가”, 다음으로 “내 채널에 더 맞는가”를 검증합니다.')
slide('closing','편집의 기준은 창작자에게.\n반복 작업은 에이전트에게.','CUTLINE','우리가 찾는 것은, 함께 검증할 첫 크리에이터입니다.',
 team='{{TEAM_NAME}}  |  {{TEAM_MEMBERS}}\n역할: {{TEAM_ROLES}}',ask='요청  ·  원본·편집본 제공이 가능한 파일럿 파트너\n피드백  ·  채널다움과 실제 수정 시간을 함께 평가',links=['데모 영상  {{YOUTUBE_URL}}','데모 URL  {{DEMO_URL}}','GitHub  {{GITHUB_URL}}'])
deck=dict(title='Cutline',font='Malgun Gothic',slides=slides,placeholders={'TEAM_NAME':'[팀명 입력]','TEAM_MEMBERS':'[발표자·팀원 입력]','TEAM_ROLES':'[담당 역할 입력]','YOUTUBE_URL':'[링크 입력]','DEMO_URL':'[링크 입력]','GITHUB_URL':'[링크 입력]'})
(ROOT/'deck.json').write_text(json.dumps(deck,ensure_ascii=False,indent=2),encoding='utf-8')
print('Initialized deck.json, facts.json, snapshots and assets')
