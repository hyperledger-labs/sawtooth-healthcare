var m = require("mithril")

var Clinic = {
    list: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/clinics",
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
            console.log("Get clinics list")
            Clinic.error = ""
            Clinic.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Clinic.error = e.message
            Clinic.list = []
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
            Clinic.current = result
        })
    },

    register: function() {
        return m.request({
            method: "POST",
            url: "/api/clinics",
            data: Clinic.current,
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Clinic.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Clinic.error = e.message
        })
    },

    grant: function(clinicPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/patients/grant/" + clinicPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Clinic.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Clinic.error = e.message
        })
    },

    revoke: function(clinicPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/patients/revoke/" + clinicPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Clinic.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Clinic.error = e.message
        })
    }
}

module.exports = Clinic