import Vue from 'vue';
import Vuex from 'vuex';
import Axios from 'axios';
import * as types from './mutation-types';

Vue.use(Vuex);

const state = {
  token: 'none',
  base_url: 'http://127.0.0.1:5042'
};

const mutations = {
  [types.USER_TOKEN] (state, token) {
    state.token = token;
  }
};

const actions = {
  logged_in (context, url) {
    Axios.post(state.base_url + '/api/loggedin', {
      token: context.state.token
    }).then(resp => {
      if (resp.data !== 'valid') {
        window.location.href = '/tryaccess/login/' + url;
      }
    }).catch(error => {
      console.log(error);
    })
  }
};

export default new Vuex.Store({
  state,
  mutations,
  actions
});
