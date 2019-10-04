var m = require("mithril")
var Contract = require("../models/Contract")

module.exports = {
    oninit:
        function(vnode){
            Contract.loadList(vnode.attrs.client_key)
        },
    view: function() {
        return m(".user-list", Contract.list.map(function(con) {
            return m("a.user-list-item", "name: " + con.name + "; " +
                                    "surname: " + con.surname + "; " +
                                    "client_pkey: " + con.client_pkey + "; " +
                                    "id: " + con.id + ";"
//                                    "PATIENT PUBLIC KEY: " + pl.public_key + ";"
                                    ) // + user.publicKey
        }),
        m("label.error", Contract.error))
    }
}