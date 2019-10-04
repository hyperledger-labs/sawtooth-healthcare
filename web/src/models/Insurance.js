var m = require("mithril")

var Insurance = {
    list: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/insurances",
            headers: {
                'ClientKey': clientKey
            }
        })
        .then(function(result) {
            console.log("Get insurances list")
            Insurance.error = ""
            Insurance.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Insurance.error = e.message
            Insurance.list = []
        })
    },

    current: {},
    register: function() {
        return m.request({
            method: "POST",
            url: "/api/insurances",
            data: Insurance.current,
            useBody: true,
        })
        .then(function(items) {
            Insurance.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Insurance.error = e.message
        })
    }
}

module.exports = Insurance