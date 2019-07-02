var m = require("mithril")
var Claim = require("../models/Claim")

module.exports = {
    oninit: Claim.loadList,
    view: function() {
        return m(".user-list", Claim.list.map(function(claim) {
            return m("a.user-list-item", {href: "/claim/" + claim.clinic_pkey + "/" + claim.claim_id, oncreate: m.route.link}, claim.clinic_pkey + " " + claim.claim_id + " " + claim.patient_pkey)
        }))
    }
}