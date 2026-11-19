# Cutline pitch v2

기존 재실행 빌드를 갱신한 13장 발표 자료입니다. 모든 작업은 이 폴더에서 수행합니다.

## 산출물

- out/Cutline_pitch.pdf — 16:9, 13장, 20 MB 이하
- out/Cutline_pitch.pptx — 편집 가능한 텍스트·도형 및 발표자 노트
- out/slides/slide-01.png … slide-13.png — PowerPoint 1920×1080 렌더
- out/contact-01-07.jpg, contact-08-13.jpg — 전체 검토용
- script.md — 데모 1분 포함 5분 대본·촬영 큐
- QA.md — 내부 준비용 질문 10개
- REPORT.md — 모든 수치의 출처·조건·공개 웹 확인 상태
- facts.json — 원값·표시값·근거·계획 여부
- out/build_report.json, out/audit.json — 크기·넘침·분리 규칙 검사
- out/numeric_contexts.json — 렌더된 모든 숫자 문맥
- evidence/manifest-v2.json — 읽은 입력의 경로·해시

## 재빌드

Windows Python, python-pptx, Pillow, pywin32, PyMuPDF와 설치된 PowerPoint 사용.

```powershell
Set-Location D:\orca\projects\cutline-pitch
python build.py
python audit.py
python report_v2.py
```

build.py는 deck.json, facts.json, layouts_v2.py, script.md와 로컬 assets만 읽어 out/을 생성합니다. 외부 앱·측정 프로젝트를 실행하지 않습니다. report_v2.py는 허용된 외부 입력의 해시만 읽습니다. python build.py --pptx-only는 PDF·PNG를 갱신하지 않습니다.

이미 PowerPoint가 실행 중이면 해당 프로세스를 건드리지 않고 PDF/PNG 내보내기를 중단합니다. 빌드가 직접 연 프레젠테이션만 닫습니다.

prepare.py는 v1 초기화 스크립트, update_v2.py와 migrate_renderer.py는 이번 1회 마이그레이션 스크립트입니다. **일상 재빌드에서 실행하지 마세요.** 콘텐츠 수정은 deck.json과 facts.json에 합니다. 레이아웃은 layouts_v2.py, 공통 디자인·내보내기는 build.py입니다.

## 자료 상태

최신 허용 샘플 화면 cutline-check.png를 사용했습니다. cutline-signals.png는 확인 시 없었습니다. 실제 방송 화면이나 private 폴더를 읽지 않았습니다. 데모 MP4는 제공되지 않아 1분 촬영 흐름을 작성했습니다. 대본은 시간 배분안이며 리허설 낭독은 미측정입니다.

팀 이름은 표지·팀 슬라이드의 Team 채널감으로만 사용합니다. 승인된 실측 주장 외 다른 프로젝트 성과·가격·매출 계획은 넣지 않습니다. 공개 가격은 2026-11-20 브라우저 표시 기준이며 Cursor Pro는 현행 가격표에서 확인되지 않아 상태를 명시했습니다. 원문 URL·재검증 한계는 REPORT.md에 있습니다.
