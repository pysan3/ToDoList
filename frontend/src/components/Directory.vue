<template>
  <div class="directory">
    <div class="inventory">
      <h2>{{ user_name }}-{{ project }}</h2>
      <button @click="new_file.type='file'">make new file</button>
      <button @click="new_file.type='dir'">make new dir</button>
      <div v-if="new_file.type!=='none'"><input type="text" value="" v-model="new_file.name" @change="newFile"></div>
      <div v-for="(item, index) in comment" :key="index">
        <this-file :comment="item"/>
      </div>
    </div>
    <div class="working-space">
      <div id="auto-save">
        <button @click="if (autoSave!=='lost connection') autoSave=!autoSave;">Auto Save</button>
        <p>{{ autoSave }}</p>
        <br>
        <button @click="file_data = {}; working_text = ['', 0]">reload files</button>
        <br>
        <button @click="saveFile()">save now</button>
      </div>
      <textarea v-model="file_data[working_text[0]]" @change="working_text[1]+=1" name="file-data" id="file-data"></textarea>
    </div>
    <div class="terminal">
      <input type="text" v-model="command[command.length-1]" id="send-command" @change="sendCommand">
      <h4>results</h4>
      <textarea readonly v-model="result_data" name="result-data" id="result-data"></textarea>
    </div>
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
      project: this.$route.params.project,
      comment: [],
      new_file: {type: 'none', name: ''},
      user_name: '',
      working_text: ['', 0],
      autoSave: true,
      file_data: {'': ''},
      command: [''],
      result_data: '',
      connection: null
    };
  },
  computed: mapState([
    'token',
    'base_url',
    'ws_url'
  ]),
  methods: {
    load_files () {
      Axios.post(this.base_url + '/api/loadfile/' + this.project, {
        token: this.token
      }).then(resp => {
        if (resp.data.valid === '1') {
          this.user_name = resp.data.user_name;
          this.comment = resp.data.comment;
          this.comment.splice();
        } else {
          alert('wrong access');
          this.$store.dispatch('logged_in', `directory-${this.project}`);
        }
      }).catch(error => {
        console.log(error);
      });
    },
    change_Workingspace (from, to) {
      this.saveFile();
      if (Object.keys(this.file_data).includes(to)) this.working_text = [to, 0];
      else {
        Axios.post(this.base_url + '/api/userfile/' + to, {
          token: this.token
        }).then(resp => {
          this.file_data[to] = resp.data;
          this.working_text = [to, 0];
        }).catch(error => {
          console.log(error);
        });
      }
    },
    saveFile () {
      if (this.autoSave && this.working_text[0] !== '' && this.working_text[1]) {
        Axios.post(this.base_url + '/api/fileupload/' + this.working_text[0], {
          token: this.token,
          data: this.file_data[this.working_text[0]]
        });
      }
    },
    newFile () {
      if (this.new_file.name.length !== 0) {
        const command = {'file': 'echo "" >', 'dir': 'mkdir'};
        this.connection.send(JSON.stringify({
          token: this.token,
          command: `${command[this.new_file.type]} ${this.new_file.name}`
        }));
        this.new_file.type = 'none';
        this.new_file.name = '';
      }
    },
    ws_connection () {
      const vm = this;
      this.connection = new WebSocket(this.ws_url + '/ws/terminal');
      this.connection.onopen = () => {
        vm.connection.send(JSON.stringify({
          token: vm.token,
          project: vm.project
        }));
      };
      this.connection.onmessage = event => {
        const data = JSON.parse(event.data);
        vm.result_data += data.result;
        vm.load_files();
      };
      this.connection.onclose = () => {
        vm.connection.close();
        vm.connection = null;
        vm.autoSave = 'lost connection';
      }
    },
    sendCommand () {
      const vm = this;
      let new_command = '!!', i = 1;
      while (new_command === '!!') {
        new_command = vm.command[vm.command.length-(i++)];
      }
      this.connection.send(JSON.stringify({
        token: vm.token,
        command: new_command
      }));
      this.result_data += `> ${new_command}\n`;
      this.command.push('');
    }
  },
  created () {
    this.$store.dispatch('logged_in', `directory-${this.project}`);
    this.load_files();
    this.working_text = ['', 0];
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
  updated () {
    const result = document.getElementById('result-data');
    result.scrollTop = result.scrollHeight;
  },
  beforeRouteLeave (to, from, next) {
    this.saveFile();
    if (this.connection !== null) {
      if (!this.autoSave) {
        const ans = window.confirm('changes not been saved!!');
        if (ans) next();
        else next(false);
      } else {
        next();
      }
    }
  },
  beforeDestroy () {
    if (this.connection !== null) {
      this.connection.close();
    }
  }
}
</script>

<style lang="stylus" scoped>
.directory, .inventory, .working-space, .terminal
  margin 0px
  border 0px
  padding 0px

.directory
  width 100%
  height 100%
  background-color black
  overflow hidden
  color black

li
  list-style none

.inventory
  width 200px
  min-height 100%
  float left
  background-color bisque
  li
    font-size medium

.working-space
  width calc(100% - 200px)
  float right
  background-color #fff
  div#auto-save
    float right

.terminal
  width calc(100% - 200px)
  min-height 100%
  float right
  background-color azure

textarea
  width 85%

#file-data
  height 50vh

#result-data
  height 15vh
</style>