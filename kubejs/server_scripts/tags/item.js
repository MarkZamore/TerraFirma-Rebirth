ServerEvents.tags('item', event => {
    //将原版铁锭移除铸铁标签，以防配方认为锻铁锭也是铸铁锭
    event.remove('c:ingots/cast_iron', 'minecraft:iron_ingot')

    //OEI统一材料后，让c标签也认群峦金属（火箭推进器等tag配方用）
    event.add('c:ingots/iron', 'tfc:metal/ingot/wrought_iron')
    event.add('c:ingots/copper', 'tfc:metal/ingot/copper')
    event.add('c:ingots/gold', 'tfc:metal/ingot/gold')
    event.add('c:plates/iron', 'tfc:metal/sheet/wrought_iron')

    //c:storage_blocks/gold和copper TFC自己注册过了，补一个iron（金/钻石升级等tag配方用）
    event.add('c:storage_blocks/iron', 'tfc:metal/block/wrought_iron')

    event.add('c:rods/wooden', [
        'afc:wood/twig/black_oak',
        'afc:wood/twig/rainbow_eucalyptus',
        'afc:wood/twig/redcedar',
        'afc:wood/twig/rubber_fig',
        'afc:wood/twig/poplar'
    ])

    event.add('tfc:glassdusts/iron', [
        'tfc:powder/limonite',
        'tfc:powder/magnetite',
        'tfc:powder/hematite'
    ])
    
    event.add('tfc:glassdusts/copper', [
        'tfc:powder/malachite',
        'tfc:powder/native_copper',
        'tfc:powder/tetrahedrite'
    ])

    // tfcr tags removed - mod not installed
    // event.add('tfcr:powdered_milk', [
    //     'artisanal:powdered_milk',
    //     'artisanal:powdered_goat_milk',
    //     'artisanal:powdered_yak_milk'
    // ])

    event.add('create:pulpifiable','immersiveengineering:dust_wood')

    //添加海带tag
    event.add('tfc:plants/kelp', ['tfc:plant/leafy_kelp', 'tfc:plant/winged_kelp', 'tfc:plant/laminaria'])

    //添加珊瑚tag（tree_fertilizer 配方用，1.21 无内置 c:coral）
    event.add('c:coral', [
        'minecraft:tube_coral',
        'minecraft:brain_coral',
        'minecraft:bubble_coral',
        'minecraft:fire_coral',
        'minecraft:horn_coral',
        'minecraft:tube_coral_fan',
        'minecraft:brain_coral_fan',
        'minecraft:bubble_coral_fan',
        'minecraft:fire_coral_fan',
        'minecraft:horn_coral_fan'
    ])

    // tfc_coldsweat 2.1.2 无 magma/cursed 物品，相关 tag 条目已删除

    //添加afc树苗造纸标签
    event.add('create:pulpifiable', /sapling/)

    // tfcr tag removed
    // event.add('tfcr:dirty_pile_dust', /dirty_pile/)

    event.add('kubejs:latex_logs', [
        "tfc:wood/log/kapok",
        "afc:wood/log/hevea",
        "afc:wood/log/rubber_fig",
        "tfc:wood/log/palm"
    ])

    //群峦圆石标签（侦测器等红石元件配方用，TFC 挖矿基础石料）
    event.add('kubejs:cobbles', /tfc:rock\/cobble\/.+/)

    // Astikor 马车全家桶标签（任务书提交用，覆盖 34 种 TFC 木变体）
    event.add('kubejs:cart_wheels', /tfcastikorcarts:wheel\/.+/)
    event.add('kubejs:hand_carts', /tfcastikorcarts:hand_cart\/.+/)
    event.add('kubejs:animal_carts', /tfcastikorcarts:animal_cart\/.+/)
    event.add('kubejs:supply_carts', /tfcastikorcarts:supply_cart\/.+/)
    event.add('kubejs:plow_carts', /tfcastikorcarts:plow\/.+/)
    event.add('kubejs:reaper_carts', /tfcastikorcarts:reaper\/.+/)
    event.add('kubejs:seed_drills', /tfcastikorcarts:seed_drill\/.+/)

    event.add('ktfcc:stockpot_ingredient', [
        "farmersdelight:minced_beef",
        "farmersdelight:chicken_cuts",
        "farmersdelight:bacon",
        "farmersdelight:cod_slice",
        "farmersdelight:salmon_slice",
        "farmersdelight:mutton_chops",
        "farmersdelight:ham",
        "farmersdelight:smoked_ham",
        "farmersdelight:raw_pasta",
        "farmersdelight:pumpkin_slice"
    ])

    event.add('ktfcc:pot_ingredient', [
        "farmersdelight:minced_beef",
        "farmersdelight:chicken_cuts",
        "farmersdelight:bacon",
        "farmersdelight:cod_slice",
        "farmersdelight:salmon_slice",
        "farmersdelight:mutton_chops",
        "farmersdelight:ham",
        "farmersdelight:smoked_ham",
        "farmersdelight:raw_pasta",
        "farmersdelight:pumpkin_slice"
    ])

    event.remove('firmalife:foods/washable', 'minecraft:pumpkin_pie', "firmalife:food/raw_pumpkin_pie")

    event.add('farmerstfc:cant_place_when_rotten', "cold_sweat:soul_sprout")

    //AFC 的传动轴/离合器等木质功能方块没注册进 TFC 对应物品标签，补齐（只有这14种木材有全套机械木块）
    const afcMechWoods = ['araucaria', 'baobab', 'beech', 'cypress', 'eucalyptus', 'fig', 'ginkgo', 'hevea', 'ipe', 'ironwood', 'mahoe', 'mahogany', 'teak', 'tualang']
    const afcMechTags = {
        'tfc:axles': 'axle',
        'tfc:clutches': 'clutch',
        'tfc:gear_boxes': 'gear_box',
        'tfc:looms': 'loom',
        'tfc:scribing_tables': 'scribing_table',
        'tfc:sewing_tables': 'sewing_table',
        'tfc:sluices': 'sluice',
        'tfc:tool_racks': 'tool_rack',
        'tfc:water_wheels': 'water_wheel'
    }
    Object.keys(afcMechTags).forEach(tag => {
        const type = afcMechTags[tag]
        event.add(tag, afcMechWoods.map(w => 'afc:wood/' + type + '/' + w))
    })
})
