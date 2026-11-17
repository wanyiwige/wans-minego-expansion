package cn.wanyiwige.minego;

import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.damagesource.DamageType;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraftforge.event.entity.living.LivingDamageEvent;
import net.minecraftforge.event.entity.living.LivingHurtEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.registries.RegistryObject;
import net.minecraftforge.registries.ForgeRegistries;
import top.theillusivec4.curios.api.CuriosApi;

public final class SoulStoneEvents {
    private static final ResourceKey<DamageType> INSECT = damage("entomology_spell:insect_magic");
    private static final ResourceKey<DamageType> DREAM = damage("dreammagic:dream_magic");
    private static final ResourceKey<DamageType> WIND = damage("wind_spellbooks:wind_magic");
    private static final ResourceKey<DamageType> SHADOW = damage("bielgg_spells:shadow_magic");
    private static final ResourceKey<DamageType> UNSTABLE = damage("bielgg_spells:unstable_magic");
    private static final ResourceKey<DamageType> RELICRON = damage("bielgg_spells:relicron_magic");
    private static final ResourceKey<DamageType> ANNIHILATION = damage("legendary_monsters:void");
    private static final ResourceKey<DamageType> INFINITY = damage("bielgg_spells:infinity_magic");
    private static final ResourceKey<DamageType> TAINTED = damage("bielgg_spells:tainted_magic");

    private SoulStoneEvents() {}

    @SubscribeEvent
    public static void onHurt(LivingHurtEvent event) {
        if (event.getEntity().level().isClientSide() || BossSoulEvents.secondary(event.getSource())) return;
        if (!(event.getSource().getEntity() instanceof Player player) || player == event.getEntity()) return;
        if (event.getSource().is(damage("iss_magicfromtheeast:symmetry_magic")) && has(player, SoulStoneItems.SYMMETRY)) {
            event.setAmount((float) (event.getAmount() * (1.0 + SoulStoneConfig.SYMMETRY_DAMAGE.get())));
        }
        if (event.getSource().is(UNSTABLE) && has(player, SoulStoneItems.UNSTABLE)
                && player.getRandom().nextDouble() < 0.20) {
            event.setAmount(event.getAmount() * 1.20F);
        }
        if (event.getSource().is(ANNIHILATION) && has(player, SoulStoneItems.ANNIHILATION)
                && event.getEntity().getHealth() <= event.getEntity().getMaxHealth() * 0.30F) {
            event.setAmount(event.getAmount() * 1.08F);
        }
        if (event.getSource().is(INFINITY) && has(player, SoulStoneItems.INFINITY)) {
            event.setAmount(event.getAmount() * 1.05F);
        }
    }

    @SubscribeEvent
    public static void onDamage(LivingDamageEvent event) {
        LivingEntity target = event.getEntity();
        if (target.level().isClientSide() || event.getAmount() <= 0 || BossSoulEvents.secondary(event.getSource())) return;
        if (!(event.getSource().getEntity() instanceof Player player) || player == target) return;
        if (event.getSource().is(damage("iss_magicfromtheeast:spirit_magic")) && has(player, SoulStoneItems.SPIRIT)) {
            int seconds = SoulStoneConfig.SPIRIT_BURN_SECONDS.get();
            if (seconds > 0 && target.isAlive()) {
                var soulburn = ForgeRegistries.MOB_EFFECTS.getValue(new ResourceLocation("iss_magicfromtheeast:soulburn"));
                if (soulburn != null) target.addEffect(new MobEffectInstance(soulburn, seconds * 20, 0));
            }
            player.heal((float) (event.getAmount() * SoulStoneConfig.SPIRIT_HEAL.get()));
        }
        if (event.getSource().is(INSECT) && has(player, SoulStoneItems.INSECT)) {
            target.addEffect(new MobEffectInstance(MobEffects.POISON, 60, 0));
        }
        if (event.getSource().is(DREAM) && has(player, SoulStoneItems.DREAM)) {
            target.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 80, 0));
        }
        if (event.getSource().is(WIND) && has(player, SoulStoneItems.WIND)) {
            player.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 100, 0));
        }
        if (event.getSource().is(SHADOW) && has(player, SoulStoneItems.SHADOW)) {
            player.heal(event.getAmount() * 0.03F);
            target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 0));
        }
        if (event.getSource().is(RELICRON) && has(player, SoulStoneItems.RELICRON)) {
            player.addEffect(new MobEffectInstance(MobEffects.ABSORPTION, 100, 0));
        }
        if (event.getSource().is(TAINTED) && has(player, SoulStoneItems.TAINTED)) {
            target.addEffect(new MobEffectInstance(MobEffects.WITHER, 60, 0));
        }
        if (event.getSource().is(damage("cursespells:curse_magic")) && has(player, SoulStoneItems.CURSE)) {
            target.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 60, 0));
        }
        if (event.getSource().is(damage("echo_spellbooks:echo_magic")) && has(player, SoulStoneItems.ECHO)) {
            target.addEffect(new MobEffectInstance(MobEffects.GLOWING, 80, 0));
        }
        if (event.getSource().is(damage("alex_caves_spellsbook:toxic_magic")) && has(player, SoulStoneItems.TOXIC)) {
            target.addEffect(new MobEffectInstance(MobEffects.POISON, 60, 0));
        }
    }

    private static ResourceKey<DamageType> damage(String id) {
        return ResourceKey.create(Registries.DAMAGE_TYPE, new ResourceLocation(id));
    }

    private static boolean has(Player player, RegistryObject<Item> stone) {
        return stone != null && stone.isPresent() && CuriosApi.getCuriosHelper().findFirstCurio(player, stone.get()).isPresent();
    }
}
