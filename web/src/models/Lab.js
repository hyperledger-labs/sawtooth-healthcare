var m = require("mithril")

var Lab = {
    list: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/labs",
            headers: {
                'ClientKey': clientKey
            }
//            url: "https://rem-rest-api.herokuapp.com/api/users",
//               url: "http://localhost:8008/state?address=3d804901bbfeb7",
//            withCredentials: true,
//            withCredentials: true,
//            credentials: 'include',
        })
        .then(function(result) {
            console.log("Get labs list")
            Lab.error = ""
            Lab.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Lab.error = e.message
            Lab.list = []
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
            Lab.current = result
        })
    },

    register: function() {
        return m.request({
            method: "POST",
            url: "/api/labs",
            data: Lab.current,
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Lab.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Lab.error = e.message
        })
    }
}

module.exports = Lab