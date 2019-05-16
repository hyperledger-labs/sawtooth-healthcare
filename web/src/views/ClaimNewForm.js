var m = require("mithril")
var Claim = require("../models/Claim")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function() {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Claim.register()
                }
            }, [
//            m("label.label", "Clinic account"),
//            m("input.input[type=text][placeholder=Clinic account]", {
//                oninput: m.withAttr("value", function(value) {Claim.current.signer = value}),
//                value: Claim.current.signer
//            }),
            m("label.label", "Claim id in clinic db"),
            m("input.input[placeholder=Claim id]", {
                oninput: m.withAttr("value", function(value) {Claim.current.claim_id = value}),
                value: Claim.current.claim_id
            }),
            m("label.label", "Patient public key"),
            m("input.input[placeholder=Patient public key]", {
                oninput: m.withAttr("value", function(value) {Claim.current.patient_public_key = value}),
                value: Claim.current.patient_public_key
            }),
            m("button.button[type=submit]", "Register"),
            m("label.error", Claim.error)
        ])
    }
}