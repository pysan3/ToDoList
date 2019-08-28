<template>
  <div>
    <p>Home page</p>
    <h1>class for css, id for js</h1>
    <p>Random number from backend: {{ randomNumber }}</p>
    <button @click="getRandom">New random number</button>
    <router-link to="/about"><a>about</a></router-link>
    <br>
    <router-link to="/projects"><a>your projects</a></router-link>
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
      axios.get(this.base_url + '/api/random')
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
