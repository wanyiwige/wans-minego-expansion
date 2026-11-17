# Foolish BOSS魂石贴图

共10张，采用已有魂石的宝石轮廓、左上高光和8×8中心符纹。
原生贴图统一18×18 RGBA，透明度仅0/255。外圈、符纹、高光均共用同一像素网格。

- native-18px：原生PNG，与源码textures/item内同名文件一致。
- preview-1260px：70倍最近邻放大，便于检查；不是额外细节。
- foolish-boss-stones-preview.png：带中文名称的十张总览。
- manifest.json：对应Boss、配色、符纹及哈希。

仅新增贴图，未注册新物品、修改旧学派贴图、构建或部署JAR。
绘制方式：复用现有Python像素绘制脚本；前次AI生成图不作为最终资产。
