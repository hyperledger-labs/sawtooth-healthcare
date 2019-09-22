var m = require("mithril")

var Doctor = {
    list: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/doctors",
            headers: {
                'ClientKey': clientKey
            }
//            withCredentials: true,
        })
        .then(function(result) {
            Doctor.error = ""
            Doctor.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Doctor.error = e.message
            Doctor.list = []
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
            method: "POST",
            url: "/api/doctors",
            data: Doctor.current,
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Doctor.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Doctor.error = e.message
        })
    },

    grant: function(doctorPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/patients/grant/" + doctorPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Doctor.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Doctor.error = e.message
        })
    },

    revoke: function(doctorPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/patients/revoke/" + doctorPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Doctor.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Doctor.error = e.message
        })
    }
}

module.exports = Doctor