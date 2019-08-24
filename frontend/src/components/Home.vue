<template>
  <div>
    <p>Home page</p>
    <p>Random number from backend: {{ randomNumber }}</p>
    <button @click="getRandom">New random number</button>
    <router-link to="/about"><a>about</a></router-link>
    <br>
    <router-link to="/tryaccess/login/user"><a>login</a></router-link>
    <br>
    <router-link to="/tryaccess/signup/user"><a>signup</a></router-link>
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
        });
    }
  },
  created () {
    this.getRandom();
  }
};
</script>
