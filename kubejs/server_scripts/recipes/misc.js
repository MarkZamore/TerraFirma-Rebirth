ServerEvents.recipes(event => {
    //起落架配方适配
    // immersive_aircraft items do not exist
    // event.replaceInput({output:"immersive_aircraft:improved_landing_gear"}, "minecraft:coal", "#minecraft:coals")
    //风帆配方适配
    // event.replaceInput({output:"immersive_aircraft:sail"}, "minecraft:string", "#forge:string")

    // create_new_age 已移除（电力系统换代为 Electro Energetics），thorium_multiplication 适配随之删除

    event.replaceInput({}, "minecraft:furnace", "farmersdelight:stove")
    event.replaceInput({}, "minecraft:blast_furnace", "farmersdelight:stove")
    event.replaceInput({}, "minecraft:stone", '#c:stones')

    //所有配方里的原版木棍统一换成群峦木棍标签（TFC/AFC/Beneath树枝、IE防腐木棍都认）
    event.replaceInput({}, 'minecraft:stick', '#c:rods/wooden')

    // ender_chest配方已移除（依赖MEK teleportation_core）
    // event.replaceInput({id: 'minecraft:ender_chest'}, "minecraft:ender_eye", "mekanism:teleportation_core")

    //蒸笼适配：竹块/竹活板门和金竹都能做
    event.remove({id: 'kaleidoscope_cookery:steamer'})
    event.shaped('kaleidoscope_cookery:steamer', ['TTT', 'BBB'], {
        B: ['minecraft:bamboo_block', 'tfc:plant/golden_bamboo'],
        T: ['minecraft:bamboo_trapdoor', 'tfc:plant/golden_bamboo']
    }).id('kubejs:crafting/steamer')

    //森罗砂锅海带配方：原版海带在群峦世界不存在，换成群峦海带标签
    event.replaceInput({mod: 'kaleidoscope_cookery'}, 'minecraft:kelp', '#tfc:plants/kelp')

    //金竹块也能上砧板：砍出草杆（对标农夫乐事的竹块切割，金竹块没有去皮变体，多给一个草杆）
    //草杆是栓绳的原料，金竹从此也能做栓绳
    event.custom({
        type: 'farmersdelight:cutting',
        ingredients: [{item: 'tfc:golden_bamboo_block'}],
        result: [{item: {count: 2, id: 'farmersdelight:straw'}}],
        sound: {sound_id: 'minecraft:item.axe.strip'},
        tool: [
            {type: 'farmersdelight:item_ability', action: 'axe_strip'},
            {tag: 'minecraft:axes'}
        ]
    }).id('kubejs:cutting/golden_bamboo_block')

    //带支撑的土（firmalifehardcore 窖藏/地下农场建材，模组本身没给配方）：
    //木材四角+对应土壤。梁变体没有物品形态（方块才有，模组未注册物品），无法做合成配方。
    const flhcSoils = ['entisol', 'aridisol', 'oxisol', 'fluvisol', 'andisol', 'podzol', 'alfisol', 'mollisol']
    flhcSoils.forEach(soil => {
        event.shaped(`2x firmalifehardcore:reinforced_${soil}`, [
            'L L',
            ' D ',
            'L L'
        ], {
            L: '#tfc:lumber',
            D: `tfc:dirt/${soil}`
        }).id(`kubejs:crafting/reinforced_${soil}`)
    })
})
