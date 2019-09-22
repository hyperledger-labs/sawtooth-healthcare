var m = require("mithril")
var Lab = require("../models/Lab")

module.exports = {
    oninit:
        function(vnode){
            Lab.loadList(vnode.attrs.client_key)
        },
    view: function() {
        return m(".user-list", Lab.list.map(function(lab) {
            return m("a.user-list-item", lab.name) // + " " + clinic.permissions)
        }),
        m("label.error", Lab.error))
    }
}