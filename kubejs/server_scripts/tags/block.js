ServerEvents.tags('block', event => {
    event.add('kubejs:cranks', [
        "create:hand_crank",
        "create_connected:crank_wheel",
        "create_connected:large_crank_wheel"
    ])

    event.add('afc:tappable_logs', [
        "tfc:wood/log/kapok",
        "tfc:wood/log/palm"
    ])

    event.add('farmerstfc:magma_block', [
        "tfc:rock/magma/granite",
        "tfc:rock/magma/diorite",
        "tfc:rock/magma/gabbro",
        "tfc:rock/magma/basalt",
        "tfc:rock/magma/andesite",
        "tfc:rock/magma/dacite"
    ])

    event.add('ktfcc:heat_source', [
        "tfc:rock/magma/granite",
        "tfc:rock/magma/diorite",
        "tfc:rock/magma/gabbro",
        "tfc:rock/magma/basalt",
        "tfc:rock/magma/andesite",
        "tfc:rock/magma/dacite"
    ])

    // AE2 tag已移除
    // event.add('ae2:growth_acceleratable', "tfc_ie_addon:mineral/budding_quartz")

    event.add('functionalstorage:drawer', /functionalstorage:tfc_/)

    // 让机械动力动态结构（轴承/活塞/列车等）识别 TFC/AFC 木箱为挂载存储
    // Create 默认只认原版箱子/木桶/潜影盒；simple_mounted_storage 靠方块实体的物品能力工作，
    // TFC 箱子已注册该能力（漏斗可正常交互），挂上标签即可被收割机/动力锯等自动存入
    const tfcChests = ['acacia', 'ash', 'aspen', 'birch', 'blackwood', 'chestnut', 'douglas_fir',
        'hickory', 'kapok', 'mangrove', 'maple', 'oak', 'palm', 'pine', 'rosewood', 'sequoia',
        'spruce', 'sycamore', 'white_cedar', 'willow']
        .flatMap(w => [`tfc:wood/chest/${w}`, `tfc:wood/trapped_chest/${w}`])
    const afcChests = ['araucaria', 'baobab', 'beech', 'cypress', 'eucalyptus', 'fig', 'ginkgo',
        'hevea', 'ipe', 'ironwood', 'mahoe', 'mahogany', 'teak', 'tualang']
        .flatMap(w => [`afc:wood/chest/${w}`, `afc:wood/trapped_chest/${w}`])
    event.add('create:simple_mounted_storage', tfcChests.concat(afcChests))

    // Beneath 下界原木标签修复：模组自身的 warped_logs 标签写成了绯红内容（复制粘贴 bug），
    // 导致诡异原木完全不在 #minecraft:logs 里，群峦斧子无法识别砍伐；矿斧标签也只登记了家具没登记原木。
    const netherLogs = ['crimson', 'warped']
        .flatMap(w => [`beneath:wood/log/${w}`, `beneath:wood/wood/${w}`,
            `beneath:wood/stripped_log/${w}`, `beneath:wood/stripped_wood/${w}`])
    event.add('minecraft:logs', netherLogs)
    event.add('minecraft:mineable/axe', netherLogs)
    event.add('beneath:warped_logs', [
        'beneath:wood/log/warped', 'beneath:wood/wood/warped',
        'beneath:wood/stripped_log/warped', 'beneath:wood/stripped_wood/warped'
    ])
})
