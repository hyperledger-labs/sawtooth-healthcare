var m = require("mithril")

var ClaimDetails = {
    list: [],
    error: "",
    load: function(clinic_pkey, claim_id) {
        return m.request({
            method: "GET",
            url: "http://localhost:8000/claim/" + clinic_pkey + "/"+  claim_id,
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
            url: "http://localhost:8000/claim/assign",
            data: ClaimDetails.current,
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
            ClaimDetails.error = ""
        })
        .catch(function(e) {
            console.log(e)
            ClaimDetails.error = e.message
        })
    }
}

module.exports = ClaimDetails