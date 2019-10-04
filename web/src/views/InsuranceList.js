var m = require("mithril")
var Insurance = require("../models/Insurance")

module.exports = {
    oninit:
        function(vnode){
            Insurance.loadList(vnode.attrs.client_key)
        },
    view: function() {
        return m(".user-list", Insurance.list.map(function(insurance) {
            return m("a.user-list-item", insurance.name) // + " " + clinic.permissions)
        }),
        m("label.error", Insurance.error))
    }
}