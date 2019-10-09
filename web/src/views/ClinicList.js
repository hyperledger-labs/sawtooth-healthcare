var m = require("mithril")
var Clinic = require("../models/Clinic")

var qrcodeurl = ''

module.exports = {
    oninit:
        function(vnode){
            Clinic.loadList(vnode.attrs.client_key)
        },
    view: function(vnode) {
//        return m(".user-list", Clinic.list.map(function(clinic) {
//            return m("a.user-list-item", clinic.name) // + " " + clinic.permissions)
//        }),
//        m("label.error", Clinic.error))
        return m(".user-list", Clinic.list.map(function(clinic) {
            return m("a.user-list-item", clinic.public_key + " " + clinic.name,
                    m("div"),
                    m("button", {
                        onclick: function() {
                            qrcodeurl='https://chart.apis.google.com/chart?cht=qr&chs=300x300&chl=' + clinic.public_key + '&chld=H|0'
                        }
                    }, 'Generate QR code for Clinic Public Key: ' + clinic.public_key),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            Clinic.grant(clinic.public_key, vnode.attrs.client_key)
                        }
                    }, 'Grant Access'),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            Clinic.revoke(clinic.public_key, vnode.attrs.client_key)
                        }
                    }, 'Revoke Access')
                    )
            }),
            m("div"),
            m("img", {src: qrcodeurl}),
            m("label.error", Clinic.error))
    }
}