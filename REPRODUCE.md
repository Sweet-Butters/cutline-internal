# 다른 Windows PC에서 침착맨 데모 재현

**소스 clone만으로 영상이 생기지는 않습니다. 아래 절차로 비공개 Release의 영상·프록시도 복원해야 합니다.**

## 준비

- 이 두 비공개 저장소에 접근 가능한 GitHub 계정
- Git, GitHub CLI(`gh`), Node.js 20+, ffmpeg/ffprobe가 PATH에 있는 Windows x64 PC
- Codex CLI 설치와 본인 구독 로그인. `codex login status`로 확인하며 미로그인이면 `codex login` 실행

`gh auth status`로 GitHub 로그인도 확인합니다. 미로그인이면 `gh auth login`을 실행합니다. Codex 로그인과 GitHub 로그인은 별개입니다.

## 새 작업 폴더에서 실행

아래는 아직 저장소나 설치본이 없는 새 폴더에서 실행하는 PowerShell 명령입니다. 이미 저장소를 받은 경우 clone 대신 해당 저장소의 `master`를 pull합니다.

```powershell
git clone https://github.com/Sweet-Butters/cutline.git
git clone https://github.com/Sweet-Butters/cutline-internal.git

# 수정된 설치본: 이전 handoff 버전 대신 repro 버전을 사용
gh release download v0.1.0-repro-20261120 --repo Sweet-Butters/cutline --pattern Cutline-win-x64.zip --dir .
Expand-Archive -LiteralPath .\Cutline-win-x64.zip -DestinationPath .\Cutline-app

# GitHub에서 원본·사람 편집본·검증한 프록시를 받고 크기와 SHA-256 확인
powershell -NoProfile -ExecutionPolicy Bypass -File .\cutline-internal\demo-chim\restore-github.ps1

# 에이전트가 사용할 CLI 경로를 이 PC에 저장
$cutlineDirectory = (Resolve-Path -LiteralPath .\Cutline-app\Cutline).Path
$demoDirectory = (Resolve-Path -LiteralPath .\cutline-internal\demo-chim).Path
New-Item -ItemType Directory -Force -Path (Join-Path $demoDirectory '.cutline') | Out-Null
Set-Content -LiteralPath (Join-Path $demoDirectory '.cutline/cli-path.txt') -Value (Join-Path $cutlineDirectory 'out/cli.js') -Encoding UTF8

# 일반 실행기로 실제 데모 폴더 열기
& (Join-Path $cutlineDirectory 'Cutline.exe') $demoDirectory
```

대화창에서 **Codex**를 선택합니다. 첫 화면은 편집 전 2시간 1분 33초짜리 원본 1클립입니다. 20–25분 하이라이트 편집은 이후 Codex에 지시하는 별도 작업입니다. 이번 수정본은 프로젝트에 복원한 프록시를 사용하므로 전체 영상을 다시 변환하지 않습니다. 다운로드 시간과 재생 준비 시간은 PC·네트워크에 따라 다릅니다.

## 직접 다운로드할 때

- [수정된 Cutline 설치본·VSIX·해시](https://github.com/Sweet-Butters/cutline/releases/tag/v0.1.0-repro-20261120)
- [원본·사람 편집본·프록시·media-manifest.json](https://github.com/Sweet-Butters/cutline-internal/releases/tag/demo-chim-media-20261120)

영상 Release의 `original.mp4`는 `demo-chim/sources/`, `human_edit.mp4`는 `demo-chim/reference/`, 긴 해시 이름의 `.webm`은 `demo-chim/.cutline-cache/` 아래에 같은 이름으로 둡니다. 정확한 크기와 해시는 `demo-chim/media-manifest.json`에 있습니다. 영상은 내부·심사용으로만 사용하며 공개 게시하지 않습니다.

## 검증 범위

이 PC의 새 GitHub clone에 세 영상 파일을 실제 다운로드해 크기·SHA-256을 확인했습니다. 수정 설치본의 일반 `Cutline.exe`로 해당 프로젝트를 열어 약 7초 안에 `canplay`를 확인했고, 재변환 파일과 재생 오류는 0건이었습니다. 앱 ZIP까지 GitHub에서 다시 내려받아 해시를 확인한 뒤, 복원한 원본의 시작·중간·끝에서 실제 프레임과 재생 시간이 증가하는 검사도 통과했습니다. 다른 사람의 실제 PC에서의 실행은 아직 확인하지 않았습니다. [검증 JSON](verification/github-media-reproduction-20261120.json)과 [상세 기록](CONTINUE_HERE.md)을 참고합니다.
