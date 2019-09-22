var m = require("mithril")

var Client = {
    list: {},
    error: "",
    loadList: function() {
        return m.request({
            method: "GET",
            url: "/api/clients",
//            url: "https://rem-rest-api.herokuapp.com/api/users",
//               url: "http://localhost:8008/state?address=3d804901bbfeb7",
//            withCredentials: true,
//            withCredentials: true,
//            credentials: 'include',
        })
        .then(function(result) {
            console.log("Get clients list")
            Client.error = ""
            Client.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Client.error = e.message
            Client.list = {}
        })
    }
}

module.exports = Client