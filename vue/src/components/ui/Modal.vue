<template>
    <div class="backdrop" @click="cancelHandler">
        
        <div class="modal flex" @click="dontCancelHandler">
            <h5>Are you sure?</h5>
            <p class="small-font">This cannot be undone</p>
            <div class="flex-row">
                <button class="button" @click="cancelHandler">Cancel</button>
                <button class="button background-red" @click="confirmHandler">Yes</button>
            </div>
        </div>

    </div>
</template>

<script>

import { mapState, mapMutations } from 'vuex'

export default {
    name: 'Modal',
    data() {
        return {
            dontCancel: false
        }
    },
    computed: {
        ...mapState(["modalPayload"])
    },
    methods: {
        ...mapMutations(["toggleModal", "resetModalPayload"]),
        cancelHandler() {
            if (!this.dontCancel) {
                this.toggleModal()
                this.resetModalPayload()                
            }
            this.dontCancel = false
        },
        dontCancelHandler() {
            this.dontCancel = true
        },
        confirmHandler() {
            this.toggleModal()
            this.modalPayload.func(this.modalPayload.payload)
            this.resetModalPayload()
        }
    }
}

</script>

<style>
</style>