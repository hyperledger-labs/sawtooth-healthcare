var m = require("mithril")
var Lab = require("../models/Lab")

module.exports = {
    view: function() {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Lab.register()
                }
            }, [
            m("label.label", "Name"),
            m("input.input[type=text][placeholder=Lab name]", {
                oninput: m.withAttr("value", function(value) {Lab.current.name = value}),
                value: Lab.current.name
            }),
            m("button.button[type=submit]", "Register"),
            m("label.error", Lab.error)
        ])
    }
}