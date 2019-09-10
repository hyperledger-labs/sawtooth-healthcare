var m = require("mithril")
var Clinic = require("../models/Clinic")

module.exports = {
    oninit:
        function(vnode){
            Clinic.loadList(vnode.attrs.client_key)
        },
    view: function() {
        return m(".user-list", Clinic.list.map(function(clinic) {
            return m("a.user-list-item", clinic.name + " " + clinic.permissions)
        }),
        m("label.error", Clinic.error))
    }
}