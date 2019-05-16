var m = require("mithril")
var User = require("../models/Doctor")

module.exports = {
    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function() {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Doctor.register()
                }
            }, [
            m("label.label", "First name"),
            m("input.input[type=text][placeholder=First name]", {
                oninput: m.withAttr("value", function(value) {Doctor.current.firstName = value}),
                value: Doctor.current.firstName
            }),
            m("label.label", "Last name"),
            m("input.input[placeholder=Last name]", {
                oninput: m.withAttr("value", function(value) {Doctor.current.lastName = value}),
                value: Doctor.current.lastName
            }),
            m("button.button[type=submit]", "Register"),
        ])
    }
}