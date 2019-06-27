var m = require("mithril")
var Clinic = require("../models/Clinic")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function() {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Clinic.register()
                }
            }, [
            m("label.label", "Name"),
            m("input.input[type=text][placeholder=Clinic name]", {
                oninput: m.withAttr("value", function(value) {Clinic.current.name = value}),
                value: Clinic.current.name
            }),
            m("button.button[type=submit]", "Register"),
            m("label.error", Clinic.error)
        ])
    }
}