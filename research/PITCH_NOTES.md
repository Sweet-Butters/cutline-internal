# Cutline 해커톤 발표 메모

2026-11-20 · 제안 기능과 검증된 결과를 구분한다. 상세 연구·라이선스·평가 설계는 [STYLE_RESEARCH.md](STYLE_RESEARCH.md), DB 설계는 [schema.sql](schema.sql).

## 발표에 사용할 8개 주장

- **[근거있음 + 출처] “편집 스타일은 측정 가능한 선택으로 나눌 수 있습니다.”** 컷 타이밍·shot 선택·속도·프레이밍 등을 모델링한 선행연구가 있다. Cutline은 여기에 내용 유형별 보존율·길이·순서·효과 빈도를 나누어 기록하려 한다. “창작자의 감각 전체를 수치화했다”는 주장은 하지 않는다. [Computational Video Editing](https://graphics.stanford.edu/papers/roughcut/), [Automatic Style Transfer](https://research.google/pubs/automatic-style-transfer-for-non-linear-video-editing/)

- **[근거있음 + 출처] “과거에 무엇을 골랐는지는 개인화의 학습 신호가 됩니다.”** 과거 GIF 선택이나 highlight 이력으로 사용자별 예측을 조건화한 연구가 있다. 이것이 한국어 채널의 원본 3개만으로 충분하다는 뜻은 아니다. [PHD-GIFs](https://arxiv.org/abs/1804.06604), [Adaptive Video Highlight Detection](https://arxiv.org/abs/2007.09598)

- **[근거있음 + 출처] “첫 실험은 실패했고, 그 실패를 설계에 반영했습니다.”** 원본 3개 held-out macro F1이 0.1205→0.0723으로 내려갔고, 게임 프로필의 스터디 전이는 5.79초만 남겼다. 후속 보정 모델의 +0.000087 F1도 성공으로 포장하지 않는다. [기존 LEARN_REPORT](../gangeuigam-mvp/reports/LEARN_REPORT.md), [STYLE_REPORT](../gangeuigam-mvp/reports/STYLE_REPORT.md)

- **[가설] “채널 스타일은 기본 내용 판단 위에 작은 보정으로 얹으면 더 안정적일 것입니다.”** 같은 채널·장르·형식에서만 보정하고, 표본이 적거나 목적이 다르면 base로 돌아간다. 기존 후속 MVP에 bound와 장르 차단은 이미 있었으며, 이번 제안은 형식·목표 길이·정렬 불확실성까지 명시한다. 품질 개선은 독립 원본 평가가 필요하다.

- **[가설] “우리의 차별점은 근거를 열어볼 수 있는 편집 메모리입니다.”** agent는 versioned style.md와 도구를 통해 “이 채널이 남긴 비슷한 순간” 및 반례를 원본 타임스탬프와 함께 읽는다. 감각적인 prompt 한 문장보다 수정·감사하기 쉬울 것으로 기대한다. 이번 산출물은 이 흐름의 연구·DB/API 설계이며 새 IDE 구현 완료 주장은 아니다.

- **[근거있음 + 출처] “단어 단위 전사와 가벼운 음성 분석은 NVIDIA GPU 없이도 시작할 수 있습니다.”** faster-whisper는 CPU int8·word timestamps, Silero는 경량 VAD를 제공한다. 전체 영상 이해의 실시간 처리나 이 노트북의 처리 속도를 보장하지 않는다. [faster-whisper](https://github.com/SYSTRAN/faster-whisper), [Silero VAD](https://github.com/snakers4/silero-vad)

- **[근거있음 + 출처] “성공은 F1 하나로 판단하지 않겠습니다.”** 영상 요약 평가에서 random과 segmentation이 F-score를 교란할 수 있다는 연구가 있다. 원본별 holdout, 동일 길이 random, 경계·pacing 지표, creator 블라인드 A/B를 함께 사용한다는 평가 계획이다. [Rethinking the Evaluation of Video Summaries](https://arxiv.org/abs/1903.11328)

- **[가설] “IDE의 수정 이력을 다음 편집에 쓸 수 있는 명시적 피드백으로 바꿀 수 있습니다.”** accept/reject/revert의 실제 구간 변화와 이유를 기록하고, 같은 구간 선택과 장기 취향을 구분해 새 profile version을 만든다. 사용자 피드백으로 요약을 개선하는 선행연구는 있지만 Cutline의 편집 시간 절감은 아직 미측정이다. [Active Video Summarization 저자 구현](https://github.com/GarciaDelMolino/active-video-summarization)

## 예상 심사 질문 5개와 정직한 답변

**1. “스타일이 주관적인데 객관적이라고 할 수 있나요?”**

취향 자체가 객관적이라고 주장하지 않습니다. 같은 과제 조건에서 무엇을 남기고 어디서 자르는지는 관측할 수 있습니다. 그 반복 경향을 통계와 근거로 표현하고, 실제로 자기 채널답다고 느끼는지는 창작자의 블라인드 평가로 따로 확인합니다. 내용 품질도 별도 문항으로 묻습니다.

**2. “기존 실험에서 더 나빠졌는데 왜 가능하다고 보나요?”**

가능성을 뒷받침하는 개인화 highlight 연구는 있지만 우리 제품의 성공 증거는 아직 없습니다. 첫 실험은 기본 판단을 수치 프로필로 대체했고 형식·도메인·표본 문제가 있었습니다. 후속에서 제한 보정과 장르 차단을 추가했지만 개선은 사실상 미미했습니다. 지금은 같은 base와 길이 예산에서 보정의 순수 효과를 측정하고, 개선되지 않으면 사례 검색·수동 규칙까지만 제공할 계획입니다.

**3. “몇 개 영상을 주면 되나요? 오늘 무엇을 입증하나요?”**

3–5개 독립 원본은 동작 시연용이지 일반화 보장용이 아닙니다. 같은 채널·장르·출력 형식으로 10–20개 pilot을 모아 분산과 learning curve를 측정하고 필요한 수를 다시 계산해야 합니다. 오늘 이 연구가 제시하는 것은 측정 정의·실패 분석·DB·평가/구현 계획입니다. 원본을 잘라 만든 clip 수를 독립 영상 수로 부풀리지 않습니다.

**4. “그냥 LLM에 ‘이 유튜버처럼 편집해’라고 하면 안 되나요?”**

그 방법도 비교할 baseline입니다. 제안한 DB는 실제 선택 이력, 근거 시각, 적용 범위, 반례, 피드백과 버전을 남깁니다. 이것이 일반 prompt보다 정확하고 빠르다는 것은 가설이므로 동일 agent/base에서 근거 없는 prompt와 비교해야 합니다. 표본이 부족하면 그 사실을 표시하며 규칙을 지어내지 않습니다.

**5. “다른 유튜버 영상을 가져와서 학습해도 되나요?”**

제품 경로는 창작자가 권한을 확인하고 원본·완성본을 직접 제공하는 것입니다. 분석·채널 스타일 재사용·외부 전송·공개 시연 동의를 구분하고, 게스트·음악·채팅 권리도 따로 확인합니다. 공개 영상은 열람 가능하다고 자동 수집·상업 학습·재배포가 허용되는 것이 아닙니다. 연구 데이터도 이용 조건을 확인하며, 철회 시 관련 특징·캐시·프로필을 제거하거나 남은 근거로 재생성하도록 설계했습니다. [YouTube 약관](https://www.youtube.com/static?template=terms), [개인정보 보호법](https://www.law.go.kr/lsInfoP.do?ancYnChk=0&lsId=011357)

## 발표 전 확인

실제 데모에 쓰는 영상의 권리와 평가 결과만 제시한다. 합성 timeline·예시 수치·oracle 응답은 화면에도 표시한다. “최초”, “3개면 충분”, “정확도 향상 입증”, “채팅/웃음 완벽 이해”, “편집시간 몇 배 단축”은 현재 근거로 주장하지 않는다.
