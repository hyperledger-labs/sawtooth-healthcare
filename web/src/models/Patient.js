var m = require("mithril")

var Patient = {
    list: [],
    loadList: function() {
        return m.request({
            method: "GET",
            url: "/api/patients",
//            withCredentials: true,
        })
        .then(function(result) {
            Patient.list = result.data
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

    register: function() {
        return m.request({
            method: "PUT",
            url: "/api/patient/new",
            data: Patient.current,
//            withCredentials: true,
        })
    }
}

module.exports = Patient