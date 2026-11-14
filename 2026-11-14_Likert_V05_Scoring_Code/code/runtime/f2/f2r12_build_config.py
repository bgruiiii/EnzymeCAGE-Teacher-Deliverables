"""Build R1 SCORING_RUN_CONFIG.json (draft; supersedes R0 draft for the
repaired tool chain — R0 file itself stays untouched in the R0 directory).

R1 deltas (audit-driven):
  - wire_protocol section: stream=true SSE receiver (ported from the
    production-proven collector) with full raw-wire preservation; the
    non-stream path exists and is tested but the frozen choice is stream=true.
  - output contract delivery: full RATING_OUTPUT_SCHEMA_R1 JSON embedded
    verbatim in the system prompt; response_format stays json_object
    (json_schema support has no exact-ID local evidence — not guessed).
  - evidence binding: F3_E0_PACKAGE structure with the REAL F3 R0 package
    identity measured now; final binding PENDING_F3_R1 (version-gated rebind
    when the F3 R1 window delivers its manifest).
  - prices: live runs read them ONLY from this confirmed config
    (cost.price_status must read CONFIRMED_BY_USER_… for the live gate to
    accept them; CLI overrides removed from the runner).

Offline: no network, no model API, no paid endpoint probing.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2r12_common import (R, F2_DIR, sha256_file, atomic_write_json, utc_now_iso,
                         MASTER_CONTRACT_SHA, TEACHER_REPLY_SHA,
                         F0_INPUT_BASELINE_MANIFEST_SHA, RUBRIC_RATER_CLEAN_DOCX_SHA,
                         RUBRIC_RATER_CLEAN_TEXT_SHA, SCOPE120_SHA, B480_INDEX_SHA)

R0_DIR = R / "LIKERT_V04_FULL_SCORING_20261029" / "F2_SCORER_BUILD"
R11_PREV_DIR = R / "LIKERT_V04_FULL_SCORING_20261029" / "F2_SCORER_BUILD_R1_1"
R12_PREV_DIR = R / "LIKERT_V04_FULL_SCORING_20261029" / "F2_SCORER_BUILD_R1_2"
R1_DIR = F2_DIR
AUDIT_DIR = R / "04_Local_Review_Audits" / "LIKERT_V04_FULL_SCORING_20261029" / "F0_INPUT_BASELINE_INDEPENDENT_AUDIT"
F123_AUDIT = R / "04_Local_Review_Audits" / "LIKERT_V04_FULL_SCORING_20261029" / "F1_F2_F3_INDEPENDENT_AUDIT"
REAUDIT = R / "04_Local_Review_Audits" / "LIKERT_V04_FULL_SCORING_20261029" / "F2_R1_INDEPENDENT_REAUDIT"
F3_DIR = R / "LIKERT_V04_FULL_SCORING_20261029" / "F3_EVIDENCE"
F3R11_DIR = R / "LIKERT_V04_FULL_SCORING_20261029" / "F3_EVIDENCE_R1_1"
G25 = R / "25_BIOSYSMODB_TEACHER_ALIGNED_EXECUTION_2026-09-26"

F3R11_MANIFEST_SHA = "7e54df82ea49a54916ad523bea924b82d44576691d2ad35448947ae6021af95e"
F3R11_CASE_MANIFEST_SHA = "1615849e26361ba1b274aa33025382688116c7d184c189880725a2416cef327d"


def main() -> int:
    system_prompt_sha = sha256_file(R1_DIR / "SCORING_SYSTEM_PROMPT.txt")
    template_sha = sha256_file(R1_DIR / "ITEM_MESSAGE_TEMPLATE.txt")
    schema_sha = sha256_file(R1_DIR / "RATING_OUTPUT_SCHEMA.json")
    f3r11_manifest_sha = sha256_file(F3R11_DIR / "EVIDENCE_MANIFEST_R1_1.json")
    if f3r11_manifest_sha != F3R11_MANIFEST_SHA:
        print(f"FATAL: F3 R1.1 manifest sha drift: {f3r11_manifest_sha}")
        return 1

    cfg = {
        "config_id": "SCORING_RUN_CONFIG_R1_2_1",
        "task": "F2_R1_2_1",
        "period": "LIKERT_V04_FULL_SCORING_20261029_R0",
        "generated_utc": utc_now_iso(),
        "config_status": "DRAFT_PENDING_USER_CONFIRMATION",
        "supersedes": {
            "r1_1_config": str(R11_PREV_DIR / "SCORING_RUN_CONFIG.json"),
            "r1_1_config_sha256": sha256_file(R11_PREV_DIR / "SCORING_RUN_CONFIG.json"),
            "note": "R0/R1/R1.1草案文件保持只读不改；本R1.2草案为现行草案（仅恢复代码修复；科学prompt/template/schema与R1.1逐字节相同；F3 R1.1绑定不变）"},
        "repair_authority": {
            "r1_2_1_hotfix_card": "LOCAL_AI_LIKERT_V04_F2_R1_2_1_ARCHIVE_IDENTITY_GATE_HOTFIX_EXECUTOR_ONLY_20261030.md",
            "r1_2_1_hotfix_card_sha256": sha256_file(R / "07_HPC_Prompts" / "LOCAL_AI_LIKERT_V04_F2_R1_2_1_ARCHIVE_IDENTITY_GATE_HOTFIX_EXECUTOR_ONLY_20261030.md"),
            "r1_2_recovery_reaudit_report_sha256": sha256_file(R / "04_Local_Review_Audits" / "LIKERT_V04_FULL_SCORING_20261029" / "F2_R1_2_INDEPENDENT_RECOVERY_REAUDIT_20261030" / "F2_R1_2_INDEPENDENT_RECOVERY_REAUDIT_REPORT.md"),
            "finding_addressed": "归档运行身份七键比较的continue层级错误（唯一阻塞项）；修复=整体候选门any()→外层continue,缺失即拒绝,不补值不冒充匹配",
            "carried_forward": "R1.2两项恢复修复+R1.1全部已修项+科学三文件与F3 R1.1绑定字节不变",
        },
        "gate_rule": ("F4/任何实际调用前：本文件所有PENDING_*字段必须由用户逐项确认填实并冻结"
                      "（产生USER_CONFIRMED_FROZEN版本+用户确认记录文件），f2r11_request_builder对任何"
                      "PENDING_*/null必填字段拒绝构建请求；live价格只从确认后的cost.price_basis读取"
                      "（price_status必须以CONFIRMED_BY_USER开头），CLI不得绕过"),

        "scoring_ai": {
            "recommended": {
                "provider": "aliyun_bailian_dashscope_openai_compatible",
                "endpoint": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                "endpoint_evidence": "24_/config/models.collection_v2.json（484次实际采集同一网关）+ BAILIAN_FIVE_MODEL_ENDPOINT_AND_MODEL_ID_PREFLIGHT_2026-09-24.md",
                "exact_model_id": "deepseek-v4-pro-0813",
                "model_id_verification": "2026-09-24预检逐字核实；exact-ID官方文档快照S27在25_/model_parameter_doc_audit/raw_sources/",
                "revision_snapshot": "-0813即快照ID；服务端无更深revision锁→逐次记录响应model并比对，漂移即停（FAILED_MODEL_DRIFT已实现并测试）",
                "server_snapshot_lockable": False,
                "status": "PENDING_USER_CONFIRMATION"
            },
            "alternative": {
                "provider": "PENDING_USER_SUPPLY（家族外裁判：Claude或Gemini类）",
                "endpoint": "PENDING_USER_SUPPLY",
                "exact_model_id": "PENDING_USER_SUPPLY",
                "reason_missing": "本地零网络边界内无该家族endpoint/model_id/价格证据；不猜填、不联网探测",
                "scientific_advantage": "与被测四家族及历史评分谱系零重叠",
                "status": "PENDING_USER_SUPPLY_MISSING_ITEMS_LISTED_IN_COST_AND_CALL_PLAN_R1"
            },
            "selection_basis": "与R0一致（谱系独立/同家族风险最小化/容量/结构化输出/价格本地在案）；R1未做也不得做按分数选裁判的实验；详见COST_AND_CALL_PLAN_R1.md",
            "rater_lineage_isolation": "qwen3.8-flash(A)/qwen3.8-max(C)/GLM-5.3(D)历史谱系之外（2026-10-14澄清记录核对）",
            "no_silent_switch": "响应model逐次比对冻结model_id；不一致=FAILED_MODEL_DRIFT+停run（T26实证）"
        },

        "wire_protocol": {
            "stream": True,
            "receiver": "SSE接收器移植自已验证生产采集器24_/scripts/run_collection_v2.py（484次真实调用）：data:前缀/[DONE]终止符/逐chunk吸收content与reasoning_content分离/usage尾帧verbatim/finish_reason/chunk解析错误计数不致命/stream_status=COMPLETE仅当见到终止标记且无读错误",
            "raw_byte_fidelity_r1_1": "P2-01修复：流式接收改用iter_content累积实际到达字节（CRLF逐字节保留,不再按行重组）；SSE解析在原始字节副本上进行；读中断错误只写meta（read_error字段）,绝不把本地注释注入provider原始响应；错误体限长64KB时显式raw_truncated=true+raw_full_length,不冒称完整wire",
            "connection_loss_accounting_r1_1": "P1-03修复：session.post进入后的任何异常（ConnectionError/RemoteDisconnected/ChunkedEncoding/Timeout等）一律may_have_billed=true→UNKNOWN_INFLIGHT保留预留；仅可证明派发前构造错误（InvalidURL/MissingSchema等PRE_DISPATCH白名单）才释放；不因'不是Timeout'假设未计费",
            "model_identity_policy_r1_1": "P2-02修复：provider未返回model字段→model_returned=null+model_identity=NOT_PROVIDED_BY_PROVIDER,规范记录model_identity_verification=NOT_PROVIDED_BY_PROVIDER；绝不用requested model补填actual；漂移=DRIFT+停run；F4首批通路检查必须观察真实provider字段行为并冻结披露政策,不谎称身份已核实",
            "non_stream_path": "已实现并离线测试（fake HTTP），但冻结选择stream=true与网关历史行为一致；改非流式=配置实质变化需重新确认",
            "raw_preservation": "每次传输归档：request_body.json原字节（Authorization永不落盘）+response_raw.bin完整SSE流或JSON envelope原字节+response_meta.json（http状态/安全header白名单/provider请求id/UTC/usage/model/finish_reason/stream_status/read_error/raw_truncated/派生content sha）；解析内容是派生层，哈希不替代原始通信",
            "safe_headers_allowlist": ["content-type", "x-request-id", "retry-after", "date", "server", "x-ratelimit-*"],
            "tested_offline": "假HTTP对象实际驱动LiveTransport.send：SSE分块/usage尾帧/缺帧截断/读中断/非JSON/缺model/429/5xx/401/非流式/finish_reason/CRLF字节保真/上传后断连保守计费（tests实测）"
        },

        "model_parameters": {
            "temperature": {"value": 0, "status": "PENDING_USER_CONFIRMATION",
                            "basis": "评分确定性；历史采集同值"},
            "top_p": {"value": "OMIT", "basis": "temperature=0已定；显式OMIT（合同§7.2）"},
            "enable_thinking": {"value": True, "status": "PENDING_USER_CONFIRMATION",
                                "basis": "exact-ID证据CONFIRMED（24_ config m3）"},
            "reasoning_effort": {"value": "OMIT", "status": "PENDING_USER_CONFIRMATION",
                                 "basis": "仅low有exact-ID证据；默认行为无官方文档→OMIT用服务默认"},
            "response_format": {"value": {"type": "json_object"}, "status": "PENDING_USER_CONFIRMATION",
                                "basis": "S27/S05支持；提示词含JSON字样；完整schema已逐字入系统提示（R1修复）；json_schema无exact-ID证据不使用"},
            "max_tokens": {"value": 65536, "status": "PENDING_USER_CONFIRMATION",
                           "basis": "评分JSON可见~4-8K+思维链；<<393216共享上限"},
            "max_input_tokens_bound": {"value": 400000, "status": "PENDING_RE_MEASURE_WITH_REAL_E0",
                                       "basis": "R0按60KB证据占位实测max≈303K；R1以真实E0切片复算（COST_AND_CALL_PLAN_R1），超界拒绝派发不截断"},
            "stream": {"value": True, "basis": "wire_protocol冻结选择"},
            "stream_options": {"value": {"include_usage": True}},
            "enable_search": {"value": False, "basis": "量表四.6/P74统一冻结证据快照"},
            "context_window_tokens": {"value": 1000000, "evidence": "exact_model_parameter_matrix.tsv EXACT_ID_OFFICIAL S27"},
            "full_question_answer_fits": "系统提示98,005B（rubric全文+schema全文逐字内嵌）+题面+答案max 35,578B+gold切片max 724KB+真实E0切片（逐case实测）；复算见COST_AND_CALL_PLAN_R1"
        },

        "content_identity": {
            "master_contract_sha256": MASTER_CONTRACT_SHA,
            "teacher_reply_sha256": TEACHER_REPLY_SHA,
            "f0_input_baseline_manifest_sha256": F0_INPUT_BASELINE_MANIFEST_SHA,
            "f0_erratum_id": "F0_SCOPE_GENERATOR_IDENTITY_ERRATUM_20261029",
            "rubric_word_sha256_period_basis": RUBRIC_RATER_CLEAN_DOCX_SHA,
            "rubric_text_extract_sha256": RUBRIC_RATER_CLEAN_TEXT_SHA,
            "scope120_sha256": SCOPE120_SHA,
            "b480_answer_index_sha256": B480_INDEX_SHA,
            "gold_label": "G1_gold_identity_corrected_20261026",
            "gold_manifest_sha256": "30257bde8f76f0afbafcbb84c9b0bd58ae1fcd19e73f0c7b5ee01f3a947f9d58",
            "cg_predefinition_sha256": "c4558b47776ce750a133fe23ec566561c493aa764890d6b1751ff5ada9cd2095",
            "system_prompt_sha256": system_prompt_sha,
            "item_template_sha256": template_sha,
            "rating_schema_sha256": schema_sha,
            "rating_schema_id": "LIKERT_V04_AI_RATING_OUTPUT_SCHEMA_R1",
            "evidence_snapshot_sha256": f3r11_manifest_sha,
            "evidence_snapshot_note": "=已审F3 R1.1包EVIDENCE_MANIFEST_R1_1实测SHA（窄修卡§2指定值一致）；E1补证层另立版本",
            "evidence_binding": {
                "mode": "F3_R11_CASE_SLICES_V2",
                "interface_contract": "F3_EVIDENCE_R1_1/F3_TO_F2_INTERFACE.md（f3r11_case_slice_v2，权威）+ E0_INTERFACE_CONTRACT_R1_1.md（F2消费侧实现说明）",
                "bound_package": {
                    "manifest_path": str(F3R11_DIR / "EVIDENCE_MANIFEST_R1_1.json"),
                    "manifest_sha256": f3r11_manifest_sha,
                    "case_evidence_manifest_sha256": sha256_file(F3R11_DIR / "CASE_EVIDENCE_MANIFEST.json"),
                    "evidence_baseline_id": "E0R11_20261029_SAME_FACTS_AS_R1",
                    "schema_version": "f3r11_case_slice_v2",
                    "baseline_reading_note": "已审父manifest顶层无baseline字段：baseline/schema身份从已绑定CASE_EVIDENCE_MANIFEST读取（值必须=E0R11_20261029_SAME_FACTS_AS_R1/f3r11_case_slice_v2），并在每个切片内复验一致；不回写F3、不硬塞旧字段兼容",
                    "adapter_verification": "见tests/E0_ACCEPTANCE_RESULTS_R1_1.json（120题×4真实装配、F7全文入body.messages、725关联、007四槽共享EC 3.3.2.10、47题显式GAP、篡改/错槽/未知schema拒绝）"
                },
                "superseded_bindings": {
                    "f3_r1_v1": {"manifest_sha256": "76c87f16db153a9eae8c755c05c13f3f672bc3e4b96f5346bebb6b501bba12a9",
                                 "reason": "复审F2R1-P1-01：725关联遗漏/F7全空，不能用于正式评分；仅作legacy回归"},
                    "f3_r0": {"manifest_sha256": "66955d0a581886d01af82de42a2897adda3a63a83ed869422e16b6e365515edc",
                              "reason": "开发期接口验证用legacy"}
                },
                "status": "BOUND_F3_R1_1_AUDITED_PENDING_USER_CONFIRMATION",
                "no_silent_fallback": "生产构建只接受F3_R11_CASE_SLICES_V2；v1/R0/夹具在生产模式一律拒绝（item builder硬门,已测）"
            },
            "code_dependency_lock": {
                "python": "3.10.12", "jsonschema": "3.2.0（draft-07）",
                "requests": "仅LiveTransport无注入session时import（live门内）；R1全程未调用",
                "lock_file": "F4运行前pip freeze > logs/ENV_LOCK_F4.txt并绑定SHA"
            }
        },

        "cost": {
            "currency": "CNY",
            "price_basis": {
                "source": "25_/model_parameter_doc_audit/pricing_matrix.tsv row deepseek-v4-pro-0813",
                "evidence_date": "lastModifiedTime 2026-09-20（派发前必须复核漂移）",
                "input_busy_cny_per_1M": 9, "input_idle_cny_per_1M": 4.5,
                "output_busy_cny_per_1M": 27, "output_idle_cny_per_1M": 13.5,
                "busy_window": "北京时间8:00-22:00",
                "reasoning_billing": "思维链+回答按输出计（S06列头口径）；reasoning含于completion只计一次",
                "cached_input": "闲时0.4（exact）；忙时UNKNOWN→预算按无缓存保守计",
                "drift_rule": "价格证据>2周：派发前用户复核；任一单价变化=漂移→暂停重新批准"
            },
            "price_status": "PENDING_USER_RE_VERIFICATION（确认时改为CONFIRMED_BY_USER_<日期>，live门只接受CONFIRMED_BY_USER前缀）",
            "estimates_cny": {
                "basis": "R1以真实E0切片+完整schema入prompt复算：见COST_AND_CALL_PLAN_R1.md（logs/ITEM_SIZE_MEASUREMENTS_R1.json逐槽实测）",
                "per_call_worst_case_reservation_busy": "PENDING_FINAL_AFTER_R1_MEASUREMENT（复算后填入；预留=实测装配tokens×输入价+max_tokens×输出价）",
                "expected_mean_total_480": "PENDING_USER_CONFIRMATION",
                "worst_case_total_incl_retries_960": "PENDING_USER_CONFIRMATION",
                "hard_cap_total_cny": "PENDING_USER_CONFIRMATION（不写虚假0元）",
                "smoke_sub_budget_cny": "PENDING_USER_CONFIRMATION（首批8份=480中的前8）",
                "unknown_charge_policy": "usage缺失/超时/在途→预留转unknown保留计账不清零；结算优先按传输结果（usage优先），评分JSON有效性不参与计费判定（R1修复）"
            },
            "accounting": "已花/在途预留/未知扣费三分栏+按槽持久尝试计数；projected>硬上限拒绝新派发；实际usage超预留→按实际入账并记OVER_RESERVE事件（启发式估算不冒称严格上界，停机机制=硬上限）"
        },

        "scheduling": {
            "unique_targets": 480,
            "max_concurrency": {"value": 2, "status": "PENDING_USER_CONFIRMATION",
                                "basis": "合同§7.2本地建议默认"},
            "rate_limit": {"value": "并发即限流；网关QPM无exact-ID本地证据→PENDING_USER_VERIFY_AT_DISPATCH，429按冻结退避"},
            "per_request_timeout_seconds": {"value": 1800, "status": "PENDING_USER_CONFIRMATION"},
            "retry_policy": {
                "max_technical_retries_per_target": 1,
                "retryable_conditions": ["HTTP_429", "HTTP_5XX", "TIMEOUT", "READ_ERROR",
                                         "NO_TERMINAL_MARKER", "CHUNK_PARSE_ERRORS",
                                         "INVALID_JSON", "SCHEMA_VALIDATION_FAILURE",
                                         "NO_CONTENT_BLOCK"],
                "non_retryable": ["HTTP_401_403（停支路）", "MODEL_DRIFT（停run）",
                                  "BUDGET_STOP", "SLOT_QUOTA_PERSISTENT",
                                  "INPUT_IDENTITY_MISMATCH"],
                "backoff_seconds": {"RATE_LIMIT": 60, "SERVER_5XX": 30, "TIMEOUT": 30,
                                    "INVALID_JSON": 0, "SCHEMA_FAIL": 0},
                "retry_content_rule": "同字节请求+冻结中性技术附注；重试body增量→按新body尺寸重新预留（R1修复）；严禁内容提示",
                "slot_quota_persistence": "按槽尝试数持久化于账本；进程重启不重置'首次+1次'配额（R1修复）",
                "status": "PENDING_USER_CONFIRMATION"
            },
            "global_attempt_cap": {"value": 960, "basis": "480×2含smoke与未知尝试（合同§7.2本地建议默认）"},
            "batching": "首批2case×8份=固定顺序前8；后续每批10case=40份；批间checkpoint+身份漂移检查",
            "success_no_resample": "成功有效响应不因分数高低再抽（T24实证）"
        },

        "run_boundaries": {
            "sends_to_scoring_ai_only": "冻结题面+原答+gold切片+scope登记+E0证据切片（含EVIDENCE_GAP显式披露）；不发模型身份/程序分/历史分/排名/协调映射/其他模型答案",
            "never_calls_tested_models": True,
            "no_silent_provider_model_switch": True,
            "no_score_based_prompt_tuning": True,
            "network_scope": "live仅冻结endpoint；证据联网走F3查询卡独立账本",
            "api_key_handling": "环境变量注入（名待确认）；只查存在性；不读值/不打印/不落盘；不沿用旧密钥旧预算",
            "api_key_env_var_name": "PENDING_USER_CONFIRMATION（BEFORE注册表实测7个常见名均不存在）"
        },

        "evidence_branch": {
            "note": "证据联网查询属F3查询卡管辖；与模型账本隔离",
            "whitelist": "PENDING_F3_QUERY_CARD（合同§8.4默认已批来源）",
            "ledger_separation": True
        },

        "cache": {
            "implementation": "code/f2r12_cache_checkpoint.py",
            "key_components": ["b_slot_uid", "answer_sha256", "question_rendered_prompt_sha256",
                               "rubric_text_sha256", "system_prompt_sha256", "item_template_sha256",
                               "gold_slice_manifest_sha256", "scope_rows_sha256",
                               "evidence_snapshot_sha256", "evidence_case_slice_sha256(R1新增)",
                               "rating_schema_sha256", "model_config_canonical_sha256",
                               "run_config_version_sha256"],
            "read_revalidation": "命中前复核存储sha+按当前schema/ctx重校验；篡改→隔离文件+按miss处理（R1修复）",
            "cross_version_hit": "不可能：任何组件变化→key变化→miss"
        },

        "resume_and_identity": {
            "run_identity_binding": "runner初始化即绑定run/config/schema/prompt/template/F0 manifest/B480索引/证据身份至checkpoint；缺项或漂移→拒绝复用旧记录（IdentityDriftError），不得拿旧槽号返回OK（R1修复）",
            "checkpoint_lock": "事务锁（O_CREAT|O_EXCL单写入者）；并发提交不丢记录（实测2线程2槽均保留）",
            "startup_reconciliation": "重启时inflight残留→unknown_reserves+RECONCILED_AFTER_RESTART事件（可能已计费不清零）",
            "canonical_repair_r1_2": "启动二进制安全修复：半行/半UTF-8尾→原始字节保留为.truncated_tail_<utc>+整文件备份+修复日志,活动文件形成可解析前缀；完整末行缺换行→保留并规范化(不丢记录)；中段真实损坏→CORRUPT_RECORDS_QUARANTINE显式隔离,周围有效记录保留；projector对不可解析canonical硬拒绝(绝不警告后产0行),并核对checkpoint VALID槽集合一致性",
            "archive_first_recovery_r1_2": "原provider归档为第一恢复源：request body sha/wire sha/meta完整性/运行身份/条目身份/传输成功六重核验后,用当前解析器重放原始字节并按当前schema/ctx重校验；唯一合法结果→按原transfer_id幂等补cache/canonical/checkpoint,零新传输,账本幂等对账(已结算不重复计费,inflight按归档usage结算,unknown仅在可验证usage时迁移)；多份不同合法结果→隔离不选边；不完整/schema失败/身份不符归档不得强行恢复为成功；cache仅作派生加速且必须引用真实归档(无归档的cache条目不冒充传输"
        },

        "pending_user_confirmation_fields": [
            "scoring_ai.recommended.status（或改选alternative并补全缺件）",
            "model_parameters.temperature/enable_thinking/reasoning_effort/response_format/max_tokens/max_input_tokens_bound(按R1.1实测复核)",
            "cost.price_status（现价复核→CONFIRMED_BY_USER_<日期>）+ estimates_cny全部金额",
            "scheduling.max_concurrency/per_request_timeout_seconds/retry_policy/global_attempt_cap",
            "run_boundaries.api_key_env_var_name",
            "content_identity.evidence_binding.status（已审F3 R1.1包7e54df82…绑定,请用户对该绑定一并确认；E1到来另立版本）"
        ]
    }

    out = R1_DIR / "SCORING_RUN_CONFIG.json"
    atomic_write_json(out, cfg)
    print(f"written: {out}")
    print(f"config_sha256={sha256_file(out)}")
    print(f"system_prompt_sha256={system_prompt_sha}")
    print(f"item_template_sha256={template_sha}")
    print(f"rating_schema_sha256={schema_sha}")
    print(f"f3_r1_1_manifest_sha256={f3r11_manifest_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
