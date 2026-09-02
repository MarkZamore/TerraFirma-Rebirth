ServerEvents.recipes(event => {
    /**
     * 
     * @param {Internal.ItemStack_[]} result 
     * @param {Ingredient_[]} ingredients 
     * @param {"axe_dig" | "pickaxe_dig" | Ingredient_} tool 
     * @returns {Internal.RecipeJS_}
     */
    function cutting(result, ingredients, tool) {
        return event.custom(cutting_json(result, ingredients, tool))
    }
    
    const {create} = event.recipes

    afc_wood.forEach(wood => {
        create.cutting([`afc:wood/stripped_log/${wood}`, "farmersdelight:tree_bark"], `afc:wood/log/${wood}`)
        .id(`tfc:lumber_cut/create/cutting/${wood}_log`)
        
        create.cutting([`afc:wood/stripped_wood/${wood}`, "farmersdelight:tree_bark"], `afc:wood/wood/${wood}`)
        .id(`tfc:lumber_cut/create/cutting/${wood}_wood`)

        create.cutting(`12x afc:wood/lumber/${wood}`, `afc:wood/stripped_log/${wood}`)
        .id(`tfc:lumber_cut/create/cutting/${wood}_from_stripped_log`)

        create.cutting(`12x afc:wood/lumber/${wood}`, `afc:wood/stripped_wood/${wood}`)
        .id(`tfc:lumber_cut/create/cutting/${wood}_from_stripped_wood`)

        cutting([`afc:wood/stripped_log/${wood}`, "farmersdelight:tree_bark"], `afc:wood/log/${wood}`, "axe_dig")
        .id(`tfc:lumber_cut/farmersdelight/cutting/${wood}_log`)
        
        cutting([`afc:wood/stripped_wood/${wood}`, "farmersdelight:tree_bark"], `afc:wood/wood/${wood}`, "axe_dig")
        .id(`tfc:lumber_cut/farmersdelight/cutting/${wood}_wood`)
    })
    
    tfc_wood.forEach(wood => {
        create.cutting([`tfc:wood/stripped_log/${wood}`, "farmersdelight:tree_bark"], `tfc:wood/log/${wood}`)
        .id(`tfc:lumber_cut/create/cutting/${wood}_log`)

        create.cutting([`tfc:wood/stripped_wood/${wood}`, "farmersdelight:tree_bark"], `tfc:wood/wood/${wood}`)
        .id(`tfc:lumber_cut/create/cutting/${wood}_wood`)

        create.cutting(`12x tfc:wood/lumber/${wood}`, `tfc:wood/stripped_log/${wood}`)
        .id(`tfc:lumber_cut/create/cutting/${wood}_from_stripped_log`)

        create.cutting(`12x tfc:wood/lumber/${wood}`, `tfc:wood/stripped_wood/${wood}`)
        .id(`tfc:lumber_cut/create/cutting/${wood}_from_stripped_wood`)

        cutting([`tfc:wood/stripped_log/${wood}`, "farmersdelight:tree_bark"], `tfc:wood/log/${wood}`, "axe_dig")
        .id(`tfc:lumber_cut/farmersdelight/cutting/${wood}_log`)

        cutting([`tfc:wood/stripped_wood/${wood}`, "farmersdelight:tree_bark"], `tfc:wood/wood/${wood}`, "axe_dig")
        .id(`tfc:lumber_cut/farmersdelight/cutting/${wood}_wood`)
    })

    //AFC"次级树种"（无去皮原木变体，官方设定为映射到主树种的木料）：动力锯/砧板一步出对应木料+树皮
    //产出率与主树种两步路径一致（1原木 = 12木料 + 1树皮），映射关系同AFC官方合成配方
    const afc_alias_lumber = {
        'gum_arabic': 'tfc:wood/lumber/acacia',
        'kauri': 'afc:wood/lumber/araucaria',
        'poplar': 'tfc:wood/lumber/aspen',
        'redcedar': 'afc:wood/lumber/cypress',
        'rainbow_eucalyptus': 'afc:wood/lumber/eucalyptus',
        'rubber_fig': 'afc:wood/lumber/fig',
        'black_oak': 'tfc:wood/lumber/oak'
    }
    Object.keys(afc_alias_lumber).forEach(wood => {
        const lumber = afc_alias_lumber[wood]
        create.cutting([`12x ${lumber}`, "farmersdelight:tree_bark"], `afc:wood/log/${wood}`)
        .id(`tfc:lumber_cut/create/cutting/${wood}_alias_log`)

        create.cutting([`12x ${lumber}`, "farmersdelight:tree_bark"], `afc:wood/wood/${wood}`)
        .id(`tfc:lumber_cut/create/cutting/${wood}_alias_wood`)

        cutting([`12x ${lumber}`, "farmersdelight:tree_bark"], `afc:wood/log/${wood}`, "axe_dig")
        .id(`tfc:lumber_cut/farmersdelight/cutting/${wood}_alias_log`)

        cutting([`12x ${lumber}`, "farmersdelight:tree_bark"], `afc:wood/wood/${wood}`, "axe_dig")
        .id(`tfc:lumber_cut/farmersdelight/cutting/${wood}_alias_wood`)
    })

    //Beneath 下界木（绯红/诡异菌木）：砧板与动力锯切割补齐，规格与 TFC/AFC 完全一致
    //（1原木 = 12木料 + 1树皮；去皮两条路都给）
    const beneath_wood = ['crimson', 'warped']
    beneath_wood.forEach(wood => {
        create.cutting([`beneath:wood/stripped_log/${wood}`, "farmersdelight:tree_bark"], `beneath:wood/log/${wood}`)
        .id(`tfc:lumber_cut/create/cutting/beneath_${wood}_log`)

        create.cutting([`beneath:wood/stripped_wood/${wood}`, "farmersdelight:tree_bark"], `beneath:wood/wood/${wood}`)
        .id(`tfc:lumber_cut/create/cutting/beneath_${wood}_wood`)

        create.cutting(`12x beneath:wood/lumber/${wood}`, `beneath:wood/stripped_log/${wood}`)
        .id(`tfc:lumber_cut/create/cutting/beneath_${wood}_from_stripped_log`)

        create.cutting(`12x beneath:wood/lumber/${wood}`, `beneath:wood/stripped_wood/${wood}`)
        .id(`tfc:lumber_cut/create/cutting/beneath_${wood}_from_stripped_wood`)

        cutting([`beneath:wood/stripped_log/${wood}`, "farmersdelight:tree_bark"], `beneath:wood/log/${wood}`, "axe_dig")
        .id(`tfc:lumber_cut/farmersdelight/cutting/beneath_${wood}_log`)

        cutting([`beneath:wood/stripped_wood/${wood}`, "farmersdelight:tree_bark"], `beneath:wood/wood/${wood}`, "axe_dig")
        .id(`tfc:lumber_cut/farmersdelight/cutting/beneath_${wood}_wood`)
    })
})
