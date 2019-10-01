var m = require("mithril")
var Claim = require("../models/Claim")

module.exports = {
    oninit:
        function(vnode){
            Claim.loadList(vnode.attrs.client_key)
        },
    view: function(vnode) {
        return m(".user-list", Claim.list.map(function(claim) {
            return m("a.user-list-item", // {href: "/claim/" + claim.clinic_pkey + "/" + claim.claim_id, oncreate: m.route.link},
                claim.description + "; " + claim.id + "; " +
                claim.client_pkey + "; " + claim.state + "; " + claim.provided_service,
                m("div"),
                m("button", {
                    onclick: function() {
                        Claim.current.claim_id = claim.id
                        Claim.current.client_pkey = claim.client_pkey
                        Claim.current.provided_service = "pills, lab tests"
                        Claim.close(vnode.attrs.client_key)
                    }
                }, 'Close claim')
            )
        }),
        m("label.error", Claim.error))
    }
}