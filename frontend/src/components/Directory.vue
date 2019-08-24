<template>
  <div class="directory">
    <div class="header">
      <div class="header-logo">auto make</div>
      <div class="header-list">
        <ul>
          <li>プログラミングとは</li>
          <li>学べるレッスン</li>
          <li>お問い合わせ</li>
        </ul>
      </div>
    </div>
    <div class="inventory">
      <h2>{{ user_name }}</h2>
      <div v-for="(item, index) in comment" :key="index">
        <this-file :comment="item"/>
      </div>
    </div>
    <div class="working-space">
      <div id="auto-save">
        <button @click="autoSave=!autoSave">Auto Save</button>
        <p>{{ autoSave }}</p>
      </div>
      <textarea v-model="file_data[working_text[0]]" @change="working_text[1]+=1" name="file-data" id="file-data"></textarea>
    </div>
    <div class="terminal">
      <div><input type="text" v-model="command[command.length-1]"></div>
      <button id="btn">send</button>
      <h2>results</h2>
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
      vm.connection.onclose = event => { // eslint-disable-line no-unused-vars
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
  updated () {
    const result = document.getElementById('result-data');
    result.scrollTop = result.scrollHeight;
  },
  beforeDestroy () {
    if (this.connection !== null) {
      this.connection.close();
    }
  }
}
</script>

<style lang="stylus" scoped>
.directory, .inventory, .working-space, .terminal {
  margin: 0px;
  border: 0px;
  padding: 0px;
}

.directory {
  width: 100%;
  height: 100%;
  background-color: black;
  overflow: hidden;
  color: black;
}

li {
  list-style: none;
}

.header {
  background-color: #26d0c9;
  color: #fff;
  height: 90px;
}

.header-logo {
  float: left;
  font-size: 36px;
}

.header-list li {
  float: left;
}

.inventory {
  width: 200px;
  min-height: 100%;
  float: left;
  background-color: bisque;
}

.inventory li {
  font-size: medium;
}

.working-space {
  width: calc(100% - 200px);
  float: right;
  background-color: #fff;
}

.working-space div#auto-save {
  float: right;
}

.terminal {
  width: calc(100% - 200px);
  min-height: 100%;
  float: right;
  background-color: azure;
}

textarea {
  width: 85%;
}

#file-data {
  height: 50vh;
}

#result-data {
  height: 15vh;
}
</style>