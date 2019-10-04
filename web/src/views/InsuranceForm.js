var m = require("mithril")
var Insurance = require("../models/Insurance")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function() {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Insurance.register()
                }
            }, [
            m("label.label", "Name"),
            m("input.input[type=text][placeholder=Insurance name]", {
                oninput: m.withAttr("value", function(value) {Insurance.current.name = value}),
                value: Insurance.current.name
            }),
            m("button.button[type=submit]", "Register"),
            m("label.error", Insurance.error)
        ])
    }
}