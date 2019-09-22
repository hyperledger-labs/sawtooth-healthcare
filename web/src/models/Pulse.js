var m = require("mithril")

var Pulse = {
    list: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/pulse",
            headers: {
                'ClientKey': clientKey
            }
//            withCredentials: true,
        })
        .then(function(result) {
            Pulse.error = ""
            Pulse.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Pulse.error = e.message
            Pulse.list = []
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

    add: function(clientKey) {
        return m.request({
            method: "POST",
            url: "/api/pulse",
            data: Pulse.current,
            headers: {
                'ClientKey': clientKey
            },
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