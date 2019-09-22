var m = require("mithril")

var LabTest = {
    list: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/labtests",
            headers: {
                'ClientKey': clientKey
            }
//            withCredentials: true,
        })
        .then(function(result) {
            LabTest.error = ""
            LabTest.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            LabTest.error = e.message
            LabTest.list = []
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
            LabTest.current = result
        })
    },

    add: function(clientKey) {
        return m.request({
            method: "POST",
            url: "/api/labtests",
            data: LabTest.current,
            headers: {
                'ClientKey': clientKey
            },
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            LabTest.error = ""
        })
        .catch(function(e) {
            console.log(e)
            LabTest.error = e.message
        })
    }
}

module.exports = LabTest