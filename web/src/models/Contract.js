var m = require("mithril")

var Contract = {
    list: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/contract",
            headers: {
                'ClientKey': clientKey
            }
        })
        .then(function(result) {
            Contract.error = ""
            Contract.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Contract.error = e.message
            Contract.list = []
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
            Contract.current = result
        })
    },

    add: function(clientKey) {
        return m.request({
            method: "POST",
            url: "/api/contract",
            data: Contract.current,
            headers: {
                'ClientKey': clientKey
            },
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Contract.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Contract.error = e.message
        })
    }
}

module.exports = Contract