# Foolish 材料与群系魂石 · 0.6.0

2026-10-10。新增 10 块材料／功能魂石、8 块群系魂石与异境之魂，共 19 件成品；另有一种记录群系类型的浸染魂石合成材料。

## 获取方式

材料／功能魂石：在工作台中央放 `mine_fargo:empty_soul_stone`，上下左右放四项材料。

群系魂石：携带空白魂石，进入下表对应的 Foolish 群系，潜行右键任意方块，消耗一块空白魂石，得到记录该主题的浸染魂石；再将其放在配方中央，上下左右放对应材料。浸染按玩家所在群系判定，不会重写已有浸染类型。普通空白魂石、无标签浸染魂石或其他主题浸染魂石不符合群系配方。浸染魂石本身不能装备。

异境之魂由八块不同的群系魂石无序合成，继承八组能力。当前没有改动原有 Boss 魂石合成路线，也没有将这套魂石自动吸收进 Mine Fargo 伊始之魂。

## 材料／功能魂石

素材 ID 无前缀时均为 `foolish:`；表内四项依次对应上、左、右、下。效果数值为默认配置。

| 名称与物品 ID | 四项材料 | 基础能力 |
|---|---|---|
| 萦光魂石 `foolish_sacilite_material_soul_stone` | sacilite_shard、dull_sacilite_shard、azure_sacilite_lens、shining_sacilite_lens | 挖掘 +15%；每 6 秒命中发射追踪晶体，按实际命中伤害的 20%，上限 8 HP |
| 雷石魂石 `foolish_thunderstone_material_soul_stone` | thunderstone、electrical_charge、thunderstone、electrical_charge | 每 4 次有效命中蓄满电荷，电击为实际命中伤害的 25%，上限 10 HP，冷却 3 秒；计数有 0.5 秒命中间隔 |
| 腐蚀魂石 `foolish_corrosive_material_soul_stone` | radium、toxic_waste、corroded_metal、waste_roots | 新施加的 Foolish 腐蚀缩短 40%；命中 20% 概率附加 3 秒腐蚀，冷却 4 秒 |
| 钝金属魂石 `foolish_blunt_material_soul_stone` | blunt_metal_ingot、blunt_metal、blunt_metal_ingot、blunt_metal | 护甲 +3、抗击退 +10% |
| 炽合金魂石 `foolish_infernal_material_soul_stone` | infernal_alloy_ingot、infernal_alloy_plate_item、scorchslate、minecraft:magma_block | 新燃烧缩短 30%；自身燃烧时攻击增伤 5%；与灰烬能力采用灰烬优先，不重复加成 |
| 固钢魂石 `foolish_keepsteel_material_soul_stone` | 四块 keepsteel_ingot | 护甲 +2、韧性 +2；生命低于 35% 时额外抗击退 +25% |
| 琥珀魂石 `foolish_amber_material_soul_stone` | warp_amber、timefruit、chronosand、timewood_planks | 移速 +5%、挖掘 +10%；受击后速度 I 2 秒，冷却 8 秒 |
| 滑行魂石 `foolish_slide_material_soul_stone` | enderskates_boots、ender_tire、chorus_leather、rotary_core | 持续疾跑 4 秒逐渐获得最多 +25% 移速，停止或卸下即重置 |
| 寄生魂石 `foolish_parasitic_material_soul_stone` | parasitic_stinger、hyper_stinger、burn_stinger、minecraft:string | 有效命中获得恢复 I 3 秒，冷却 6 秒 |
| 魂裳魂石 `foolish_soulcoat_material_soul_stone` | soulsucker_fur、soul_coat_chestplate、minecraft:soul_sand、minecraft:soul_soil | 受击向攻击者发射追踪魂火，实际受击伤害的 20%，上限 8 HP，冷却 6 秒，距离 16 格 |

材料版不需要浸染，也没有当地群系加成。萦光／雷石／腐蚀／琥珀与绽晶／风暴／废土／时沙对应为同一能力组：两个方向都禁止重复装备，异境之魂也不能与这四种材料版同时装备。

## 群系魂石

| 名称与物品 ID | 群系 ID（`foolish:`） | 四项材料 | 基础能力 |
|---|---|---|---|
| 绽晶魂石 `foolish_bloom_biome_soul_stone` | sacilite_bloom、sacilite_cavern | sacilite_shard、dull_sacilite_shard、azure_sacilite_lens、rose_sacilite_lens | 与萦光共用基础能力 |
| 风暴魂石 `foolish_storm_biome_soul_stone` | storm_jungle | thunderstone、electrical_charge、storm_apple、thunderstone | 疾跑 6 秒蓄满电荷；水中／雨中蓄电速度 ×1.5，命中释放电击，比例、上限和冷却与雷石相同 |
| 时沙魂石 `foolish_time_biome_soul_stone` | sands_of_time | chronosand、warp_amber、timefruit、timewood_log | 与琥珀共用基础能力 |
| 猩野魂石 `foolish_scarlet_biome_soul_stone` | scarlet_fields | scarlet_silt、egg_membrane、scarlet_glow_fungus、scarlant_capsule | 命中 15% 概率召唤有主人归属的魂蚁，冷却 10 秒；附近与女王魂蚁共用数量检查，默认最多 2 只；寿命 8 秒、生命 10、攻击 2 |
| 废土魂石 `foolish_waste_biome_soul_stone` | wasteland、irradiated_undergrowth | radium、toxic_waste、corroded_metal、waste_soil | 与腐蚀共用基础能力 |
| 泥沼魂石 `foolish_mire_biome_soul_stone` | miserable_mire | bunyip_fur、large_lily_pad、darkenstone、murken_berry | 游泳 +20%；水中／雨中每 8 秒恢复 1 HP |
| 繁生魂石 `foolish_growth_biome_soul_stone` | overgrowth | soft_leaf、sharp_leaf、pollen_burst、stem_planks | 攻击或受伤后 5 秒视为战斗中；每 10 秒对周围 4 格内最多 4 个敌人施加缓慢 I 2 秒，并恢复 1 HP |
| 灰烬魂石 `foolish_ash_biome_soul_stone` | ashen_woods、volcanic_valley、emberlight_valley | ashen_log、scorchslate、ashflower、volcanic_hollowstone_rod | 新燃烧缩短 40%；自身燃烧时攻击增伤 8%；每 8 秒对 3 格内最多 3 个敌人造成 2 HP 余烬伤害 |
| 异境之魂 `soul_of_otherworld` | 继承全部八组对应群系 | 八块不同群系魂石，无序合成 | 完整继承八组基础能力和各自当地加成 |

对应群系中的增强倍率默认为 ×1.5，具体强化项如下：

- 绽晶：挖掘增益、晶体伤害。
- 风暴：蓄电速度、电击伤害。
- 时沙：挖掘增益、受击加速时间；基础移速属性不随群系变化。
- 猩野：召唤概率。
- 废土：腐蚀缩时比例、附加腐蚀概率。
- 泥沼：每次回复量；游泳属性不随群系变化。
- 繁生：减速时间、回复量。
- 灰烬：燃烧缩时比例、燃烧增伤、余烬伤害。

离开群系保留基础能力。当地倍率不提升伤害上限、召唤数量，也不缩短冷却；持续时间缩减最高 90%。未把本体明确标注 Unused 的群系加入必需收集列表。

## 运行边界

- Foolish 缺失时跳过这 20 件物品（19 成品及 1 浸染材料）注册，配方有 `forge:mod_loaded` 条件；没有新增对 Foolish Java 类的硬链接。
- 能力由服务端结算。直接命中、箭矢和铁魔法伤害能触发命中效果；反伤、燃烧 DOT 和魂石二次伤害不触发。
- 晶体、魂火检查主人、目标、距离、视线与路径碰撞；卸下对应能力后消失。
- 魂蚁有主人、寿命和数量限制；不掉物品或经验，卸下能力后消失。复用现有有归属的魂蚁实现，不生成野生敌对 Foolish 生物。
- 范围花粉和余烬只选择可见的敌对生物、正攻击玩家的生物或玩家刚攻击的目标，排除自身、友军、玩家自己的宠物和召唤物。
- 滑行和固钢的条件属性使用临时修饰符，状态结束即删除；炽合金和灰烬不重复缩短同一段燃烧。
- 配方使用了核对存在的素材 ID，避开紫晶心脏、雷核、镭晶体、猩红护符、泥沼宝石等已确认 Boss 核心。具体世界中素材生成与完整探索获取仍需实玩验收。

## 贴图规则

19 张全新成品贴图均为 18×18 原生 RGBA，透明度仅 0／255；统一已确认轮廓、切面、左上光源。中央符纹和外圈使用相同像素网格，应用中轴柔化及左右上边缘亮度修正，最近邻整数倍放大预览。现有 32 张学派与 Boss 魂石图逐张哈希验证保持不变。

总览：`art/foolish-all-stones-0.6.0.png`。单项原图、放大图和清单分别位于 `art/foolish-material-stones-0.6.0/` 与 `art/foolish-biome-stones-0.6.0/`。

## 配置与验收

群系配置：存档 `serverconfig/wans_minego_expansion-biome-souls.toml`；材料配置：`serverconfig/wans_minego_expansion-material-souls.toml`。材料版与群系版共用的基础参数由群系配置管理，其余材料能力由材料配置管理。

重启后依次检查：19 件成品及浸染材料的物品显示；8 个主题的浸染、正确与错误 NBT 的配方；八件无序合成；单块／合成品／同主题材料版双向装备排斥；移速、挖掘、游泳与停止滑行后的属性恢复；冷却与伤害上限；召唤物数量、寿命和友伤排除；当地加成；既有 32 件物品的显示和效果回归。

构建、独立服务端检查与实际整合包游戏内验收分别记录在发布凭据中，不能互相代替。

## 发布记录

正式版 Java 17 / Gradle 8.8 离线构建成功并执行 `reobfJar`。源资源与最终 JAR 逐项一致；72 个配方、51 个可选 Curios 标签项、新旧图标、双语占位符及伤害标签静态检查通过。验证专用 Java 类和空白测试结构未进入正式 JAR。

独立 Forge GameTest 世界在 `ServerStartingEvent` 阶段通过 89 项检查：10 个材料配方、8 个群系配方及正确／错误／无标签浸染匹配，组合配方，Curios 槽位及能力继承，材料／群系／组合品双向排斥，滑行上限及停止重置、固钢低血量属性及恢复清除、燃烧与腐蚀只缩短一次。移除 Foolish 的独立环境通过另 3 项物品与配方跳过检查。其后完整测试服启动被本机回环连接错误阻断：普通服务器发生于 Netty 初始化，GameTest 服务器发生于 Iron's Lib `PatreonHandler` 创建 HTTP 客户端；没有修改全局 Java、网络或其他模组来规避。上述 92 项检查通过不等于完整测试服启动成功，也不等于整合包实玩通过。

已安装 `mods/wans_minego_expansion-0.6.0.jar`，226,725 字节；构建和安装 SHA-256 均为 `89B4D4E9184945B97F743008332DA9E4D58C553EEDDD0FFF34F944865F7730CD`。当前仅一份生效的 Wan 魂石扩展 JAR。旧版已校验备份到 `backups/20261010-191531-before-exploration-souls-0.6.0/`，其中 `deployment.json` 记录旧版哈希、回滚路径和验证边界。发布凭据也位于本项目 `audit/20261010-biome-souls/release-receipt.json`。未重启用户的整合包，客户端显示、实际群系探索获取和实战效果仍待验收。
