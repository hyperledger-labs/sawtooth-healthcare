var m = require("mithril")
var ClaimDetails = require("../models/ClaimDetails")

module.exports = {
    oninit: function(vnode) {ClaimDetails.load(vnode.attrs.clinic_pkey, vnode.attrs.claim_id)},
    view: function() {
        return m(".user-list", ClaimDetails.list.map(function(event) {
            return m("a.user-list-item", "'" + event.clinic_pkey + "' '" + event.claim_id + "' '" + event.event + "' '" + event.description + "' '" + event.event_time + "'")
        }))
    }
//    view: function() {
//        return m("form", {
//                onsubmit: function(e) {
//                    e.preventDefault()
//                    User.save()
//                }
//            }, [
//            m("label.label", "First name"),
//            m("input.input[type=text][placeholder=First name]", {
//                oninput: m.withAttr("value", function(value) {User.current.firstName = value}),
//                value: User.current.firstName
//            }),
//            m("label.label", "Last name"),
//            m("input.input[placeholder=Last name]", {
//                oninput: m.withAttr("value", function(value) {User.current.lastName = value}),
//                value: User.current.lastName
//            }),
//            m("button.button[type=submit]", "Save"),
//        ])
//    }
}