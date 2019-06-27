var m = require("mithril")

var Claim = {
    list: [],
    error: "",
    loadList: function() {
        return m.request({
            method: "GET",
            url: "http://healthcare-rest-api:8000/claims",
//            withCredentials: true,
        })
        .then(function(result) {
            Claim.error = ""
            Claim.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Claim.error = e.message
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
            Doctor.current = result
            Claim.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Claim.error = e.message
        })
    },

    register: function() {
        return m.request({
            method: "POST",
            url: "http://healthcare-rest-api:8000/claims",
            data: Claim.current,
            useBody: true,
//            headers: {
//                    'Content-Type': 'text/plain',
//                    'Access-Control-Allow-Origin': 'http://localhost:6334',
//
////            'Content-Type': 'application/json; charset=UTF-8',
//                        'Access-Control-Request-Headers': 'Content-Type',
//                        'Access-Control-Request-Method': 'POST,GET,OPTIONS',
//                        'Access-Control-Allow-Headers': 'X-Requested-With,Content-Type'
//            }
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Claim.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Claim.error = e.message
        })
    }
}

module.exports = Claim