var m = require("mithril")
var Doctor = require("../models/Doctor")

var qrcodeurl = ''

module.exports = {
    oninit:
        function(vnode){
            Doctor.loadList(vnode.attrs.client_key)
        },
    view: function(vnode) {
        return m(".user-list", Doctor.list.map(function(doctor) {
            return m("a.user-list-item", doctor.public_key + " " + doctor.name + " " + doctor.surname,
                    m("div"),
                    m("button", {
                        onclick: function() {
//                    PatientDetails.load(vnode.attrs.patient_pkey, vnode.attrs.doctor_pkey)
//                    vnode.state.count++
                            qrcodeurl='https://chart.apis.google.com/chart?cht=qr&chs=300x300&chl=' + doctor.public_key + '&chld=H|0'
                        }
                    }, 'Generate QR code for Doctor Public Key: ' + doctor.public_key),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            Doctor.grant(doctor.public_key, vnode.attrs.client_key)
                        }
                    }, 'Grant Access'),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            Doctor.revoke(doctor.public_key, vnode.attrs.client_key)
                        }
                    }, 'Revoke Access')
                    ) // + " " +  doctor.permissions)
            }),
            m("div"),
            m("img", {src: qrcodeurl}),
            m("label.error", Doctor.error))
    }
}