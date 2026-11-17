package cn.wanyiwige.minego;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.core.BlockPos;
import net.minecraft.client.model.SilverfishModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid=WansMinegoExpansion.MOD_ID,bus=Mod.EventBusSubscriber.Bus.MOD,value=Dist.CLIENT)
public final class BossSoulClient {
    @SubscribeEvent public static void renderers(EntityRenderersEvent.RegisterRenderers event){
        if(BossSoulEntities.ANT!=null && BossSoulEntities.ANT.isPresent())event.registerEntityRenderer(BossSoulEntities.ANT.get(),AntRenderer::new);
        if(BossSoulEntities.BOLT!=null && BossSoulEntities.BOLT.isPresent())event.registerEntityRenderer(BossSoulEntities.BOLT.get(),BoltRenderer::new);
    }
    private static final class AntRenderer extends MobRenderer<SoulAntEntity,SilverfishModel<SoulAntEntity>> {
        AntRenderer(EntityRendererProvider.Context context){super(context,new SilverfishModel<>(context.bakeLayer(ModelLayers.SILVERFISH)),.3f);}
        @Override public ResourceLocation getTextureLocation(SoulAntEntity entity){return new ResourceLocation(WansMinegoExpansion.MOD_ID,"textures/entity/soul_ant.png");}
    }
    private static final class BoltRenderer extends EntityRenderer<SoulBoltEntity> {
        BoltRenderer(EntityRendererProvider.Context context){super(context);}
        @Override protected int getBlockLightLevel(SoulBoltEntity entity,BlockPos pos){return 15;}
        @Override public ResourceLocation getTextureLocation(SoulBoltEntity entity){
            return new ResourceLocation(WansMinegoExpansion.MOD_ID,"textures/entity/"+(entity.crystal()?"soul_bloom":entity.star()?"soul_star":"soul_wraith")+".png");
        }
        @Override public void render(SoulBoltEntity entity,float yaw,float partial,PoseStack pose,MultiBufferSource buffers,int light){
            pose.pushPose();pose.mulPose(entityRenderDispatcher.cameraOrientation());pose.scale(.65f,.65f,.65f);
            var vertex=buffers.getBuffer(RenderType.entityCutoutNoCull(getTextureLocation(entity)));
            var transform=pose.last();
            corner(vertex,transform,-.5f,-.5f,0,1,light);corner(vertex,transform,.5f,-.5f,1,1,light);
            corner(vertex,transform,.5f,.5f,1,0,light);corner(vertex,transform,-.5f,.5f,0,0,light);
            pose.popPose();super.render(entity,yaw,partial,pose,buffers,light);
        }
        private static void corner(VertexConsumer out,PoseStack.Pose pose,float x,float y,float u,float v,int light){
            out.vertex(pose.pose(),x,y,0).color(255,255,255,255).uv(u,v).overlayCoords(OverlayTexture.NO_OVERLAY)
                .uv2(light).normal(pose.normal(),0,0,1).endVertex();
        }
    }
    private BossSoulClient(){}
}
