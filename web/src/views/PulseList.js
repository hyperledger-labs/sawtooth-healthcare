var m = require("mithril")
var Pulse = require("../models/Pulse")

module.exports = {
    oninit:
        function(vnode){
            Pulse.loadList(vnode.attrs.client_key)
        },
    view: function() {
        return m(".user-list", Pulse.list.map(function(pl) {
            return m("a.user-list-item", "name: " + pl.name + "; " +
                                    "surname: " + pl.surname + "; " +
                                    "PULSE: " + pl.pulse + "; " +
                                    "TIMESTAMP: " + pl.timestamp + ";"
//                                    "PATIENT PUBLIC KEY: " + pl.public_key + ";"
                                    ) // + user.publicKey
        }),
        m("label.error", Pulse.error))
    }
}