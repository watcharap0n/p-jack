new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        esp: []
    },
    created() {
        this.initialized();
    },
    methods: {
        initialized() {
            axios.get('/esp')
                .then((res) => {
                    this.esp = res.data
                })
                .catch((err) => {
                    this.esp = [
                        {
                            elc: 'Lost Connect...',
                            description: 'Lost Connect...',
                            status: false,
                            sensor: null
                        },
                        {
                            elc: 'Lost Connect...',
                            description: 'Lost Connect...',
                            status: false,
                            sensor: null
                        },
                        {
                            elc: 'Lost Connect...',
                            description: 'Lost Connect...',
                            status: false,
                            sensor: null
                        },
                        {
                            elc: 'Lost Connect...',
                            description: 'Lost Connect...',
                            status: false,
                            sensor: null
                        }
                    ]
                    console.error(err)
                })
        },
    },
    delimiters: ["[[", "]]"]
})