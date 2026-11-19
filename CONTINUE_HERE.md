# 다른 PC에서 이어가기 — 2026-11-20 검증 기록

이 문서는 현재 PC에서 직접 확인한 결과를 기록한다. 최초 인수인계는 `HANDOFF.md`, 설치 순서는 `SETUP_OTHER_PC.md`를 참고한다. 두 저장소는 비공개로 유지하며 영상·대본·내부 자료를 외부로 업로드하지 않는다.

## 현재 작업

- 앱: `Sweet-Butters/cutline`, 작업 브랜치 `Sweet-Butters/humpback`, 시작 커밋 `cb6ec15`.
- 내부 자료: `Sweet-Butters/cutline-internal`, 작업 브랜치 `setup/local-cli-path`.
- 내부 자료의 `9e642ba`는 이 PC용 CLI 경로 변경이다. 다른 PC에서는 `demo-chim/tools/vidcli.js`의 `require` 경로를 그 PC에서 빌드한 `cutline/out/cli.js`로 바꾼다.
- 이 세션은 로컬 커밋만 만든다. GitHub에 push하거나 공개 배포하지 않는다. 다른 PC에서 새 변경을 받으려면 해당 커밋의 전달이 별도로 필요하다.

## 확인 완료

- Node 24.3.0, Python 3.13.5, ffmpeg/ffprobe, Claude·Codex CLI가 설치되어 있다.
- Codex는 `codex login status`로 로그인 확인. Claude는 `claude auth status --json` 결과 미로그인이다. Claude 사용 전 사용자가 `claude auth login`을 실행해야 한다. 다른 PC에서는 각 PC의 로그인 상태를 다시 확인한다.
- 앱 `npm ci`, `npm test`: 빌드 성공, 테스트 28개 통과.
- `demo-chim`에서 CLI `summary` 실행과 `compare.js --self-test` 통과.
- VS Code 1.131.0에서 앱 통합 테스트 통과: 영상 메타데이터·`canplay`, 실제 프레임 진행과 클립 전환, 대본 탐색, 수동 편집·되돌리기, 버전 비교 확인.
- 이 VS Code에서는 WebM의 demux 오류 후 MP4 호환 프록시로 전환했다. 전환 후 640×360 재생과 프레임 진행을 확인했다. 모든 환경에서 WebM이 실패한다는 뜻은 아니다.
- 앱 커밋 `ec7efdc`: 새 checkout에서도 VSIX 출력 폴더를 자동 준비한다. `dist/cutline.vsix` 생성 성공.
- 앱 커밋 `da231da`: 통합 테스트의 이전 PC 전용 `D:` 경로를 제거했다. Windows의 일반 VS Code 설치 경로를 자동 탐색하고, 없으면 테스트 도구가 내려받는다. `CUTLINE_VSCODE`로 명시할 수도 있다. 설정 없이 `npm run test:integration` 재실행 통과.
- 내부 자료 루트 `.venv`에 yt-dlp와 numpy 설치 완료. 다른 PC에서는 가상환경을 다시 만든다.
- `app/dist/Cutline-win-x64.zip` 생성 및 독립 압축 해제 확인. ZIP 안에 실행 파일과 설치된 확장이 있고 침착맨 프로젝트 경로·대표적인 인증 파일명은 없음을 확인했다. 실제 패키지의 재생 검증은 아래 최종 기록을 확인한다.

## 진행 중 — 완료로 간주하지 말 것

- 앱 패키징과 VSCodium 기반 ZIP 생성·검증.
- 침착맨 원본 및 사람 편집본 복원.
- 2시간 원본 전체를 Cutline 패널에서 열어 `canplay`와 프레임 진행·후반 탐색 확인.

현재 PC의 작업 기록은 Git 밖의 다음 폴더에 있다:

`C:\Users\pxh7y\.agents\state\work-status\838a7d2d4c1c4f5f\setup-complete-20261120\`

`root.json`은 조정 작업, `app-validation.json`은 앱 검증, `media-playback.json`은 영상 복원을 기록한다. 프로세스 생존이나 heartbeat는 완료 증거가 아니다. 다른 PC에서는 이 상태 경로 대신 이 문서와 실제 산출물을 확인한다.

## 다른 PC에서 먼저 할 일

1. 두 저장소의 로컬 변경을 확인한 뒤 원격 변경을 가져온다. 이 세션에서 만든 커밋이 아직 원격에 없으면 먼저 전달받는다.
2. `SETUP_OTHER_PC.md`대로 도구와 앱 의존성을 설치하고 빌드한다. `.venv`, 프록시 캐시, 앱 ZIP은 Git에 들어가지 않는다.
3. `demo-chim/tools/vidcli.js` 경로를 새 PC에 맞추고 `summary`를 실행한다.
4. 영상을 복원한 뒤 `validate`를 실행한다. 길이 차이가 있으면 원본 타임라인을 임의로 덮어쓰지 말고 확인한다.
5. 아래의 최종 검증 기록이 갱신되었는지 확인하고, 미완료 항목부터 이어간다.

## 최종 검증 기록

진행 중. 작업별 결과와 커밋·산출물 경로를 확인한 뒤 갱신한다.
