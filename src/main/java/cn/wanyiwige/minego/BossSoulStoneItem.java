package cn.wanyiwige.minego;

import com.google.common.collect.LinkedHashMultimap;
import com.google.common.collect.Multimap;
import java.util.EnumSet;
import java.util.List;
import java.util.UUID;
import javax.annotation.Nullable;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraftforge.common.ForgeMod;
import top.theillusivec4.curios.api.CuriosApi;
import top.theillusivec4.curios.api.SlotContext;
import top.theillusivec4.curios.api.type.capability.ICurioItem;

public final class BossSoulStoneItem extends Item implements ICurioItem {
    public enum Kind {
        PYRE("pyre"), TIMEWELDER("timewelder"), THRASHER("thrasher"),
        SACILIC_ABOMINATION("sacilic_abomination"), VARMINT_KING("varmint_king"),
        THUNDERBIRD("thunderbird"), SCARLANT_QUEEN("scarlant_queen"),
        TERRORFLORA("terrorflora"), WENDIGRUDGE("wendigrudge"), ASTRALIS("astralis"),
        STELLAR_HOLLOW("stellar_hollow"), FOOLISH("foolish");

        private final String key;
        Kind(String key) { this.key = key; }
        public String key() { return key; }
        public String id() {
            return this == STELLAR_HOLLOW ? "soul_of_stellar_hollow"
                    : this == FOOLISH ? "soul_of_foolish" : "foolish_" + key + "_soul_stone";
        }
        public EnumSet<Kind> abilities() {
            return this == FOOLISH ? EnumSet.range(PYRE, ASTRALIS)
                    : this == STELLAR_HOLLOW ? EnumSet.range(PYRE, WENDIGRUDGE) : EnumSet.of(this);
        }
    }

    private final Kind kind;
    public BossSoulStoneItem(Kind kind) {
        super(new Properties().stacksTo(1).fireResistant());
        this.kind = kind;
    }
    public Kind kind() { return kind; }

    public static EnumSet<Kind> equipped(LivingEntity entity) {
        var abilities = EnumSet.noneOf(Kind.class);
        CuriosApi.getCuriosHelper().findCurios(entity, stack -> stack.getItem() instanceof BossSoulStoneItem)
                .forEach(slot -> abilities.addAll(((BossSoulStoneItem)slot.stack().getItem()).kind.abilities()));
        return abilities;
    }

    @Override
    public boolean canEquip(SlotContext slot, ItemStack stack) {
        var existing = equipped(slot.entity());
        existing.retainAll(kind.abilities());
        return existing.isEmpty();
    }

    @Override
    public Multimap<Attribute, AttributeModifier> getAttributeModifiers(SlotContext slot, UUID uuid, ItemStack stack) {
        Multimap<Attribute, AttributeModifier> result = LinkedHashMultimap.create();
        var abilities = kind.abilities();
        if (abilities.contains(Kind.TIMEWELDER)) add(result, Attributes.MOVEMENT_SPEED, uuid,
                BossSoulConfig.value("timewelder.move_speed"), AttributeModifier.Operation.MULTIPLY_BASE);
        if (abilities.contains(Kind.THRASHER)) add(result, ForgeMod.SWIM_SPEED.get(), uuid,
                BossSoulConfig.value("thrasher.swim_speed"), AttributeModifier.Operation.MULTIPLY_BASE);
        if (abilities.contains(Kind.SACILIC_ABOMINATION)) add(result, Attributes.ARMOR_TOUGHNESS, uuid,
                BossSoulConfig.value("crystal.toughness"), AttributeModifier.Operation.ADDITION);
        // Queen damage is applied once to actual owned-summon damage, including our temporary ants.
        return result;
    }

    private static void add(Multimap<Attribute, AttributeModifier> result, Attribute attribute, UUID uuid,
                            double amount, AttributeModifier.Operation operation) {
        result.put(attribute, new AttributeModifier(uuid, "wan_boss_soul", amount, operation));
    }

    @Override
    public void appendHoverText(ItemStack stack, @Nullable Level level, List<Component> tooltip, TooltipFlag flag) {
        for (var ability : kind.abilities()) {
            SoulTooltip.add(tooltip, Component.translatable("tooltip.wans_minego_expansion.foolish." + ability.key()));
            SoulTooltip.add(tooltip, Component.translatable("tooltip.wans_minego_expansion.foolish.stats." + ability.key(), stats(ability)));
        }
        SoulTooltip.add(tooltip, Component.translatable("tooltip.wans_minego_expansion.foolish_rules"));
    }

    private static Object[] stats(Kind ability) {
        String keys = switch(ability) {
            case PYRE -> "pyre.ignite_chance% pyre.ignite_seconds pyre.burning_bonus% pyre.fire_spell_bonus% pyre.fire_reduction%";
            case TIMEWELDER -> "timewelder.move_speed% timewelder.chance% timewelder.spell_chance% timewelder.shift% timewelder.duration timewelder.cooldown timewelder.refund_chance% timewelder.refund_ratio% timewelder.refund_cap timewelder.refund_cooldown";
            case THRASHER -> "thrasher.swim_speed% thrasher.water_bonus% thrasher.splash_ratio% thrasher.spell_ratio% thrasher.radius thrasher.targets thrasher.cooldown";
            case SACILIC_ABOMINATION -> "crystal.toughness crystal.reflect_flat crystal.reflect_ratio% crystal.reflect_cap crystal.reflect_cooldown crystal.stagger_chance% crystal.stagger_seconds crystal.stagger_cooldown";
            case VARMINT_KING -> "varmint.poison_seconds varmint.corrosion_chance% varmint.armor_loss% varmint.corrosion_seconds varmint.spell_bonus%";
            case THUNDERBIRD -> "thunderbird.chance% thunderbird.first_ratio% thunderbird.second_ratio% thunderbird.damage_cap thunderbird.cooldown thunderbird.speed% thunderbird.speed_seconds";
            case SCARLANT_QUEEN -> "queen.summon_bonus% queen.chance% queen.spell_chance% queen.max_ants queen.life_seconds queen.health queen.attack queen.cooldown";
            case TERRORFLORA -> "flora.chance% flora.nature_chance% flora.root_seconds flora.cooldown flora.heal_ratio% flora.heal_per_second";
            case WENDIGRUDGE -> "wraith.start_hp% wraith.peak_hp% wraith.bonus% wraith.heal wraith.heal_interval wraith.chance% wraith.ratio% wraith.damage_cap wraith.cooldown";
            case ASTRALIS -> "star.chance% star.spell_chance% star.ratio% star.damage_cap star.cooldown star.parry_chance% star.parry_reduction% star.parry_cooldown star.riposte_bonus% star.riposte_seconds";
            default -> "";
        };
        return java.util.Arrays.stream(keys.split(" ")).map(key -> {
            boolean percent=key.endsWith("%");double number=BossSoulConfig.value(percent?key.substring(0,key.length()-1):key)*(percent?100:1);
            return (Object)java.math.BigDecimal.valueOf(number).stripTrailingZeros().toPlainString();
        }).toArray();
    }
}
