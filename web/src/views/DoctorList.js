var m = require("mithril")
var Doctor = require("../models/Doctor")

module.exports = {
    oninit: Doctor.loadList,
    view: function() {
        return m(".user-list", Doctor.list.map(function(doctor) {
            return m("a.user-list-item", doctor.public_key + " " + doctor.name + " " +  doctor.surname) // + user.publicKey
        }))
    }
}