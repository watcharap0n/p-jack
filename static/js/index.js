new Vue({
    el: '#app',
    vuetify: new Vuetify(),
    data: {
        esp: [],
        user: {}
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