<template lang="">
  <div class="user-list-page">
    <Header />
    <h2>Tus Configuraciones</h2>
    
  </div>
</template>

<script>
import Header from "../components/Header.vue";

export default {
  data() {
    return {
      movies: []
    }
  },
  components: {
    Header,
  },
  methods: {
  },
}
</script>