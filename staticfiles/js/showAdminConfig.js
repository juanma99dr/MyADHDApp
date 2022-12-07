let vm = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
      toogle: false,
    },
    methods: {
      toogleAction() {
        if (this.toogle) {
          this.toogle = false;
        } else {
          this.toogle = true;
        }
      }
    }
  });
  