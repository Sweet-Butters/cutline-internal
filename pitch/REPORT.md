# Cutline pitch v2 — 출처·수치·검수 보고서

기준일: 2026-11-20(KST). 작업·출력은 cutline-pitch 안에서만 수행. 허용된 외부 문서는 읽기만 했으며 video-ide/private는 접근하지 않았습니다. 이전 제작 스크립트는 v1 보관본이며 현재 재빌드는 build.py만 사용합니다.

## 결과 및 구성

13장: 표지 → 익명 인터뷰 → 시장 → 실제 샘플 앱 → 검증 루프 → 스타일 메모리 → 실측 → 1분 데모 구성 → 경쟁 → BM → 가격 → 다음 목표 → 팀.

편집 가능한 텍스트·도형 PPTX, PowerPoint PDF, 1920×1080 슬라이드 PNG, 5분 대본 및 발표자 노트, 내부 QA 10문항을 생성합니다. 완성 검사 수치는 out/audit.json과 out/build_report.json이 원본입니다.

## 공개시장 근거와 확인 상태

- **RAPA 2025**: [2025년 디지털크리에이터 활동현황 조사 원문](https://www.meplex.co.kr/fileHandler/downloadFile?file_seq=6936), 본문 p8(PDF p30), 2025년 5월 조사 모집단. 38,896개 중 구독자 1만 미만 17,581개를 PDF 텍스트로 직접 확인. 이는 응답자 수나 국내 전체 채널 수가 아닙니다. 로컬 원문: evidence/rapa-2025.pdf.
- **SOOP 2026**: [2026년 5월 IR Book](https://kind.krx.co.kr/external/dst/irReference/18658/2605_IR_Book_SOOP_Kor.pdf), p13 이미지 직접 확인. Active 스트리머 13,511명. 각주 정의는 과거 연속 3개월 동안 한 달에 최소 5시간 이상 방송한 스트리머. 인원과 채널은 합산하지 않음. 로컬 원문 및 확인 이미지: evidence/soop-2026-05.pdf, soop-p13.png.
- **수입 2024**: 원출처는 국세청 2024 종합소득세 신고자료(박성훈 의원실). [한국경제TV 2026-06-16 보도](https://m.wowtv.co.kr/NewsCenter/AMP/Read?articleId=A202606160292)로 하위 50%의 연평균 수입 2,463만 원을 교차 확인. 국세청 원표 직접 확보는 못했으며 허용 팩트시트 [11]와 일치. 2,463÷12=205.25만 원 → 약 205만 원/월. 순소득·모든 창작자 평균이 아닙니다.
- **외주비**: 허용된 2026-11-17 팩트시트 공개시장 항목 [6]의 크몽 과거 가격 안내(편당 5~40만 원) × 월 12편 = 월 60~480만 원. 원 안내의 발행연도·정확한 URL은 팩트시트에 없고 현재 동일 범위 재확인 불가. 따라서 슬라이드에도 ‘과거 안내·연도 미기재·산식’으로 표시. 현재 평균가·확정 절감액으로 사용하지 않습니다. 서로 다른 모집단·작업 범위의 비교입니다.

시장 팩트시트 경로(내부 근거 식별용): D:/자료실/02_프로젝트/창업경진대회_왕중왕전/2026-11-17_제출확정_발표준비패키지/03_전체상세_팩트시트_인수인계.txt. 이 문서에서는 공개 시장 정보만 전용했습니다. 제품·실측·팀·매출 계획은 전용하지 않았습니다.

## 공개 가격: 오늘 확인한 표시와 제안의 분리

| 제품 | 2026-11-20 공식 사이트 표시 | 적용 조건 |
|---|---|---|
| [Cursor](https://cursor.com/pricing) | Premium $30/월 | 요청한 Pro는 현행 가격표에 없음. 과거 Pro 금액을 현재가로 대체하지 않음. 세금·타사 모델 사용량 별도 |
| [Descript](https://www.descript.com/pricing) | Hobbyist $24/인·월; 연 결제 월환산 $16 | 덱의 앵커는 월 결제 $24 |
| [Opus Clip](https://www.opus.pro/pricing) | Starter 정가 $15, 당일 할인 $12 billed monthly | 실제 브라우저가 표시한 프로모션 가격 채택. 검색 색인에는 $15만 보임 |
| [Vrew](https://vrew.ai/en/payment/pricepolicy) | Light $133.99/년, 월환산 $11.17 | 연 결제 금액이며 VAT 포함 표기. 월 결제 요금으로 오인하지 않음 |

브라우저 원문 텍스트는 evidence/web-v2-prices.json, web-v2-prices2.json, web-v2-more.json에 보존. 첫 Vrew /en/pricing은 없는 경로였으며 공식 홈 링크를 따라 /en/payment/pricepolicy에서 확인했습니다. Opus 첫 탐색 타임아웃 후 정상 페이지 본문을 읽었습니다. 과거 Cursor 설명은 [2025-07-04 공식 글](https://cursor.com/blog/june-2025-pricing)도 확인했으나 현행 요금 앵커에는 사용하지 않았습니다.

Cutline 월 12,000원/채널, 월 39,000원/편집자(5개 채널 포함)는 이번 덱에서 제안한 **목표 가격**입니다. VAT 포함 목표, 실제 판매·매출·결제 의향 데이터가 아닙니다. 1채널과 5채널 구성 역시 상품 기획값. 무료 앱은 배포 계획이고 유료 메모리 제품은 개발 목표입니다. 추가 지불 가치와 반복 사용·실제 결제로 검증합니다.

## 경쟁과 설계 참고 원문

- [Descript MCP](https://www.descript.com/mcp): 자연어로 미디어 가져오기·편집·전사·게시. [Underlord](https://www.descript.com/underlord): AI 편집 보조. 단순히 ‘채팅 편집이 없다’고 비교하지 않았습니다.
- [video-editor-mcp](https://github.com/PlbKin190/video-editor-mcp): ffmpeg 기반 trim·concat·JSON timeline render·자동 QA 공개 저장소. 존재와 README 기능 범위 확인, 직접 설치·성능시험은 하지 않음.
- [Premiere Text-Based Editing](https://helpx.adobe.com/in/premiere/desktop/edit-projects/edit-video-using-text-based-editing/overview-of-text-based-editing.html): 전사 텍스트 편집과 타임라인 연결.
- [CapCut](https://www.capcut.com/), [Vrew](https://vrew.ai/en/), [Opus Clip](https://www.opus.pro/pricing): AI 편집·자막·텍스트 편집·숏폼 제품군의 예. 모든 제품이 모든 기능을 동일하게 지원한다는 주장은 아님.
- [Cursor](https://cursor.com/), [Claude Code 공식 개요](https://code.claude.com/docs/en/overview): 코드·파일 편집 및 실행 도구. Cutline의 상대적 위치는 팀 평가이며 전수 비교나 독점성 주장이 아닙니다.
- [NVIDIA SimReady FAQ](https://docs.omniverse.nvidia.com/simready/latest/simready-faq.html): Profile 요구조건에 대한 검사→수정→재검사. [TRINIX](https://ndotlight.com/), [Digital Twin](https://ndotlight.com/solutions/digital-twin): 대화와 시뮬레이션 자산, 피드백 루프에 대한 공급사 설명. Cutline의 설계 유추이며 파트너·인증·동일 엔진을 뜻하지 않습니다. TRINIX 규칙별 보고서·git 기능은 확인된 것으로 쓰지 않음.

## 모든 수치의 원장

슬라이드 주요 수치는 facts.json에서 관리합니다. 아래 ‘종류’는 실측·관찰, 계산, 과거 자료, 구조적 사실, 계획을 구분합니다.

| 키 | 덱 표시 | 원값 | 종류 | 원출처 / 조건 |
|---|---|---|---|---|
| COVERAGE | 93.55% | 93.55 | fact | D:/orca/projects/cutline-measure/MEASUREMENT.md (2026-11-20);  |
| F1_RAW | 0.11 | 0.108 | fact | D:/orca/projects/cutline-measure/MEASUREMENT.md (2026-11-20); 소수 둘째 자리 반올림; 원본 시간축 겹침 F1 |
| F1_STYLE | 0.21 | 0.207 | fact | D:/orca/projects/cutline-measure/MEASUREMENT.md (2026-11-20); 소수 둘째 자리 반올림 |
| F1_RATIO | 약 2배 | 1.9166666666666665 | derived | D:/orca/projects/cutline-measure/MEASUREMENT.md (2026-11-20); 0.207 / 0.108 = 1.9167, 반올림 |
| KEY_RAW | 2.7개 | 2.7 | fact | D:/orca/projects/cutline-measure/MEASUREMENT.md (2026-11-20);  |
| KEY_STYLE | 7개 | 7 | fact | D:/orca/projects/cutline-measure/MEASUREMENT.md (2026-11-20);  |
| KEY_TOTAL | 24개 | 24 | fact | D:/orca/projects/cutline-measure/MEASUREMENT.md (2026-11-20); 사람이 15초 이상 남긴 구간 중 30% 이상 겹치면 포착 |
| RUNS | 각 3회 평균 | 3 | fact | D:/orca/projects/cutline-measure/MEASUREMENT.md (2026-11-20);  |
| AGENT_TIME | 약 2~3분 | [2, 3] | fact | D:/orca/projects/cutline-measure/MEASUREMENT.md (2026-11-20); Claude Code 구독 에이전트 편집 실행. 전사 준비·최종 렌더·사람 검토 시간 아님 |
| ORIGINAL | 2:01:33 | 7293 | fact | D:/orca/projects/cutline-measure/MEASUREMENT.md (2026-11-20);  |
| HUMAN | 23분 | 1398 | fact | D:/orca/projects/cutline-measure/MEASUREMENT.md (2026-11-20); 23:18을 분 단위 요약 |
| RAPA_SMALL | 17,581개 | 17581 | fact | RAPA, 2025년 디지털크리에이터 활동현황 조사, 2025-05 모집단, 본문 p8/PDF p30; https://www.meplex.co.kr/fileHandler/downloadFile?file_seq=6936;  |
| RAPA_TOTAL | 38,896개 | 38896 | fact | RAPA, 2025년 디지털크리에이터 활동현황 조사, 2025-05 모집단, 본문 p8/PDF p30; https://www.meplex.co.kr/fileHandler/downloadFile?file_seq=6936;  |
| SOOP_ACTIVE | 13,511명 | 13511 | fact | SOOP IR Book 2026-05, p13; https://kind.krx.co.kr/external/dst/irReference/18658/2605_IR_Book_SOOP_Kor.pdf; Active: 과거 연속 3개월 동안 한 달에 최소 5시간 이상 방송. 채널 수와 합산 금지 |
| INCOME | 약 205만 원/월 | 205.25 | derived | 국세청 2024 신고자료(박성훈 의원실), 하위 50% 연평균 수입 2,463만원; 2026-06-16 보도 https://m.wowtv.co.kr/NewsCenter/AMP/Read?articleId=A202606160292; 2,463만원 / 12개월 = 205.25만원. 순소득 아님; 허용된 팩트시트 [11]과 일치 |
| OUTSOURCE | 60~480만 원/월 | [60, 480] | historical-derived | 허용된 2026-11-17 팩트시트 공개시장 항목 [6] 크몽 과거 가격 안내; 편당 5~40만원 × 월12편. 안내 발행연도·원 URL 미기재, 오늘 동일 범위 재검증 불가. 현재 평균가/절감액 아님 |
| DESCRIPT | $24/인·월 | 24 | fact | https://www.descript.com/pricing (2026-11-20 브라우저 확인); Hobbyist 월 결제; 연 결제 월환산 $16과 구분 |
| OPUS | $12/월 | 12 | fact | https://www.opus.pro/pricing (2026-11-20 브라우저 확인); Starter 당일 할인 표시 $12 billed monthly, 정가 $15. 검색 캐시는 $15; 실제 브라우저 표시 채택 |
| VREW | $133.99/년 | 133.99 | fact | https://vrew.ai/en/payment/pricepolicy (2026-11-20 브라우저 확인); Light 연 결제, 사이트 월환산 $11.17, VAT 포함 표기 |
| CURSOR | $30/월 | 30 | fact | https://cursor.com/pricing (2026-11-20 브라우저 및 웹 확인); 현재 Premium 표시. 요청된 Pro는 현행 가격표에 없음. Pro 현행가 확인 불가; 과거 $20을 현재가로 사용하지 않음. 세금·타사 모델 사용량 별도 |
| CHANNEL_PRICE | 월 12,000원 | 12000 | plan | 이번 v2 덱의 가격 제안(브리프 BM 요청에 따라 작성); 제안: 채널 1개 스타일 메모리, VAT 포함 목표. 지불 의향 미검증 |
| EDITOR_PRICE | 월 39,000원 | 39000 | plan | 이번 v2 덱의 가격 제안(브리프 BM 요청에 따라 작성); 제안: 편집자 1명/채널 5개 포함, VAT 포함 목표. 지불 의향 미검증 |
| INFERENCE_COST | 거의 0 | 0 | structural | video-ide/README.md: 확장은 API를 직접 호출하지 않고 사용자의 구독 CLI 실행; Cutline이 직접 부담하는 AI 추론 API 비용 기준. 구독은 고객 부담; 저장·결제·지원 비용 별도 |
| TEAM_NUMBERS | TOP 10 · 2기 · 1년 | [10, 2, 1] | user-provided | 사용자 v2 브리프 (2026-11-20); 정회광 Cursor 트레인톤 TOP10·모두의 창업2기, 조남하 Coloso 1년. 다른 이력 가져오지 않음 |
| DEMO_SECONDS | 1분 | 60 | plan | 사용자 v2 브리프 (2026-11-20); 영상 흐름 0–8/8–16/16–24/24–34/34–44/44–53/53–60초. 시연 구성 목표; 녹화 파일 제공 없음 |

### 추가로 보이는 숫자와 단위

- 실측 원값 0.108→0.207을 소수 둘째 자리로 표시한 것이 0.11→0.21. 비율은 반올림 전 0.207÷0.108≈1.92로 ‘약 2배’. 핵심 장면 24개는 사람이 15초 이상 남긴 구간이며 30% 이상 겹치면 포착. 각 조건 3회 평균(내부 QA 측정 정의).
- 23분은 사람 편집본 23:18의 요약. 2시간은 원본 2:01:33의 요약. 데모의 ‘약 23분’은 편집 목표로 별도 표시하며 AI가 정확히 그 길이로 출력했다는 주장이 아님.
- 샘플 화면 안의 8/9 통과·경고 1·실패 0·미평가 1, 4 clips·04:00, 120초 원본, [180,250] 길이, clip 길이·timecode 등 모든 UI 숫자는 assets/cutline-check.png 원본 픽셀 및 video-ide/README.md의 샘플 사양에서 유래. 방송 실측 성능으로 세지 않음. 화면의 20분·3분·30초 프롬프트 칩은 예시 요청값.
- 가격 보조값 $16, $15, $11.17은 위 공개 가격 표와 브라우저 저장 텍스트. 5채널, 1채널, VAT 포함 제안은 내부 상품 기획값. ‘추론 거의 0’은 우리가 대신 지불하는 AI API 비용의 구조적 설명이며 실제 손익률 아님.
- TOP 10·모두의 창업 2기·Coloso 1년은 사용자 브리프의 해당 팀원 이력. A2A의 2는 Agent-to-Agent 명칭이며 성과 수치가 아님.
- 3D는 참고 분야명. F1은 측정 지표명. MP4는 출력 형식명. 문서의 p8·p13·p30 등은 원문 위치, URL·파일명 속 숫자는 식별자.
- 01–13 / 13은 슬라이드 순번. 16:9·13장·5분·300초·20MB는 제작 규격. 1920×1080은 PNG 출력 해상도. 240초 발표+60초 데모 및 슬라이드별 시간·데모의 00/08/16/24/34/44/53/60초는 이번 구성의 시간 배분이지 실측 속도가 아님.
- 2025·2024·2026.05 등 통계 기준연도는 각 원문. 2026-11-17은 시장 팩트시트 기록일. 2026-11-20은 이번 확인·실측·브리프 기준일. ‘v2’는 덱 개정 식별자.

## 이미지·제한·남은 준비

cutline-check.png가 허용된 폴더의 최신 스크린샷이며 sample-project임을 화면 제목으로 직접 확인했습니다. cutline-signals.png는 확인 시 존재하지 않아 포함하지 않았습니다. 외부 이미지·강의 이미지·방송 화면을 새로 만들거나 사적 폴더에서 가져오지 않았습니다.

1분 데모의 촬영 흐름은 완성했으나 원본 데모 MP4가 제공되지 않았으므로 녹화·영상 삽입은 하지 않았습니다. 실제 촬영 때 약 23분 목표를 실제 실행 결과 길이로 바꾸고 축약 구간에 경과 시간을 표기합니다. 대본은 5분 시간 배분안이며 실제 낭독은 미측정입니다.

실측 보고서 전체는 내부 자료이므로 복제하지 않고 승인된 결과와 내부 QA에 필요한 측정 정의만 반영했습니다. 파일 해시는 evidence/manifest-v2.json에 기록했습니다. 슬라이드·대본에는 제외하라는 내부 비교 수치를 넣지 않았습니다. 일반화·통계적 유의성·구별 불가 달성을 주장하지 않습니다.

## 검수 결과

PDF 529,327 bytes (0.529 MB), 상한 20 MB 이내. 13장 / PNG 13장. PowerPoint 텍스트 넘침 0건, 텍스트 상자 겹침 0건, 슬라이드 밖 0건. 본문 16pt 미만 0건(출처·라벨·이미지 UI 제외). 팀명은 표지와 팀 슬라이드에만 허용. 텍스트·도형 편집 가능, 발표 노트 포함. 전체 연락처·학번 없음.
