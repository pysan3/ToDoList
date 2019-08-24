<template>
  <div class="projects">
    <h2>{{ user_name }}</h2>
    <ul>
      <li v-for="project in projects" :key="project.name">
        <router-link v-bind:to="{name: 'directory', params: {project: project.name}}">{{ project.name }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import Axios from 'axios';

export default {
  data () {
    return {
      user_name: '',
      projects: []
    }
  },
  computed: mapState([
    'token',
    'base_url'
  ]),
  methods: {
    load_projects () {
      Axios.post(this.base_url + '/api/loadproject', {
        token: this.token
      }).then(resp => {
        if (resp.data.valid === '1') {
          this.user_name = resp.data.user_name;
          this.projects = resp.data.projects;
          this.comment.splice();
        } else {
          alert('wrong access');
          this.$store.dispatch('logged_in', 'projects');
        }
      }).catch(error => {
        console.log(error);
      });
    }
  },
  created () {
    this.load_projects();
  }
}
</script>