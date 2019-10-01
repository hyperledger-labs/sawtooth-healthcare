var m = require("mithril")

var Payment = {
    list: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/payment",
            headers: {
                'ClientKey': clientKey
            }
        })
        .then(function(result) {
            Payment.error = ""
            Payment.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Payment.error = e.message
            Payment.list = []
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
            Payment.current = result
        })
    },

    add: function(clientKey) {
        return m.request({
            method: "POST",
            url: "/api/payment",
            data: Payment.current,
            headers: {
                'ClientKey': clientKey
            },
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Payment.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Payment.error = e.message
        })
    }
}

module.exports = Payment