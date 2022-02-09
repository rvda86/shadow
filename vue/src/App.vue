<template>
    <Preloader v-if="!dataIsLoaded && authenticated" />
    <Layout v-if="(dataIsLoaded && authenticated) || !authenticated">
        <router-view></router-view>
    </Layout>
</template>

<script>

import { mapState, mapActions } from 'vuex'

import Layout from './components/layout/Layout.vue'
import Preloader from './components/ui/Preloader.vue'

export default {
  name: 'App',
  components: {
      Layout,
      Preloader
  },
  computed: {
    ...mapState(["dataIsLoaded", "authenticated"])
  },
  methods: {
    ...mapActions(["fetchDataRequest"])
  },
  created() {
      if (!this.dataLoaded && this.authenticated) {
          this.fetchDataRequest()
      }
    }
}

</script>
