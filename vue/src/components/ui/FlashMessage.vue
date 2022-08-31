<template>

    <div class="flash-message">
        <p class="small-font"><strong>{{ flashMessage }}</strong></p>
    </div>

</template>

<script>

import { mapState } from 'vuex'

export default {
    name: 'FlashMessage',
    computed: {
        ...mapState(["flashMessage", "showFlashMessage", "flashMessageSuccess"])
    }
}
</script>

<style>

.flash-message {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background-color: white;
    padding: 20px;
}

</style>