new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        esp: [],
        user: {},
        spinCard: false
    },
    async created() {
        await this.initializedLIFF()
        await this.initialized();
    },
    methods: {
        initializedLIFF() {
            liff.init({liffId: '1656545825-Dg2zr4BQ'}, () => {
                    if (liff.isLoggedIn()) {
                        liff.getProfile()
                            .then((profile) => {
                                this.user.user_id = profile.userId
                                this.user.display_name = profile.displayName
                                this.user.img = profile.pictureUrl
                                this.user.email = liff.getDecodedIDToken().email
                            })
                    } else {
                        liff.login();
                    }
                }
            )
        },
        initialized() {
            this.spinCard = false
            axios.get('/esp')
                .then((res) => {
                    this.esp = res.data
                    this.spinCard = true
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
                    this.spinCard = true
                    console.error(err)
                })
        },
        ticket(obj) {
            this.spinCard = false
            if (obj.id === 0) {
                if (obj.status) {
                    this.updateVal(4)
                } else if (obj.status) {
                    this.updateVal(3)
                }
            }
            if (obj.id === 1) {
                if (obj.status) {
                    this.updateVal(6)
                } else if (obj.status) {
                    this.updateVal(5)
                }
            }
            if (obj.id === 2) {
                if (obj.status) {
                    this.updateVal(7)
                } else if (obj.status) {
                    this.updateVal(8)
                }
            }
            if (obj.id === 3) {
                if (obj.status) {
                    this.updateVal(9)
                } else if (obj.status) {
                    this.updateVal(10)
                }
            }
        },
        updateVal(val) {
            axios.get(`/esp?relay=${val}`)
                .then((res) => {
                    this.esp = res.data
                    this.spinCard = true
                })
                .catch((err) => {
                    console.log(err)
                    this.spinCard = true
                })
        }

    },
    delimiters: ["[[", "]]"]
})