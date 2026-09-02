// JEI 隐藏：包内明确无法获得/已被禁用的物品（配合 remove.js 的配方清理）
// 原则：只藏“确定做不出来也没有其他用途”的，别误伤可用物品
RecipeViewerEvents.removeEntries('item', event => {
    const hidden = [
        // 末影之眼：无末影人/烈焰人来源，末影箱配方也早已移除
        'minecraft:ender_eye',

        // 注意：OEI 替换表里的原版源物品（iron_ingot 等）不能在这里隐藏！
        // OEI 是注册层替换，源物品在 JEI 里就是群峦物品本身，藏源 = 把群峦物品也藏掉。

        // 锻铁序列组装的中间产物：无正式译名，只在组装流程里出现（kubejs 命名空间，不受 OEI 影响，可安全隐藏）
        'kubejs:unfinished_wrought_iron',

        // 航空学把手全系（铁/铜/16 染色）：配方已禁，藏掉避免误导
        /simulated:.*handle.*/,

        // 压块模具：配套的两条压块配方（9锭压1块血亏）已删，模具本身也藏掉
        'tfc_ie_addon:mold_block',

        // 引擎总成及其中间产物：便携引擎已改为直接合成，序列组装配方已删，这两件已无用途
        'simulated:engine_assembly',
        'simulated:incomplete_engine_assembly',

        // 冲压机：功能在包内完全用不上，配方已在 aerospace.js 删除
        'tfc_aeronautics:stamping_press',

        // 木质讲台全系（TFC/AFC/Beneath）：已统一为原版讲台（lectern_unify.js），旧存档里的不受影响
        /^(tfc|afc|beneath):wood\/lectern\/.*/,

        // Create Tracks 的中型/大型履带与驱动轮：模组作者连续两个版本均以 neoforge:false 禁用
        //（物理尚未完工），无可合成配方，藏掉避免"搜得到做不出"
        'tracks:suspension_track',
        'tracks:large_suspension_track',
        'tracks:track_drive_wheel',
        'tracks:large_track_drive_wheel'
    ]

    hidden.forEach(id => event.remove(id))
})
