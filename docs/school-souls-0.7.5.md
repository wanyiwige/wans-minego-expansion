# 0.7.5 补齐学派魂石

## 范围与来源

本轮新增 15 块学派魂石，依据 2026-10-20 当前安装的 JAR 核对注册类、属性、材料、焦点标签和卷轴贴图；《法术统计.md》作为查漏清单。用户本轮明确授权把此前暂缓的自制学派也补齐。混沌仍暂缓，当前包也未安装其模组。

当前 Mine Fargo 1.3.97 已提供源流、律灵、岩土、梦幻魂石，已核对其实际法强引用，不重复注册。已有 20 块附属学派魂石保留原有注册 ID、配方、效果及贴图。本轮是在现有 0.7.4 工程上继续制作；构建后经用户明确要求，已将游戏目录中的 0.7.1 替换为 0.7.5。

## 数值与标识

基础效果统一沿用公共配置默认值：对应学派法强 +10%、最大法力 +60。星辉法强属性基础值为 0，因此使用加算 +0.10；其余新学派使用基础值乘算 +10%。

| 学派 | 物品 ID（`wans_minego_expansion:`） | 额外效果 | 中央标识 |
| --- | --- | --- | --- |
| 锻造 | `smithing_soul_stone` | 护甲 +2 | 锤与砧台 |
| 诅咒 | `curse_soul_stone` | 诅咒魔法命中施加虚弱 I，3 秒 | 断裂咒链 |
| 时间 | `time_soul_stone` | 法术冷却缩减 +5% | 缺口时盘与偏置指针 |
| 回响 | `echo_soul_stone` | 回响魔法命中使目标发光，4 秒 | 不等高声波谱 |
| 星宇 | `exo_soul_stone` | 护甲韧性 +1 | 不对称三节点回路 |
| 磁极 | `magnetic_school_soul_stone` | 击退抗性 +0.10 | 红蓝反向磁通 |
| 糖果 | `candy_school_soul_stone` | 最大生命 +2 | 糖纹旋卷 |
| 云 | `cloud_school_soul_stone` | 移动速度 +5% | 云团与分散雨滴 |
| 辐射 | `toxic_school_soul_stone` | 辐射魔法命中施加中毒 I，3 秒 | 异位同位素节点 |
| 星辉 | `astral_soul_stone` | 法力回复 +5% | 折线星座 |
| 旅者 | `traveller_soul_stone` | 移动速度 +5% | 折叠路线 |
| 寰宇 | `hazen_cosmic_soul_stone` | 召唤物伤害 +5% | 彗核与离散尾迹 |
| 光辉 | `hazen_radiance_soul_stone` | 法术抗性 +5% | 地平线上升起的光冠 |
| 黑暗 | `hazen_shadow_soul_stone` | 施法时间缩减 +5% | 弯折暗幕 |
| 海怒 | `hazen_hydro_soul_stone` | 游泳速度 +10% | 双层破浪 |

命中特效仅服务端处理，要求伤害来源归属于玩家、伤害大于零、对应魂石已装备，并排除本模组的二次伤害。特效通过原版状态机制施加，受目标自身免疫规则限制。魂石继承原有重复装备及主魂石互斥检查。

## 配方

新增 30 个有序配方：每块两条路线。

- 诅咒、时间、回响、磁极、糖果、寰宇：`EAE / BOC / EDE`，四角为学派焦点，A/B/C/D 为学派四件套，O 为空白魂石。
- 其余九块：`ERE / ROR / ERE`，E 为学派焦点，R 为符文或代表材料，O 为空白魂石。
- 全部另有 `RRR / ROR / RRR` 八符文或八材料路线。

| 学派 | R 符文／代表材料 | 焦点标签 |
| --- | --- | --- |
| 锻造 | `iron_spell_smithing_template_addon:smithing_rune` | `iron_spell_smithing_template_addon:smithing_focus` |
| 诅咒 | `cursespells:curse_rune` | `cursespells:curse_focus` |
| 时间 | `irons_chronomancy:time_rune` | `irons_chronomancy:time_focus` |
| 回响 | `echo_spellbooks:echo_rune` | `echo_spellbooks:echo_focus` |
| 星宇 | `roacw:charged_auric_ingot` | `curios:exo_focus` |
| 磁极 | `alex_caves_spellsbook:magnetic_polarity_rune` | `alex_caves_spellsbook:magnetic_focus` |
| 糖果 | `alex_caves_spellsbook:candy_rune` | `alex_caves_spellsbook:candy_focus` |
| 云 | `minecraft:phantom_membrane` | `alex_caves_spellsbook:cloud_focus` |
| 辐射 | `alexscaves:uranium` | `alex_caves_spellsbook:toxic_focus` |
| 星辉 | `asterismarcanum:astral_rune` | `kubejs:astral_focus` |
| 旅者 | `minecraft:ender_pearl` | `kubejs:traveller_focus` |
| 寰宇 | `alex_caves_spellsbook:hazen_cosmic_rune` | `alex_caves_spellsbook:hazen/cosmic_focus` |
| 光辉 | `alex_caves_spellsbook:hazen_radiance_rune` | `alex_caves_spellsbook:hazen/radiance_focus` |
| 黑暗 | `alex_caves_spellsbook:hazen_shadow_rune` | `alex_caves_spellsbook:hazen/shadow_focus` |
| 海怒 | `alex_caves_spellsbook:hazen_hydro_rune` | `alex_caves_spellsbook:hazen/hydro_focus` |

材料和焦点的具体资源已与当前安装 JAR 交叉检查。资源存在是静态证据，不替代游戏内配方、注册表和合成验收。

## 动态检测

- 锻造、诅咒、时间、回响按各自提供模组检测；星宇检测 `roacw`。
- 另外十个自制学派检测真正提供者 `alex_caves_spellsbook`，要求其版本至少 1.2.2，避免旧版本尚无完整学派而出现无效魂石。星辉与旅者不以 `kubejs` 是否安装作为注册条件。
- 所有新依赖在 `mods.toml` 中均为可选。
- 每条配方先检查提供模组，再检查结果魂石、全部直接材料是否存在；焦点路线额外检查焦点标签非空。材料缺失时跳过相应配方。
- Curios 新标签条目全部 `required:false`。创造标签页沿用已注册条目动态列出。

## 贴图与可编辑源

当前 15 张均为 18×18 RGBA、0/255 二值透明，同一原生网格；预览采用整数倍最近邻放大。轮廓沿用本系列已确认的魂石外形，配色参考对应学派卷轴。动画卷轴只取单帧分析，未将纵向帧条压缩为图标。

根据用户“标识不要与原有魂石重复”的补充要求，15 张中央图案已二次绘制，避开原有月牙、十字、星形、三叉、圆环及磁铁 U 形等构图。已与原有学派图册视觉对照，并检查新标识及原有绘制器标识在旋转、镜像下无完全相同的像素掩码；该检测不等同于证明所有观感相似性均消除。逐像素比较确认本次二次绘制仅改变中央 8×8。

- 可编辑定义与生成器：`tools/create_remaining_school_souls.py`
- 校验器：`tools/validate_remaining_school_souls.py`
- 当前预览：`art/remaining-school-souls-0.7.5/preview.png`
- 重画前图案：`art/remaining-school-souls-0.7.5/before-glyph-redraw/`
- 原有图案对照：`audit/20261020-schools/existing-school-icons.png`
- 当前学派卷轴来源：`audit/20261020-schools/scroll-sources.json`
- 工程修改前备份：`backups/20261020-before-school-souls/`

## 验证边界

源文件及资源校验通过：15 块新魂石、30 条新配方、模型、双语描述、原生网格、中央修改范围、材料／焦点资源；89 张原有贴图哈希不变。构建结果以 `audit/20261020-schools/` 的日志及 `validation.json` 为准。游戏目录 JAR 已替换；未完成重启、进服、装备及效果验收。

2026-10-20 构建完成：Gradle 8.8、Java 17.0.20.1，执行 `reobfJar` 并得到 `BUILD SUCCESSFUL`。Wrapper 遇到本机 loopback 异常后，使用现有本地 Gradle 直接启动方式构建，未更改全局 Java 或网络配置。成品与新增资源逐字节核对通过；94 条原有配方和原有翻译值保持不变。

- 成品：`build/libs/wans_minego_expansion-0.7.5.jar`
- 大小：362385 字节
- SHA-256：`b24b32e0b69b39e7dc806f06ca14d0c2413193c76559475de1cccd1696a0d1ce`

2026-10-20 部署完成：旧 0.7.1 先备份并验证 SHA-256，再移出 `mods/`；0.7.5 安装后哈希与上述成品一致，目录中仅一个本模组有效 JAR。备份与回执：`backups/20261020-before-0.7.5-deploy-52b13424/`，其中 `deployment.json` 记录旧包和新包哈希。未修改游戏配置及存档。
