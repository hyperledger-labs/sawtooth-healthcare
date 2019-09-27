var m = require("mithril")
var Contract = require("../models/Contract")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function(vnode) {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Contract.add(vnode.attrs.client_key)
                }
            }, [
            m("label.label", "ID"),
            m("input.input[type=text][placeholder=ID]", {
                oninput: m.withAttr("value", function(value) {Contract.current.id = value}),
                value: Contract.current.id
            }),
            m("label.label", "CLIENT PKEY"),
            m("input.input[placeholder=CLIENT PKEY]", {
                oninput: m.withAttr("value", function(value) {Contract.current.client_pkey = value}),
                value: Contract.current.client_pkey
            }),
            m("button.button[type=submit]", "Add"),
            m("label.error", Contract.error)
        ])
    }
}