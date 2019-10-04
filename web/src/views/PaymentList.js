var m = require("mithril")
var Payment = require("../models/Payment")

module.exports = {
    oninit:
        function(vnode){
            Payment.loadList(vnode.attrs.client_key)
        },
    view: function() {
        return m(".user-list", Payment.list.map(function(pay) {
            return m("a.user-list-item", "PATIENT PKEY: " + pay.patient_pkey +
                                    "; CONTRACT ID: " + pay.contract_id +
                                    "; ID: " + pay.id +
                                    "; CLAIM ID: " + pay.claim_id
//                                    "PATIENT PUBLIC KEY: " + pl.public_key + ";"
                                    ) // + user.publicKey
        }),
        m("label.error", Payment.error))
    }
}