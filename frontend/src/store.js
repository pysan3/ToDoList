import Vue from 'vue'
import Vuex from 'vuex'
import * as types from './mutation-types'

Vue.use(Vuex)

const state = {
  user_id: -1,
  base_url: 'http://127.0.0.1:5042'
}

const mutations = {
  [types.USER_ID] (state, num) {
    state.user_id = num - 0;
  }
}

const actions = {
  logged_in (context, url) {
    const request = new XMLHttpRequest();
    request.responseType = 'text';
    request.onload = () => {
      if (request.responseText === '0') {
        window.location.href = '/tryaccess/login/' + url;
      }
    }
    request.open('GET', state.base_url + '/api/login/' + context.state.user_id, true);
    request.send();
  }
}

export default new Vuex.Store({
  state,
  mutations,
  actions
})
