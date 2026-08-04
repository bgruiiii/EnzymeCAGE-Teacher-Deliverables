# M3 Q3 BioTransformer ENVMICRO 源码摘录与 jar 身份证据

日期：2026-08-04  
对应老师要求：`TEACHER_REPLY_M3_COMBINED_THREE_QUESTIONS_AND_NEXT_STEPS_2026-08-03.md` §9.4 / §9.5 F5  
状态：F5 证据补充稿

## 1. 本文件回答什么

老师要求补充：

```text
Q3 源码摘录 + jar 包身份证据（SHA256）
```

具体包括：

- 核查的 BioTransformer GitHub commit `7149f7ec...` 与 HPC 返回包工具身份一致；
- 提供 BioTransformer jar SHA256；
- 给出 `BiotransformerExecutable` / `EnvMicroBTransformer` / `ChemStructureExplorer` 各 5–10 行关键源码摘录，便于复核。

本文件只补充可复核证据，不新增 BioTransformer 评分、不新增运行、不改变 Q3 原结论。

## 2. HPC 返回包中的工具身份

使用的返回包：

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_p1_2_1_small_pollutant_strict_v0_1_biotransformer_envmicro_prediction_20260728.tar.gz
```

返回包外部 identity：

```text
archive_sha256=20e3827f68f9b0bc8290acc95fc89cd39ff63193ca4f55631355b265993120b9
bytes=29264
created_utc=2026-07-29T01:28:42Z
tool_id=biotransformer_envmicro
final_status=M3_P1_2_1_SMALL_POLLUTANT_BIOTRANSFORMER_NORMALIZED_PREDICTIONS_READY_FOR_LOCAL_AUDIT
```

返回包内 `metadata/BIOTRANSFORMER_SOURCE_IDENTITY.txt` 记录：

```text
repository=https://github.com/Wishartlab-openscience/Biotransformer.git
expected_commit=7149f7ec6b2f32f9f789bab53aa4a71db49e59e2
actual_commit=7149f7ec6b2f32f9f789bab53aa4a71db49e59e2
```

返回包内 `metadata/BIOTRANSFORMER_JAR_SHA256.txt` 记录：

```text
e5c3c27de7dfc87b448f1eed6fe986ef48ed90c53bad9b848f95378f08efee80  /tmp/enzymecage_m3_p1_2_1_three_tool_valid_single_parent_biotransformer_envmicro_prediction_rerun4_20260728/Biotransformer/target/biotransformer-3.0.0.jar
```

返回包内 `metadata/TOOL_RUN_METADATA.json` 还记录：

```text
tool_display_name=BioTransformer 3.0 ENVMICRO
tool_id=biotransformer_envmicro
tool_commit=7149f7ec6b2f32f9f789bab53aa4a71db49e59e2
jar_sha256=e5c3c27de7dfc87b448f1eed6fe986ef48ed90c53bad9b848f95378f08efee80
command_template=java -jar <jar> -k pred -b env -ismi <parent_smiles> -ocsv <case_output_csv> -s 1
operator_or_executor_note=no answer key read; no scoring performed
```

判定：HPC 返回包中记录的 BioTransformer commit 与本文件回源核查的 commit 一致；jar SHA256 已由返回包内 metadata 和 TOOL_RUN_METADATA 双重记录。

边界：这证明该 jar 在晨羽该返回包任务中被构建/执行并留下身份记录；不等于本轮新部署了一个持久生产服务。

## 3. 源码回源身份

回源仓库：

```text
https://github.com/Wishartlab-openscience/Biotransformer.git
```

回源 commit：

```text
7149f7ec6b2f32f9f789bab53aa4a71db49e59e2
```

本地只读核查结果：

```text
git rev-parse HEAD
7149f7ec6b2f32f9f789bab53aa4a71db49e59e2
```

源码路径注意：该 commit 中 `BiotransformerExecutable.java` 位于：

```text
src/main/java/executable/BiotransformerExecutable.java
```

不是 `src/main/java/biotransformer/commandline/`。

## 4. 关键源码摘录

### 4.1 `BiotransformerExecutable.java`：`-b env` 进入 ENVMICRO 执行路径

源码位置：

```text
src/main/java/executable/BiotransformerExecutable.java:957-965
```

摘录：

```java
else if (optionsToBtTypes.get(biotransformerType.toLowerCase()) == bType.ENV){
    EnvMicroBTransformer ebt = new EnvMicroBTransformer();
    
    if (singleInput !=null){
        number_of_molecules++;
        if(oFormat.contentEquals("csv")){

            ebt.simulateEnvMicrobialDegradationAndSaveToCSV(singleInput, true, true, nrOfSteps, scoreThreshold, outputF, annotate);
            successful_predictions++;
```

解释：命令行参数 `-b env` 对应 `bType.ENV`，单个输入分子时实例化 `EnvMicroBTransformer`，并走 `simulateEnvMicrobialDegradationAndSaveToCSV(...)`。

### 4.2 `EnvMicroBTransformer.java`：输入通过 PPS 检查后进入 ENVMICRO 反应链

源码位置：

```text
src/main/java/biotransformer/btransformers/EnvMicroBTransformer.java:196-207
```

摘录：

```java
if(ChemStructureExplorer.isPpsValid(target)){
    ArrayList<Biotransformation> biotransformations = new ArrayList<Biotransformation>();
    AtomContainerSet startingSet = new AtomContainerSet();
    startingSet.addAtomContainer(target);
    
    biotransformations = metabolizeWithEnzymesBreadthFirst(startingSet,
            this.enzymesByreactionGroups.get("envMicroReactions"), preprocess, filter, nr_of_steps, scoreThreshold);
```

解释：ENVMICRO 并不是对所有 SMILES 直接生成产物；它先用 `ChemStructureExplorer.isPpsValid(target)` 做环境/PPS 风格的适用性检查，通过后才进入 `envMicroReactions` 的广度优先转化链。

### 4.3 `EnvMicroBTransformer.java`：规则匹配后生成候选产物

源码位置：

```text
src/main/java/biotransformer/btransformers/EnvMicroBTransformer.java:307-325
```

摘录：

```java
for (MetabolicReaction i : reactions) {
    boolean match_constraints = ChemStructureExplorer.compoundMatchesReactionConstraints(i, starget);
    if (match_constraints) {
        matchedReactions.add(i);
    }
}       
if(filter == false){
    filteredReactions = matchedReactions;     
} else{
    filteredReactions = new ArrayList<MetabolicReaction>(this.mRFilter.filterReactions(matchedReactions).values());
}

for(MetabolicReaction j : filteredReactions){
    IAtomContainerSet partialSet = generateAllMetabolitesFromAtomContainer(starget, j, false);
```

解释：每条 ENVMICRO metabolic reaction 先通过 `compoundMatchesReactionConstraints(...)` 判断底物是否满足反应约束；通过过滤后，`generateAllMetabolitesFromAtomContainer(...)` 按反应模板生成候选产物。

### 4.4 `ChemStructureExplorer.java`：PPS 输入有效性约束

源码位置：

```text
src/main/java/biotransformer/utils/ChemStructureExplorer.java:1256-1277
```

摘录：

```java
public static boolean isPpsValid(IAtomContainer molecule) throws CDKException{
    String inchikey = molecule.getProperty("InChIKey");
    if(inchikey ==null){
        InChIGeneratorFactory factory = InChIGeneratorFactory.getInstance();
        InChIGenerator gen1 = factory.getInChIGenerator(molecule);
        inchikey = gen1.getInchiKey();         
    }
    
    boolean valid = (!(isPpsCofactor(inchikey) || isPpsDeadEndCompound(inchikey)))  &&  AtomContainerManipulator.getNaturalExactMass(molecule)<1000.0 && 
            containsCarbon(molecule) && !isMixture(molecule) && 
```

解释：BioTransformer ENVMICRO 会先排除 PPS cofactor / dead-end compound，要求分子量小于 1000、含碳、不是 mixture 等。这支持我们此前写的“ENVMICRO 有输入适用域，不是任意 SMILES 全覆盖生成器”。

## 5. 与 Q3 机制结论的对应关系

本证据支持以下 Q3 结论：

```text
输入 parent SMILES
→ BioTransformer 命令行 -b env
→ BiotransformerExecutable 选择 bType.ENV
→ EnvMicroBTransformer
→ ChemStructureExplorer.isPpsValid 输入域检查
→ 遍历 ENVMICRO/envMicroReactions
→ compoundMatchesReactionConstraints 进行规则约束匹配
→ generateAllMetabolitesFromAtomContainer 生成候选产物
→ 输出 BioTransformer vendor CSV
→ 我方 adapter 再做 RDKit 规范化、去重、Top-10 截断
```

仍需保留的边界：

- BioTransformer ENVMICRO 不是深度学习生成模型；
- 不是 Rhea/EC/UniProt 查询；
- `Enzyme(s)=Unspecified environmental bacterial enzyme` 不是 UniProt UID；
- BioTransformer 的 vendor 输出顺序不是概率或置信度；
- 本文件不证明 BioTransformer 对新污染物未见路径具有泛化能力。

## 6. F5 完成判定

| 老师 F5 要求 | 本文件对应证据 | 判定 |
|---|---|---|
| GitHub commit 与 HPC 工具身份一致 | 返回包 metadata 中 `actual_commit=7149f7ec...`，源码回源 `git rev-parse HEAD=7149f7ec...` | PASS |
| jar 包 SHA256 | `BIOTRANSFORMER_JAR_SHA256.txt` 与 `TOOL_RUN_METADATA.json` 均记录 `e5c3c27d...ee80` | PASS |
| `BiotransformerExecutable` 5–10 行源码摘录 | §4.1 | PASS |
| `EnvMicroBTransformer` 5–10 行源码摘录 | §4.2；另以 §4.3 补充规则匹配/产物生成 | PASS |
| `ChemStructureExplorer` 5–10 行源码摘录 | §4.4 | PASS |

最终判定：F5 内容层面已补齐；仍需在后续 GitHub 同步 step 中提交并检查远端可见性。

