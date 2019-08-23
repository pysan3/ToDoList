<template>
  <div class="directory">
    <div class="inventory">
      <p>{{ user_name }}</p>
      <ul>
        <li v-for="(item, index) in comment" :key="index">
          <this-file :comment="item"/>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import Axios from 'axios';
import ThisFile from '@/components/ThisFile'

export default {
  components: {
    ThisFile
  },
  data () {
    return {
      'comment': [],
      'user_name': ''
    }
  },
  computed: mapState([
    'token',
    'base_url'
  ]),
  methods: {
    load_files () {
      Axios.post(this.base_url + '/api/loadfile', {
        token: this.token
      }).then(resp => {
        if (resp.data.valid === '1') {
          this.comment = resp.data.comment;
          this.user_name = resp.data.user_name;
          this.comment.splice();
        } else {
          alert('wrong access');
          window.location.href = '/tryaccess/login/' + 'directory';
        }
      }).catch(error => {
        console.log(error);
      });
    }
  },
  created () {
    this.$store.dispatch('logged_in', 'user');
    this.load_files();
  }
}
</script>
