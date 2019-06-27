var m = require("mithril")

var ClaimDetails = {
    list: [],
    error: "",
    load: function(clinic_pkey, claim_id) {
        return m.request({
            method: "GET",
            url: "/api/claim/" + clinic_pkey + "/"+  claim_id,
//            withCredentials: true,
        })
        .then(function(result) {
            ClaimDetails.error = ""
            ClaimDetails.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            ClaimDetails.error = e.message
        })
    },

    current: {},

    assign_doctor: function() {
        return m.request({
            method: "POST",
            url: "/api/claim/assign",
            data: ClaimDetails.current,
            useBody: true,

        })
        .then(function(items) {
//            Data.todos.list = items
            ClaimDetails.error = ""
        })
        .catch(function(e) {
            console.log(e)
            ClaimDetails.error = e.message
        })
    },

    first_visit: function() {
        return m.request({
            method: "POST",
            url: "/api/claim/first_visit",
            data: ClaimDetails.current,
            useBody: true,

        })
        .then(function(items) {
//            Data.todos.list = items
            ClaimDetails.error = ""
        })
        .catch(function(e) {
            console.log(e)
            ClaimDetails.error = e.message
        })
    },

    eat_pills: function() {
        return m.request({
            method: "POST",
            url: "/api/claim/eat_pills",
            data: ClaimDetails.current,
            useBody: true,

        })
        .then(function(items) {
//            Data.todos.list = items
            ClaimDetails.error = ""
        })
        .catch(function(e) {
            console.log(e)
            ClaimDetails.error = e.message
        })
    },

    pass_tests: function() {
        return m.request({
            method: "POST",
            url: "/api/claim/pass_tests",
            data: ClaimDetails.current,
            useBody: true,

        })
        .then(function(items) {
//            Data.todos.list = items
            ClaimDetails.error = ""
        })
        .catch(function(e) {
            console.log(e)
            ClaimDetails.error = e.message
        })
    },

    attend_procedures: function() {
        return m.request({
            method: "POST",
            url: "/api/claim/attend_procedures",
            data: ClaimDetails.current,
            useBody: true,

        })
        .then(function(items) {
//            Data.todos.list = items
            ClaimDetails.error = ""
        })
        .catch(function(e) {
            console.log(e)
            ClaimDetails.error = e.message
        })
    },

    next_visit: function() {
        return m.request({
            method: "POST",
            url: "/api/claim/next_visit",
            data: ClaimDetails.current,
            useBody: true,

        })
        .then(function(items) {
//            Data.todos.list = items
            ClaimDetails.error = ""
        })
        .catch(function(e) {
            console.log(e)
            ClaimDetails.error = e.message
        })
    },
}

module.exports = ClaimDetails