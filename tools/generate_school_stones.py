"""Generate the nine added stones' recipes, models, names, and Curios tag.

Textures are maintained separately by render_scroll_style_stones.py.
"""

from __future__ import annotations

import json
from pathlib import Path



ROOT = Path(__file__).resolve().parents[1]
MOD_ID = "wans_minego_expansion"
RES = ROOT / "src" / "main" / "resources"
ASSETS = RES / "assets" / MOD_ID
RECIPES = RES / "data" / MOD_ID / "recipes"

STONES = {
    "trailblazer_arcana": {
        "name": "开拓奥秘", "english": "Trailblazer Arcana",
        "mod": "astralrail_cube", "focus": ("tag", "astralrail_cube:trailblazer_arcana"),
        "armor": ["preservation_helmet", "preservation_chestplate", "preservation_leggings", "preservation_boots"],
        "rune": "astralrail_cube:path_crystal", "rune_label": "crystals",
        "effect_zh": "法术抗性 +5%", "effect_en": "+5% Spell Resist",
    },
    "fusion": {
        "name": "混合", "english": "Fusion", "mod": "iss_csw",
        "focus": ("item", "iss_csw:rune_weave"),
        "armor": ["arcane_helmet", "arcane_chestplate", "arcane_leggings", "arcane_boots"],
        "rune": "iss_csw:rune_weave", "rune_label": "weaves",
        "effect_zh": "法力回复 +5%", "effect_en": "+5% Mana Regen",
    },
    "ars_nouveau": {
        "name": "魔艺", "english": "Ars Nouveau", "mod": "ars_nouveau_spellbooks",
        "focus": ("tag", "ars_nouveau_spellbooks:ars_nouveau_focus"),
        "armor": ["source_mage_helmet", "source_mage_chestplate", "source_mage_leggings", "source_mage_boots"],
        "rune": "ars_nouveau_spellbooks:ars_nouveau_rune", "rune_label": "runes",
        "effect_zh": "召唤物伤害 +5%", "effect_en": "+5% Summon Damage",
    },
    "abyssal": {
        "name": "深渊", "english": "Abyssal", "mod": "cataclysm_spellbooks",
        "focus": ("tag", "cataclysm_spellbooks:abyssal_focus"),
        "armor": ["abyssal_warlock_helmet", "abyssal_warlock_chestplate", "abyssal_warlock_leggings", "abyssal_warlock_boots"],
        "rune": "cataclysm_spellbooks:abyssal_rune", "rune_label": "runes",
        "effect_zh": "法术抗性 +5%", "effect_en": "+5% Spell Resist",
    },
    "technomancy": {
        "name": "械术", "english": "Technomancy", "mod": "cataclysm_spellbooks",
        "focus": ("tag", "cataclysm_spellbooks:technomancy_focus"),
        "armor": ["engineer_hood", "engineer_suit", "engineer_leggings", "engineer_boots"],
        "rune": "cataclysm_spellbooks:technomancy_rune", "rune_label": "runes",
        "effect_zh": "法术冷却缩减 +5%", "effect_en": "+5% Spell Cooldown Reduction",
    },
    "esoteric": {
        "name": "秘法", "english": "Esoteric", "mod": "esoteric_spell",
        "focus": ("tag", "irons_spellbooks:esoteric_focus"),
        "armor": ["esoteric_mage_helmet", "esoteric_mage_chestplate", "esoteric_mage_leggings", "esoteric_mage_boots"],
        "rune": "esoteric_spell:esoteric_rune", "rune_label": "runes",
        "effect_zh": "施法时间缩减 +5%", "effect_en": "+5% Cast Time Reduction",
    },
    "gluttony": {
        "name": "饕魔", "english": "Gluttony", "mod": "farmers_spell",
        "focus": ("tag", "farmers_spell:gluttony_focus"),
        "armor": ["gluttony_chef_hat", "gluttony_chef_apron", "gluttony_chef_leggings", "gluttony_chef_boots"],
        "rune": "farmers_spell:glutton_rune", "rune_label": "runes",
        "effect_zh": "最大生命值 +2", "effect_en": "+2 Max Health",
    },
    "glintstone": {
        "name": "辉石", "english": "Glintstone", "mod": "iss_elden_ring",
        "focus": ("tag", "iss_elden_ring:glintstone_focus"),
        "armor": ["astrologer_hat", "astrologer_robe", "astrologer_leggings", "astrologer_boots"],
        "rune": "iss_elden_ring:glintstone_rune", "rune_label": "runes",
        "effect_zh": "法力回复 +5%", "effect_en": "+5% Mana Regen",
    },
    "glutton": {
        "name": "大胃王", "english": "Glutton", "mod": "bigeater_magic",
        "focus": ("tag", "irons_spellbooks:glutton_focus"),
        "armor": ["glutton_helmet", "glutton_chestplate", "glutton_leggings", "glutton_boots"],
        "rune": "bigeater_magic:glutton_rune", "rune_label": "runes",
        "effect_zh": "最大生命值 +2", "effect_en": "+2 Max Health",
    },
}


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ingredient(kind: str, value: str) -> dict:
    return {kind: value}


def recipe(name: str, info: dict, alternate: bool) -> dict:
    mod = info["mod"]
    if alternate:
        pattern = ["RRR", "ROR", "RRR"]
        key = {"R": ingredient("item", info["rune"])}
    else:
        pattern = ["EAE", "BOC", "EDE"]
        key = {"E": ingredient(*info["focus"])}
        for letter, armor in zip("ABCD", info["armor"]):
            key[letter] = ingredient("item", f"{mod}:{armor}")
    key["O"] = ingredient("item", "mine_fargo:empty_soul_stone")
    return {
        "conditions": [{"type": "forge:mod_loaded", "modid": mod}],
        "type": "minecraft:crafting_shaped", "pattern": pattern, "key": key,
        "result": {"item": f"{MOD_ID}:{name}_soul_stone"},
    }


def main() -> None:
    zh_path = ASSETS / "lang" / "zh_cn.json"
    en_path = ASSETS / "lang" / "en_us.json"
    zh = json.loads(zh_path.read_text(encoding="utf-8"))
    en = json.loads(en_path.read_text(encoding="utf-8"))
    zh["tooltip.wans_minego_expansion.trailblazer_base"] = "开拓奥秘伤害增幅 +%s%%，最大法力 +%s"
    en["tooltip.wans_minego_expansion.trailblazer_base"] = "+%s%% Trailblazer Arcana Damage Boost, +%s Max Mana"
    for name, info in STONES.items():
        item_id = f"{name}_soul_stone"
        zh[f"item.{MOD_ID}.{item_id}"] = info["name"] + "学派魂石"
        en[f"item.{MOD_ID}.{item_id}"] = info["english"] + " School Soul Stone"
        zh[f"tooltip.{MOD_ID}.{name}"] = info["effect_zh"]
        en[f"tooltip.{MOD_ID}.{name}"] = info["effect_en"]
        save_json(ASSETS / "models" / "item" / f"{item_id}.json", {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"{MOD_ID}:item/{item_id}"},
        })
        save_json(RECIPES / f"{item_id}.json", recipe(name, info, False))
        save_json(RECIPES / f"{item_id}_{info['rune_label']}.json", recipe(name, info, True))
    save_json(zh_path, zh)
    save_json(en_path, en)
    tag_path = RES / "data" / "curios" / "tags" / "items" / "soul_stone.json"
    tag = json.loads(tag_path.read_text(encoding="utf-8"))
    for name in STONES:
        value = {"id": f"{MOD_ID}:{name}_soul_stone", "required": False}
        if value not in tag["values"]:
            tag["values"].append(value)
    save_json(tag_path, tag)
    # Reapply the shared registration/recipe dependency rules after regeneration.
    from integrate_boss_resources import main as integrate_boss_resources
    integrate_boss_resources()


if __name__ == "__main__":
    main()
