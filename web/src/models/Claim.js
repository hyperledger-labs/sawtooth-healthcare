var m = require("mithril")

var Claim = {
    list: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/claims",
            headers: {
                'ClientKey': clientKey
            }
        })
        .then(function(result) {
            Claim.error = ""
            Claim.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Claim.error = e.message
            Claim.list = []
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
            Claim.current = result
            Claim.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Claim.error = e.message
        })
    },

    close: function(clientKey) {
        return m.request({
            method: "POST",
            url: "/api/claims/close",
            data: Claim.current,
            headers: {
                'ClientKey': clientKey
            },
            useBody: true,
        })
        .then(function(items) {
            Claim.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Claim.error = e.message
        })
    },

    register: function(clientKey) {
        return m.request({
            method: "POST",
            url: "/api/claims",
            data: Claim.current,
            headers: {
                'ClientKey': clientKey
            },
            useBody: true,
        })
        .then(function(items) {
            Claim.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Claim.error = e.message
        })
    }
}

module.exports = Claim