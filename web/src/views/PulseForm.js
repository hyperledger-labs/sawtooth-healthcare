var m = require("mithril")
var Pulse = require("../models/Pulse")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function(vnode) {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Pulse.add(vnode.attrs.client_key)
                }
            }, [
            m("label.label", "PULSE"),
            m("input.input[type=text][placeholder=PULSE]", {
                oninput: m.withAttr("value", function(value) {Pulse.current.pulse = value}),
                value: Pulse.current.pulse
            }),
            m("label.label", "TIMESTAMP"),
            m("input.input[placeholder=TIMESTAMP]", {
                oninput: m.withAttr("value", function(value) {Pulse.current.timestamp = value}),
                value: Pulse.current.timestamp
            }),
            m("button.button[type=submit]", "Add"),
            m("label.error", Pulse.error)
        ])
    }
}