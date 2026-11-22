# 独立工具R4：接已有CURRENT95资产（2026-11-22）

接续 revision3_native_cpu_verified_20261121（原R3不改）。本目录在**不重训、不重提特征、不生成新资产**的前提下，把今天收尾卡指定的三个已审复用件接进独立工具，并对两个固定步骤做了真实GPU评分验证。

## 复用来源（字节同一，SHA见scripts/expected_identities.json与节点回执）
- `recovery_helpers.build_3b_index`（节点`PKG/scripts/`，sha 1a16d5f0…）
- `historical_a109/c95_asset_index_ext.C95AssetIndex`（节点`PKG/historical/a109/`，sha ad6a64b6…）
- `r3_gf_unified.bind_ctx`登记的merged配置/context/UID映射（r3_gf_unified sha 0f7a1009…=C2身份表consumer_source_identities；merged cfg `asset_repair_r3_20261101/output/materialize_{ctx}/cfg/c95_3b_merged_config.yaml`；runtime map `PKG/inputs/{ctx}/RUNTIME_SEQUENCE_PARENT.tsv`）

## 公共接口
- 新后端：`enzyme_cage_wrapper_native_c95`（config_examples/tool_config_chenyu_native_c95.json）
- 适配器：`tool/enzyme_host_tool/native_c95_assets.py`（薄、进程内；`_ViewWithValues`仅为已审overlay视图补上在线wrapper `_dataset` 需要的 `.values()` 只读探针，数据本体不变；不修改任何wrapper/depending/训练文件）
- 语义：`model.evaluate()`输出为每seed概率，五概率只平均一次；不再做sigmoid；排序沿用`(-score, uid)`；TopK仅显示前缀；冻结池顺序即batch顺序

## 真实验证（attempt_6_20261122T051601Z，本地副本native_results_20261122/）
- 同一把既有GPU锁（old_five_numeric_control_20261121/gpu.lock，非阻塞试取；两卡空闲、无外来计算进程才继续）
- CPU先验：7个模块/基类SHA、5个checkpoint SHA、pool表SHA、13/31候选身份与11/4归档raw逐字节对账；原生C95索引下S02=13/13、S03=31/31资产可用、反应无缺件
- 真实调用：**每步各一次**，S02 13候选全部评分、S03 31候选全部评分，typed缺项0；逐seed全trace与全部署分数落盘（先落RAW再断言）；结束复验源/权重/pool SHA相同；模型释放、GPU归1MiB
- 信息性对照：whole-step结果与C2 legacy_esm2_3b名次13/13、31/31一致，概率差≤1e-6（协议不同，不据此互推）

## 尝试账本
attempt1 驱动预建目录bug（锁未取，纯工程失败，FAIL留档）；attempt2/3 节点路径修正（SRC_SNAP、c95_dir）；attempt4 enzymecage包路径修正；attempt5 定位到`.values()`探针缺失（FORWARD_FAILED_TYPED，全候选typed保留，FAIL留档）；attempt6 成功。原R3、旧回包、审计、depending main未改；节点写入仅限`workspaces/current95_ngpu32g_20261031/tool_r4_s02_s03_20261122/`。

## 维护者接口摘要
- CLI：`python -m enzyme_host_tool --config tool_config_chenyu_native_c95.json …`（同R3）
- 配置三根不变 + `scoring.native_binding={"paths":{pkg,a109,c95_dir,wrap_pkg_root,rh_dir,enzymecage_source_root,merged_cfg{ctx},module_shas},"ctx":main|delta15}`
- 真缺口时先列任务清单再走T3B/蛋白工具既有入口（见ASSET_TOOLS交接页），性状重型预测保持独立按需，不进默认补资产分支
