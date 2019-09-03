var m = require("mithril")
var PatientDetails = require("../models/PatientDetails")

var qrcodeurl = ''

module.exports = {

    oninit: function(vnode) {
        vnode.attrs.doctor_pkey = ''
//        vnode.attrs.qrcode = ''
//    PatientDetails.load(vnode.attrs.clinic_pkey, vnode.attrs.claim_id)
    },
    view: function(vnode) {
        return [
            m("label.label", "Patient public key"),
            m("input.input[type=text][placeholder=Patient public key][disabled=false]", {
//                oninput: m.withAttr("value", function(value) {User.current.firstName = value}),
                value: vnode.attrs.patient_pkey
            }),
            m("label.label", "Doctor public key"),
            m("input.input[type=text][placeholder=Doctor public key]", {
                oninput: m.withAttr("value", function(value) {vnode.attrs.doctor_pkey = value}),
                value: vnode.attrs.doctor_pkey
            }),
            m(".user-list", PatientDetails.pulseList.map(function(pulse) {
                return m("a.user-list-item", "'" + pulse.public_key + "' '" + pulse.pulse + "' '" + pulse.timestamp +"'")
            })),
            m("button", {
                onclick: function() {
                    PatientDetails.load(vnode.attrs.patient_pkey, vnode.attrs.doctor_pkey)
//                    vnode.state.count++
                }
            }, "Get Pulse List"),
            m("label.error", PatientDetails.error),
            vnode.attrs.doctor_pkey != '' ? null:
                m("label.error", 'Doctor public key is empty'),
            m("button", {
                onclick: function() {
//                    PatientDetails.load(vnode.attrs.patient_pkey, vnode.attrs.doctor_pkey)
//                    vnode.state.count++
                    qrcodeurl='https://chart.apis.google.com/chart?cht=qr&chs=300x300&chl=' + vnode.attrs.doctor_pkey + '&chld=H|0'
                }
            }, 'Generate QR code for Doctor Public Key: ' + vnode.attrs.doctor_pkey),
            m("div"),
            m("img", {src: qrcodeurl}),
        ]
    }
//    view: function() {
//        return m("form", {
//                onsubmit: function(e) {
//                    e.preventDefault()
//                    User.save()
//                }
//            }, [
//            m("label.label", "First name"),
//            m("input.input[type=text][placeholder=First name]", {
//                oninput: m.withAttr("value", function(value) {User.current.firstName = value}),
//                value: User.current.firstName
//            }),
//            m("label.label", "Last name"),
//            m("input.input[placeholder=Last name]", {
//                oninput: m.withAttr("value", function(value) {User.current.lastName = value}),
//                value: User.current.lastName
//            }),
//            m("button.button[type=submit]", "Save"),
//        ])
//    }
}