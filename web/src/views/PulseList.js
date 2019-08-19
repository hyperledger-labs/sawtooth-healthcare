var m = require("mithril")
var Pulse = require("../models/Pulse")

module.exports = {
    oninit: Pulse.loadList,
    view: function() {
        return m(".user-list", Pulse.list.map(function(pl) {
            return m("a.user-list-item", "PULSE: " + pl.pulse + "; " +
                                    "TIMESTAMP: " + pl.timestamp + "; " +
                                    "PATIENT PUBLIC KEY: " + pl.public_key + ";"
                                    ) // + user.publicKey
        }))
    }
}