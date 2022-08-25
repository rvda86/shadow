<template>
    <div class="card">
        <h2>Loading</h2>
        <font-awesome-icon class="load-spinner" icon="fa-solid fa-spinner" />
    </div>
</template>

<script>

export default {
    name: 'Preloader'
}

</script>

<style>

.load-spinner {
    animation: spin 1s infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}


</style>