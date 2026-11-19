# 다른 PC에서 이어가기 — 2026-11-20 검증 기록

이 문서는 현재 PC에서 직접 확인한 결과를 기록한다. 최초 인수인계는 `HANDOFF.md`, 설치 순서는 `SETUP_OTHER_PC.md`를 참고한다. 두 저장소는 비공개로 유지하며 영상·대본·내부 자료를 외부로 업로드하지 않는다.

## 현재 작업

- 앱: `Sweet-Butters/cutline`, 작업 브랜치 `Sweet-Butters/humpback`, 시작 커밋 `cb6ec15`.
- 내부 자료: `Sweet-Butters/cutline-internal`, 작업 브랜치 `setup/local-cli-path`.
- 내부 자료의 `ca1d579`는 CLI 경로를 `CUTLINE_CLI_PATH` → `demo-chim/.cutline/cli-path.txt` → 나란히 둔 `cutline/out/cli.js` 순으로 찾는다. 이전의 이 PC 전용 경로 변경 `9e642ba`를 대체한다. 새 PC에서 두 저장소를 나란히 두면 wrapper를 고칠 필요가 없다.
- 이 세션은 로컬 커밋만 만든다. GitHub에 push하거나 공개 배포하지 않는다. 다른 PC에서 새 변경을 받으려면 해당 커밋의 전달이 별도로 필요하다.

## 확인 완료

- Node 24.3.0, Python 3.13.5, ffmpeg/ffprobe, Claude·Codex CLI가 설치되어 있다.
- Codex는 `codex login status`로 로그인 확인. **사용자 지시로 이 PC에서는 Codex 구독 로그인만 사용한다.** Claude는 설치되어 있지만 미로그인이며 설정 완료 조건에서 제외한다. 다른 PC에서도 사용할 CLI의 로그인 상태를 확인한다.
- 앱 `npm ci`, `npm test`: 빌드 성공, 테스트 28개 통과.
- `demo-chim`에서 CLI `summary` 실행과 `compare.js --self-test` 통과.
- VS Code 1.131.0에서 앱 통합 테스트 통과: 영상 메타데이터·`canplay`, 실제 프레임 진행과 클립 전환, 대본 탐색, 수동 편집·되돌리기, 버전 비교 확인.
- 이 VS Code에서는 WebM의 demux 오류 후 MP4 호환 프록시로 전환했다. 전환 후 640×360 재생과 프레임 진행을 확인했다. 모든 환경에서 WebM이 실패한다는 뜻은 아니다.
- 앱 커밋 `ec7efdc`: 새 checkout에서도 VSIX 출력 폴더를 자동 준비한다. `dist/cutline.vsix` 생성 성공.
- 앱 커밋 `da231da`: 통합 테스트의 이전 PC 전용 `D:` 경로를 제거했다. Windows의 일반 VS Code 설치 경로를 자동 탐색하고, 없으면 테스트 도구가 내려받는다. `CUTLINE_VSCODE`로 명시할 수도 있다. 설정 없이 `npm run test:integration` 재실행 통과.
- 내부 자료 루트 `.venv`에 yt-dlp와 numpy 설치 완료. 다른 PC에서는 가상환경을 다시 만든다.
- `app/dist/Cutline-win-x64.zip` 생성 및 독립 압축 해제 확인. ZIP 안에 실행 파일과 설치된 확장이 있고 침착맨 프로젝트 경로·대표적인 인증 파일명은 없음을 확인했다. 실제 패키지의 재생 검증은 아래 최종 기록을 확인한다.

## 진행 중 — 완료로 간주하지 말 것

- 2시간 원본 전체를 Cutline 패널에서 열어 `canplay`와 프레임 진행·후반 탐색 확인.

## 패키지·영상 복원 검증

- ZIP: `cutline/app/dist/Cutline-win-x64.zip`, 189,286,284 bytes. SHA-256: `ac407325a166836cbe36329ae891abefc3c879a534ed67012f48a1c7b6ec3fc3`.
- VSIX: `cutline/dist/cutline.vsix`, 68,131 bytes. SHA-256: `4a3896d9d1d1106bdffbfd10f5326b8aec829ed5365c39b761b9bcae5a8b5fca`.
- 두 파일 옆에 `.sha256` 파일이 있다. 이 파일들은 Git에 들어가지 않는다.
- ZIP에서 독립적으로 압축 해제한 VSCodium 1.100.33714와 포함된 확장의 통합 테스트가 종료 코드 0으로 통과했다. WebM 직접 재생, 640px 영상, 프레임 진행·오디오 디코딩을 확인했다.
- 실행기의 폴더 인자, 최초 샘플 복사, 기존 프로젝트 편집 보존 검사 통과.
- 원본: `demo-chim/sources/original.mp4`, 7,293.062676초, 1,361,925,581 bytes, 1280×720 AV1/AAC. 타임라인의 마지막 초와 정확히 일치하며 `validate` 통과.
- 사람 편집본: `demo-chim/reference/human_edit.mp4`, 1,398.189569초, 294,914,142 bytes, 1280×720 AV1/AAC.
- 이번 파일은 이전 PC의 240p 원본과 다르다. 타임라인 시간은 일치하지만 원본 바이트가 다르므로 프록시 캐시는 공유되지 않는다.
- 위의 오디오 디코딩 검사는 스피커로 소리를 직접 들어본 검사가 아니다.
- 내부 자료 `a723bcd`의 `demo-chim/download.ps1`은 저장소 루트 `.venv`를 사용해 두 파일을 올바른 프로젝트 경로로 복원한다. `-DryRun`은 다운로드하지 않고 계획·기존 파일 보존 여부를 출력한다. 파일 덮어쓰기 방지와 실패 처리·정리는 오프라인 검사했다.

## 긴 영상 재생 검사 재실행

앱 커밋 `024d8b3`의 `tools/test-playback.js`를 앱 저장소에서 실행한다. 아래 예시는 두 저장소가 나란히 있고 앱을 직접 빌드한 경우다. ZIP을 따로 풀었다면 실행 파일·확장 폴더 경로를 바꾼다.

```powershell
node tools/test-playback.js --project ../cutline-internal/demo-chim --vscode ./app/build/Cutline/VSCodium.exe --extension ./app/build/Cutline/data/extensions/cutline-local.cutline-0.1.0
```

출력 JSON의 `passed: true`와 3개 `checks`를 확인한다. 첫 클립의 시작·중간·끝 근처에서 실제 재생 시간과 디코딩된 프레임 증가를 확인한다. 별도 임시 사용자 프로필을 사용하며, 대본 내용은 결과 JSON에 저장하지 않는다. 프록시 캐시가 없으면 전체 영상 변환을 기다리므로 오래 걸릴 수 있다. 무음 자동 검사이므로 스피커 출력은 시연 전에 직접 확인한다.

현재 PC의 작업 기록은 Git 밖의 다음 폴더에 있다:

`C:\Users\pxh7y\.agents\state\work-status\838a7d2d4c1c4f5f\setup-complete-20261120\`

`root.json`은 조정 작업, `app-validation.json`은 앱 검증, `media-playback.json`은 영상 복원을 기록한다. 프로세스 생존이나 heartbeat는 완료 증거가 아니다. 다른 PC에서는 이 상태 경로 대신 이 문서와 실제 산출물을 확인한다.

## 다른 PC에서 먼저 할 일

1. 두 저장소의 로컬 변경을 확인한 뒤 원격 변경을 가져온다. 이 세션에서 만든 커밋이 아직 원격에 없으면 먼저 전달받는다.
2. `SETUP_OTHER_PC.md`대로 도구와 앱 의존성을 설치하고 빌드한다. `.venv`, 프록시 캐시, 앱 ZIP은 Git에 들어가지 않는다.
3. 두 저장소를 나란히 두거나 `CUTLINE_CLI_PATH`에 앱의 `out/cli.js` 절대경로를 지정한 뒤 `node demo-chim/tools/vidcli.js summary`를 실행한다.
4. 영상을 복원한 뒤 `validate`를 실행한다. 길이 차이가 있으면 원본 타임라인을 임의로 덮어쓰지 말고 확인한다.
5. 아래의 최종 검증 기록이 갱신되었는지 확인하고, 미완료 항목부터 이어간다.

## 최종 검증 기록

진행 중. 작업별 결과와 커밋·산출물 경로를 확인한 뒤 갱신한다.

## GitHub에 push하지 않고 다른 PC로 옮기기

현재 PC의 `C:\Users\pxh7y\orca\deliverables\cutline-handoff-20261120\`에 로컬 변경만 담은 Git bundle을 준비한다. 이 세션의 bundle은 기존 앱 `cb6ec15`, 내부 자료 `bca451b` 커밋을 전제로 하므로 먼저 GitHub에서 두 저장소를 clone하거나 최신 상태로 받는다. 영상·캐시·가상환경은 bundle에 들어가지 않는다.

아래는 전달 폴더를 새 PC의 `C:\handoff`에 복사하고, 두 저장소가 현재 폴더 아래에 있다는 예시다. 기존 작업을 먼저 커밋하거나 보관한다.

```powershell
git -C cutline bundle verify C:/handoff/cutline-changes.bundle
git -C cutline fetch C:/handoff/cutline-changes.bundle HEAD:refs/heads/handoff-20261120
git -C cutline switch handoff-20261120

git -C cutline-internal bundle verify C:/handoff/cutline-internal-changes.bundle
git -C cutline-internal fetch C:/handoff/cutline-internal-changes.bundle HEAD:refs/heads/handoff-20261120
git -C cutline-internal switch handoff-20261120
```

이미 같은 이름의 브랜치에서 작업 중이라면 자동으로 덮어쓰지 말고 다른 새 브랜치 이름을 쓴다. 앱 ZIP과 VSIX는 위 패키지 경로에서 별도로 복사하거나 새 PC에서 빌드한다. 원본 영상은 내부 용도로만 복사하거나 문서의 두 URL에서 다시 받는다. bundle의 최종 커밋과 해시는 전달 폴더의 `manifest.json`에서 확인한다.
