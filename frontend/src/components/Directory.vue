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
    <div class="working-space">
      <button @click="autoSave=!autoSave">Auto Save</button>
      <p>{{ autoSave }}</p>
      <textarea v-model="file_data[working_text[0]]" @change="working_text[1]+=1" name="file-data" id="file-data" cols="30" rows="10"></textarea>
    </div>
    <div class="terminal">
      <div><input type="text" v-model="command[command.length-1]"></div>
      <button id="btn">send</button>
    </div>
    <h2>results</h2>
    <p style="white-space:pre-wrap; word-wrap:break-word;">{{ result_data }}</p>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import Axios from 'axios';
import ThisFile from '@/components/ThisFile';

export default {
  components: {
    ThisFile
  },
  data () {
    return {
      'comment': [],
      'user_name': '',
      'user_id': '',
      'working_text': ['', 0],
      'autoSave': true,
      'file_data': {'': ''},
      'command': [''],
      'result_data': '',
      'connection': null
    };
  },
  computed: mapState([
    'token',
    'base_url',
    'ws_url'
  ]),
  methods: {
    load_files () {
      Axios.post(this.base_url + '/api/loadfile', {
        token: this.token
      }).then(resp => {
        if (resp.data.valid === '1') {
          this.user_id = resp.data.user_id;
          this.user_name = resp.data.user_name;
          this.comment = resp.data.comment;
          this.comment.splice();
        } else {
          alert('wrong access');
          window.location.href = '/tryaccess/login/' + 'directory';
        }
      }).catch(error => {
        console.log(error);
      });
    },
    change_Workingspace (from, to) {
      if (this.autoSave && from !== '' && this.working_text[1]) this.saveFile(from);
      if (Object.keys(this.file_data).includes(to)) this.working_text = [to, 0];
      else {
        Axios.post(this.base_url + '/api/userfile/' + to, {
          token: this.token
        }).then(resp => {
          this.file_data[to] = resp.data;
          this.working_text = [to, 0];
        }).catch(error => {
          console.log(error);
        })
      }
    },
    saveFile (file_name) {
      Axios.post(this.base_url + '/api/fileupload/' + file_name, {
        token: this.token,
        data: this.file_data[file_name]
      })
    },
    ws_connection () {
      const vm = this;
      vm.connection = new WebSocket(this.ws_url + '/ws/terminal');
      vm.connection.onopen = event => { // eslint-disable-line no-unused-vars
        vm.connection.send(JSON.stringify({
          token: vm.token
        }));
      };
      vm.connection.onmessage = event => {
        const data = JSON.parse(event.data);
        vm.result_data += data.result;
      };
      vm.connection.onclose = event => {
        vm.connection.close();
        vm.connection = null;
        alert('ERROR: please reload this page');
      }
      const btn = document.getElementById('btn');
      btn.onclick = () => {
        let new_command = '!!', i = 1;
        while (new_command === '!!') {
          new_command = vm.command[vm.command.length-(i++)];
        }
        vm.connection.send(JSON.stringify({
          token: vm.token,
          command: new_command
        }));
        vm.result_data += `> ${new_command}\n`;
        vm.command.push('');
      };
    }
  },
  mounted () {
    this.$store.watch(
      (state, getters) => getters.current_fileID,
      (to, from) => {
        this.change_Workingspace(from, to);
      }
    )
    this.ws_connection();
  },
  created () {
    this.$store.dispatch('logged_in', 'user');
    this.load_files();
  },
  beforeDestroy () {
    if (this.connection !== null) {
      this.connection.close();
    }
  }
}
</script>
