# 无限与污秽魂石效果记录

对应版本：Wan's Minego Expansion 0.3.0；BielGG's Spells 1.5 patchwork localpatch；Forge 1.20.1。

## 无限学派魂石

- 物品：`wans_minego_expansion:infinity_soul_stone`，位于创造标签页“Wan的魂石”和 Curios `soul_stone` 栏位。
- 基础属性：`bielgg_spells:infinity_spell_power` +10%（`MULTIPLY_BASE`），最大法力 +60。
- 特色效果：佩戴者造成 `bielgg_spells:infinity_magic` 伤害时，在 `LivingHurtEvent` 将该次伤害乘以 1.05。伤害来源的施法者必须是佩戴该魂石的玩家；不是每次法术施放都触发，只有实际产生该伤害类型的攻击才触发。
- 配方一：`ERE / ROR / ERE`。`E` 为 `bielgg_spells:infinity_focus`（当前前置提供 `avaritia:infinity_catalyst`），`R` 为 `bielgg_spells:infinity_rune`，`O` 为 `mine_fargo:empty_soul_stone`。
- 配方二：`RRR / ROR / RRR`，八个无限符文围绕空白魂石。
- 前置：`bielgg_spells` 与 `avaritia`。当前实例的 BielGG 配置 `enableInfinityContent = true`。
- 贴图：参考 `assets/bielgg_spells/textures/item/scroll_infinity.png` 的虹彩卷轴配色，使用静态虹彩魂石图。

## 污秽学派魂石

- 物品：`wans_minego_expansion:tainted_soul_stone`，位于创造标签页“Wan的魂石”和 Curios `soul_stone` 栏位。
- 基础属性：`bielgg_spells:tainted_spell_power` +10%（`MULTIPLY_BASE`），最大法力 +60。
- 特色效果：佩戴者造成 `bielgg_spells:tainted_magic` 伤害且该次实际伤害大于 0 时，在 `LivingDamageEvent` 对目标施加 3 秒凋零 I（60 tick，效果等级 0）。伤害来源的施法者必须是佩戴该魂石的玩家，目标不能是施法者本人。
- 配方一：`ERE / ROR / ERE`。`E` 为 `bielgg_spells:tainted_focus`（当前前置提供 `witherstormmod:tainted_dust`），`R` 为 `bielgg_spells:rune_of_the_order`，`O` 为 `mine_fargo:empty_soul_stone`。
- 配方二：`RRR / ROR / RRR`，八个秩序符文围绕空白魂石。
- 前置：`bielgg_spells` 与 `witherstormmod`。当前实例的 BielGG 配置 `enableTaintedContent = true`。
- 贴图：参考 `assets/bielgg_spells/textures/item/scroll_tainted.png` 的深紫与洋红卷轴配色。

## 验证边界

以上为当前源代码和 JAR 资源的静态记录。0.3.0 已构建并部署；游戏中的伤害数值、凋零触发、创造标签页展示及贴图效果尚未通过重启后实测。
