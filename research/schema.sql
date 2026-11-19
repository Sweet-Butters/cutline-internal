-- Cutline 연구 제안 / SQLite 3.38+ (JSON 함수 포함) / 2026-11-20
-- 빈 로컬 DB에 적용. 미디어/모델/서버를 만들지 않는 설계 DDL.
-- 연결마다 foreign_keys=ON. 시간은 정수 millisecond, 반열린 구간 [start,end).
-- UUID는 앱이 생성하는 TEXT. UTC 시각은 ISO-8601 TEXT.
-- 단일 사용자 로컬 파일용: 다중 사용자 서비스는 인증/RLS를 별도 구현해야 한다.
PRAGMA foreign_keys = ON;
BEGIN;

CREATE TABLE channels (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

-- 동의는 채널의 모든 미디어에 대한 포괄 권한이 아니다.
-- evidence_ref에 대상 파일/출연자/권리자/고지 버전 명세를 연결한다.
CREATE TABLE consents (
  id TEXT PRIMARY KEY,
  channel_id TEXT NOT NULL REFERENCES channels(id),
  purpose TEXT NOT NULL CHECK (purpose IN ('local_analysis','channel_style','external_processing','research','publication')),
  status TEXT NOT NULL CHECK (status IN ('pending','granted','revoked','expired')),
  policy_version TEXT NOT NULL,
  evidence_ref TEXT NOT NULL,
  scope_json TEXT NOT NULL CHECK (json_valid(scope_json)),
  granted_at TEXT,
  expires_at TEXT,
  revoked_at TEXT,
  UNIQUE(id, channel_id),
  CHECK (status <> 'granted' OR granted_at IS NOT NULL),
  CHECK (status <> 'revoked' OR revoked_at IS NOT NULL)
);

-- source/edited를 한 테이블로 정규화하여 특징 추출 코드를 공유한다.
-- source_group은 같은 촬영/방송의 재인코딩·발췌를 묶는 평가 누출 방지 키.
-- media_ref는 로컬 불투명 핸들. 클라우드 동기화 시 로컬 경로/서명 URL 금지.
CREATE TABLE videos (
  id TEXT PRIMARY KEY,
  channel_id TEXT NOT NULL REFERENCES channels(id),
  consent_id TEXT NOT NULL,
  kind TEXT NOT NULL CHECK (kind IN ('source','edited')),
  source_group TEXT NOT NULL,
  sha256 TEXT NOT NULL CHECK (length(sha256)=64 AND sha256 NOT GLOB '*[^0-9a-f]*'),
  media_ref TEXT NOT NULL,
  duration_ms INTEGER NOT NULL CHECK (duration_ms>0),
  genre TEXT NOT NULL,
  output_format TEXT NOT NULL, -- source이면 raw, edit이면 shorts/long_form 등
  language TEXT NOT NULL DEFAULT 'ko',
  editor_alias TEXT, -- 채널과 편집자가 다른 경우 분리
  timebase_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(timebase_json)),
  delete_after TEXT,
  deleted_at TEXT,
  UNIQUE(id, channel_id),
  UNIQUE(channel_id, sha256, kind),
  FOREIGN KEY (consent_id,channel_id) REFERENCES consents(id,channel_id)
);

-- 한 원본 -> 여러 편집본, 한 편집본 <- 여러 원본 모두 표현 가능.
-- 목적/형식이 다른 편집본의 keep 합집합을 자동 정답으로 만들지 않는다.
CREATE TABLE pairs (
  id TEXT PRIMARY KEY,
  channel_id TEXT NOT NULL REFERENCES channels(id),
  source_id TEXT NOT NULL,
  edit_id TEXT NOT NULL,
  task_json TEXT NOT NULL CHECK (json_valid(task_json)), -- 장르, 목표 길이, 의도, editor
  alignment_version TEXT NOT NULL,
  review_state TEXT NOT NULL DEFAULT 'pending' CHECK (review_state IN ('pending','partial','verified','rejected')),
  coverage_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(coverage_json)),
  UNIQUE(id,source_id),
  UNIQUE(source_id,edit_id,alignment_version),
  CHECK (source_id<>edit_id),
  FOREIGN KEY (source_id,channel_id) REFERENCES videos(id,channel_id),
  FOREIGN KEY (edit_id,channel_id) REFERENCES videos(id,channel_id)
);

-- edit 순서로 정렬. source 시각은 역행·반복 가능(재배치·리플레이).
-- audio/video track별로 J/L cut·b-roll을 표현. 결측은 unmatched이며 삭제가 아님.
CREATE TABLE alignment_spans (
  id TEXT PRIMARY KEY,
  pair_id TEXT NOT NULL REFERENCES pairs(id),
  track TEXT NOT NULL CHECK (track IN ('av','audio','video')),
  seq INTEGER NOT NULL CHECK (seq>=0),
  edit_start_ms INTEGER NOT NULL CHECK (edit_start_ms>=0),
  edit_end_ms INTEGER NOT NULL CHECK (edit_end_ms>edit_start_ms),
  source_start_ms INTEGER,
  source_end_ms INTEGER,
  status TEXT NOT NULL CHECK (status IN ('matched','unmatched','uncertain')),
  method TEXT NOT NULL,
  confidence REAL NOT NULL CHECK (confidence BETWEEN 0 AND 1),
  verified_by TEXT,
  residual_ms REAL CHECK (residual_ms IS NULL OR residual_ms>=0),
  UNIQUE(pair_id,track,seq),
  CHECK ((source_start_ms IS NULL AND source_end_ms IS NULL) OR
         (source_start_ms IS NOT NULL AND source_end_ms IS NOT NULL AND
          source_start_ms>=0 AND source_end_ms>source_start_ms)),
  CHECK (status<>'matched' OR source_start_ms IS NOT NULL),
  CHECK (status<>'unmatched' OR source_start_ms IS NULL)
);
CREATE INDEX alignment_edit_time ON alignment_spans(pair_id,edit_start_ms);

-- canonical source time. 고정 창/발화 구간은 segmenter_version으로 구별.
-- features: words[{start_ms,end_ms,text}], audio_events, chat_rate, missingness,
-- content_type, detector/model revisions, embedding(model+dimension+values).
-- 작은 데이터는 JSON과 전체 cosine 검색으로 시작. 결측을 0으로 저장하지 않음.
CREATE TABLE segments (
  id TEXT PRIMARY KEY,
  video_id TEXT NOT NULL REFERENCES videos(id),
  start_ms INTEGER NOT NULL CHECK (start_ms>=0),
  end_ms INTEGER NOT NULL CHECK (end_ms>start_ms),
  segmenter_version TEXT NOT NULL,
  transcript TEXT,
  speaker_alias TEXT,
  features_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(features_json)),
  feature_version TEXT NOT NULL,
  UNIQUE(id,video_id),
  UNIQUE(video_id,start_ms,end_ms,segmenter_version,feature_version)
);
CREATE INDEX segments_time ON segments(video_id,start_ms);

CREATE TABLE style_profiles (
  id TEXT PRIMARY KEY,
  channel_id TEXT NOT NULL REFERENCES channels(id),
  genre TEXT NOT NULL,
  output_format TEXT NOT NULL,
  version INTEGER NOT NULL CHECK (version>0),
  base_version TEXT NOT NULL,
  feature_version TEXT NOT NULL,
  independent_sources INTEGER NOT NULL CHECK (independent_sources>=0),
  delta_cap REAL NOT NULL DEFAULT 0.10 CHECK (delta_cap BETWEEN 0 AND 0.12),
  shrinkage REAL NOT NULL DEFAULT 0 CHECK (shrinkage BETWEEN 0 AND 1),
  parameters_json TEXT NOT NULL CHECK (json_valid(parameters_json)),
  targets_json TEXT NOT NULL CHECK (json_valid(targets_json)),
  training_manifest_json TEXT NOT NULL CHECK (json_valid(training_manifest_json)),
  -- manifest: source_groups, pair/label/consent IDs, snapshot hashes, train split,
  -- feature revisions, masks, hyperparameters, seed, excluded synthetic data.
  validation_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(validation_json)),
  state TEXT NOT NULL CHECK (state IN ('draft','validated','insufficient')),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  UNIQUE(id,channel_id),
  UNIQUE(channel_id,genre,output_format,version)
);
CREATE TRIGGER profile_no_update BEFORE UPDATE ON style_profiles
BEGIN SELECT RAISE(ABORT,'Create a new immutable profile version'); END;

CREATE TABLE edit_sessions (
  id TEXT PRIMARY KEY,
  channel_id TEXT NOT NULL REFERENCES channels(id),
  source_id TEXT NOT NULL,
  profile_id TEXT,
  base_version TEXT NOT NULL,
  task_json TEXT NOT NULL CHECK (json_valid(task_json)),
  agent_version TEXT NOT NULL,
  prompt_hash TEXT NOT NULL,
  current_revision INTEGER NOT NULL DEFAULT 0 CHECK (current_revision>=0),
  state TEXT NOT NULL CHECK (state IN ('open','review','closed','failed')),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  UNIQUE(id,source_id),
  FOREIGN KEY (source_id,channel_id) REFERENCES videos(id,channel_id),
  FOREIGN KEY (profile_id,channel_id) REFERENCES style_profiles(id,channel_id)
);

-- 초기 MVP session은 단일 원본. 다중 원본은 후속 session_sources로 확장.
-- timeline clips에 stable clip_id, source bounds, edit bounds, rate, track,
-- effects와 source refs를 저장. 단순 파일 diff로 학습하지 않음.
CREATE TABLE timeline_versions (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES edit_sessions(id),
  revision INTEGER NOT NULL CHECK (revision>=0),
  parent_id TEXT,
  timeline_json TEXT NOT NULL CHECK (json_valid(timeline_json)),
  timeline_sha256 TEXT NOT NULL,
  scores_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(scores_json)),
  origin TEXT NOT NULL CHECK (origin IN ('base','agent','human','revert','synthetic')),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  UNIQUE(id,session_id),
  UNIQUE(session_id,revision),
  FOREIGN KEY (parent_id,session_id) REFERENCES timeline_versions(id,session_id)
);
CREATE TRIGGER timeline_no_update BEFORE UPDATE ON timeline_versions
BEGIN SELECT RAISE(ABORT,'Append a timeline revision'); END;

-- accept는 무조건 keep이 아님. before/after의 동작과 시각으로 해석한다.
-- 선택하지 않음/미리보기/자동 저장은 implicit; human 정답으로 쓰지 않는다.
CREATE TABLE feedback_events (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES edit_sessions(id),
  before_timeline_id TEXT NOT NULL,
  after_timeline_id TEXT,
  event_type TEXT NOT NULL CHECK (event_type IN ('accept','reject','revert','adjust_boundary','prefer_a','prefer_b','tie','skip')),
  provenance TEXT NOT NULL CHECK (provenance IN ('human_explicit','implicit','oracle','synthetic')),
  actor_alias TEXT NOT NULL,
  reason TEXT,
  reason_scope TEXT CHECK (reason_scope IN ('content','pacing','boundary','effect','style','other')),
  payload_json TEXT NOT NULL CHECK (json_valid(payload_json)), -- A/B IDs, affected clip IDs, displayed context
  reverses_event_id TEXT REFERENCES feedback_events(id),
  request_key TEXT NOT NULL,
  expected_revision INTEGER NOT NULL CHECK (expected_revision>=0),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  UNIQUE(session_id,request_key),
  FOREIGN KEY (before_timeline_id,session_id) REFERENCES timeline_versions(id,session_id),
  FOREIGN KEY (after_timeline_id,session_id) REFERENCES timeline_versions(id,session_id)
);
CREATE TRIGGER feedback_no_update BEFORE UPDATE ON feedback_events
BEGIN SELECT RAISE(ABORT,'Append correction/revert event'); END;

-- 근거 종류를 분리. 편집본 미채택(unselected)은 가치 없음(drop)의 확정이 아님.
-- segment 전체의 거친 이진화를 피하고 keep_fraction과 대상 범위를 보존.
CREATE TABLE labels (
  id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL REFERENCES videos(id),
  segment_id TEXT,
  pair_id TEXT,
  feedback_id TEXT REFERENCES feedback_events(id),
  start_ms INTEGER NOT NULL CHECK (start_ms>=0),
  end_ms INTEGER NOT NULL CHECK (end_ms>start_ms),
  decision TEXT NOT NULL CHECK (decision IN ('keep','drop','unselected','unknown')),
  keep_fraction REAL CHECK (keep_fraction BETWEEN 0 AND 1),
  provenance TEXT NOT NULL CHECK (provenance IN ('alignment','human','llm','oracle','synthetic')),
  reason TEXT,
  reason_author TEXT CHECK (reason_author IN ('editor','annotator','model','unknown')),
  confidence REAL NOT NULL CHECK (confidence BETWEEN 0 AND 1),
  weight REAL NOT NULL DEFAULT 1 CHECK (weight BETWEEN 0 AND 1),
  supersedes_id TEXT REFERENCES labels(id),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  FOREIGN KEY (segment_id,source_id) REFERENCES segments(id,video_id),
  FOREIGN KEY (pair_id,source_id) REFERENCES pairs(id,source_id),
  CHECK (provenance<>'alignment' OR pair_id IS NOT NULL),
  CHECK (provenance<>'human' OR feedback_id IS NOT NULL)
);
CREATE INDEX labels_source ON labels(source_id,pair_id,start_ms);
CREATE TRIGGER labels_no_update BEFORE UPDATE ON labels
BEGIN SELECT RAISE(ABORT,'Append a superseding label'); END;

CREATE TABLE profile_evidence (
  profile_id TEXT NOT NULL REFERENCES style_profiles(id),
  rule_key TEXT NOT NULL,
  label_id TEXT NOT NULL REFERENCES labels(id),
  relation TEXT NOT NULL CHECK (relation IN ('supports','counterexample')),
  PRIMARY KEY(profile_id,rule_key,label_id)
);

CREATE TABLE evaluation_runs (
  id TEXT PRIMARY KEY,
  protocol_version TEXT NOT NULL,
  dataset_manifest_json TEXT NOT NULL CHECK (json_valid(dataset_manifest_json)),
  split_manifest_json TEXT NOT NULL CHECK (json_valid(split_manifest_json)),
  config_json TEXT NOT NULL CHECK (json_valid(config_json)),
  results_json TEXT NOT NULL CHECK (json_valid(results_json)),
  -- per-source metrics, baseline/profile IDs, masks, seeds, length budgets,
  -- source-cluster CIs, A/B assignments. N/A is NULL + reason, never fake zero.
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

-- 앱 트랜잭션 필수 검증 (DDL만으로 보장하지 않는 것):
-- 1. pairs source.kind=source/edit.kind=edited; 세션 원본 kind=source.
-- 2. 모든 범위<=영상길이; matched map의duration ratio, track 중복 검수.
-- 3. 프로필 channel/genre/format/base/feature 버전 일치, 권리 유효성.
-- 4. label source와feedback session.source 일치; supersedes/reverts 소속 일치,
--    순환 금지; profile_evidence 채널/학습split 일치; 철회 전파.
-- 5. JSON Schema 검증(words/events의 시각·결측·버전, timeline 참조/속도/길이).
-- 6. BEGIN IMMEDIATE -> expected_revision 비교 -> feedback/label/timeline append
--    -> current_revision 증가 -> COMMIT. request_key 재시도는 동일payload만 허용.
-- 7. profile updater는 새 버전만 생성; held-out source는 학습 manifest에서 제외.
-- 8. 삭제는 별도 권한 경로. 의존행을 자식부터 제거하고 cache/style.md도 폐기.
--    append-only는 정상 사용의 원칙이며 동의 철회/개인정보 삭제를 차단하지 않는다.
COMMIT;
