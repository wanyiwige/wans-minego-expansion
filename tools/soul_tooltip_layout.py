"""Semantic line breaks for soul descriptions, preserving all numeric placeholders."""
ZH_STATS={
 'pyre':'点燃概率 %s%%，持续 %s秒\n燃烧目标增伤 %s%%（火法 %s%%）\n火焰伤害减免 %s%%',
 'timewelder':'移速 +%s%%\n时流触发 %s%%（法术 %s%%）\n加速／减速 %s%%，持续 %s秒\n时流冷却 %s秒\n回流触发 %s%%，返还 %s%%\n返还上限 %s 法力，冷却 %s秒',
 'thrasher':'游泳速度 +%s%%\n水中攻击增伤 %s%%\n冲击伤害 %s%%（法术 %s%%）\n范围 %s格，最多 %s目标\n冲击冷却 %s秒',
 'sacilic_abomination':'护甲韧性 +%s\n反伤 %s HP + 实际生命损失的 %s%%\n反伤上限 %s HP，冷却 %s秒\n晶震概率 %s%%，持续 %s秒\n晶震冷却 %s秒',
 'varmint_king':'中毒持续 %s秒\n腐蚀概率 %s%%\n腐蚀减少护甲 %s%%，持续 %s秒\n自然／污秽法术增伤 %s%%',
 'thunderbird':'电弧触发 %s%%\n两次电弧伤害分别为 %s%%、%s%%\n单次上限 %s HP，冷却 %s秒\n移速 +%s%%，持续 %s秒',
 'scarlant_queen':'所属召唤物伤害 +%s%%\n援军触发 %s%%（法术 %s%%）\n最多 %s只，存活 %s秒\n随从生命 %s HP，攻击 %s HP\n援军冷却 %s秒',
 'terrorflora':'缠绕触发 %s%%（自然 %s%%）\n缠绕持续 %s秒，冷却 %s秒\n按原始有效伤害的 %s%% 回血\n每秒最多恢复 %s HP',
 'wendigrudge':'生命低于 %s%% 时开始增伤\n生命 %s%% 时达到 %s%% 增伤\n恢复 %s HP，间隔 %s秒\n炮击概率 %s%%，伤害 %s%%\n炮击上限 %s HP，冷却 %s秒',
 'astralis':'星刃概率 %s%%（法术 %s%%）\n星刃伤害 %s%%，上限 %s HP\n星刃冷却 %s秒\n招架概率 %s%%，减伤 %s%%\n招架冷却 %s秒\n反击增伤 %s%%，持续 %s秒'}
def format_lang(data,lang):
    for key,text in list(data.items()):
        if not key.startswith('tooltip.wans_minego_expansion.'):continue
        if lang=='zh_cn':
            text=text.replace('，','\n').replace('；','\n').replace('。','\n').strip()
        else:
            text=text.replace('; ','\n').replace('. ','\n').replace(', +','\n+').strip()
            if '.foolish.stats.' in key:text=text.replace(' / ','\n')
        data[key]=text.strip('\n')
    if lang=='zh_cn':
        for boss,text in ZH_STATS.items():data['tooltip.wans_minego_expansion.foolish.stats.'+boss]=text
    return data

def main():
    from pathlib import Path
    from datetime import datetime
    import json,shutil
    root=Path(__file__).resolve().parents[1]
    backup=root/'backups'/('20261009-'+datetime.now().strftime('%H%M%S')+'-before-tooltip-layout')
    backup.mkdir(parents=True)
    for lang in ('zh_cn','en_us'):
        path=root/'src/main/resources/assets/wans_minego_expansion/lang'/(lang+'.json')
        shutil.copy2(path,backup/path.name)
        data=json.loads(path.read_text(encoding='utf-8'));format_lang(data,lang)
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Saved localized semantic tooltip line breaks; backup:',backup)
if __name__=='__main__':main()
