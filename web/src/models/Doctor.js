var m = require("mithril")

var Doctor = {
    list: [],
    loadList: function() {
        return m.request({
            method: "GET",
            url: "http://healthcare-rest-api:8000/doctors",
//            withCredentials: true,
        })
        .then(function(result) {
            Doctor.list = result.data
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
        })
    },

    save: function() {
        return m.request({
            method: "PUT",
            url: "https://rem-rest-api.herokuapp.com/api/users/" + Doctor.current.id,
            data: Doctor.current,
            withCredentials: true,
        })
    }
}

module.exports = Doctor