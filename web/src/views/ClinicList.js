var m = require("mithril")
var Clinic = require("../models/Clinic")

module.exports = {
    oninit: Clinic.loadList,
    view: function() {
        return m(".user-list", Clinic.list.map(function(clinic) {
            return m("a.user-list-item", clinic.public_key + " " + clinic.name )
        }))
    }
}