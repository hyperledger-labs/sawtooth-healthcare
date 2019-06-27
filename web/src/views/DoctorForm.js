var m = require("mithril")
var Doctor = require("../models/Doctor")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function() {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Doctor.register()
                }
            }, [
            m("label.label", "First name"),
            m("input.input[type=text][placeholder=First name]", {
                oninput: m.withAttr("value", function(value) {Doctor.current.name = value}),
                value: Doctor.current.name
            }),
            m("label.label", "Last name"),
            m("input.input[placeholder=Last name]", {
                oninput: m.withAttr("value", function(value) {Doctor.current.surname = value}),
                value: Doctor.current.surname
            }),
            m("button.button[type=submit]", "Register"),
            m("label.error", Doctor.error)
        ])
    }
}