var m = require("mithril")
var Patient = require("../models/Patient")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function() {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Patient.register()
                }
            }, [
            m("label.label", "First name"),
            m("input.input[type=text][placeholder=First name]", {
                oninput: m.withAttr("value", function(value) {Patient.current.name = value}),
                value: Patient.current.name
            }),
            m("label.label", "Last name"),
            m("input.input[placeholder=Last name]", {
                oninput: m.withAttr("value", function(value) {Patient.current.surname = value}),
                value: Patient.current.surname
            }),
            m("button.button[type=submit]", "Register"),
            m("label.error", Patient.error)
        ])
    }
}