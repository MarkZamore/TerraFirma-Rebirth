BlockEvents.rightClicked(event => {
    const {block, item, hand, player} = event
    
    /**
     * 
     * @param {string} id 
     * @returns 
     */
    function packBlock(id) {
        if(hand.name() != 'MAIN_HAND') return
        if(block.id != id) return
        if(item.hasTag('minecraft:shovels') || item.hasTag('tfcsuperhammer:supershovels')) {
            block.set('air')
            player.give(id)
            item.hurtAndBreak(10, player, p => {})
            event.success()
            event.cancel()
        }
    }

    packBlock("tfc:firepit")
    packBlock("tfc:pot")
})