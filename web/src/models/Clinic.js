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

/* this does not work.
HTTP/1.1 200 OK
Connection: close
Access-Control-Allow-Credentials: True
Content-Length: 2183
Content-Type: application/json
*/

/*
Access-Control-Allow-Credentials: true
Access-Control-Allow-Origin: http://localhost:63342
Connection: keep-alive
Content-Type: application/json
Date: Fri, 16 Nov 2018 13:23:16 GMT
Server: Cowboy
Transfer-Encoding: chunked
Via: 1.1 vegur

request:

ccept: application/json, text/*
Origin: http://localhost:63342
Referer: http://localhost:63342/healthcare/web/index.html?_ijt=2ruajc0i2o2ss83s3qui2bvudd
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36
*/
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

//    save: function() {
//        return m.request({
//            method: "PUT",
//            url: "https://rem-rest-api.herokuapp.com/api/users/" + Clinic.current.id,
//            data: Clinic.current,
//            withCredentials: true,
//        })
//    }
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
    }
}

module.exports = Clinic