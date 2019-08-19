var m = require("mithril")

var Pulse = {
    list: [],
    error: "",
    loadList: function() {
        return m.request({
            method: "GET",
            url: "/api/pulse",
//            withCredentials: true,
        })
        .then(function(result) {
            Pulse.error = ""
            Pulse.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Pulse.error = e.message
        })
    },

    current: {},
    load: function(id) {
        return m.request({
            method: "GET",
            url: "https://rem-rest-api.herokuapp.com/api/users/" + id,
            withCredentials: true,
        })
        .then(function(result) {
            Pulse.current = result
        })
    },

    add: function() {
        return m.request({
            method: "POST",
            url: "/api/pulse",
            data: Pulse.current,
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Pulse.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Pulse.error = e.message
        })
    }
}

module.exports = Pulse