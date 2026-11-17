# Wan's Minego Expansion

## 0.7.5 学派魂石补齐

新增锻造、诅咒、时间、回响、星宇及十个自制学派魂石，共 15 块、30 条配方。新增标识已按用户要求重画；配方、效果、依赖检测、贴图说明及验收状态见 [0.7.5 记录](docs/school-souls-0.7.5.md)。发布 JAR 已构建，并于 2026-10-20 按用户要求替换游戏目录中的 0.7.1；重启与游戏内验收尚待完成。

Forge 1.20.1 附属模组，`mod_id=wans_minego_expansion`。0.6.0 包含原有 20 块附属学派魂石和 12 件 Foolish Boss 系列饰品，以及新增的 10 块材料／功能魂石、8 块群系魂石和异境之魂，共 51 件成品；另有浸染魂石合成材料。所有物品按对应模组动态注册。新系列效果、配方、配置和验证边界见 [Foolish 探索魂石说明](docs/foolish-exploration-souls-0.6.0.md)，Boss 系列见 [Foolish 实装记录](docs/foolish-boss-souls-0.5.0.md)。暗影和暗影水晶按同一学派设计，共用一块魂石。`irons_spells_delight` 没有注册新学派，因此没有对应魂石。`chaos_seed:chaos` 和五个自制学派按用户要求暂不制作。

创造模式有独立的“Wan的魂石”标签页，只展示依赖齐全、已注册的魂石。标签页不会包含 Mine Fargo 原模组的魂石。

## 魂石

| 物品 ID                                                 | 装备效果（默认配置）                         | 特色效果                             |
| ----------------------------------------------------- | ---------------------------------- | -------------------------------- |
| `wans_minego_expansion:symmetry_sect_soul_stone`      | 两仪法强 +10%，最大法力 +60，法术抗性 +5%        | 两仪魔法伤害 +5%                       |
| `wans_minego_expansion:spirit_sect_soul_stone`        | 魂灵法强 +10%，最大法力 +60                 | 魂灵魔法命中施加 3 秒魂焰灼烧，按实际伤害的 5% 治疗施法者 |
| `wans_minego_expansion:insect_soul_stone`             | 虫群法强 +10%，最大法力 +60                 | 虫群魔法命中施加 3 秒中毒                   |
| `wans_minego_expansion:dream_soul_stone`              | 梦境法强 +10%，最大法力 +60                 | 梦境魔法命中施加 4 秒虚弱                   |
| `wans_minego_expansion:wind_soul_stone`               | 风法强 +10%，最大法力 +60                  | 风魔法命中后获得 5 秒速度 I                 |
| `wans_minego_expansion:annihilation_soul_stone`       | 湮灭法强 +10%，最大法力 +60                 | 对生命不高于 30% 的目标，湮灭魔法伤害 +8%        |
| `wans_minego_expansion:shadow_soul_stone`             | 暗影法强 +10%，最大法力 +60                 | 暗影魔法命中减速目标 2 秒，并按伤害的 3% 回复生命     |
| `wans_minego_expansion:unstable_soul_stone`           | 失稳法强 +10%，最大法力 +60                 | 失稳魔法有 20% 几率造成 +20% 伤害           |
| `wans_minego_expansion:relicron_soul_stone`           | Relicron 法强 +10%，最大法力 +60，法术抗性 +5% | Relicron 魔法命中获得 5 秒伤害吸收 I        |
| `wans_minego_expansion:infinity_soul_stone`           | 无限法强 +10%，最大法力 +60                 | 无限魔法伤害 +5%                       |
| `wans_minego_expansion:tainted_soul_stone`            | 污秽法强 +10%，最大法力 +60                 | 污秽魔法命中施加 3 秒凋零                   |
| `wans_minego_expansion:trailblazer_arcana_soul_stone` | 开拓奥秘伤害增幅 +10%，最大法力 +60             | 法术抗性 +5%                         |
| `wans_minego_expansion:fusion_soul_stone`             | 混合法强 +10%，最大法力 +60                 | 法力回复 +5%                         |
| `wans_minego_expansion:ars_nouveau_soul_stone`        | 魔艺法强 +10%，最大法力 +60                 | 召唤物伤害 +5%                        |
| `wans_minego_expansion:abyssal_soul_stone`            | 深渊法强 +10%，最大法力 +60                 | 法术抗性 +5%                         |
| `wans_minego_expansion:technomancy_soul_stone`        | 械术法强 +10%，最大法力 +60                 | 法术冷却缩减 +5%                       |
| `wans_minego_expansion:esoteric_soul_stone`           | 秘法法强 +10%，最大法力 +60                 | 施法时间缩减 +5%                       |
| `wans_minego_expansion:gluttony_soul_stone`           | 饕魔法强 +10%，最大法力 +60                 | 最大生命值 +2                         |
| `wans_minego_expansion:glintstone_soul_stone`         | 辉石法强 +10%，最大法力 +60                 | 法力回复 +5%                         |
| `wans_minego_expansion:glutton_soul_stone`            | 大胃王法强 +10%，最大法力 +60                | 最大生命值 +2                         |

无限与污秽魂石的触发条件、数值、配方和验证状态详见 [效果记录](docs/bielgg-infinity-tainted-soul-stones.md)。

所有成品魂石使用 Mine Fargo 的 Curios `soul_stone` 栏位。学派魂石拒绝同种重复佩戴；已经佩戴奥法之魂或 Inolia 之魂时，也会拒绝佩戴学派魂石。原版主魂石的反向装备判定尚未修改。Foolish 材料、群系与 Boss 系列按各自能力组检查重复，详见对应说明。法强、法力及两仪／魂灵／Relicron 的数值配置位于游戏实例生成的 `wans_minego_expansion-common.toml`；其他学派特色效果采用上表固定数值。开拓奥秘学派使用前置的独立伤害增幅属性，基础值为 0，因此魂石以加算方式给予 +0.10；其他学派法强以基础值乘算方式增加 10%。

## 合成

配方参照 Mine Fargo 的空白魂石加学派材料结构：

- 有套装的学派使用 `EAE / BOC / EDE`：`O` 为空魂石，`A/B/C/D` 依次为学派套装头盔、胸甲、护腿、靴子，四个 `E` 为学派焦点。风使用 Aeromancer 套装；湮灭使用 Oblivionmancer；暗影使用 Roaring Knight；失稳使用 Broken；Relicron 使用同名套装。
- 无套装的虫群与梦境使用 `ERE / ROR / ERE`：`E` 是学派焦点，`R` 是学派符文。
- 无限与污秽也使用 `ERE / ROR / ERE` 焦点加符文路线：无限用 `avaritia:infinity_catalyst` 焦点与 `bielgg_spells:infinity_rune`；污秽用 `witherstormmod:tainted_dust` 焦点与 `bielgg_spells:rune_of_the_order`。
- 所有魂石还有 `RRR / ROR / RRR` 的八符文路线。暗影额外支持八个 `roaring:shadow_crystal` 围绕空白魂石合成同一块暗影魂石。
- 0.4.0 新增的九块优先使用学派套装加学派焦点的 `EAE / BOC / EDE` 路线，同时保留八符文路线。开拓奥秘以寻路水晶代替符文，混合以编织符文代替符文；配方使用前置 JAR 中实际存在的套装与材料。

## 构建与阶段

暗影、失稳、Relicron、无限、污秽五张贴图参考 BielGG 1.5 对应学派卷轴的颜色，保持原有魂石的轮廓和粗像素风格。Relicron 的中央齿轮采用用户确认的修正版。新增九张魂石的当前工程源贴图，按用户确认的械术样稿统一改为 18×18 方形像素格：从 `art/reference-teal-soul-stone.png` 取得相同轮廓与明暗结构，分别按对应卷轴配色，并在中心绘制同格尺寸的符文。`tools/render_scroll_style_stones.py` 生成九张 1260×1260 贴图及 `art/stones-18px/` 的原始格点文件；总览见 `art/new-school-stones-preview-v2.png`。旧版九张源贴图保存在 `backups/20260930-before-scroll-style-redraw`，重绘前的三张 BielGG 旧贴图保存在 `backups/20260930-before-bielgg-scroll-recolor`。

使用 JDK 17 构建，发布 JAR 由 `reobfJar` 处理。`libs` 下的本地依赖来自当前实例，仅用于开发，未打包进发布 JAR。工程未修改 Mine Fargo 原 JAR 或奥法之魂的配方与效果；后者留待下一阶段设计实现。0.4.1 已将上述九张新贴图构建并部署到当前整合包；0.4.0 的备份位于 `backups/20260930-before-0.4.1-deploy`，实例内旧包改名为 `.jar.disabled`。0.4.1 发布包与安装包 SHA-256 均为 `65C071AE5B4485A029685901F468B6860E9F0F9734C14EB3600E0F3C4C249784`。游戏内贴图仍需在重启后验收。
