"""Generate the F2-R1.2-derived F4 locked run card + identity in 07_HPC_Prompts.

New file LOCAL_AI_LIKERT_V04_F4_LOCKED_RUN_R1_2_20261030.md; R0/R1/R1.1
cards are NOT modified (repair card boundary: 旧卡不覆盖). All artifact
identities are recomputed at generation time from the actual R1.2 files.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2r12_common import (R, F2_DIR, sha256_file, atomic_write_text,
                          atomic_write_json, utc_now_iso, MASTER_CONTRACT_SHA,
                          TEACHER_REPLY_SHA, F0_INPUT_BASELINE_MANIFEST_SHA)

PROMPTS = R / "07_HPC_Prompts"
CARD_NAME = "LOCAL_AI_LIKERT_V04_F4_LOCKED_RUN_R1_2_1_20261030.md"
REAUDIT = R / "04_Local_Review_Audits" / "LIKERT_V04_FULL_SCORING_20261029" / "F2_R1_2_INDEPENDENT_RECOVERY_REAUDIT_20261030"
F3R11 = R / "LIKERT_V04_FULL_SCORING_20261029" / "F3_EVIDENCE_R1_1"
R0_DIR = R / "LIKERT_V04_FULL_SCORING_20261029" / "F2_SCORER_BUILD"
R11_DIR = R / "LIKERT_V04_FULL_SCORING_20261029" / "F2_SCORER_BUILD_R1_1"
R12_DIR_PREV = R / "LIKERT_V04_FULL_SCORING_20261029" / "F2_SCORER_BUILD_R1_2"

ARTIFACTS = [
    ("SCORING_SYSTEM_PROMPT.txt", F2_DIR / "SCORING_SYSTEM_PROMPT.txt"),
    ("ITEM_MESSAGE_TEMPLATE.txt", F2_DIR / "ITEM_MESSAGE_TEMPLATE.txt"),
    ("RATING_OUTPUT_SCHEMA.json", F2_DIR / "RATING_OUTPUT_SCHEMA.json"),
    ("SCORING_RUN_CONFIG.json(R1_2_1草案)", F2_DIR / "SCORING_RUN_CONFIG.json"),
    ("FIELD_DICTIONARY_R1_2.md(字段合同沿用,本轮零字段变更)", R12_DIR_PREV / "FIELD_DICTIONARY_R1_2.md"),
    ("RULE_TO_FIX_TEST_MATRIX_R1_2_1.tsv", F2_DIR / "RULE_TO_FIX_TEST_MATRIX_R1_2_1.tsv"),
    ("RULE_TO_FIX_TEST_MATRIX_R1_2.tsv(上轮沿用)", R12_DIR_PREV / "RULE_TO_FIX_TEST_MATRIX_R1_2.tsv"),
    ("RULE_TO_VALIDATOR_MATRIX.tsv(R0语义层沿用)", R0_DIR / "RULE_TO_VALIDATOR_MATRIX.tsv"),
    ("COST_AND_CALL_PLAN_R1_1.md(尺寸费用零漂移沿用)", R11_DIR / "COST_AND_CALL_PLAN_R1_1.md"),
    ("E0_INTERFACE_CONTRACT_R1_1.md(证据接口沿用)", R11_DIR / "E0_INTERFACE_CONTRACT_R1_1.md"),
    ("R1_2_1_INPUT_IDENTITY_REGISTRY_BEFORE.json", F2_DIR / "R1_2_1_INPUT_IDENTITY_REGISTRY_BEFORE.json"),
    ("code/f2r12_common.py", F2_DIR / "code" / "f2r12_common.py"),
    ("code/f2r12_evidence_adapter.py", F2_DIR / "code" / "f2r12_evidence_adapter.py"),
    ("code/f2r12_item_builder.py", F2_DIR / "code" / "f2r12_item_builder.py"),
    ("code/f2r12_gold_slicer.py", F2_DIR / "code" / "f2r12_gold_slicer.py"),
    ("code/f2r12_transport.py", F2_DIR / "code" / "f2r12_transport.py"),
    ("code/f2r12_request_builder.py", F2_DIR / "code" / "f2r12_request_builder.py"),
    ("code/f2r12_response_validator.py", F2_DIR / "code" / "f2r12_response_validator.py"),
    ("code/f2r12_budget_ledger.py", F2_DIR / "code" / "f2r12_budget_ledger.py"),
    ("code/f2r12_cache_checkpoint.py", F2_DIR / "code" / "f2r12_cache_checkpoint.py"),
    ("code/f2r12_scorer_runner.py", F2_DIR / "code" / "f2r12_scorer_runner.py"),
    ("code/f2r12_project_tables.py", F2_DIR / "code" / "f2r12_project_tables.py"),
    ("independent_validator/f2r12_independent_validator.py", F2_DIR / "independent_validator" / "f2r12_independent_validator.py"),
    ("tests/f2r12_regression_tests.py", F2_DIR / "tests" / "f2r12_regression_tests.py"),
    ("tests/f2r12_fix_tests.py", F2_DIR / "tests" / "f2r12_fix_tests.py"),
    ("tests/f2r12_closure_tests.py", F2_DIR / "tests" / "f2r12_closure_tests.py"),
    ("tests/f2r12_recovery_tests.py", F2_DIR / "tests" / "f2r12_recovery_tests.py"),
    ("tests/f2r12_identity_gate_tests.py", F2_DIR / "tests" / "f2r12_identity_gate_tests.py"),
    ("tests/f2r12_e0_acceptance.py", F2_DIR / "tests" / "f2r12_e0_acceptance.py"),
    ("tests/run_all_r12_tests.py", F2_DIR / "tests" / "run_all_r12_tests.py"),
    ("tests/TEST_RESULTS.json", F2_DIR / "tests" / "TEST_RESULTS.json"),
    ("tests/E0_ACCEPTANCE_RESULTS_R1_2_1.json", F2_DIR / "tests" / "E0_ACCEPTANCE_RESULTS_R1_2_1.json"),
    ("tests/fixtures/rating_factory.py", F2_DIR / "tests" / "fixtures" / "rating_factory.py"),
    ("tests/fixtures/synthetic_evidence_fixture.json", F2_DIR / "tests" / "fixtures" / "synthetic_evidence_fixture.json"),
    ("logs/ITEM_SIZE_MEASUREMENTS_R1_2_1.json", F2_DIR / "logs" / "ITEM_SIZE_MEASUREMENTS_R1_2_1.json"),
]


def main() -> int:
    rows = []
    for label, path in ARTIFACTS:
        if not os.path.exists(path):
            print(f"FATAL missing artifact: {path}")
            return 1
        rows.append((label, sha256_file(path), os.path.getsize(path)))
    table = "\n".join(f"| {l} | {s} | {b} |" for l, s, b in rows)
    d = {l: (s, b) for l, s, b in rows}
    cfg_sha = d["SCORING_RUN_CONFIG.json(R1_2_1草案)"][0]
    prompt_sha = d["SCORING_SYSTEM_PROMPT.txt"][0]
    schema_sha = d["RATING_OUTPUT_SCHEMA.json"][0]
    template_sha = d["ITEM_MESSAGE_TEMPLATE.txt"][0]
    tests = json.load(open(F2_DIR / "tests" / "TEST_RESULTS.json", encoding="utf-8"))
    f3r11_manifest_sha = sha256_file(F3R11 / "EVIDENCE_MANIFEST_R1_1.json")
    f3r11_case_manifest_sha = sha256_file(F3R11 / "CASE_EVIDENCE_MANIFEST.json")
    reaudit_sha = sha256_file(REAUDIT / "F2_R1_2_INDEPENDENT_RECOVERY_REAUDIT_REPORT.md")
    hotfix_card_sha = sha256_file(PROMPTS / "LOCAL_AI_LIKERT_V04_F2_R1_2_1_ARCHIVE_IDENTITY_GATE_HOTFIX_EXECUTOR_ONLY_20261030.md")
    r12_card_sha = sha256_file(PROMPTS / "LOCAL_AI_LIKERT_V04_F4_LOCKED_RUN_R1_2_20261030.md")
    ut = tests["unittest_totals"]

    card = f"""# F4锁定运行卡R1.2.1（F2 R1.2.1派生）：480份AI评分的配置冻结与分批执行

- 日期：2026-10-30。派生者：F2 R1.2.1身份门热修窗口（热修卡sha256={hotfix_card_sha}；
  R1.2恢复复审报告sha256={reaudit_sha}，结论RECOVERY_REPROS_CLOSED_ARCHIVE_IDENTITY_CONTROL_FLOW_REPAIR_REQUIRED）。
- 本卡**取代**R1.2卡（{r12_card_sha[:8]}…）、R1.1卡（014e9132…）、R1卡（54dd1a78…）、R0卡（34c1cade…）用于F4执行；四代旧卡与identity只读保留。
- R1.2.1修复范围=仅归档运行身份七键比较的候选门（复审§一唯一阻塞项：continue层级错误致身份不符归档被误恢复）；
  修复=七键整体布尔门any()→外层候选循环continue，缺失即拒绝、不补值、未知不冒充匹配；
  科学prompt/template/schema与R1.2/R1.1**逐字节相同**（0829ae54…/4534bda6…/c387ba77…注册表实测）；
  F3 R1.1证据绑定不变；R1.2两项恢复修复及其余全部已修项保留（211项unittest实证）；尺寸/费用复测零漂移。
- **本卡自身不解锁任何调用**（live_calls_authorized=false）。
- 上位合同：MASTER_CONTRACT…20261029.md（SHA256={MASTER_CONTRACT_SHA}）；老师批复（SHA256={TEACHER_REPLY_SHA}）。
- F0消费入口：INPUT_BASELINE_MANIFEST.json（SHA256={F0_INPUT_BASELINE_MANIFEST_SHA}，按F0勘误消费）。
- 证据绑定：**唯一活动包=已审F3 R1.1**（EVIDENCE_MANIFEST_R1_1.json sha256={f3r11_manifest_sha}；
  CASE_EVIDENCE_MANIFEST sha256={f3r11_case_manifest_sha}；baseline E0R11_20261029_SAME_FACTS_AS_R1；
  interface f3r11_case_slice_v2）。联合验收按卡§4.2在科学文本与绑定字节未变前提下重跑：J1–J7全PASS
  （480槽装配/四模型共享事实/725关联/F7入body/47 GAP/007 EC）。生产构建仅接受v2（无静默fallback）。

## 一、F2 R1.2冻结工件绑定（生成时实测重算，非手抄）

| 工件 | SHA256 | 字节 |
| --- | --- | --- |
{table}

离线测试实测（tests/TEST_RESULTS.json，分栏计数不合并冒充）：
unittest五套件={ut['ran']}项/{ut['passed']}通过/{ut['failed']}失败/{ut['errors']}错误
（回归103+R1修复与v2接口72+R1.1运行闭合14+R1.2恢复窗口13+**R1.2.1身份门9**：七键逐一变更/缺失14子例全拒、
跨配置复现B旧分不洗白、七键全匹配正例仍原7分/0新传输/费用恰0.0117一次、canonical/cache派生层不可绕过同一拒绝）；
联合验收节段={tests['joint_sections_passed']}；独立validator聚合复验={tests['independent_validator']['verdict']}（0 findings）。
NETWORK_ATTEMPTS=0；MODEL_API_ATTEMPTS=0。
运行中任何工件字节变化=输入漂移：立即停止，重跑battery并产生新run/version（合同§13）。

## 二、首次实际调用前置条件（全部满足才可live；缺一即BLOCKED_<原因>）

1. 用户逐项确认SCORING_RUN_CONFIG.json(R1.2)缺件清单（COST_AND_CALL_PLAN_R1_1.md§五，金额零漂移沿用：
   480预期mean≈693元/p90≈1,004元；预留合计1,335.2元；960包络2,670.5元；硬上限A=4,300/B=2,700推荐/C=1,400限额；smoke≤35.5元）：
   评分AI选择、现行单价复核（历史证据2026-09-20）、硬上限+smoke子预算、并发/超时/重试/960上限、参数细节、密钥变量名、F3 R1.1绑定确认。
2. 协调侧生成USER_CONFIRMED_FROZEN版config（零PENDING值字段，新config SHA；price_status=CONFIRMED_BY_USER_<日期>）。
3. 用户确认记录F4_USER_CONFIG_CONFIRMATION.json落盘（confirmed_by=USER、confirmed_config_sha256实测绑定、
   live_paid_calls_authorized=true、逐项批复引用）。
4. 证据绑定复核：F3 R1.1父/case manifest sha与本卡题头一致；E1或新版本→重绑+重跑联合验收+复算尺寸预算后再确认。
5. API密钥环境变量存在（只查名不读值；BEFORE注册表实测本shell 7个常见名均不存在）。
6. 依赖锁：pip freeze > logs/ENV_LOCK_F4.txt并登记SHA。
7. CLI显式旗标--i-confirm-live-paid-calls。
工具侧硬门：config_gate（状态+确认记录+零PENDING）、密钥存在、证据绑定非PENDING、旗标、LiveTransport构造复核；
live价格只从确认config读取（无CLI旁路）；wire=SSE流式（iter_content字节保真接收器）。

## 三、运行步骤（F4执行窗口）

1. **顺序固定（看任何AI分之前）**：case按random.Random(20261029)排序；每case四槽匿名次序固定；协调映射不入请求。
2. **条目构建**：f2r12_item_builder生产模式（--e0-manifest/--e0-manifest-sha绑定F3 R1.1+--production）；
   gold切片从只读gold生成到F4工作区；恢复槽自动密封tar内存提取三重校验；逐条登记实测装配tokens；超400,000上界拒绝。
3. **首批8份通路检查**（=480中的前8，非调参集），技术门=十字段身份回显全过/输出JSON合法且schema VALID/
   引用定位零伪造/总分状态联动/usage与成本入账（含无效JSON计费）/SSE wire归档字节级可回放（CRLF保真）/
   **恢复演练四题（R1.2/R1.2.1,全部离线实证过）**：
   ①归档重放——完整合法响应归档后cache/canonical前kill→重启零新传输、原transfer_id、原分数保留、费用恰一次；
   ②截断尾——canonical半行/半UTF-8尾→启动修复（证据文件保留）→恢复补齐→投影行数=checkpoint VALID槽数；
   ③在途对账——结算前kill→重启inflight→unknown→归档usage可验证迁移，不猜费用不重复计费；
   ④**身份门**——旧配置归档导入新配置运行根→拒绝恢复（不洗白旧分）；七键任一变更/缺失→拒绝；七键全匹配→正常恢复；
   以及model字段行为观察并冻结NOT_PROVIDED披露政策/账本-checkpoint-归档同transfer_id闭合。
   不以分数好看或接近旧分为放行标准（合同§9.4）。
4. **后续批次**：每批10case=40份；批前输入漂移检查（§一工件SHA复验）；批后checkpoint+RUN_REPORT增补
   （唯一完成数/失败未核复核队列/committed+inflight+unknown三栏/剩余额度/attempts与按槽配额/隔离区计数/修复日志计数）。
5. **停止条件**（自动）：401/403停支路；预算projected>硬上限停派发打partial return；模型漂移停run；
   连续5份schema失败暂停报告；真双结果→隔离该槽（FAILED_DUAL_RESULT_QUARANTINED）待人工复核,不选边不重付；
   中段canonical损坏→隔离行+人工复核,周围有效记录保留。
6. **产出**（合同§9.9）：RUN_REPORT.md、REQUEST_RESPONSE_INDEX.tsv、ATTEMPT_LEDGER.jsonl、CHECKPOINT.json、
   RATINGS_CANONICAL.jsonl（单一规范源）、RATINGS_480.tsv与RATING_DIMENSIONS_3360.tsv（投影带expected_committed_uids
   一致性门；480行均有状态；失败槽维度字段留空；MISSING=1参与总分三层同一合同）、REVIEW_QUEUE.tsv、
   QUARANTINE_DUAL_RESULTS.jsonl与CORRUPT_RECORDS_QUARANTINE.jsonl与CANONICAL_REPAIR_LOG.jsonl（如有）、逐批简报；
   收尾跑f2r12_independent_validator全量复验（I1–I12）。
7. 结构合法但论证存疑→REVIEW_QUEUE不改分；成功响应不因分高低再抽；013 CG04/CG10 UNRESOLVED路由裁决；
   B001 pending_external_review原样披露不自动判KE。

## 四、命令参考

```bash
cd R/LIKERT_V04_FULL_SCORING_20261029/F2_SCORER_BUILD_R1_2_1
python3 -B code/f2r12_scorer_runner.py --mode validate-config    # 配置门自检(草案必须CLOSED)
python3 -B tests/run_all_r12_tests.py                             # 211项unittest+联合验收+validator复跑
python3 -B tests/f2r12_e0_acceptance.py                           # F3 R1.1联合验收复跑
python3 -B code/f2r12_item_builder.py <b_slot_uid> <F4I-nnnn> <gold_slice_root> <out.json> \\
    --e0-manifest <F3_EVIDENCE_R1_1/EVIDENCE_MANIFEST_R1_1.json> --e0-manifest-sha <7e54df82…> --production
python3 -B independent_validator/f2r12_independent_validator.py <run_root> --price-in <确认价> --price-out <确认价> --projection-dir <proj>
# live（仅全部前置满足后，由F4执行窗口按用户派发运行）
python3 -B code/f2r12_scorer_runner.py --mode live --items-dir <dir> --run-root <F4工作区> --i-confirm-live-paid-calls
```

## 五、边界与禁止（沿总合同+三代修复卡，不重复全文）

- 只写F4_AI_RATINGS/（及获派简报位置）；F0/F1/F2五代目录/F3三代目录/审计目录与全部只读源不可修改。
- 不调用被测四模型；不联网查询证据（证据支路走F3查询卡独立账本）；不改提示词/schema/gold/规则追求"通过"。
- 不访问/打印密钥值；协调映射、被测模型身份、程序分、历史分数不进任何评分请求或人类包。
- 未经用户指令不上传GitHub、不代发老师消息；不重开评分标准/证据包/gold/F1程序分（R1.2卡§1）。

## 六、回包格式（每批与最终）

```text
TASK_ID=F4_BATCH_<n>
STATUS=PENDING_INDEPENDENT_REVIEW_OR_SPECIFIC_BLOCK
BATCH_UNIQUE_COMPLETED=<actual>/480累计
FAILED_NOT_RUN_UNKNOWN=<actual逐状态计数>
REVIEW_QUEUE_SIZE=<actual>
QUARANTINE_DUAL_RESULTS=<actual计数>
CANONICAL_REPAIR_EVENTS=<actual计数+证据文件清单>
LEDGER=committed:<x>元 inflight:<y>元 unknown:<z>元 cap:<确认值>元 attempts:<n>/960 slot_quota_events:<n>
WIRE_ARCHIVE=完整归档计数=<n> authorization_stored=false核验=<PASS> CRLF保真抽验=<PASS>
RECOVERY_DRILLS=<首批三题演练结果:归档重放/截断尾修复/在途对账>
INPUT_DRIFT_CHECK=<PASS/FAIL明细>
ARTIFACT_SHAS_VS_LOCKED_CARD_R1_2_1=<逐一比对结果>
INDEPENDENT_VALIDATOR=<PASS/findings(I1-I12)>
NEXT_ACTION=<继续下批(预授权)/停止待用户>
```
"""

    card_path = PROMPTS / CARD_NAME
    atomic_write_text(card_path, card)
    card_sha = sha256_file(card_path)
    card_bytes = os.path.getsize(card_path)

    identity = {
        "task_id": "F4_LOCKED_RUN_CARD_R1_2_1_DERIVED_BY_F2_R1_2_1",
        "derived_by": f"F2_R1_2_1 identity-gate hotfix (card {hotfix_card_sha[:16]}…; recovery reaudit {reaudit_sha[:16]}…)",
        "generated_utc": utc_now_iso(),
        "status": "DERIVED_PENDING_USER_CONFIGURATION_CONFIRMATION",
        "supersedes_for_execution": [
            "LOCAL_AI_LIKERT_V04_F4_LOCKED_RUN_R1_2_20261030.md (retained read-only)",
            "LOCAL_AI_LIKERT_V04_F4_LOCKED_RUN_R1_1_20261029.md (retained read-only)",
            "LOCAL_AI_LIKERT_V04_F4_LOCKED_RUN_R1_20261029.md (retained read-only)",
            "LOCAL_AI_LIKERT_V04_F4_LOCKED_RUN_20261029.md (retained read-only)"],
        "path": f"custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/07_HPC_Prompts/{CARD_NAME}",
        "bytes": card_bytes,
        "sha256": card_sha,
        "contract_sha256": MASTER_CONTRACT_SHA,
        "authority_sha256": TEACHER_REPLY_SHA,
        "f0_input_baseline_manifest_sha256": F0_INPUT_BASELINE_MANIFEST_SHA,
        "science_byte_identity_vs_r1_2_and_r1_1": {
            "SCORING_SYSTEM_PROMPT.txt": prompt_sha,
            "ITEM_MESSAGE_TEMPLATE.txt": template_sha,
            "RATING_OUTPUT_SCHEMA.json": schema_sha,
            "note": "三文件与R1.2/R1.1逐字节相同（注册表science_byte_identity实测True）；本轮零科学改动,仅恢复身份门候选逻辑"},
        "f3_r1_1_evidence_binding": {
            "manifest": str(F3R11 / "EVIDENCE_MANIFEST_R1_1.json"),
            "manifest_sha256": f3r11_manifest_sha,
            "case_evidence_manifest_sha256": f3r11_case_manifest_sha,
            "evidence_baseline_id": "E0R11_20261029_SAME_FACTS_AS_R1",
            "interface": "f3r11_case_slice_v2",
            "joint_acceptance": "PASS J1-J7 rerun (tests/E0_ACCEPTANCE_RESULTS_R1_2.json); binding bytes unchanged"},
        "bound_r1_2_1_artifacts": {l: {"sha256": s, "bytes": b} for l, s, b in rows},
        "config_r1_2_1_draft_sha256": cfg_sha,
        "system_prompt_sha256": prompt_sha,
        "item_template_sha256": template_sha,
        "rating_schema_sha256": schema_sha,
        "offline_battery": {
            "unittest_total": ut["ran"], "unittest_passed": ut["passed"],
            "unittest_failed": ut["failed"], "unittest_errors": ut["errors"],
            "suites": {k: v["ran"] for k, v in tests["unittest_suites"].items()},
            "identity_gate_hotfix": "seven-key whole-candidate gate; 14 mutation/omission negatives + cross-config repro B + positive control all pass",
            "joint_sections": tests["joint_sections_passed"],
            "independent_validator": tests["independent_validator"]["verdict"],
            "network_attempts": 0, "model_api_attempts": 0},
        "live_calls_authorized_by_this_navigation_card": False,
        "unlock_requirements": "本卡§二全部前置条件；核心=USER_CONFIRMED_FROZEN config+F4_USER_CONFIG_CONFIRMATION.json+F3 R1.1绑定复核+密钥存在+CLI旗标",
    }
    id_path = PROMPTS / (CARD_NAME + ".identity.json")
    atomic_write_json(id_path, identity)
    print(f"written: {card_path}\n  sha256={card_sha} bytes={card_bytes}")
    print(f"written: {id_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
