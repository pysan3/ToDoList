<template>
  <div class="current-file">
    <div @click="hidden">
      <img id="file-type" v-if="comment.type==='dir'" :src="images.folder" alt="folder" height="16px" width="16px">
      <img id="file-type" v-if="comment.type==='file'" :src="images.file" alt="file" height="16px" width="16px">
      <p id="comment-name">{{ comment.name }}</p>
    </div>
    <ul v-if="comment.show === '1'">
      <li class="inside" v-for="inside in comment.insides" :key="inside.id">
        <this-file :comment="inside"/>
      </li>
    </ul>
  </div>
</template>

<script>
import ThisFile from '@/components/ThisFile';
import * as types from '@/mutation-types';

export default {
  name: 'this-file',
  data () {
    return {
      images: {
        folder: require('@/assets/folder.png'),
        file: require('@/assets/file.png')
      }
    };
  },
  components: {
    ThisFile
  },
  props: {
    comment: {
      type: Object,
      required: true
    }
  },
  methods: {
    hidden () {
      if (this.comment.type === 'dir') {
        this.comment.show = (this.comment.show === '1' ? '0' : '1');
      } else if (this.comment.type === 'file') {
        this.$store.commit(types.CURRENT_FILEID, this.comment.id);
      }
    }
  }
};
</script>

<style lang="stylus" scoped>
.current-file
  margin 0px
  border 0px
  padding 0px
  ul
    list-style none
    padding-left 16px

p#comment-name
  font-size medium

img#file-type
  float left
</style>