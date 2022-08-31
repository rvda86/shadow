<template>
    <div class="backdrop">
        
        <div class="modal flex">
            <h5>Are you sure?</h5>
            <div class="flex-row">
                <button class="button" @click="cancelHandler">Cancel</button>
                <button class="button" @click="confirmHandler">Confirm</button>
            </div>
        </div>

    </div>
</template>

<script>

import { mapState, mapMutations } from 'vuex'

export default {
    name: 'Modal',
    computed: {
        ...mapState(["modalPayload"])
    },
    methods: {
        ...mapMutations(["toggleModal", "resetModalPayload"]),
        cancelHandler() {
            this.toggleModal()
            this.resetModalPayload()
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