let pomodoroComponent = new Vue({
    el: '#pomodoro',
    delimiters: ['${', '}'],
    created() {
        this.fetchPomodoros();
        this.fetchUsers();
    },
    data: {
        dataSaved: false,
        finished: false,
        auxMinutes: 1,
        auxRestMinutes: 1,
        auxName: '',
        auxDescription: '',
        pomodoros: [],
        users: [],
        toogle: false,
        API_URL: 'http://127.0.0.1:8000/',
        pomodoro: {
            minutes: 1,
            seconds: 0,
            running: false,
            completed: false,
            paused: false,
            started: false,
        },
        shortBreak: {
            minutes: 1,
            seconds: 0,
            running: false,
            completed: false,
            paused: false,
            started: false,
        },
    },
    methods: {
        toogleAction() {
            if (this.toogle) {
                this.toogle = false;
            } else {
                this.toogle = true;
            }
        },
        fetchUsers() {
            axios.get(this.API_URL + 'main_app/users/?format=json')
                .then(response => {
                    this.users = response.data;
                    this.sumPomodoroDurationByUser();

                })
                .catch(error => {
                    console.log(error);
                });

        },
        fetchPomodoros() {
            axios.get(this.API_URL + 'main_app/pomodoros/?format=json')
                .then(response => {
                    this.pomodoros = response.data;
                })
                .catch(error => {
                    console.log(error);
                });
        },

        startPomodoro() {
            if (this.auxMinutes > 0 && this.auxMinutes <= 60) {
                if (this.auxRestMinutes > 0 && this.auxRestMinutes <= 60) {
                    this.finished = false;
                    this.pomodoro.minutes = this.auxMinutes;
                    this.pomodoro.running = true;
                    this.pomodoro.started = true;
                    this.pomodoro.completed = false;
                    this.pomodoro.paused = false;
                    this.shortBreak.running = false;
                    this.shortBreak.started = false;
                    this.shortBreak.completed = false;
                    this.shortBreak.paused = false;
                } else {
                    alert("Please, insert a valid rest time (1-60 minutes)");
                }
            } else {
                alert("Please, insert a valid time (1-60 minutes)");
            }
        },
        startShortBreak() {
            this.shortBreak.minutes = this.auxRestMinutes;
            this.shortBreak.running = true;
            this.shortBreak.started = true;
            this.shortBreak.completed = false;
            this.shortBreak.paused = false;

        },
        pausePomodoro() {
            this.pomodoro.running = false;
            this.pomodoro.paused = true;
        },
        pauseShortBreak() {
            this.shortBreak.running = false;
            this.shortBreak.paused = true;
        },
        playPomodoro() {
            this.pomodoro.running = true;
            this.pomodoro.paused = false;
        },
        playShortBreak() {
            this.shortBreak.running = true;
            this.shortBreak.paused = false;
        },
        resetPomodoro() {
            this.pomodoro.minutes = this.auxMinutes;
            this.pomodoro.seconds = 0;
            this.pomodoro.running = false;
            this.pomodoro.completed = false;
            this.pomodoro.paused = false;
            this.pomodoro.started = false;
        },
        resetShortBreak() {
            this.shortBreak.minutes = this.auxRestMinutes;
            this.shortBreak.seconds = 0;
            this.shortBreak.running = false;
            this.shortBreak.completed = false;
            this.shortBreak.paused = false;
            this.shortBreak.started = false;
        },
        tick() {
            if (this.pomodoro.running) {
                if (this.pomodoro.seconds > 0) {
                    this.pomodoro.seconds--;
                } else {
                    if (this.pomodoro.minutes > 0) {
                        this.pomodoro.minutes--;
                        this.pomodoro.seconds = 59;
                    } else {
                        this.pomodoro.running = false;
                        this.pomodoro.completed = true;
                        alert("Pomodoro completed, take a short break!");
                    }
                }
            }
            if (this.shortBreak.running) {
                if (this.shortBreak.seconds > 0) {
                    this.shortBreak.seconds--;
                } else {
                    if (this.shortBreak.minutes > 0) {
                        this.shortBreak.minutes--;
                        this.shortBreak.seconds = 59;
                    } else {
                        this.shortBreak.running = false;
                        this.shortBreak.completed = true;
                        this.finished = true;
                        alert("Short break completed, start a new pomodoro!");
                    }
                }
            }
        },
        newPomodoro() {
            this.resetPomodoro();
            this.resetShortBreak();
            this.finished = false;
            this.auxDescription = '';
            this.auxName = '';
        },
        sumPomodoroDurationByUser() {
            for (let i = 0; i < this.users.length; i++) {
                let totalDuration = 0;
                for (let j = 0; j < this.pomodoros.length; j++) {
                    if (this.users[i].id == this.pomodoros[j].user) {
                        totalDuration += this.pomodoros[j].duration;
                    }
                }
                this.users[i].total_duration = totalDuration;
            }
            this.orderUsersByTotalDuration();
            if (this.users.length > 10) {
                this.users = this.users.slice(0, 10);
            }
        },
        orderUsersByTotalDuration() {
            this.users.sort(function (a, b) {
                return b.total_duration - a.total_duration;
            });
        },
    },
    computed: {
        pomodoroTime() {
            if (this.pomodoro.minutes < 10) {
                var minutes = '0' + this.pomodoro.minutes;
            }
            else {
                var minutes = this.pomodoro.minutes;
            }
            if (this.pomodoro.seconds < 10) {
                var seconds = '0' + this.pomodoro.seconds;
            }
            else {
                var seconds = this.pomodoro.seconds;
            }
            return minutes + ':' + seconds;
        },
        shortBreakTime() {
            if (this.shortBreak.minutes < 10) {
                var minutes = '0' + this.shortBreak.minutes;
            }
            else {
                var minutes = this.shortBreak.minutes;
            }
            if (this.shortBreak.seconds < 10) {
                var seconds = '0' + this.shortBreak.seconds;
            }
            else {
                var seconds = this.shortBreak.seconds;
            }
            return minutes + ':' + seconds;
        }
    },
    mounted() {
        setInterval(this.tick, 1000);
    },
});