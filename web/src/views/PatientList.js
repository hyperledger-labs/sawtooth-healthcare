var m = require("mithril")
var Patient = require("../models/Patient")

module.exports = {
//    oninit: Patient.loadList,
    oninit:
        function(vnode){
            Patient.loadList(vnode.attrs.client_key)
        },
    view: function() {
        return m(".user-list", Patient.list.map(function(patient) {
//            return m("a.user-list-item", {href: "/patient/" + patient.public_key, oncreate: m.route.link}, patient.public_key + " " + patient.name + " " +  patient.surname)
            return m("a.user-list-item",
                "PUBLIC KEY: " + patient.public_key +
                "; NAME: " + patient.name +
                "; SURNAME: " +  patient.surname)
        }),
        m("label.error", Patient.error))
    }
}