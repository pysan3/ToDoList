<template>
  <div>
    <p>User page</p>
    <p>Random number from backend: {{ randomNumber }}</p>
    <button @click="getRandom">New random number</button>
    <router-link to="/about"><a>about</a></router-link>
    <router-link to="/musiclist"><a>musiclist</a></router-link>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
export default {
  data () {
    return {
      randomNumber: 0
    };
  },
  computed: mapState([
    'base_url'
  ]),
  methods: {
    getRandom () {
      const path = this.base_url + '/api/random';
      axios.get(path)
        .then(response => {
          this.randomNumber = response.data.randomNumber;
        })
        .catch(error => {
          console.log(error);
        })
    }
  },
  created () {
    this.$store.dispatch('logged_in', 'user');
    this.getRandom();
  }
};
</script>
