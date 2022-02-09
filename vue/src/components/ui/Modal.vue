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

.backdrop {
    position: fixed;
    left: 0;
    top: 0;
    height: 100%;
    width: 100%;
    background-color: rgba(109, 109, 109, 0.8);
    z-index: 1
}
.modal {
    position: relative;
    display: flex;
    top: 20%;
    margin: auto;
    padding: 1em;
    max-width: 400px;
    background-color: white;
    z-index: 2
}

</style>