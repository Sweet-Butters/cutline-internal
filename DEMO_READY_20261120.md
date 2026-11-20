# Cutline — 이 PC 시연 준비 완료 (2026-11-20)

## 실행

PowerShell에서:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File D:\orca\projects\cutline-recording-20261120\Start-Cutline-Demo.ps1
```

이 실행 파일은 수정된 로컬 앱과 녹화용 프로젝트를 열고, 이미 생성한 프로젝트 프록시를 재사용한다. 원본 프로젝트는 `D:\orca\projects\cutline-demo-chim\project`에 그대로 보존했다. 녹화용 프로젝트는 별도 사본이며 원격 저장소를 연결하지 않았다. 초기 타임라인 커밋은 `87dbbd2`다.

## 확인 완료

- 실제 패키지의 확장으로 2:01:33 원본 시작·중간·끝 탐색 및 프레임 진행 통과. 오디오 디코딩 바이트 증가, 재생 오류 0건.
- 단위 테스트 29개, 패키지 확장의 편집·대본 탐색·되돌리기·비교·버전·검증표 통합 검사 통과.
- 녹화 프로젝트 validate 및 비교 도구 self-test 통과. 소리 신호 1,459구간 준비.
- 이 PC Codex 구독 로그인 확인. 채팅창에서 Codex를 선택한다.
- 상세 수치와 패키지 해시: `verification/local-playback-fix-20261120.json`.

자동 검사는 무음으로 세 위치를 확인한 것이다. 스피커 청취, 2시간 연속 재생, 실제 녹화는 완료한 것으로 간주하지 않는다. 녹화 전에 재생 버튼을 눌러 출력 장치와 소리를 직접 확인한다.

## 60초 촬영 흐름

1. 0–8초: 전체 원본 길이와 재생 화면.
2. 8–16초: Codex 선택 후 아래 지시 입력.
3. 16–24초: 편집 진행 표시. 기다린 부분을 축약하면 실제 경과 시간을 별도 표시.
4. 24–34초: 완료된 타임라인의 실제 길이와 변경 표시.
5. 34–44초: 사람 편집과 원본 구간 비교. 결과 점수는 실행 결과 그대로 사용.
6. 44–53초: 검증표를 펼치고 통과·경고·미평가 확인.
7. 53–60초: 재생 확인 후 MP4 내보내기. 완료되지 않은 내보내기는 완료로 편집하지 않는다.

지시문:

> style.md와 대본, 이미 준비된 소리 신호를 참고해 20–25분 편집본을 만들어줘. 대사가 없는 공연 장면도 검토하고, 장면을 남긴 이유를 한국어로 적어줘. 원본·대본·참조 파일은 수정하지 말고 timeline.json만 편집해줘. 정답 타임라인을 읽어 복사하지 말고, 편집 후 validate와 check로 확인해줘.

한 번 편집한 뒤 되돌릴 때는 앱의 초기 버전을 선택해 미리보기·복원을 사용한다. 대본 문구를 임의로 고치지 않는다. 출처는 영상 프레임에 넣지 않고 아래 companion credits 내용을 영상 설명에 사용한다.

## 파일

- 발표자료: `D:\orca\projects\cutline-pitch\out\Cutline_pitch.pdf`, `.pptx`
- 앱 ZIP: `D:\orca\projects\video-ide\app\dist\Cutline-win-x64.zip`
- VSIX: `D:\orca\projects\video-ide\dist\cutline.vsix`
- 공개용 로컬 사본: `D:\orca\projects\cutline-public` (이번 재생 수정 반영; 게시하지 않음)

기존 GitHub Release는 이번 로컬 수정 패키지와 다르다. 이번 작업에서는 Release 업로드, 공개 게시, 영상 업로드 및 제출을 하지 않았다.
