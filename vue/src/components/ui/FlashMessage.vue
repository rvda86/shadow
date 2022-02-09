<template>

    <div class="card">
        <p>{{ flashMessage }}</p>
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