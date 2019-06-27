var m = require("mithril")
var ClaimDetails = require("../models/ClaimDetails")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function() {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    ClaimDetails.eat_pills()
                }
            }, [
            m("label.label", "Claim id in clinic db"),
            m("input.input[placeholder=Claim id]", {
                oninput: m.withAttr("value", function(value) {ClaimDetails.current.claim_id = value}),
                value: ClaimDetails.current.claim_id
            }),
            m("button.button[type=submit]", "Eat Pills"),
            m("label.error", ClaimDetails.error)
        ])
    }
}