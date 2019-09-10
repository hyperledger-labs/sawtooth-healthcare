var m = require("mithril")
var Doctor = require("../models/Doctor")

module.exports = {
    oninit:
        function(vnode){
            Doctor.loadList(vnode.attrs.client_key)
        },
    view: function() {
        return m(".user-list", Doctor.list.map(function(doctor) {
            return m("a.user-list-item", doctor.name) // + " " +  doctor.permissions)
        }),
        m("label.error", Doctor.error))
    }
}