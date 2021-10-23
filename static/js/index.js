new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        hiddenCard: false,
        hiddenAuto: true,
        esp: [],
        switch1: false,
        user: {},
        spinCard: false
    },
    async created() {
        await this.initializedLIFF()
        await this.initialized();
        setInterval(
            function () {
                this.sensors();
            }.bind(this), 5000);
    },
    watch: {
        switch1(val) {
            if (val) {
                this.autoVal(true)
                this.hiddenCard = true
                this.hiddenAuto = false
            } else {
                this.autoVal(false)
                this.hiddenCard = false
                this.hiddenAuto = true
                this.initialized()
            }
        }
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
                    if (res.data.node === 0){
                        this.switch1 = true
                        this.esp = res.data.ref
                    }
                    else{
                        this.esp = res.data.ref
                    }
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
        sensors() {
            axios.get('/esp')
                .then((res) => {
                    console.log('get')
                    this.esp = res.data.ref
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
            console.log(obj)
            this.spinCard = false
            if (obj.id === 0) {
                if (obj.status) {
                    this.updateVal(4)
                } else {
                    this.updateVal(3)
                }
            }
            if (obj.id === 1) {
                if (obj.status) {
                    this.updateVal(6)
                } else {
                    this.updateVal(5)
                }
            }
            if (obj.id === 2) {
                if (obj.status) {
                    this.updateVal(7)
                } else {
                    this.updateVal(8)
                }
            }
            if (obj.id === 3) {
                if (obj.status) {
                    this.updateVal(9)
                } else {
                    this.updateVal(10)
                }
            }
        },
        updateVal(val) {
            axios.get(`/esp?relay=${val}`)
                .then((res) => {
                    this.esp = res.data.ref
                    this.spinCard = true
                })
                .catch((err) => {
                    console.log(err)
                    this.spinCard = true
                })
        },
        autoVal(val) {
            this.spinCard = false
            axios.get(`esp/auto?auto=${val}`)
                .then((res) => {
                    console.log(res.data)
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