<template>
  <div>
    <p @click="hidden">{{ comment.name }}</p>
    <ul v-if="comment.show === '1'">
      <li class="inside" v-for="inside in comment.insides" :key="inside.id">
        <this-file :comment="inside"/>
      </li>
    </ul>
  </div>
</template>

<script>
import ThisFile from '@/components/ThisFile'

export default {
  name: 'this-file',
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
      this.comment.show = (this.comment.show === '1' ? '0' : '1');
    }
  }
}
</script>