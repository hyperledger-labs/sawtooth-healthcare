var m = require("mithril")
var ClaimDetails = require("../models/ClaimDetails")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function() {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    ClaimDetails.first_visit()
                }
            }, [
            m("label.label", "Claim id in clinic db"),
            m("input.input[placeholder=Claim id]", {
                oninput: m.withAttr("value", function(value) {ClaimDetails.current.claim_id = value}),
                value: ClaimDetails.current.claim_id
            }),
            m("label.label", "Doctor public key"),
            m("input.input[placeholder=Doctor public key]", {
                oninput: m.withAttr("value", function(value) {ClaimDetails.current.doctor_pkey = value}),
                value: ClaimDetails.current.doctor_pkey
            }),
            m("button.button[type=submit]", "First visit"),
            m("label.error", ClaimDetails.error)
        ])
    }
}