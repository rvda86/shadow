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

</style>